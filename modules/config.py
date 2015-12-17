import ConfigParser
import os
from .resources import ResourcesManager
from .driver import create_new_driver


class ApplicationUtils(object):
    def __init__(self):
        self.configuration_parser = ConfigurationParser()
        self.resources_manager = ResourcesManager()

    def create_driver(self, scenario, browser_size, user_agent):
        return create_new_driver(self.get_driver_name(), self.get_proxy_url(),
                                 self.get_timeout(), browser_size, user_agent)

    def get_base_url(self):
        base_url = os.environ.get('BASE_URL')
        if not base_url:
            base_url = self.configuration_parser.get_base_url()
        return base_url

    def get_driver_name(self):
        driver_name = os.environ.get('DRIVER_NAME')
        if not driver_name:
            driver_name = self.configuration_parser.get_driver_name()

        return driver_name

    def get_proxy_url(self):
        proxy_url = os.environ.get('PROXY_URL')
        if not proxy_url:
            proxy_url = self.configuration_parser.get_proxy_url()

        return proxy_url

    def get_screenshot_directory(self):
        return self.configuration_parser.get_screenshot_directory()

    def get_timeout(self):
        return self.configuration_parser.get_timeout()


class ConfigurationParser(object):
    def __init__(self):
        self._config_parser = ConfigParser.ConfigParser()
        url = self._get_config_file_url('setup.cfg')
        self._config_parser.readfp(open(url))

    def get_base_url(self):
        return self._config_parser.get('general', 'base_url')

    def _get_config_file_url(self, conf_file_name):
        home_setup_file_path = conf_file_name
        if os.path.isfile(home_setup_file_path):
            url = home_setup_file_path
        else:
            url = conf_file_name
        return url

    def get_driver_name(self):
        return self._config_parser.get('selenium', 'driver')

    def get_proxy_url(self):
        if self._config_parser.has_option('selenium', 'proxy'):
            return self._config_parser.get('selenium', 'proxy')
        return None

    def get_screenshot_directory(self):
        return self._config_parser.get('general', 'screenshot_folder')

    def get_timeout(self):
        return self._config_parser.get('selenium', 'timeout')
