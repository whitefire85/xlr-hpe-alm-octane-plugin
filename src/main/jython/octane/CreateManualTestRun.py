#
# Copyright 2017 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

from octane.Octane import OctaneClient
from markdown_logger import MarkdownLogger as mdl
import json
octane = OctaneClient.get_client(octane_workspace)
manual_test_id = octane.resolve_entity_id("manual_tests", testName)["id"]
release_id = octane.resolve_entity_id("releases", releaseName)["id"]
statuses = octane.get_manual_run_native_statuses()
if not status in statuses.keys():
  raise Exception("Unknown status %s" % status)



request_body = {
  "data": [
    {
      "name": runName,
      "description": runDescription,
      "test": {
        "type": "test_manual",
        "id": manual_test_id
      },
      "release": {
        "type": "release",
        "id": release_id
      },
      "native_status": {
        "type": "list_node",
        "id": statuses[status]
      }
    }
  ]
}

response = octane.get_response_for_endpoint("POST", "manual_runs", "Failed to create test run.", json_data=request_body)
runId = response["data"][0]["id"]
runUrl = octane.generate_test_run_url(runId)

mdl.println("[Test run %s](%s) created." % (runId, runUrl))
