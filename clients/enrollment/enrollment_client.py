import requests
from conf.settings import Config
from http import HTTPStatus
from clients.authorization import VeeaAuthorization


class EnrollmentClient:
    __config = {}

    def __init__(self):
        self.__config = Config()

    def get_mesh_config(self, username):
        user = self.get_user_access_info(username)
        token = user['accessToken']
        user_id = user['veeaUserId']
        header_values = {"Authorization": "Bearer " + token, 'Content-type': 'application/json', 'Accept': 'text/plain'}
        endpoint = "{}/enroll/user/{}/config".format(self.__config.get_enrollment_base_url(), user_id)
        response = requests.get(endpoint, json={}, headers=header_values)
        if response.status_code != HTTPStatus.OK:
            print(response.json())
        return response

    def start(self, payload, username):
        token = self.get_user_access_info(username)['accessToken']
        header_values = {"Authorization": "Bearer " + token, 'Content-type': 'application/json', 'Accept': 'text/plain'}
        endpoint = "{}/enroll/start".format(self.__config.get_enrollment_base_url())
        response = requests.post(endpoint, json=payload, headers=header_values)

        return response

    def upgrade_mesh(self, mesh_id, package_id, username):
        user = self.get_user_access_info(username)
        token = user['accessToken']
        user_id = user['veeaUserId']
        payload = {
            "userId": user_id,
            "subscriptionId": "",
            "meshId": mesh_id,
            "packageId": package_id
        }
        header_values = {"Authorization": "Bearer " + token, 'Content-type': 'application/json', 'Accept': 'text/plain'}
        endpoint = "{}/subscription/upgrade".format(self.__config.get_enrollment_base_url())
        response = requests.post(endpoint, json=payload, headers=header_values)

        return response

    def get_user_access_info(self, username):
        support_user_name = self.__config.get_auth_support_username()
        support_password = self.__config.get_auth_support_password()
        impersonated_email = username

        user = VeeaAuthorization().get_impersonated_user(support_user_name, support_password, impersonated_email)

        return user

    def un_enroll_veeahub(self, username, serial_number):
        print("un-enroll {} => {}".format(username, serial_number))
        token = self.get_user_access_info(username)['accessToken']
        header_values = {"Authorization": "Bearer " + token, 'Content-type': 'application/json'}
        endpoint = "{}/enroll/device/{}".format(self.__config.get_enrollment_base_url(), serial_number)
        response = requests.delete(endpoint, headers=header_values)
        print(response.json())
        return response
