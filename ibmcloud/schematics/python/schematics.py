from ibm_schematics.schematics_v1 import *
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import sys, os

def GetSchematicsService() :
    return SchematicsV1.new_instance()

def ListWorkspaces() :
    service = GetSchematicsService()
    response = service.list_workspaces()
    print(response)

def main() :
    iam_api_key = sys.argv[1]
    os.environ["SCHEMATICS_APIKEY"] = iam_api_key
    os.environ["SCHEMATICS_URL"] = 'https://schematics.cloud.ibm.com'
    print("===== LISTING WORKSPACES =====")
    ListWorkspaces()
    print("===== END =====")

main()