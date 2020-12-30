import redis
import sys
from pathlib import Path

# project_path = Path(".").resolve()
# sys.path.insert(0, str(project_path))
# print("#####################################")
# print(sys.path)

from conf.settings import Config


class RedisClient:

    def __init__(self):
        self.config = Config()
        self.redis_cli = redis.Redis(
            host=self.config.get_redis_db()["host"],
            port=self.config.get_redis_db()["port"],
            charset="utf-8",
            decode_responses=True)

    def get_veea_hub_progress_data(self, serial_number):
        keys = self.redis_cli.keys()
        key = self.__get_key_from_list_if_short_name_match(keys, serial_number)
        return self.redis_cli.hgetall(key)

    def exist_key_for_veea_hub(self, serial_number):
        keys = self.redis_cli.keys()
        key = self.__get_key_from_list_if_short_name_match(keys, serial_number)
        return key is not None

    def __get_key_from_list_if_short_name_match(self, keys, short_string):
        for key in keys:
            print(key)
            if key.find(short_string) != -1:
                return key
        return None


# cli = RedisClient()
# data = cli.get_veea_hub_progress_data("C05BCB00C0A000001022")
# print(data)
