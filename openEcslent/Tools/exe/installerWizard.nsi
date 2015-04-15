; Script generated by the HM NIS Edit Script Wizard.

; HM NIS Edit Wizard helper defines
!define PRODUCT_NAME "ECSLENT - Intelligent Aggressor"
!define PRODUCT_VERSION "Beta"
!define PRODUCT_PUBLISHER "Evolutionary Computing Systems Lab (ECSL)"
!define PRODUCT_WEB_SITE "http://ecsl.cse.unr.edu"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
!define PRODUCT_UNINST_ROOT_KEY "HKLM"

; MUI 1.67 compatible ------
!include "MUI.nsh"
!include "ZipDLL.nsh"

; MUI Settings
!define MUI_ABORTWARNING
!define MUI_ICON "${NSISDIR}\Contrib\Graphics\Icons\modern-install.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall.ico"

; Welcome page
;!insertmacro MUI_PAGE_WELCOME
; License page
!insertmacro MUI_PAGE_LICENSE "License.txt"
; Directory page
!insertmacro MUI_PAGE_DIRECTORY
; Instfiles page
!insertmacro MUI_PAGE_INSTFILES
; Finish page
;!insertmacro MUI_PAGE_FINISH

; Uninstaller pages
!insertmacro MUI_UNPAGE_INSTFILES

; Language files
!insertmacro MUI_LANGUAGE "English"

; MUI end ------

Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "ECSLENTSetup.exe"
InstallDir "$DOCUMENTS\ECSLENT"
ShowInstDetails show
ShowUnInstDetails show

Section "ECSLENT" SEC01
  SetOutPath "$INSTDIR"
  SetOverwrite ifnewer
  File "ecslent.zip"
  ZipDLL::extractall "$INSTDIR\ecslent.zip" "$INSTDIR\"

; write uninstaller
;  WriteUninstaller $INSTDIR\ECSLENTUninstall.exe
  CreateDirectory "$SMPROGRAMS\ECSLENT"
  CreateShortCut "$SMPROGRAMS\ECSLENT\ECSLENT.lnk" "$INSTDIR\main.exe"
  CreateShortCut "$SMPROGRAMS\ECSLENT\ECSLENTUninstall.lnk" "$INSTDIR\ECSLENTUninstall.exe"
;  CreateShortCut "$SMPROGRAMS\ECSLENT\ECSLENT.lnk" "$INSTDIR\main.exe"
  CreateShortCut "$DESKTOP\ECSLENT.lnk" "$INSTDIR\main.exe"
SectionEnd

Section -AdditionalIcons
  WriteIniStr "$INSTDIR\${PRODUCT_NAME}.url" "InternetShortcut" "URL" "${PRODUCT_WEB_SITE}"
  CreateShortCut "$SMPROGRAMS\ECSLENT\Website.lnk" "$INSTDIR\${PRODUCT_NAME}.url"
;  CreateShortCut "$SMPROGRAMS\ECSLENT\Uninstall.lnk" "$INSTDIR\ECSLENTUninstall.exe"
SectionEnd

Section -Post
  WriteUninstaller "$INSTDIR\ECSLENTUninstall.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayName" "$(^Name)"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\ECSLENTUninstall.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
SectionEnd


Function un.onUninstSuccess
  HideWindow
  MessageBox MB_ICONINFORMATION|MB_OK "ECSLENT was successfully removed from your computer."
FunctionEnd

Function un.onInit
  MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 "Are you sure you want to completely remove ECSLENT and all of its components?" IDYES +2
  Abort
FunctionEnd

Section Uninstall
  Delete "$INSTDIR\${PRODUCT_NAME}.url"
  Delete "$INSTDIR\ECSLENTUninstall.exe"
  Delete "$INSTDIR\ecslent.zip"


;  Delete "$SMPROGRAMS\ECSLENT"

  RMDir /r "$SMPROGRAMS\ECSLENT"

  
  RMDir /r "$INSTDIR"
  RMDir "$INSTDIR"
  Delete "$SMPROGRAMS\ECSLENT\ECSLENT.lnk"
  Delete "$SMPROGRAMS\ECSLENT\ECSLENTUninstall.lnk"
;  Delete "$SMPROGRAMS\ECSLENT\ECSLENT.lnk"
  Delete "$SMPROGRAMS\ECSLENT\Website.lnk"
  Delete "$DESKTOP\ECSLENT.lnk"
  DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}"
  SetAutoClose true
SectionEnd


;________________________________________________________________________________
; Helper Functions

;________________________________________________________________________________
; These three taken from NSIS wiki
Function un.RMDirUP
         !define RMDirUP '!insertmacro RMDirUPCall'

         !macro RMDirUPCall _PATH
                push '${_PATH}'
                Call un.RMDirUP
         !macroend

         ; $0 - current folder
         ClearErrors

         Exch $0
         ;DetailPrint "ASDF - $0\.."
         RMDir "$0\.."

         IfErrors Skip
         ${RMDirUP} "$0\.."
         Skip:

         Pop $0
FunctionEnd
