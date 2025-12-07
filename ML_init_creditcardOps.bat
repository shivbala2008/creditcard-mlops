@echo off
setlocal ENABLEDELAYEDEXPANSION

REM =====================================================
REM  Credit Card Fraud MLOps Project - Bootstrap Script
REM  Usage:
REM    1. Create an empty folder, e.g. C:\projects\creditcard-mlops
REM    2. Copy this file (init_mlops_project.bat) into that folder
REM    3. Double-click it OR run from cmd:  init_mlops_project.bat
REM =====================================================

echo Creating directory structure...

REM Top-level files
if not exist README.md type nul > README.md
if not exist requirements.txt type nul > requirements.txt
if not exist params.yaml type nul > params.yaml
if not exist dvc.yaml type nul > dvc.yaml
if not exist .gitignore type nul > .gitignore
if not exist .env.example type nul > .env.example

REM Data directories
if not exist data mkdir data
if not exist data\raw mkdir data\raw
if not exist data\processed mkdir data\processed
if not exist data\models mkdir data\models

REM Optionally create .gitkeep files to keep empty dirs in git
if not exist data\raw\.gitkeep type nul > data\raw\.gitkeep
if not exist data\processed\.gitkeep type nul > data\processed\.gitkeep
if not exist data\models\.gitkeep type nul > data\models\.gitkeep

REM src package
if not exist src mkdir src
if not exist src\__init__.py type nul > src\__init__.py
if not exist src\config.py type nul > src\config.py
if not exist src\data_prep.py type nul > src\data_prep.py
if not exist src\train.py type nul > src\train.py
if not exist src\evaluate.py type nul > src\evaluate.py
if not exist src\utils.py type nul > src\utils.py

REM service (API + Dockerfile)
if not exist service mkdir service
if not exist service\app.py type nul > service\app.py
if not exist service\model_loader.py type nul > service\model_loader.py
if not exist service\Dockerfile type nul > service\Dockerfile

REM monitoring (Prometheus + Grafana)
if not exist monitoring mkdir monitoring
if not exist monitoring\prometheus.yml type nul > monitoring\prometheus.yml
if not exist monitoring\grafana mkdir monitoring\grafana

REM tests
if not exist tests mkdir tests
if not exist tests\test_data_prep.py type nul > tests\test_data_prep.py
if not exist tests\test_train.py type nul > tests\test_train.py
if not exist tests\test_api.py type nul > tests\test_api.py

REM GitHub Actions CI
if not exist .github mkdir .github
if not exist .github\workflows mkdir .github\workflows
if not exist .github\workflows\ci.yml type nul > .github\workflows\ci.yml

echo.
echo Adding minimal starter comments to new files (without overwriting if already edited)...

REM Helper: only write header if file is empty
for %%F in (README.md requirements.txt params.yaml dvc.yaml .gitignore .env.example) do (
  for /f "usebackq delims=" %%L in ("%%F") do (
    set foundLine=1
    goto :skipTop
  )
  if not defined foundLine (
    if "%%F"=="README.md" echo # Credit Card Fraud Detection MLOps Project>%%F
    if "%%F"=="requirements.txt" echo # Add your Python dependencies here>%%F
    if "%%F"=="params.yaml" echo # YAML parameters for data, model, training, and mlflow>%%F
    if "%%F"=="dvc.yaml" echo # DVC pipeline stages will be defined here>%%F
    if "%%F"==".gitignore" echo .venv/>%%F
    if "%%F"==".env.example" echo # Example environment variables go here>%%F
  )
  set "foundLine="
  :skipTop
)

REM src files
for %%F in (src\config.py src\data_prep.py src\train.py src\evaluate.py src\utils.py src\__init__.py) do (
  if not exist %%F type nul > %%F
  for /f "usebackq delims=" %%L in ("%%F") do (
    set foundLine=1
    goto :skipSrc
  )
  if not defined foundLine (
    echo """%%~nxF - TODO: paste implementation from ChatGPT.""">%%F
  )
  set "foun
