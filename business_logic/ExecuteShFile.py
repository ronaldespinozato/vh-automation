import subprocess
from pathlib import Path


class ExecuteShFile:
    device_self_signed_cert = "/tmp/{}/device_self_signed_cert.pem"
    device_private_key = "/tmp/{}/device_priv.pem"

    def veea_hub_start_software_downloading(self, serial_number):
        # print(self.device_self_signed_cert)

        full_path_file = Path(__file__).resolve()
        execute_file = Path(
            "{}/{}".format(full_path_file.parent, "/sh/devices/scripts/submit_download_log.sh")).resolve()
        veea_hub_self_signed_cert = self.device_self_signed_cert.format(serial_number)
        veea_hub_private_key = self.device_private_key.format(serial_number)
        # print(veea_hub_self_signed_cert)
        # print(veea_hub_private_key)

        response = subprocess.call(['sh', execute_file, veea_hub_self_signed_cert, veea_hub_private_key, serial_number])
        if response == 0:
            return True
        else:
            raise Exception("Exception trying execute the file {}".format(execute_file))

    def veea_hub_complete_software_configuration(self, serial_number):
        full_path_file = Path(__file__).resolve()
        execute_file = Path(
            "{}/{}".format(full_path_file.parent, "/sh/devices/scripts/submit_configure_log.sh")).resolve()
        veea_hub_self_signed_cert = self.device_self_signed_cert.format(serial_number)
        veea_hub_private_key = self.device_private_key.format(serial_number)
        response = subprocess.call(
            ['sh', execute_file, veea_hub_self_signed_cert, veea_hub_private_key, serial_number, "Success"])
        if response == 0:
            return True
        else:
            raise Exception("Exception trying execute the file {}".format(execute_file))

    def veea_hub_complete_downloading_and_configuration(self, serial_number):
        full_path_file = Path(__file__).resolve()
        execute_file = Path("{}/{}".format(full_path_file.parent, "/sh/devices/scripts/veeahub_completed.sh")).resolve()
        response = subprocess.call(['sh', execute_file, serial_number])
        if response == 0:
            return True
        else:
            raise Exception("Exception trying execute the file {}".format(execute_file))


# execute = ExecuteShFile()
# execute.veea_hub_start_software_downloading("C05BCB00C0A000001022")
# execute.veea_hub_complete_software_configuration("C05BCB00C0A000001022")
# execute.veea_hub_complete_downloading_and_configuration("C05BCB00C0A000001022")
