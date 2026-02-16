@echo off
echo ========================================
echo GitHub Push Script - Cintabuku
echo ========================================
echo.

cd /d d:\uma\cintabuku

echo [1/7] Checking git...
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git not installed!
    pause
    exit /b 1
)

echo [2/7] Initializing git repository...
if not exist ".git" (
    git init
    echo - Git initialized
) else (
    echo - Already initialized
)

echo.
echo [3/7] Setting remote...
git remote remove origin >nul 2>&1
git remote add origin https://github.com/herulife/tokobuku.git
echo - Remote set to: https://github.com/herulife/tokobuku.git

echo.
echo [4/7] Adding files...
git add .
echo - Files added

echo.
echo [5/7] Committing...
git commit -m "Deploy: Cintabuku e-commerce application"
echo - Committed

echo.
echo [6/7] Setting branch to main...
git branch -M main
echo - Branch set to main

echo.
echo [7/7] Pushing to GitHub...
echo.
echo NOTE: Jika diminta login:
echo   Username: herulife
echo   Password: [GitHub Personal Access Token]
echo.
pause
git push -u origin main

echo.
echo ========================================
if errorlevel 0 (
    echo SUCCESS! Code pushed to GitHub
    echo.
    echo Next: Run deployment script
    echo   python scripts\deploy_from_github.py
) else (
    echo FAILED! Check error above
)
echo ========================================
echo.
pause
