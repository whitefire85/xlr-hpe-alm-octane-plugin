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


def convert_phase_names_to_ids(octane, phase_names):
    defect_phases = octane.get_defect_phases()
    phase_ids = []
    invalid_phase_names = []
    for phase_name in phase_names:
        if phase_name in defect_phases.keys():
            phase_ids.append(defect_phases[phase_name])
        else:
            invalid_phase_names.append(phase_name)

    if len(invalid_phase_names) > 0:
        mdl.print_header3("Invalid phase names detected.")
        mdl.println("Phase names %s do not exist." % invalid_phase_names)
        mdl.println("Available phase names are %s" % defect_phases.keys())
        raise Exception("Invalid phase names")
    return phase_ids


def convert_severity_names_to_ids(octane, severity_names):
    invalid_severity_names = []
    severity_ids = []
    defect_severities = octane.get_defect_severity()
    for severity_name in severity_names:
        if severity_name in defect_severities.keys():
            severity_ids.append(defect_severities[severity_name])
        else:
            invalid_severity_names.append(severity_name)
    if len(invalid_severity_names) > 0:
        mdl.print_header3("Invalid severity names detected.")
        mdl.println("severity names %s do not exist." % invalid_severity_names)
        mdl.println("Available severity names are %s" % severity_names.keys())
        raise Exception("Invalid severity names")
    return severity_ids

def fail_gate(msg):
    mdl.println(msg)
    raise Exception(msg)


octane = OctaneClient.get_client(octane_workspace)
phase_ids = convert_phase_names_to_ids(octane, queryDefectPhases)
severity_ids = convert_severity_names_to_ids(octane, queryDefectSeverity)
release_id = octane.resolve_entity_id("releases", releaseName)

response = octane.get_defects_in_phase_for_release_by_severity(release_id["id"], phase_ids, severity_ids, limit=1)
total_count = response["total_count"]
if thresholdOperator == "EQ" and threshold != total_count:
    fail_gate("Gate failed because threshold %s does not match number of defects found %s" % (threshold, total_count))
elif thresholdOperator == "GT" and threshold > total_count:
    fail_gate("Gate failed because threshold %s is greater than total defects found %s" % (threshold, total_count))
elif thresholdOperator == "LT" and threshold < total_count:
    fail_gate("Gate failed because threshold %s is less than total defects found %s" % (threshold, total_count))

mdl.println("Condition satified.  threshold %s %s %s defects found." % (threshold, thresholdOperator, total_count))
