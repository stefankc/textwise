REM Change directory and start Docker containers
cd text-reader-app
docker-compose up -d

REM Wait a few seconds for containers to initialize
timeout /t 5 /nobreak

REM Open default browser to localhost:3000
start http://localhost:3000