@echo off
cd /d "%~dp0"
python -m src.main --package org.slf4j:slf4j-api --repo https://repo.maven.apache.org/maven2 --version 2.0.13 --output graph.svg --ascii
pause
