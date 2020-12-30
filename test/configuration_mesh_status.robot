*** Variables ***
${VEEA_HUB_SERIAL_NUMBER_MEN}   C05BCB00C0A000001022
${VEEA_HUB_SERIAL_NUMBER_MN}   C05BCB00C0A000001023
${USER_NAME}   ronald.espinoza@mojix.com
${ENROLLMENT_RESPONSE}   empty

*** Settings ***
#Resource          resource.robot
Library           ../business_logic/EnrollmentVeeahubManager.py
Library           ../business_logic/UnEnrollmentManager.py
Library           ../business_logic/ConfigurationStatusMeshManager.py   WITH NAME   meshConfigStatus

*** Test Cases ***
Enroll a Veea Hub ${VEEA_HUB_SERIAL_NUMBER_MEN} (MEN) in new Mesh
    ${ENROLLMENT_RESPONSE} =   enroll the veea hub in new mesh   ${VEEA_HUB_SERIAL_NUMBER_MEN}   ${USER_NAME}
    sleep    5s
    Set Global Variable   ${ENROLLMENT_RESPONSE}

Add Veea Hub ${VEEA_HUB_SERIAL_NUMBER_MN} (MN) into already exists Mesh
    ${MESH_ID} =   get mesh id from enrollment response   ${ENROLLMENT_RESPONSE}
    ${ENROLLMENT_RESPONSE} =   add veea hub in mesh   ${VEEA_HUB_SERIAL_NUMBER_MN}   ${MESH_ID}
    sleep    5s

Get Mesh configuration status for user ${USER_NAME}
    ${ENROLLMENT_RESPONSE}=   get configuration status mesh   ${USER_NAME}
    Set Global Variable   ${ENROLLMENT_RESPONSE}
    meshConfigStatus.should return status code 200 after get configuration status mesh   ${ENROLLMENT_RESPONSE}
    meshConfigStatus.check_assert_mesh_configuration_status_after_enrollment_veea_hub   ${ENROLLMENT_RESPONSE}


Un-enroll the Veea Hub ${VEEA_HUB_SERIAL_NUMBER_MN} and ${VEEA_HUB_SERIAL_NUMBER_MEN}
    sleep    5s
    un enrollment veea hub   ${VEEA_HUB_SERIAL_NUMBER_MN}   ${USER_NAME}
    un enrollment veea hub   ${VEEA_HUB_SERIAL_NUMBER_MEN}   ${USER_NAME}






