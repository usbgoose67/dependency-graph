@echo off
cd /d "%~dp0"

echo =====================================
echo GRAPH DEMONSTRATION
echo =====================================
echo.

echo [1/3] PACKAGE A
python -m src.main --package A --repo tests/data/normal.txt --test --output a.svg --ascii
if errorlevel 1 goto failed

echo.
echo [2/3] PACKAGE B
python -m src.main --package B --repo tests/data/normal.txt --test --output b.svg --ascii
if errorlevel 1 goto failed

echo.
echo [3/3] PACKAGE C
python -m src.main --package C --repo tests/data/normal.txt --test --output c.svg --ascii
if errorlevel 1 goto failed

echo.
echo =====================================
echo ALL THREE GRAPHS GENERATED
echo =====================================
echo Files:
echo output\a.svg
echo output\b.svg
echo output\c.svg

pause
exit /b 0

:failed
echo.
echo ERROR: Graph generation failed.
pause
exit /b 1