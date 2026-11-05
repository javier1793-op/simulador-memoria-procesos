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
Source: "..\dist\simulador-consola.exe"; DestDir: "{app}"
Source: "..\datos\*.csv"; DestDir: "{app}\datos"
Source: "..\HOWTO.md"; DestDir: "{app}"; Flags: isreadme

[Icons]
; Version con ventana: abre el ejemplo y tiene botones para abrir otro CSV o cargar a mano
Name: "{group}\Simulador"; Filename: "{app}\simulador.exe"; WorkingDir: "{app}"
; Version de consola (texto), con el ejemplo o con carga manual por teclado
Name: "{group}\Simulador en consola (ejemplo)"; Filename: "{app}\simulador-consola.exe"; Parameters: """{app}\datos\procesos-ejemplo.csv"""; WorkingDir: "{app}"
Name: "{group}\Simulador en consola (carga manual)"; Filename: "{app}\simulador-consola.exe"; WorkingDir: "{app}"
Name: "{group}\Desinstalar"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Simulador SO"; Filename: "{app}\simulador.exe"; WorkingDir: "{app}"

[Run]
Filename: "{app}\simulador.exe"; Description: "Ejecutar el simulador con el ejemplo"; Flags: postinstall nowait skipifsilent
