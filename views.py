import json
import logging
from enum import Enum
from httplib import OK
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from modules.packages.models import Package
from modules.packages.models import Webhook
from modules.packages.models import Circle
import modules.common.database_operations as database_operations
from modules.common.utils import get_params, api_method
import requests
import numpy as np
import matplotlib.pyplot as plt

x = ["add_site_cancel", "add_site_happy_flow", "add_site_missing_param", "add_mission_missing_param",
     "add_mission_cancel", "add_mission_happy_flow", "user_header", "package_header", "site_header", "routes_header"]

logger = logging.getLogger('.'.join(__file__.split('/')[-2:]).rstrip('.py'))


class AddPackageStatus(Enum):
    AddedSuccessfully = 1
    PackageAlreadyExists = 2
    MissingParameters = 3
    LocationInformationInvalid = 4
    InvalidParameters = 5


@csrf_exempt
def webhook_listener(request):
    """
    Listens to webhook from Github, to retrieve unique sha value and the pull request address
    :return: ok
    """
    # Receiving payload, and obtaining circle_sha from CircleCI
    webhook_payload = json.loads(request.body)
    # Check if it is a pull request related commit, will store relevant data in database if True.
    if "pull_request" in webhook_payload:
        comment_address = webhook_payload['pull_request']['comments_url']
        sha = webhook_payload['pull_request']['head']['sha']
        Webhook.objects.create(pull_address=comment_address, sha_number=sha).save()
        logger.debug("New pull request details of %s are stored successfully", sha)
    else:
        logger.debug("This is not a pull request")
    return HttpResponse(content="ok")


@csrf_exempt
def circle_listener(request):
    """
    Listens to webhook from circleci, including selenium test data package.
    :return: ok
    """
    # Initialising list container for each test, and putting them all in one list.
    package_header, add_mission_cancel, add_mission_happy_flow, \
    add_mission_missing_param, user_header, add_site_cancel, \
    add_site_happy_flow, site_header, add_site_missing_param, \
    routes_header = ([] for i in range(len(x)))
    y = [add_site_cancel, add_site_happy_flow, add_site_missing_param, add_mission_missing_param, add_mission_cancel,
         add_mission_happy_flow, user_header, package_header, site_header, routes_header]

    # Receiving payload, and obtaining circle_sha from CircleCI
    circle_payload = json.loads(request.body)
    try:
        circle_sha = circle_payload['sha']
    except EnvironmentError:
        circle_sha = "Does not exist"

    # input data into postgres data base
    for row in circle_payload['data']:
        Circle.objects.create(test_name=row, test_time=circle_payload['data'][str(row)])

    # Arranging all selenium test time data from the database into a list of tests
    for row in Circle.objects.all():
        for i in range(len(x)):
            if x[i] in row.test_name:
                y[i].append(row.test_time)

    # If the sha number provided by CircleCI webhook matches with the pull request sha of Github will trigger
    # comment api and upload a graph and table of the current test results as compared to the past results.
    if Webhook.objects.filter(sha_number=circle_sha).count():

        logger.debug("Found matching sha number")

        # Retrieving the pull request address in github to send comment
        circle_current_build = circle_payload['current_build']
        pull_path = str(Webhook.objects.get(sha_number=circle_sha).pull_address)
        ave = plot_graph(y, x, circle_sha)
        issue = {"body": "# Selenium Test Scatter Plot \n\n"
                         "![test](http://dcd3e134.ngrok.io/static/%s.png) \n\n"
                         "### [Click here for details of the build](%s) \n\n"
                         "Number | Test names | Average time(s)\n "
                         "--------|--------|-------\n"
                         "0 | %s | %s\n"
                         "1 | %s | %s\n"
                         "2 | %s | %s\n"
                         "3 | %s | %s\n"
                         "4 | %s | %s\n"
                         "5 | %s | %s\n"
                         "6 | %s | %s\n"
                         "7 | %s | %s\n"
                         "8 | %s | %s\n"
                         "9 | %s | %s\n"
                         % (circle_sha, circle_current_build, x[0], ave[0], x[1], ave[1], x[2], ave[2],x[3], ave[3],
                            x[4], ave[4], x[5], ave[5], x[6], ave[6], x[7], ave[7], x[8], ave[8], x[9], ave[9])
                 }
        session = requests.Session()
        session.auth = ('darius@flytrex.com', 'Asdf1234%')
        r = session.post(pull_path, json.dumps(issue))
        if r.status_code == 201:
            logger.debug("Successfully created Issue")
        else:
            logger.debug("Could not create Issue")
            logger.debug("Response: %s", r.content)
    else:
        logger.debug("Failed to post comment")
    return HttpResponse(content="ok")


