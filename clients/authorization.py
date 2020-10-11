import requests
from conf.settings import Config


class VeeaAuthorization:
    __config = {}
    __auth_base_url = ""
    realm = "veea"
    clientId = "veeahub-cli"

    def __init__(self):
        self.__config = Config()
        self.__auth_base_url = self.__config.get_auth_base_url()
        self.realm = "veea"
        self.clientId = "veeahub-cli"

    def get_token(self, user_name, password):
        endpoint_token = "{}/auth/realms/{}/protocol/openid-connect/token".format(self.__auth_base_url, self.realm)
        resp = requests.post(endpoint_token,
                             headers={"Content-Type": "application/x-www-form-urlencoded"},
                             data={"client_id": self.clientId, "grant_type": "password", "username": user_name,
                                   "password": password})
        return resp.json()["access_token"]

    def get_impersonated_token(self, user_name, password, impersonated_email):
        token = self.get_token(user_name, password)

        endpoint_token = "{}/auth/admin/realms/{}/users?email={}".format(self.__auth_base_url, self.realm,
                                                                         impersonated_email)
        user = requests.get(endpoint_token, headers={"Authorization": "Bearer " + token}).json()[0]
        userId = user['id']

        endpoint_token = "{}/auth/realms/{}/protocol/openid-connect/token".format(self.__auth_base_url, self.realm)
        resp = requests.post(endpoint_token,
                             headers={"Content-Type": "application/x-www-form-urlencoded"},
                             data={"client_id": self.clientId,
                                   "grant_type": "urn:ietf:params:oauth:grant-type:token-exchange",
                                   "requested_subject": self.userId, "subject_token": token})

        return resp.json()["access_token"]

    def get_impersonated_user(self, user_name, password, impersonated_email):
        user_data = {}

        token = self.get_token(user_name, password)

        endpoint_token = "{}/auth/admin/realms/{}/users?email={}".format(self.__auth_base_url, self.realm,
                                                                         impersonated_email)
        impersonate_user = requests.get(endpoint_token, headers={"Authorization": "Bearer " + token}).json()[0]

        impersonate_user_id = impersonate_user['id']

        endpoint_token = "{}/auth/realms/{}/protocol/openid-connect/token".format(self.__auth_base_url, self.realm)
        resp = requests.post(endpoint_token,
                             headers={"Content-Type": "application/x-www-form-urlencoded"},
                             data={"client_id": self.clientId,
                                   "grant_type": "urn:ietf:params:oauth:grant-type:token-exchange",
                                   "requested_subject": impersonate_user_id, "subject_token": token})

        user_data['veeaUserId'] = impersonate_user['attributes']['userId'][0]
        user_data['accessToken'] = resp.json()["access_token"]
        return user_data

    def get_user_inf(self):
        support_username = self.__config.get_auth_support_username()
        support_password = self.__config.get_auth_support_password()
        impersonated_username = self.__config.get_auth_impersonated_username()
        return self.get_impersonated_user(support_username, support_password, impersonated_username)
