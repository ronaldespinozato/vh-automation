import mysql.connector
from conf.settings import Config


class EnrollmentDB:
    db = {}

    def __init__(self):
        db_config = Config().get_config_enrollment_db()
        self.db = mysql.connector.connect(
            host=db_config["host"],
            port=db_config["port"],
            database=db_config["name"],
            user=db_config["user"],
            password=db_config["password"],
            ssl_disabled=True
        )

    def get_owner_data(self, user_name):
        query = """SELECT id, owner_id, owner_cert_serial_number, email, realm 
                FROM enrollment_db.`user` u 
                WHERE u.email = '{}'""".format(user_name)
        data = self.__get_query_result(query)
        if len(data) > 0:
            return data[0]

        return None

    def get_owner_by_id(self, owner_id):
        query = """SELECT id, owner_id, owner_cert_serial_number, email, realm 
                FROM enrollment_db.`user` u 
                WHERE u.owner_id = '{}'""".format(owner_id)
        return self.__get_query_result(query)

    def get_enroll_status(self):
        query = """SELECT es.serial_number, es.user_id, es.`action`, es.status
                    FROM enrollment_db.enroll_status es"""
        return self.__get_query_result(query)

    def get_enroll_status_by_veea_hub(self, serial_number):
        query = """SELECT serial_number, user_id, `action`, status
                    FROM enrollment_db.enroll_status es 
                    WHERE serial_number = '{}'""".format(serial_number)
        data = self.__get_query_result(query)
        if len(data) > 0:
            return data[0]
        return None

    def __get_query_result(self, query):
        cursor = self.db.cursor()
        cursor.execute(query)
        row_headers = [x[0] for x in cursor.description]
        records = cursor.fetchall()

        response = []
        for data in records:
            response.append(dict(zip(row_headers, data)))
        return response