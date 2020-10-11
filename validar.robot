*** Settings ***
Library           SeleniumLibrary

*** Variables ***
${SERVER}         https://www.google.com/
${BROWSER}        Chrome
${DELAY}          5s
${VALID USER}     demo
${VALID PASSWORD}    mode
${LOGIN URL}      https://www.google.com/
${WELCOME URL}    http://${SERVER}/welcome.html
${ERROR URL}      http://${SERVER}/error.html

*** Test Cases ***
Open Browser To Login Page
    Open Browser    ${LOGIN URL}    ${BROWSER}
    Maximize Browser Window
    Set Selenium Speed    ${DELAY}
    Close Browser