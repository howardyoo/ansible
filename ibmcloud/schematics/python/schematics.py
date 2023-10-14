from ibm_platform_services.schematics_v1 import *

def GetSchematicsService():
    return SchematicsV1.new_instance()

def ListWorkspaces():
    service = GetSchematicService()
    response = service.list_workspaces()
    print(response.result)