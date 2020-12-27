*** Variables ***
${VEEA_HUB_SERIAL_NUMBER_MEN}   C05BCB00C0A000001022
${VEEA_HUB_SERIAL_NUMBER_MN}   C05BCB00C0A000001023
${USER_NAME}   ronald.espinoza@mojix.com
${UN_ENROLLMENT_RESPONSE}   empty

*** Settings ***
#Resource          resource.robot
Library           ../business_logic/EnrollmentVeeahubManager.py
Library           ../business_logic/UnEnrollmentManager.py

*** Test Cases ***
Enroll Veea Hub ${VEEA_HUB_SERIAL_NUMBER_MEN} (MEN) in new Mesh
    ${ENROLLMENT_RESPONSE}=   enroll the veea hub in new mesh   ${VEEA_HUB_SERIAL_NUMBER_MEN}   ${USER_NAME}
    # Wait because the mesh is being created and the following step require meshId
    sleep    5s

Un-Enroll the Veea Hub ${VEEA_HUB_SERIAL_NUMBER_MEN} (MN)
    ${UN_ENROLLMENT_RESPONSE}=   un enrollment veea hub   ${VEEA_HUB_SERIAL_NUMBER_MEN}   ${USER_NAME}
    should return status code 200 after un enrollment   ${UN_ENROLLMENT_RESPONSE}
    sleep    5s
    data in database should be cleaned   ${VEEA_HUB_SERIAL_NUMBER_MEN}   ${USER_NAME}
