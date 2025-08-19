#!/bin/bash

if pwd | grep -q "compile"; then
    cd ..
fi
python3.11 -m venv .
source bin/activate
pip3.11 install -r requirements.txt
cd src
python3.11 -m PyInstaller --onefile --noconfirm --name=CubeLab_MacOS_ARM --clean --distpath=../ CubeLab.py --optimize=2
if [ $? -ne 0 ]; then
    python3.11 -m pyinstaller --onefile --noconfirm --name=CubeLab_MacOS_ARM --clean --distpath=../ CubeLab.py --optimize=2
fi
for f in *.spec; do
    rm $f
done
rm -rf build/
rm -rf dist/
