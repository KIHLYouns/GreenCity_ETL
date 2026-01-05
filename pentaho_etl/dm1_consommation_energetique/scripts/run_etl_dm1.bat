@echo off
REM ================================================================
REM   ETL Data Mart 1 - Consommation Énergétique
REM   GreenCity BI Project
REM   Exécution automatique
REM ================================================================

echo ================================================================
echo   ETL DATA MART 1 - GREEN CITY
echo   Date : %date%
echo   Heure : %time%
echo ================================================================

REM === 1. CHEMIN VERS PENTAHO (CORRIGÉ GRÂCE AU DETECTIVE) ===
set PENTAHO_HOME=C:\Users\Lenovo\Downloads\pdi-ce-10.2.0.0-222\data-integration

REM === 2. CHEMINS DE TON PROJET ===
set JOB_DIR=C:\GreenCity_BI\pentaho\jobs
set LOG_DIR=C:\GreenCity_BI\pentaho\logs
set JOB_NAME=job_etl_dm1_consommation.kjb

REM === 3. CREATION DU DOSSIER LOG S'IL MANQUE ===
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

REM === 4. NOM DU FICHIER LOG ===
set CURRENT_TIME=%time: =0%
set LOG_FILE=%LOG_DIR%\etl_%date:~6,4%-%date:~3,2%-%date:~0,2%_%CURRENT_TIME:~0,2%h%CURRENT_TIME:~3,2%.log

REM === 5. VERIFICATION CRITIQUE ===
if not exist "%PENTAHO_HOME%\Kitchen.bat" (
    echo.
    echo [ERREUR] Toujours pas trouve !
    echo Je cherche ici : %PENTAHO_HOME%\Kitchen.bat
    echo Verifie que tu n'as pas deplace le dossier depuis le test Detective.
    pause
    exit /b 1
)

REM === 6. EXECUTION DU JOB ===
echo.
echo Lancement de Pentaho (Kitchen)...
echo Veuillez patienter, cela peut prendre quelques secondes...
cd /d "%PENTAHO_HOME%"

call Kitchen.bat /file:"%JOB_DIR%\%JOB_NAME%" /level:Basic /log:"%LOG_FILE%"

REM === 7. BILAN ===
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================================
    echo  [SUCCES] BRAVO ! L'ETL a termine correctement.
    echo  Tu peux voir le rapport ici : %LOG_FILE%
    echo ========================================================
    color 2
) else (
    echo.
    echo ========================================================
    echo  [ECHEC] Mince, une erreur est survenue pendant l'ETL.
    echo  Regarde le fichier log pour comprendre : %LOG_FILE%
    echo ========================================================
    color 4
)

echo.
pause