import re
import urllib
import requests

from pyhellofax.utils import convert_to_utf8_str
from pyhellofax.exceptions import HelloFaxAPIException

re_path_template = re.compile('{\w+}')


def bind_api_method(**config):

    class APIMethod(object):

        path = config['path']
        allowed_param = config.get('allowed_param', [])
        method = config.get('method', 'GET')
        require_auth = config.get('require_auth', True) #almost all methods required authentication

        def __init__(self, api, args, kargs):
            # If authentication is required and no credentials
            # are provided, throw an error.
            if self.require_auth and not (api.email and api.password and api.guid):
                raise Exception('Authentication required!')

            self.api = api
            self.build_parameters(args, kargs)

            # Perform any path variable substitution
            self.build_path()

        def build_parameters(self, args, kargs):
            self.parameters = {}
            for idx, arg in enumerate(args):

                try:
                    self.parameters[self.allowed_param[idx]] = convert_to_utf8_str(arg)
                except IndexError:
                    raise Exception('Too many parameters supplied!')

            for k, arg in kargs.items():
                if arg is None:
                    continue
                if k in self.parameters:
                    raise Exception('Multiple values for parameter %s supplied!' % k)

                self.parameters[k] = convert_to_utf8_str(arg)

        def build_path(self):
            for variable in re_path_template.findall(self.path):
                name = variable.strip('{}')
                if name == 'guid' and self.api.guid:
                    # No 'user' parameter provided, fetch it from current user_id instead.
                    value = self.api.guid
                else:
                    try:
                        value = urllib.quote(self.parameters[name])
                    except KeyError:
                        raise Exception('No parameter value found for path variable: %s' % name)
                    del self.parameters[name]
                self.path = self.path.replace(variable, value)

        def execute(self):
            # Build the request URL
            url = "https://%s%s%s" % (self.api.host, self.api.api_root, self.path)
            auth = (self.api.email, self.api.password) if self.require_auth else None
            try:
                response = requests.request(self.method, url, data=self.parameters, auth=auth)
            except Exception, ex:
                raise HelloFaxAPIException('Failed requesting hellofax api: %s' % ex)

            if response.status_code != 200:
                raise HelloFaxAPIException(response.content)

            return response.content


    def _call(api, *args, **kargs):

        method = APIMethod(api, args, kargs)
        return method.execute()

    return _call
  