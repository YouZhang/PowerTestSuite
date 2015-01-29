cd %~dp0
REM cmd tool\emon\DisableSignatureEnforcement.bat
bcdedit -set loadoptions DISABLE_INTEGRITY_CHECKS
bcdedit -set TESTSIGNING ON
enableApp_InternalOnly.exe
InitReg.bat
