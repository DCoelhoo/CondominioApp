[Setup]
AppName=CondominioApp
AppVersion=1.0.0
DefaultDirName={autopf}\CondominioApp
DefaultGroupName=CondominioApp
OutputDir=installer
OutputBaseFilename=CondominioApp_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Files]
Source: "dist\CondominioApp\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\CondominioApp"; Filename: "{app}\CondominioApp.exe"
Name: "{commondesktop}\CondominioApp"; Filename: "{app}\CondominioApp.exe"

[Run]
Filename: "{app}\CondominioApp.exe"; Description: "Abrir CondominioApp"; Flags: nowait postinstall skipifsilent