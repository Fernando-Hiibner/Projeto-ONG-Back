echo Iniciando Setup
echo Tentando por PIP
pip install -r ".\requirements.txt"
if %ERRORLEVEL% neq 0 goto PIP3

echo Finalizado usando o PIP
pause
exit /b 0

:PIP3
echo Tentando por PIP3
pip3 install -r ".\requirements.txt"
if %ERRORLEVEL% neq 0 goto ERRO

echo Finalizado usando o PIP3
pause
exit /b 0

:ERRO
echo Incapaz de terminar operação
pause
exit /b 1