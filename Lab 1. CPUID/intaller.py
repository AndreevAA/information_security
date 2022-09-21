# file == bd os.tmpfile()
from sys import platform
from subprocess import check_output
import hashlib
import os

# Elem struct
class LElem:
    def __init__(self, hard_uuid, serial_num):
        self.hard_uuid = hard_uuid
        self.serial_num = serial_num

    def get_sum_str(self):
        return self.hard_uuid + " " + self.serial_num

# License object
class License:
    _pwd_license_key = ""

    # Initialization with key's pwd 
    def __init__(self, pwd_license_key):
        self._pwd_license_key = pwd_license_key

    # Method of writing license
    def to_license_key(self):
        with open(self._pwd_license_key, "w") as lic_file:
            lic_file.write(self._get_CPUsum())

    # Method of getting license
    def from_license_key(self):
        with open(self._pwd_license_key, "r") as lic_file:
            return lic_file.readline()

    # Private method of platform composite
    def _get_CPUsum(self):
        if platform == "win32":  
            tmp_elem = self._get_lelem_win32()
        elif platform == "linux" or platform == "linux2": #dmidecode | grep -i uuid 
            tmp_elem = self._get_lelem_linux()
        elif platform == "darwin":
            tmp_elem = self._get_lelem_darwin()

        return hashlib.sha256(tmp_elem.get_sum_str().encode('utf-8')).hexdigest()

    # Private method of verification
    def check_CPUsum(self):
        if self.from_license_key() != self._get_CPUsum():
            return False
        return True

    # Private method of win32 info getter
    def _get_lelem_win32(self):
        output_uuid = check_output("wmic csproduct get UUID", shell=True).decode()
        output_sn = output = check_output("wmic csproduct get IdentifyingNumber", shell=True).decode()

        return LElem(
            hard_uuid = output_uuid.split("\n")[1], 
            serial_num = output_sn.split("\n")[1]
            )

    # Private method of linux/2 info getter
    def _get_lelem_linux(self):
        output = check_output("dmidecode -s system-uuid", shell=True).decode()

        return LElem(
            hard_uuid = output.split(":")[1][1:-1], 
            serial_num = check_output("dmidecode -s system-serial-number", shell=True).decode()
            )

    # Private method of darwin(MacOS) info getter
    def _get_lelem_darwin(self):
        output_uuid = check_output("system_profiler SPHardwareDataType | grep UUID", shell=True).decode()
        output_sn = output = check_output("system_profiler SPHardwareDataType | grep Serial", shell=True).decode()

        return LElem(
            hard_uuid = output_uuid.split(":")[1][1:-1], 
            serial_num = output_sn.split(":")[1][1:-1]
            )

if __name__ == "__main__":
    license = License("license.key")

    license.to_license_key()
    print(license.from_license_key())
