@echo off
docker version 
IF %ERRORLEVEL% EQU 0 (
    echo "Docker is installed!"
) ELSE (
    echo "Please install Docker before running!"
    EXIT 1
)
docker-compose pull
echo "Done!"
