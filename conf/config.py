import configparser
import os


class Config(object):

    def __init__(self,environment="DEFAULT"):
        config_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'config.ini')
        self.config = configparser.ConfigParser()
        self.config.read(config_path)
        environment = environment.upper()
        self.author = self.config[environment]['AUTHOR']
        self.app = self.config[environment]['APPLICATION']
        self.env = self.config[environment]['ENVIRONMENT']