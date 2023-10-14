from ibm_schematics.schematics_v1 import *


def GetSchematicsService() :
    return SchematicsV1.new_instance()

def ListWorkspaces() :
    service = GetSchematicsService()
    response = service.list_workspaces()
    print(response.result)

def main() :
    ListWorkspaces()

main()