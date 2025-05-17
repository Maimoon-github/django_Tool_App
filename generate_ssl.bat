@echo off
powershell -NoProfile -ExecutionPolicy Bypass -Command "& { Start-Process PowerShell -ArgumentList '-NoProfile -ExecutionPolicy Bypass -File "".\generate_ssl.ps1""' -Verb RunAs }"
