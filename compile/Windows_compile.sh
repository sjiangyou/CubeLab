#!/bin/bash

if pwd | grep -q "compile"; then
    cd ..
fi
python -m venv . 
source Scripts/activate
pip install -r requirements.txt
cd src
python -m PyInstaller --onefile --noconfirm --name=CubeLab_Windows --clean --distpath=../ CubeLab.py
if [ $? -ne 0 ]; then
    python -m pyinstaller --onefile --noconfirm --name=CubeLab_Windows--clean --distpath=../ CubeLab.py
fi
for f in *.spec; do
    rm $f
done
rm -rf build/
rm -rf dist/
