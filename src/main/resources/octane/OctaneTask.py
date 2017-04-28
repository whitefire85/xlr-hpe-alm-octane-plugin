#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

from octane.Octane import OctaneClient

octane = OctaneClient.get_client(octane_authentication)
method = str(task.getTaskType()).lower().replace('.', '_')
call = getattr(octane, method)
response = call(locals())
for key,value in response.items():
    locals()[key] = value