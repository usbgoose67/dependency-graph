@echo off
cd /d "%~dp0"

echo =====================================
echo RUNNING ALL UNIT TESTS
echo =====================================
echo.

python -m unittest discover -s tests -p "test_*.py" -v

if errorlevel 1 (
    echo.
    echo TESTS FAILED
    pause
    exit /b 1
)

echo.
echo ALL TESTS PASSED
pause