*** Variables ***
${VEEA_HUB_SERIAL_NUMBER_MEN}   C05BCB00C0A000001022
${VEEA_HUB_SERIAL_NUMBER_MN}   C05BCB00C0A000001023
${USER_NAME}   ronald.espinoza@mojix.com
${RESPONSE}   empty
${PREMIUM_PACKAGE}   2DD00F921A1B4C089B4F262591520387

*** Settings ***
#Resource          resource.robot
Library           ../business_logic/EnrollmentVeeahubManager.py
Library           ../business_logic/UnEnrollmentManager.py
Library           ../business_logic/ConfigurationStatusMeshManager.py   WITH NAME   meshConfigStatus
Library           ../business_logic/UpgradeMeshManager.py   WITH NAME   upgradeMesh
Library           ../business_logic/ExecuteShFile.py   WITH NAME   executeShell

*** Test Cases ***
Enroll a Veea Hub ${VEEA_HUB_SERIAL_NUMBER_MEN} (MEN) in new Mesh
    ${RESPONSE} =   enroll the veea hub in new mesh   ${VEEA_HUB_SERIAL_NUMBER_MEN}   ${USER_NAME}
    sleep    5s
    Set Global Variable   ${RESPONSE}

Add Veea Hub ${VEEA_HUB_SERIAL_NUMBER_MN} (MN) into already exists Mesh
    ${MESH_ID} =   get mesh id from enrollment response   ${RESPONSE}
    Set Global Variable   ${MESH_ID}
    ${RESPONSE} =   add veea hub in mesh   ${VEEA_HUB_SERIAL_NUMBER_MN}   ${MESH_ID}
    sleep    8s

Get Mesh configuration status after enrollment for user ${USER_NAME}
    ${RESPONSE}=   get configuration status mesh   ${USER_NAME}
    Set Global Variable   ${RESPONSE}
    meshConfigStatus.should return status code 200 after get configuration status mesh   ${RESPONSE}
    meshConfigStatus.check_assert_mesh_configuration_status_after_enrollment_veea_hub   ${RESPONSE}

VeeaHubs starting downloading and Complete its configuration after enrollment
    executeShell.veea_hub_complete_downloading_and_configuration   ${VEEA_HUB_SERIAL_NUMBER_MEN}
    executeShell.veea_hub_complete_downloading_and_configuration   ${VEEA_HUB_SERIAL_NUMBER_MN}
    sleep    10s

Upgrade Mesh with package ${PREMIUM_PACKAGE}
    ${RESPONSE}=   upgradeMesh.upgrade_mesh_with_premium_package   ${MESH_ID}   ${PREMIUM_PACKAGE}   ${USER_NAME}
    upgradeMesh.check_assert_action_in_mesh_should_be_recovery_after_upgrade   ${RESPONSE}
    sleep    10s

Get Mesh configuration status after upgrade the mesh for user ${USER_NAME}
    ${RESPONSE}=   get configuration status mesh   ${USER_NAME}
    Set Global Variable   ${RESPONSE}
    meshConfigStatus.should return status code 200 after get configuration status mesh   ${RESPONSE}
    meshConfigStatus.check_assert_mesh_configuration_status_after_upgrade_mesh   ${RESPONSE}

VeeaHubs starting downloading and Complete its configuration after upgrade
    executeShell.veea_hub_complete_downloading_and_configuration   ${VEEA_HUB_SERIAL_NUMBER_MEN}
    executeShell.veea_hub_complete_downloading_and_configuration   ${VEEA_HUB_SERIAL_NUMBER_MN}
    sleep    10s

Get Mesh configuration status after upgrade and complete its configuration of the mesh for user ${USER_NAME}
    ${RESPONSE}=   get configuration status mesh   ${USER_NAME}
    Set Global Variable   ${RESPONSE}
    meshConfigStatus.should return status code 200 after get configuration status mesh   ${RESPONSE}
    meshConfigStatus.check_assert_mesh_configuration_status_after_upgrade_mesh_and_complete_its_configuration   ${RESPONSE}

Un-enroll the Veea Hub ${VEEA_HUB_SERIAL_NUMBER_MN} and ${VEEA_HUB_SERIAL_NUMBER_MEN}
    sleep    8s
    un enrollment veea hub   ${VEEA_HUB_SERIAL_NUMBER_MN}   ${USER_NAME}
    un enrollment veea hub   ${VEEA_HUB_SERIAL_NUMBER_MEN}   ${USER_NAME}
