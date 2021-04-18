#!/usr/bin/python3

from os.path import exists
from sys import argv, exit, stderr
import json

def find_vulnerability_location(str, keyword):
    result = {
        "start_line": 1,
        "end_line": 1,
        "start_column": 1,
        "end_column": 1
    }
    for num, line in enumerate(str.split("\n")):
        if keyword in line:
            result["start_line"] = num + 1
            result["end_line"] = num + 1
            result["start_column"] = line.find(keyword) + 1
            result["end_column"] = line.find(keyword) + len(keyword)
            return result

if (len(argv) < 2):
    print("Please specify npm-audit-report.json path!", file=stderr)
    exit(1)

if (exists(argv[1]) == False):
    print(f"File {argv[1]} is not exists!", file=stderr)
    exit(1)

file = open(argv[1], "r")
original_file = file.read()
file.close()

# Check source of vulnerabilities
if (exists("package-lock.json")):
    resource = "package-lock.json"
elif (exists("yarn.lock")):
    resource = "yarn.lock"
else:
    resource = "N/A"
    
file = open(resource, "r")
pkg_lock = file.read()
file.close()

report = json.loads(original_file)
rules = []
results = []

for idx, finding_id in enumerate(report["advisories"].keys()):
    # Define default item value
    name = report["advisories"][finding_id]["module_name"]
    url = report["advisories"][finding_id]["url"] # Advisory URL
    cwe = report["advisories"][finding_id]["cwe"]

    if len(report["advisories"][finding_id]["cves"]) > 0:
        cve = "\r\n- ".join(report["advisories"][finding_id]["cves"])
    else:
        cve = "N/A"
    overview = report["advisories"][finding_id]["overview"]
    recommendation = report["advisories"][finding_id]["recommendation"]
    references = report["advisories"][finding_id]["references"]
    vulnerable_versions = report["advisories"][finding_id]["vulnerable_versions"]
    patched_versions = report["advisories"][finding_id]["patched_versions"]
    title = report["advisories"][finding_id]["title"] # vulnerability name

    # Convert severity to SARIF level
    if (report["advisories"][finding_id]["severity"] == "critical"):
        level = "error"
    elif (report["advisories"][finding_id]["severity"] == "high"):
        level = "error"
    elif (report["advisories"][finding_id]["severity"] == "medium"):
        level = "warning"
    else:
        level = "note"

    
    # Find vulnerability location
    location = find_vulnerability_location(pkg_lock, name)

    # Passing information to SARIF scheme
    rule = {
        "id": f"npm-audit-{finding_id}",
        "name": name,
        "shortDescription": {
            "text": overview
        },
        "fullDescription": {
            "text": overview
        },
        "help": {
            "text": f'"{name}\nVulnerabily Name: {title}\nCWE ID: {cwe}\nCVE:\n- {cve}\nRecommendation: {recommendation}\nVulnerable Versions: {vulnerable_versions}\nPatched Versions: {patched_versions}Reference: {references}"',
        },
        "defaultConfiguration": {
            "level": level
        }
    }
    result = {
        "ruleId": f"npm-audit-{finding_id}",
		"ruleIndex": idx,
		"level": "error",
		"message": {
			"text": f"npm-audit-{finding_id}"
		},
		"locations": [
			{
				"physicalLocation": {
					"artifactLocation": {
						"uri": resource
					},
					"region": {
						"startLine": location["start_line"],
						"endLine": location["end_line"],
                        "startColumn": location["start_column"],
                        "endColumn": location["end_column"]
					}
				}
			}
		]
	}
    rules.append(rule)
    results.append(result)

sarif_template_report = {
    "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
    "version": "2.1.0",
    "runs": []
}

set_run = {
    "tool":{
		"driver": {
			"name": "checkov",
			"version": "2.1.0",
			"informationUri": "https://github.com/bridgecrewio/checkov/",
            "rules": rules
        }
    },
    "results": results
}
sarif_template_report["runs"].append(set_run)
print(json.dumps(sarif_template_report))