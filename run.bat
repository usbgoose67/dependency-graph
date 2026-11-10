@echo off
cd /d "%~dp0"
python -m src.main --package A --repo tests/data/empty.txt --test --version 1.0 --output graph.svg
pause
