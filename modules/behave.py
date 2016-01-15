import logging
import errno
import re
import os
import shutil
from .config import ApplicationUtils
from ui_tests.pages.base import PageObjectFactory
from .driver import WebDriverFacade
from json import dumps
from reports import generate_report


logger = logging.getLogger(__file__)

results = []


class ContextSubject(object):
    def __init__(self, context):
        self.events = dict()
        self.context = context

    def notify(self, event):
        if event in self.events:
            for observer in self.events[event]:
                observer.notify(self.context)
                if observer.execute_once:
                    self.un_register(observer, event)


class Observer(object):
    @property
    def execute_once(self):
        return False

    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return self.name == other.name

    def notify(self, context):
        pass


def after_feature(context, feature):
    match = re.search(r'\w*\.feature$', feature.filename)
    if not match:
        raise ValueError("Invalid feature name")

    context.feature_name = match.group()
    context.context_subject.notify("after_feature")
    build_report(feature.filename)


def after_scenario(context, scenario):
    if "failed" == scenario.status:
        take_screenshot(context, scenario, scenario.status)
        data = dumps({'passed': False})
        try:
            os.mkdir(os.path.join(context.utils.get_screenshot_directory(),
                                  scenario.status))
        except OSError, e:
            if e.errno != errno.EEXIST:
                raise
        source_fld = context.utils.get_screenshot_directory()
        destination_fld = scenario.status
        file_names = WebDriverFacade(context.driver).\
            list_files_with_extension(source_fld, ".png")
        for f in file_names:
            if "FAILED" in f:
                shutil.move(os.path.join(source_fld, f), os.path.join(
                    source_fld, destination_fld, f))
    elif "passed" == scenario.status:
        take_screenshot(context, scenario, scenario.status)
        data = dumps({'passed': True})
        try:
            os.mkdir(os.path.join(context.utils.get_screenshot_directory(),
                                  scenario.status))
        except OSError, e:
            if e.errno != errno.EEXIST:
                raise
        source_fld = context.utils.get_screenshot_directory()
        destination_fld = scenario.status
        file_names = WebDriverFacade(context.driver).list_files_with_extension(
            source_fld, ".png")
        for f in file_names:
            if "PASSED" in f:
                shutil.move(os.path.join(source_fld, f), os.path.join(
                    source_fld, destination_fld, f))

    test_data = {'name': scenario.name, 'status': scenario.status}
    results.append(test_data)

    context.driver.quit()
    context.context_subject.notify("after_scenario")


def before_scenario(context, scenario):
    new_scenario_name = scenario.name[0:50]
    new_scenario_name = re.sub(r'[\W_]+', '_', new_scenario_name)
    context.driver = context.utils.create_driver(new_scenario_name,
                                                 context.browser_size,
                                                 context.user_agent)
    # PageFactory initialization
    page_factory = PageObjectFactory()
    page_factory.driver = context.driver
    page_factory.base_url = context.base_url


def build_report(feature_name):
    generate_report(feature_name, results)


def context_initializer(context, browser_size=None, user_agent=None):
    if not context.config.log_capture:
        logging.basicConfig(level=logging.DEBUG)
    context.utils = ApplicationUtils()
    context.base_url = context.utils.get_base_url()
    context.context_subject = ContextSubject(context)
    context.browser_size = browser_size
    context.user_agent = user_agent


def take_screenshot(context, scenario, status):
    new_scenario_name = scenario.name[0:9]
    new_scenario_name = re.sub(r'[\W_]+', '_',
                               status.upper() + '_' + new_scenario_name)
    png_file_name = new_scenario_name + ".png"
    ss_file = os.path.join(context.utils.get_screenshot_directory(),
                           png_file_name)
    WebDriverFacade(context.driver).take_screenshot(ss_file)
