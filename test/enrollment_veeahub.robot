*** Variables ***
${VEEA_HUB_SERIAL_NUMBER_MEN}   C05BCB00C0A000001022
${VEEA_HUB_SERIAL_NUMBER_MN}   C05BCB00C0A000001023
${USER_NAME}   ronald.espinoza@mojix.com
${ENROLLMENT_RESPONSE}   empty

*** Settings ***
#Resource          resource.robot
Library           ../business_logic/ManagerEnrollVeeaHub.py
*** Test Cases ***
Enroll a Veea Hub MEN
    ${ENROLLMENT_RESPONSE} =   enroll the veea hub in new mesh   ${VEEA_HUB_SERIAL_NUMBER_MEN}   ${USER_NAME}
    should return status code 200 after enroll veea hub   ${ENROLLMENT_RESPONSE}
    sleep    5s
    response data should match with database   ${ENROLLMENT_RESPONSE}
    Set Global Variable   ${ENROLLMENT_RESPONSE}

Add Veea Hub in Mesh alread exists MN
    ${MESH_ID} =   get mesh id from enrollment response   ${ENROLLMENT_RESPONSE}
    ${ENROLLMENT_RESPONSE} =   add veea hub in mesh   ${VEEA_HUB_SERIAL_NUMBER_MN}   ${MESH_ID}
    sleep    5s
    response data should match with database   ${ENROLLMENT_RESPONSE}








