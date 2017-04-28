#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import requests
from requests import Request

class OctaneClient(object):
    def __init__(self, octane_authentication):
        self.url = octane_authentication["url"]
        self.client_id = octane_authentication["client_id"]
        self.client_secret = octane_authentication["client_secret"]
        self.headers = {}

    @staticmethod
    def get_client(octane_authentication):
        return OctaneClient(octane_authentication)

    def octane_getepics(self, variables):
        self.login()
        endpoint = "api/shared_spaces/%s/workspaces/%s/epics" %(variables['shared_space_uid'], variables['workspace_id'])
        response = self.get_response_for_endpoint('GET', endpoint, "Could not retrieve stories.")
        return {'output' : response}

    def login(self):
        endpoint = "/authentication/sign_in"
        content = {"client_id" : "%s" % self.client_id, "client_secret" : "%s" % self.client_secret}
        session = requests.Session()
        headers_dict = {"contentType" : "application/json", "Cookie" : "LWSSO_COOKIE_KEY"}
        req = Request('post', "%s%s" % (self.url, endpoint), json=content, headers=headers_dict)
        prepped = session.prepare_request(req)
        resp = session.send(prepped, verify=False)
        if resp.status_code != 200:
            raise Exception("Failed To Authenticate.")
        cookies_dict = session.cookies.get_dict()
        self.headers={"Cookie" : "LWSSO_COOKIE_KEY=%s" % cookies_dict['LWSSO_COOKIE_KEY']}

    def open_url(self, method, url, headers=None, data=None, json_data=None):
        if headers is None:
            headers = self.headers
        return requests.request('%s' % method, url, data=data, json=json_data, headers=headers, verify=False)

    def get_response_for_endpoint(self, method, endpoint, error_message, object_id=None, json_data=None, data=None, headers=None):
        full_endpoint_url = "%s/%s" % (self.url, endpoint)
        if object_id is not None and object_id:
            full_endpoint_url = "%s/%s" % (full_endpoint_url, object_id)
        response = self.open_url(method, full_endpoint_url, headers=headers, json_data=json_data, data=data)
        if not response.ok:
            raise Exception("Error: %s, status code: %s, message: %s" % (error_message, response.status_code, response.text))
        return response.text
