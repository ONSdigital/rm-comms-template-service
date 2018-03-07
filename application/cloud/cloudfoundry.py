import cfenv
import re


class ONSCloudFoundry(object):

    def __init__(self):
        self._cf_env = cfenv.AppEnv()

    @property
    def detected(self):
        return self._cf_env.app

    @property
    def db(self):
        return self._cf_env.get_service(label=re.compile(r'rds*'))
