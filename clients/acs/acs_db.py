import mysql.connector
from conf.settings import Config


class AcsDB:
    db = {}

    def __init__(self):
        db_config = Config().get_config_acl_db()
        self.db = mysql.connector.connect(
            host=db_config["host"],
            port=db_config["port"],
            database=db_config["name"],
            user=db_config["user"],
            password=db_config["password"],
            ssl_disabled=True
        )

    def get_enduser_package_config(self):
        query = """SELECT commercial_package_id, mesh_id, package_config_data 
                FROM enduser_package_config_data"""
        return self.__get_query_result(query)

    def get_veeahub_to_privafy_carrier_id(self):
        query = """SELECT serial_number, carrier_id 
                FROM veeahub_to_privafy_id;"""
        return self.__get_query_result(query)

    def get_realm_to_privafy_carrier_id(self):
        query = """SELECT realm, carrier_id 
                FROM realm_to_privafy_carrier_id;"""
        return self.__get_query_result(query)

    def __get_query_result(self, query):
        cursor = self.db.cursor()
        cursor.execute(query)
        row_headers = [x[0] for x in cursor.description]
        records = cursor.fetchall()

        response = []
        for data in records:
            response.append(dict(zip(row_headers, data)))
        return response
