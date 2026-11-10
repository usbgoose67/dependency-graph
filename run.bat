@echo off
cd /d "%~dp0"

echo =====================================
echo MAVEN DEPENDENCY GRAPH - STAGE 5
echo =====================================
echo.

python -m src.main --package A --repo tests/data/normal.txt --test --version 1.0 --output graph.svg --ascii

if errorlevel 1 (
    echo.
    echo ERROR: Program failed.
    pause
    exit /b 1
)

echo.
echo Graph successfully generated.
echo Check output\graph.svg

pause