from ibm_schematics.schematics_v1 import *
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import sys, os
import requests

def GetRefreshToken() :
    api_token = os.environ["SCHEMATICS_APIKEY"]
    refresh_token = None
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey" : f"{api_token}",
        "user": "bx:bx"
    }
    try:
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            refresh_token = response.json().get('access_token')
    except requests.exceptions.RequestException as e:
        print("Error:", e)
    return refresh_token

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
                print(f"[DELETING INACTIVE] {workspace['id']} / {workspace['name']} ...")
                refresh_token = GetRefreshToken()
                if refresh_token is not None:
                    delete_response = service.delete_workspace(refresh_token=refresh_token, w_id=workspace['id'], destroy_resources='true')
                    print(delete_response)
                else:
                    print("refresh_token was not available, thus skipping delete_workspace..")
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