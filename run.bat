@echo off
cd /d "%~dp0"
python -m src.main --package F --repo tests/data/normal.txt --test --reverse
pause
