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
feature_id = octane.resolve_entity_id("work_items", "Backlog")
endpoint = 'list_nodes?query="(list_root={logical_name = ^list_node.item_origin^ })"'
origin_list_nodes = octane.get_response_for_endpoint('GET', endpoint, "Could not execute query.")
if origin_list_nodes["total_count"] <= 1:
  raise Exception("Cannot resolve list_nodes with root name list_node.item_origin")
item_origin = None
for list_node in origin_list_nodes["data"]:
  if list_node["name"] == "Xebia":
    item_origin = list_node
if item_origin is None:
  request_body = {
    "data": [
      {
        "name": defectName,
        "description": defectDescription,
        "parent": {
          "type": "work_item",
          "id": feature_id["id"]
        }
      }
    ]
  }
else:
  request_body = {
    "data": [
      {
        "name": defectName,
        "description": defectDescription,
        "item_origin": {
          "type": "list_node",
          "id": item_origin["id"]
        },
        "parent": {
          "type": "work_item",
          "id": feature_id["id"]
        }
      }
    ]
  }

response = octane.get_response_for_endpoint("POST", "defects", "Failed to create defect.", json_data=request_body)
defectId = response["data"][0]["id"]
defectUrl = octane.generate_defect_url(feature_id)

mdl.println("[Defect %s](%s) created." % (defectId, defectUrl))
