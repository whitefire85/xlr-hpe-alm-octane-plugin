#
# Copyright 2017 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import requests
from requests import Request
from markdown_logger import MarkdownLogger as mdl

class OctaneClient(object):
    def __init__(self, octane_workspace):
        self.url = octane_workspace["url"]
        self.client_id = octane_workspace["client_id"]
        self.client_secret = octane_workspace["client_secret"]
        self.shared_space_uid = octane_workspace["shared_space_uid"]
        self.workspace_id = octane_workspace["workspace_id"]
        self.headers = {}
        self.logged_in = False

    @staticmethod
    def get_client(octane_workspace):
        return OctaneClient(octane_workspace)

    def generate_defect_url(self, defect_id):
        # https://mqast001pngx.saas.hpe.com/ui/?p=190188/1002#/product-overview/hierarchy/defects?selectedEntities=%5B%222001%22%5D
        return "%s/ui?p=%s/%s#/product-overview/hierarchy/defects?selectedEntities=[\"%s\"]" % (self.url, self.shared_space_uid, self.workspace_id, defect_id)

    def get_defect_phases(self):
        query_result = self.query("phases", "logical_name EQ ^phase.defect.*^", ["name"])
        lookup = {}
        for phase in query_result["data"]:
            lookup[phase["name"]] = phase["id"]
        return lookup

    def get_defects_in_phase_for_feature(self, feature_id, phase_ids=[], negate=False, limit=20):
        #"parent EQ {id EQ 3001};((phase EQ {id EQ 1002})||(phase EQ {id EQ 1001}))"
        query = "parent EQ {id EQ %s}" % feature_id
        if len(phase_ids) > 0:
            phase_query = ["(phase EQ {id EQ %s})" % p for p in phase_ids]
            phase_query_string = "||".join(phase_query)
            if not negate:
                query = "%s;(%s)" % (query, phase_query_string)
            else:
                query = "%s;!(%s)" % (query, phase_query_string)
        mdl.println(query)
        query_result = self.query("defects", query, ["id","name"], limit=limit)
        return query_result

    def resolve_entity_id(self, entity_type, entity_name):
        query_result = self.query(entity_type, "name EQ ^%s^" % entity_name, ["id", "name"])
        if query_result["total_count"] != 1:
            raise Exception("Cannot resolve %s with name '%s'" % (entity_type, entity_name))
        return query_result["data"][0]

    def query(self, entity_type, query_statement, fields=[], limit=20):
        endpoint = '%s?query="%s"&limit=%s' % (entity_type, query_statement, limit)
        if len(fields) > 0:
            endpoint="%s&fields=%s" % (endpoint, ",".join(fields))
        response = self.get_response_for_endpoint('GET', endpoint, "Could not execute query.")
        return response

    def _login(self):
        if not self.logged_in:
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
            self.logged_in = True

    def _open_url(self, method, url, headers=None, data=None, json_data=None):
        if headers is None:
            headers = self.headers
        return requests.request('%s' % method, url, data=data, json=json_data, headers=headers, verify=False)

    def get_response_for_endpoint(self, method, endpoint, error_message, object_id=None, json_data=None, data=None, headers=None):
        self._login()
        full_endpoint_url = "%s/api/shared_spaces/%s/workspaces/%s/%s" % (self.url, self.shared_space_uid, self.workspace_id, endpoint)
        if object_id is not None and object_id:
            full_endpoint_url = "%s/%s" % (full_endpoint_url, object_id)
        response = self._open_url(method, full_endpoint_url, headers=headers, json_data=json_data, data=data)
        if not response.ok:
            mdl.print_error("Error: %s, status code: %s, message: %s" % (error_message, response.status_code, response.text))
            raise Exception("Call to HPE ALM Octane failed.")
        return response.json()
