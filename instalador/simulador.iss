; RESPONSABLE: Miembro 7
; Script de Inno Setup: arma SimuladorSetup.exe a partir de dist\simulador.exe (generado por PyInstaller).
; Se compila con instalador\construir.bat

#define Nombre "Simulador de Memoria y Procesos"
#define Version "1.0"

[Setup]
AppName={#Nombre}
AppVersion={#Version}
AppPublisher=Grupo SO - UTN FRRe
DefaultDirName={autopf}\SimuladorSO
DefaultGroupName={#Nombre}
OutputDir=salida
OutputBaseFilename=SimuladorSetup
Compression=lzma
SolidCompression=yes
; Instala sin pedir permisos de administrador (en la carpeta del usuario)
PrivilegesRequired=lowest

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Files]
Source: "..\dist\simulador.exe"; DestDir: "{app}"
Source: "..\datos\*.csv"; DestDir: "{app}\datos"
Source: "..\HOWTO.md"; DestDir: "{app}"; Flags: isreadme

[Icons]
; Acceso directo que abre el simulador con el archivo de ejemplo
Name: "{group}\Simulador (ejemplo)"; Filename: "{app}\simulador.exe"; Parameters: """{app}\datos\procesos-ejemplo.csv"""; WorkingDir: "{app}"
; Acceso directo con carga manual de procesos
Name: "{group}\Simulador (carga manual)"; Filename: "{app}\simulador.exe"; WorkingDir: "{app}"
Name: "{group}\Desinstalar"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Simulador SO"; Filename: "{app}\simulador.exe"; WorkingDir: "{app}"

[Run]
Filename: "{app}\simulador.exe"; Parameters: """{app}\datos\procesos-ejemplo.csv"""; Description: "Ejecutar el simulador con el ejemplo"; Flags: postinstall nowait skipifsilent
