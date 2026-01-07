@echo off
REM ============================================================
REM Script d'automatisation ETL Data Mart Rentabilite GreenCity
REM Date de creation : 07/01/2026
REM Description : Execute le job Pentaho tous les jours a 02h00
REM ============================================================

REMDefinir les chemins
SET PENTAHO_HOME=C:\Users\hp\Downloads\pdi-ce-10.2.0.0-222\data-integration
SET JOB_PATH=C:\Pentaho_Projects\Greencity\JOB_DM_Rentabilite_COMPLET.kjb
SET LOG_DIR=C:\Pentaho_Projects\Greencity\logs
SET LOG_FILE=%LOG_DIR%\etl_rentabilite_%date:~-4,4%%date:~-7,2%%date:~-10,2%_%time:~0,2%%time:~3,2%%time:~6,2%.log

REM Creer le repertoire de logs s'il n'existe pas
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

REM Afficher l'heure de debut
echo ============================================================ >> "%LOG_FILE%"
echo DEBUT EXECUTION ETL DATA MART RENTABILITE >> "%LOG_FILE%"
echo Date/Heure : %date% %time% >> "%LOG_FILE%"
echo ============================================================ >> "%LOG_FILE%"
echo. >> "%LOG_FILE%"

REM Se placer dans le repertoire Pentaho
cd /d "%PENTAHO_HOME%"

REM Executer le job Pentaho avec Kitchen.bat
call Kitchen.bat /file:"%JOB_PATH%" /level:Basic >> "%LOG_FILE%" 2>&1

REM Capturer le code de sortie
SET EXIT_CODE=%ERRORLEVEL%

REM Afficher le resultat
echo. >> "%LOG_FILE%"
echo ============================================================ >> "%LOG_FILE%"
if %EXIT_CODE%==0 (
    echo STATUT : SUCCES >> "%LOG_FILE%"
    echo Le job ETL s'est termine avec succes. >> "%LOG_FILE%"
) else (
    echo STATUT : ERREUR >> "%LOG_FILE%"
    echo Le job ETL a echoue avec le code d'erreur : %EXIT_CODE% >> "%LOG_FILE%"
)
echo Heure de fin : %date% %time% >> "%LOG_FILE%"
echo ============================================================ >> "%LOG_FILE%"

REM Envoyer une notification par email (optionnel - necessite configuration SMTP)
REM call send_notification.bat %EXIT_CODE%

exit /b %EXIT_CODE%