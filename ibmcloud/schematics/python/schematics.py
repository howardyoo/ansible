from ibm_schematics.schematics_v1 import *
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import sys, os

def GetSchematicsService() :
    return SchematicsV1.new_instance()

def ListWorkspaces() :
    service = GetSchematicsService()
    response = service.list_workspaces(offset=0, limit=1000)
    if response.status_code == 200:
        workspaces = response.result['workspaces']
        inactive_workspaces = 0
        active_workspaces = 0
        for workspace in workspaces:
            if workspace['status'] == "INACTIVE" and workspace['last_action_name'] == "DESTROY":
                inactive_workspaces = inactive_workspaces+1
                print(f"[DELETING INACTIVE] {workspace['id']} / {workspace['name']}")
                service.delete_workspace(w_id=workspace['id'])
            if workspace['status'] == "ACTIVE":
                active_workspaces = active_workspaces+1
        print(f"active workspaces: {active_workspaces}, inactive workspaces: {inactive_workspaces}")

def main() :
    iam_api_key = sys.argv[1]
    os.environ["SCHEMATICS_APIKEY"] = iam_api_key
    os.environ["SCHEMATICS_URL"] = 'https://schematics.cloud.ibm.com'
    print("===== LISTING WORKSPACES =====")
    ListWorkspaces()
    print("===== END =====")

main()