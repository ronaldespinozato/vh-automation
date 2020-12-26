from typing import List, Any

from conf.settings import set_env
import os
import json
import requests
from conf.settings import Config
from http import HTTPStatus
from clients.authorization import VeeaAuthorization


class PackageWriter:
    config = {}
    path_folder = "/tmp/backup/packages"

    def __init__(self):
        self.config = Config()
        if not os.path.exists(self.path_folder):
            os.makedirs(self.path_folder)

    def get_active_package_resources(self):
        return self.__get_package_resources("true")

    def get_inactive_package_resources(self):
        return self.__get_package_resources("false")

    def __get_all_package_resources(self):
        acs_base_url = self.config.get_acs_base_url()
        user = self.__get_user()
        token = user['accessToken']
        user_id = user['veeaUserId']
        header_values = {"Authorization": "Bearer " + token, 'Content-type': 'application/json', 'Accept': 'text/plain'}
        query = {
            "where": "type eq 'VeeahubSoftwarePackage'",
            "pageSize": 10000
        }
        endpoint = "{}/resource".format(acs_base_url)
        response = requests.get(endpoint, headers=header_values, params=query)

        if response.status_code != HTTPStatus.OK:
            print(response.json())
        return response.json()

    def __get_package_resources(self, is_package_active):
        acs_base_url = self.config.get_acs_base_url()
        user = self.__get_user()
        token = user['accessToken']
        user_id = user['veeaUserId']
        header_values = {"Authorization": "Bearer " + token, 'Content-type': 'application/json', 'Accept': 'text/plain'}
        query = {
            "where": "type eq 'VeeahubSoftwarePackage'",
            "pageSize": 10000,
            "nested": "resourceCharacteristic(contains(name, 'packageActive')) NESTED_AND resourceCharacteristic(contains(value, '{}'))".format(
                is_package_active)
        }
        endpoint = "{}/resource".format(acs_base_url)
        response = requests.get(endpoint, headers=header_values, params=query)

        if response.status_code != HTTPStatus.OK:
            print(response.json())
        return response.json()

    def __get_mas_service_configuration(self):
        acs_base_url = self.config.get_acs_base_url()
        user = self.__get_user()
        token = user['accessToken']
        user_id = user['veeaUserId']
        header_values = {"Authorization": "Bearer " + token, 'Content-type': 'application/json', 'Accept': 'text/plain'}
        query = {}
        endpoint = "{}/service".format(acs_base_url)
        response = requests.get(endpoint, headers=header_values, params=query)

        if response.status_code != HTTPStatus.OK:
            print(response.json())
        return response.json()

    def __get_user(self):
        support_user_name = self.config.get_auth_support_username()
        support_password = self.config.get_auth_support_password()
        impersonated_email = self.config.get_auth_impersonated_username()

        user = VeeaAuthorization().get_impersonated_user(support_user_name, support_password, impersonated_email)
        return user

    def __get_package_container(self, resources_data):
        result = []
        for resource in resources_data["results"]:
            package_id = resource["id"]
            config_id = resource["relatedParty"][0]["id"]

            acs_base_url = self.config.get_acs_base_url()
            user = self.__get_user()
            token = user['accessToken']
            user_id = user['veeaUserId']
            header_values = {"Authorization": "Bearer " + token, 'Content-type': 'application/json', 'Accept': 'text/plain'}
            query = {}
            endpoint = "{}/resource/{}/config/{}".format(acs_base_url, package_id, config_id)

            response = requests.get(endpoint, headers=header_values, params=query)

            if response.status_code != HTTPStatus.OK:
                print(response.json())
            else:
                result.append(response.json())

        return result

    def __save_mas_service_documents_into_file(self, file_name, mas_data):
        total = len(mas_data)
        response = {
            "took": 5,
            "timed_out": False,
            "_shards": {
                "total": 5,
                "successful": 5,
                "failed": 0
            },
            "hits": {
                "total": total,
                "max_score": 0,
                "hits": []
            }
        }
        document_schema = '''{
            "_index": "service_v1.0",
            "_type": "service",
            "_id": "",
            "_score": 0,
            "_source": {}
        }'''

        hits = []
        for data in mas_data:
            del data["_version"]
            document = json.loads(document_schema)
            document["_id"] = data["id"]
            document["_source"] = data
            hits.append(document)

        response["hits"]["hits"] = hits

        f = open(file_name, "w")
        f.write(json.dumps(response, indent=2))
        f.close()

    def __save_configuration_documents_into_file(self, file_name, configuration_data):
        total = len(configuration_data)
        # resources = configuration_data["results"]
        response = {
            "took": 5,
            "timed_out": False,
            "_shards": {
                "total": 5,
                "successful": 5,
                "failed": 0
            },
            "hits": {
                "total": total,
                "max_score": 0,
                "hits": []
            }
        }
        document_schema = '''{
            "_index": "configuration_v1.2",
            "_type": "configuration",
            "_id": "",
            "_score": 0,
            "_source": {}
        }'''

        hits = []
        for data in configuration_data:
            del data["_version"]
            document = json.loads(document_schema)
            document["_id"] = data["id"]
            document["_source"] = data
            hits.append(document)

        response["hits"]["hits"] = hits

        f = open(file_name, "w")
        f.write(json.dumps(response, indent=2))
        f.close()

    def __save_resource_documents_into_file(self, file_name, resource_data):
        total = resource_data["total"]
        resources = resource_data["results"]
        response = {
            "took": 5,
            "timed_out": False,
            "_shards": {
                "total": 5,
                "successful": 5,
                "failed": 0
            },
            "hits": {
                "total": total,
                "max_score": 0,
                "hits": []
            }
        }
        document_schema = '''{
            "_index": "resource_v1.1",
            "_type": "resource",
            "_id": "",
            "_score": 0,
            "_source": {}
        }'''

        hits = []
        for data in resources:
            del data["_version"]
            document = json.loads(document_schema)
            document["_id"] = data["id"]
            document["_source"] = data
            hits.append(document)

        response["hits"]["hits"] = hits

        f = open(file_name, "w")
        f.write(json.dumps(response, indent=2))
        f.close()

    def create_active_package_documents_into_files(self):
        resources = self.get_active_package_resources()
        self.__save_resource_documents_into_file("{}/resources.active.json".format(self.path_folder), resources)

        configurations = self.__get_package_container(resources)
        self.__save_configuration_documents_into_file("{}/configurations.active.json".format(self.path_folder), configurations)

        mas_services = self.__get_mas_service_configuration()
        self.__save_mas_service_documents_into_file("{}/services.json".format(self.path_folder), mas_services)

    def create_inactive_package_documents_into_files(self):
        resources = self.get_inactive_package_resources()
        self.__save_resource_documents_into_file("{}/resources.inactive.json".format(self.path_folder), resources)

        configurations = self.__get_package_container(resources)
        self.__save_configuration_documents_into_file("{}/configurations.inactive.json".format(self.path_folder), configurations)

        mas_services = self.__get_mas_service_configuration()
        self.__save_mas_service_documents_into_file("{}/services.json".format(self.path_folder), mas_services)

    def create_all_package_documents_into_files(self):
        resources = self.__get_all_package_resources()
        self.__save_resource_documents_into_file("{}/resources.all.json".format(self.path_folder), resources)

        configurations = self.__get_package_container(resources)
        self.__save_configuration_documents_into_file("{}/configurations.all.json".format(self.path_folder), configurations)

        mas_services = self.__get_mas_service_configuration()
        self.__save_mas_service_documents_into_file("{}/services.json".format(self.path_folder), mas_services)

    def create_package_files(self):
        # self.create_active_package_documents_into_files()
        # self.create_inactive_package_documents_into_files()
        self.create_all_package_documents_into_files()
