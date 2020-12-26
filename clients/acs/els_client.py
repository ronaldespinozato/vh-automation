import json
from elasticsearch import Elasticsearch
from conf.settings import Config


class ElasticSearchACS:
    elastic = {}

    def __init__(self):
        config = Config().get_config_elasticsearch_acs()
        self.elastic = Elasticsearch(hosts=[config["host"]], port=config["port"])

    def __get_veeahub_resource_documents(self, field_name, value):
        query = {
            "query": {
                "bool": {
                    "must":
                        [
                            {"match": {"type": "EnrollmentVeeahub"}},
                            {"nested": {
                                "path": "resourceCharacteristic",
                                "query": {
                                    "bool": {
                                        "must": [
                                            {"match": {"resourceCharacteristic.name": "{}".format(field_name)}},
                                            {"match": {"resourceCharacteristic.value.raw": "{}".format(value)}}
                                        ]
                                    }
                                }
                            }}
                        ]
                }
            }
        }
        documents = self.elastic.search(index="resources", body=query)
        return self.__get_documents(documents)

    def get_veeahub_resource_by_user_id(self, user_id):
        return self.__get_veeahub_resource_documents("veeaUserId", user_id)

    def get_veeahub_resource_by_mesh_id(self, mesh_id):
        return self.__get_veeahub_resource_documents("meshId", mesh_id)

    def get_veeahub_resource_by_serial_number(self, serial_number):
        return self.__get_veeahub_resource_documents("veeahubSerialNumber", serial_number)

    def get_resource_by_id(self, id):
        document = self.elastic.get(index="resources", id=id)
        if document["_source"] is None:
            return None
        return document["_source"]

    def get_configuration_by_id(self, id):
        document = self.elastic.get(index="configurations", id=id)
        if document["_source"] is None:
            return None
        return document["_source"]

    def get_mas_user_data(self, user_id):
        resources = self.get_veeahub_resource_by_user_id(user_id)
        if len(resources) == 0:
            return None
        mas_config_id = resources[0]["relatedParty"][0]["id"]
        return self.get_configuration_by_id(mas_config_id)

    def get_veeahub_config(self, user_id):
        resources = self.get_veeahub_resource_by_user_id(user_id)
        if len(resources) == 0:
            return None
        resource_id = resources[0]["resourceRelationship"][0]["resource"]["id"]
        resource = self.get_resource_by_id(resource_id)
        if resource is None:
            return None
        veeahub_config_id = resource["relatedParty"][0]["id"]
        return self.get_configuration_by_id(veeahub_config_id)

    def __get_package_resource_documents(self, field_name, value):
        query = {
            "query": {
                "bool": {
                    "must":
                        [
                            {"match": {"type": "VeeahubSoftwarePackage"}},
                            {"nested": {
                                "path": "resourceCharacteristic",
                                "query": {
                                    "bool": {
                                        "must": [
                                            {"match": {"resourceCharacteristic.name": "{}".format(field_name)}},
                                            {"match": {"resourceCharacteristic.value.raw": "{}".format(value)}}
                                        ]
                                    }
                                }
                            }}
                        ]
                }
            }
        }
        return self.elastic.search(index="resources", body=query)

    def get_active_package_resource_documents(self):
        return self.__get_package_resource_documents("packageActive", "true")
    
    def get_inactive_package_resource_documents(self):
        return self.__get_package_resource_documents("packageActive", "false")
    
    def get_package_configuration_documents(self, list_ids):
        query = {
            "query": {
                "bool": {
                    "filter": {
                        "ids": {
                            "values": list_ids
                        }
                    }
                }
            }
        }
        return self.elastic.search(index="configurations", body=query)

    def __get_documents(self, documents):
        response = []
        for data in documents["hits"]["hits"]:
            response.append(data["_source"])
        return response
