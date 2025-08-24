# coursera-downloader-gui-install.sh

#!/bin/bash

pip install git+https://github.com/mathyc0de/coursera-helper-py3.13;
echo "Starting the download of Coursera Downloader Gui...";
USERPROFILE="$HOME/Coursera Downloader Gui";
DESKTOP="$HOME/Desktop";
ZIP_URL="https://github.com/mathyc0de/coursera-downloader-gui/archive/refs/heads/main.zip";
ZIP_FILE="/tmp/coursera-downloader-gui.zip";
EXTRACT_PATH="/tmp/coursera-downloader-gui";
wget -O "$ZIP_FILE" "$ZIP_URL";
echo "Extracting to Program Files...";
unzip -q "$ZIP_FILE" -d "$EXTRACT_PATH";
SOURCE_FOLDER="$EXTRACT_PATH/coursera-downloader-gui-main/build";
echo "Creating link on desktop...";
mkdir -p "$USERPROFILE";
cp -r "$SOURCE_FOLDER/"* "$USERPROFILE/";
SHORTCUT="$DESKTOP/Coursera Downloader.desktop";
cat > "$SHORTCUT" <<EOL
[Desktop Entry]
Type=Application
Name=Coursera Downloader
Exec=xdg-open "$USERPROFILE"
Icon=folder
Terminal=false
EOL;
chmod +x "$SHORTCUT";
rm -f "$ZIP_FILE";
rm -rf "$EXTRACT_PATH";
echo "Coursera Downloader;