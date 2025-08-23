pip install git+https://github.com/mathyc0de/coursera-helper-py3.13
Write-Host "Starting the download of Coursera Downloader Gui..."
# Variáveis
$programFiles = "${env:ProgramFiles}\coursera-downloader-gui"
$desktop = [Environment]::GetFolderPath("Desktop")

# Baixar a pasta usando GitHub API (zip da pasta)
$zipUrl = "https://github.com/mathyc0de/coursera-downloader-gui/archive/refs/heads/main.zip"
$zipFile = "$env:TEMP\coursera-downloader-gui.zip"
Invoke-WebRequest -Uri $zipUrl -OutFile $zipFile

Write-Host "Extracting to Program Files..."
Add-Type -AssemblyName System.IO.Compression.FileSystem
$extractPath = "$env:TEMP\coursera-downloader-gui"
[System.IO.Compression.ZipFile]::ExtractToDirectory($zipFile, $extractPath)

# Caminho da pasta extraída
$sourceFolder = Join-Path $extractPath "coursera-downloader-gui-main\build\"

Write-Host "Creating link do destkop..."
if (!(Test-Path $programFiles)) {
    New-Item -ItemType Directory -Path $programFiles | Out-Null
}
Copy-Item -Path $sourceFolder\* -Destination $programFiles -Recurse -Force

$WshShell = New-Object -ComObject WScript.Shell
$shortcut = $WshShell.CreateShortcut("$desktop\Coursera Downloader.lnk")
$shortcut.TargetPath = $programFiles
$shortcut.WorkingDirectory = $programFiles
$shortcut.Save()

# Limpar arquivos temporários
Remove-Item $zipFile -Force
Remove-Item $extractPath -Recurse -Force

Write-Host "Coursera Downloader GUI installed"