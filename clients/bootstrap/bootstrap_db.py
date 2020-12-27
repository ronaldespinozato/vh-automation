import mysql.connector
from conf.settings import Config


class BootstrapDB:
    db = {}

    def __init__(self):
        db_config = Config().get_config_bootstrap_db()
        self.db = mysql.connector.connect(
            host=db_config["host"],
            port=db_config["port"],
            database=db_config["name"],
            user=db_config["user"],
            password=db_config["password"],
            ssl_disabled=True
        )

    def get_mesh_id_from_veeahubs(self, serial_number_list):
        serial_numbers = "{}".format(",".join(serial_number_list)).replace(",", "','")
        query = """select serial_number, mesh_uuid 
                from veea_hub vh 
                where vh.serial_number in ('{}') and mesh_uuid is not null""".format(serial_numbers)
        return self.__get_query_result(query)

    def get_mesh_by_id(self, mesh_id):
        query = """SELECT uuid, serial_number, public_key, owner_uuid, configuration_key 
                    FROM mesh m
                    WHERE uuid = '{}'""".format(mesh_id)
        return self.__get_query_result(query)

    def get_veeahub_by_serial_number(self, serial_number):
        query = """select serial_number, owner_uuid, mesh_uuid
                    from veea_hub vh
                    where serial_number = '{serial_number}'""".replace("{serial_number}", serial_number)

        data = self.__get_query_result(query)
        if len(data) > 0:
            return data[0]
        return None

    def get_veeahub_by_owner_uuid(self, owner_uuid):
        query = """select serial_number, owner_uuid, mesh_uuid
                    from veea_hub vh
                    where owner_uuid = '{owner_uuid}'""".replace("{owner_uuid}", owner_uuid)

        return self.__get_query_result(query)

    def get_veeahub_by_mesh_uuid(self, mesh_uuid):
        query = """select serial_number, owner_uuid, mesh_uuid
                    from veea_hub vh
                    where owner_uuid = '{mesh_uuid}'""".replace("{mesh_uuid}", mesh_uuid)

        return self.__get_query_result(query)

    def get_veea_hub_configuration_data(self, serial_number):
        query = """select uuid, tgz,veea_hub_serial_number
                    from veea_hub_configuration_data vhcd
                    where veea_hub_serial_number = '{veea_hub_serial_number}'
                    order by veea_hub_serial_number""".replace("{veea_hub_serial_number}", serial_number)
        return self.__get_query_result(query)

    def get_offered_software_veea_hub(self, serial_number):
        query = """SELECT id, software_uuid, veea_hub_serial_number 
                    FROM offered_software_veea_hub osvh
                    WHERE veea_hub_serial_number = '{}'""".format(serial_number)
        return self.__get_query_result(query)

    def get_veea_hub_logs_by_serial_number(self, serial_number):
        query = """SELECT *
                FROM veea_hub_log vhl
                WHERE veea_hub_serial_number = '{}'""".format(serial_number)
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