def extract_data(test_time, extracted):
    """
    Used to extract the last test time data of various tests
    :param test_time: A list of test time arranged base on the test name in a list
    :param extracted: newly initiated list of float values to keep the last test time
    :return: The last timing of each of the tests
    """
    for i in range(len(test_time)):
        extracted[i] = float(test_time[i][-1])
        del test_time[i][-1]
    return extracted


def plot_graph(test_time, test_name, circle_sha):
    """
    Generates graphs from the new data collected from CircleCI and old data from the postgres database
    :param test_time: A list of test time arranged base on the test name in a list
    :param test_name: A list of all the test name
    :param circle_sha: The Sha of the push and pull request
    :return: A list of average time for each test
    """
    # Initiating the variables for every webhook
    # Variable extracted is the last input data to tests, average is the average time of each test.
    extracted = np.arange(0, float(len(test_name)))
    a = np.arange(0, len(test_name))
    average = find_average(test_time, test_name)
    last_data = extract_data(test_time, extracted)
    plt.plot(a, average, "k-")
    plt.plot(a, last_data, "ro")
    for xe, ye in zip(a, test_time):
        plt.scatter([xe] * len(ye), ye)
    plt.title('Selenium Test Timing Scatter Plot')
    plt.xlim((-1, len(test_time)))
    plt.savefig("./modules/static/%s.png" % circle_sha)
    return average


def find_average(test_time, test_name):
    """
    Used to find and retrieve the average selenium test time of each test
    :param test_time: A list of test time arranged base on the test name in a list
    :param test_name: A list of all the test name
    :return: A list of average time for each test
    """
    ave = np.arange(0, float(len(test_name)))
    for i in range(len(test_name)):
        average = sum(test_time[i]) / float(len(test_time[i]))
        ave[i] = average
        logger.debug(test_name[i] + ": %.2fs on average.", average)
    return ave


def list(request):
    """
    Get a list of all existing packages
    :return: list
    """
    return database_operations.list_items('Packages',
                                          Package.objects.all(),
                                          list.__name__,
                                          logger)


@csrf_exempt
@api_method
def add(request):
    """
    Add a new package to database.
    validates the received parameters using django forms.
    :return: package id
    """
    logger.debug("Received new package creation request")

    # Load new center dictionary data
    details = json.loads(request.body)

    # Create new Center model
    item = Package.create(**details)

    # Save and validate new model
    item.save()

    logger.debug("New package created successfully %s" % item.tracking_number)

    return HttpResponse(json.dumps({'package_id': item.id}), status=OK)


@api_method
def get(request):
    '''
    get a specific package. checks if it exists
    :param package_id: package id
    '''
    package_id = get_params(request, logger, '!package_id')

    return database_operations.get_item('Package',
                                        package_id,
                                        Package.objects.get,
                                        logger,
                                        Package.DoesNotExist)


@api_method
def delete(request):
    '''
    deletes a specific package. checks if it exists, and handles db access errors.
    :param package_id: package id
    '''
    package_id = get_params(request, logger, '!package_id')

    return database_operations.delete_item('Package',
                                           package_id,
                                           logger,
                                           Package.objects.get,
                                           Package.DoesNotExist)


class TempUser(object):
    @property
    def username(self):
        return 'shlomi'


@api_method
def notify_mobile_user(request, package_id):
    '''
    Helper method to simulate the Delivery Initiation procedure by an end user
    :param package_id: package id
    '''

    # room = get_room_or_error('1', '')
    # room.send_message(package_id, TempUser())
    return HttpResponse('OK')
