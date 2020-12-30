import json
from pathlib import Path

ENVIRONMENT = None
ENV_SUPPORT_USER_NAME = None
ENV_SUPPORT_PASSWORD = None
ENV_IMPERSONATED_USER_NAME = None

def set_local_env():
    global ENVIRONMENT
    ENVIRONMENT = 'local'

def set_env(env, impersonated_user):
    global ENVIRONMENT
    global ENV_IMPERSONATED_USER_NAME

    ENV_IMPERSONATED_USER_NAME = impersonated_user
    ENVIRONMENT = 'local'
    if env == 'dev':
        ENVIRONMENT = 'dev'
    if env == 'qa':
        ENVIRONMENT = 'qa'
    if env == 'prod':
        ENVIRONMENT = 'prod'

class Config:
    config_json = None

    def __init__(self):
        set_local_env()
        self.config_json = None

    def get_config_bootstrap_db(self):
        conf = self.__get_config()
        return conf["databases"]["bootstrap"]

    def get_config_enrollment_db(self):
        conf = self.__get_config()
        return conf["databases"]["enrollment"]

    def get_config_acl_db(self):
        conf = self.__get_config()
        return conf["databases"]["acl"]

    def get_acs_base_url(self):
        conf = self.__get_config()
        return conf["services"]["acs"]["baseUrl"]

    def get_enrollment_base_url(self):
        conf = self.__get_config()
        return conf["services"]["enrollment"]["baseUrl"]

    def get_bootstrap_base_url(self):
        conf = self.__get_config()
        return conf["services"]["bootstrap"]["baseUrl"]

    def get_auth_base_url(self):
        conf = self.__get_config()
        return conf["services"]["auth"]["baseUrl"]

    def get_redis_db(self):
        conf = self.__get_config()
        return conf["redis"]

    def get_certificate_base_url(self):
        conf = self.__get_config()
        return conf["services"]["certificate"]["baseUrl"]

    def get_auth_support_username(self):
        conf = self.__get_config()
        if ENV_SUPPORT_USER_NAME is None:
            return conf["services"]["auth"]["supportUserName"]
        return ENV_SUPPORT_USER_NAME

    def get_auth_support_password(self):
        conf = self.__get_config()
        if ENV_SUPPORT_PASSWORD is None:
            return conf["services"]["auth"]["supportUserPassword"]
        return ENV_SUPPORT_PASSWORD

    def get_auth_impersonated_username(self):
        conf = self.__get_config()
        if ENV_IMPERSONATED_USER_NAME is None:
            return conf["services"]["auth"]["impersonatedName"]
        return ENV_IMPERSONATED_USER_NAME

    def get_config_elasticsearch_acs(self):
        conf = self.__get_config()
        return conf["elasticsearch"]["acs"]

    def __get_config(self):
        application_file = "application.{}.json".format(ENVIRONMENT)
        if self.config_json is None:
            project_path = Path(".").resolve()
            file = Path("{}/{}".format(project_path, application_file)).resolve()
            with open(file) as f:
                self.config_json = json.load(f)
        return self.config_json
