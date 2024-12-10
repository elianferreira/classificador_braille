@echo off
setlocal

REM Caminho para o arquivo HTML na pasta template
set "HTML_PATH=%cd%\templates\index.html"

REM Porta em que a API Flask estará rodando
set PORT=5000

REM Inicia a API Flask em segundo plano
echo Iniciando a API...
start "" python app.py

REM Aguarda até que a porta da API esteja aberta
echo Aguardando a API estar online na porta %PORT%...

:wait_api
netstat -an | find ":%PORT% " | find "LISTENING" >nul
if %errorlevel%==0 (
    echo API online! Abrindo o arquivo HTML...
    start "" "%HTML_PATH%"
) else (
    timeout /t 3 >nul
    goto wait_api
)

echo Script finalizado.
pause
