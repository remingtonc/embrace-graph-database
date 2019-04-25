@echo off
echo "Rebuilding containers!"
CALL .\stop.bat
docker-compose build
CALL .\start.bat
echo "Done!"
