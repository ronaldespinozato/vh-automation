import requests
from conf.settings import Config
from http import HTTPStatus
from clients.authorization import VeeaAuthorization


class PackageClient:
    config = {}

    def __init__(self):
        self.config = Config()

    def get_package_by_id(self, package_id):
        username = self.config.get_auth_impersonated_username()
        data = self.__get_package_by_username(username, package_id)
        if data is None:
            return None
        return data[0]

    def __get_package_by_username(self, username, package_id):
        acs_base_url = self.config.get_acs_base_url()
        support_user_name = self.config.get_auth_support_username()
        support_password = self.config.get_auth_support_password()
        impersonated_email = username
        if username is None:
            impersonated_email = self.config.get_auth_impersonated_username

        user = VeeaAuthorization().get_impersonated_user(support_user_name, support_password, impersonated_email)
        token = user['accessToken']
        user_id = user['veeaUserId']
        header_values = {"Authorization": "Bearer " + token, 'Content-type': 'application/json', 'Accept': 'text/plain'}
        query = {"filterByAcl": 0,
                 "id": "{}".format(package_id)
                 }

        endpoint = "{}/serviceCatalog/package".format(acs_base_url)
        response = requests.get(endpoint, headers=header_values, params=query)

        if response.status_code != HTTPStatus.OK:
            print(response.json())
        return response.json()["results"]

    def get_all_packages(self):
        acs_base_url = self.config.get_acs_base_url()
        support_user_name = self.config.get_auth_support_username()
        support_password = self.config.get_auth_support_password()
        impersonated_email = self.config.get_auth_impersonated_username()

        user = VeeaAuthorization().get_impersonated_user(support_user_name, support_password, impersonated_email)
        token = user['accessToken']
        user_id = user['veeaUserId']
        header_values = {"Authorization": "Bearer " + token, 'Content-type': 'application/json', 'Accept': 'text/plain'}
        query = {"filterByAcl": 0}

        endpoint = "{}/serviceCatalog/package".format(acs_base_url)
        response = requests.get(endpoint, headers=header_values, params=query)

        if response.status_code != HTTPStatus.OK:
            print(response.json())
        return response.json()["results"]

    def get_package_summary(self, package_id):
        package_list = self.__get_package_by_username(None, package_id)
        if len(package_list) == 0:
            return None

        package = package_list["results"][0]
        return {"id": package["id"], "type": package["type"], "title": package["title"]}
