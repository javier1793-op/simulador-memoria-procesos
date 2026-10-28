@echo off
REM RESPONSABLE: Miembro 7
REM Genera el instalador para el profe en 2 pasos:
REM   1) PyInstaller empaqueta Python + el simulador en un solo simulador.exe (no necesita Python instalado)
REM   2) Inno Setup arma SimuladorSetup.exe (instalador con acceso directo en el menu Inicio)
REM Requisitos SOLO en la PC que construye:  pip install pyinstaller   +   Inno Setup 6 (jrsoftware.org)

cd /d "%~dp0.."

echo === 1/2 PyInstaller ===
python -m PyInstaller --onefile --console --name simulador --clean main.py || goto :error

echo === 2/2 Inno Setup ===
"%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" instalador\simulador.iss || goto :error

echo.
echo Listo: instalador\salida\SimuladorSetup.exe
goto :eof

:error
echo Fallo la construccion.
exit /b 1
