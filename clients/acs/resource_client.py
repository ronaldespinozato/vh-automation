import requests
from conf.settings import Config
from http import HTTPStatus
from clients.authorization import VeeaAuthorization


class ResourceClient:
    config = {}

    def __init__(self):
        self.config = Config()

    def get_resource_by_username(self):
        acs_base_url = self.config.get_acs_base_url()
        support_user_name = self.config.get_auth_support_username()
        support_password = self.config.get_auth_support_password()
        impersonated_email = self.config.get_auth_impersonated_username()

        user = VeeaAuthorization().get_impersonated_user(support_user_name, support_password, impersonated_email)
        token = user['accessToken']
        user_id = user['veeaUserId']
        header_values = {"Authorization": "Bearer " + token, 'Content-type': 'application/json', 'Accept': 'text/plain'}
        query = {"where": "type eq 'EnrollmentVeeahub'",
                 "nested": "resourceCharacteristic(name eq 'veeaUserId' and value eq '{}')".format(user_id),
                 "pageSize": 1000}

        endpoint = "{}/resource".format(acs_base_url)
        response = requests.get(endpoint, headers=header_values, params=query)

        if response.status_code != HTTPStatus.OK:
            print(response.json())
        return response.json()["results"]
