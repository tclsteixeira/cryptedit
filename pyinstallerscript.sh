#!/bin/bash
pyinstaller cryptedit.py --add-data="config.ini:." --add-data="main_window.glade:." --add-data="MANIFEST.in:." 
--add-data="README.md:." --add-data="LICENSE:." --add-binary="crypteditlogo.svg:." --add-binary="crypteditlogo.png:."

echo ""
echo "You must copy extra folders that your app may needs to dist output folder, for ex: idioms translate files and their folder tree structure"
