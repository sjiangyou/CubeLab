#!/bin/bash

if [ ! -d "venv" ]; then
    python3 -m venv . 
    pip3 install -r requirements.txt
fi
source bin/activate

if pwd | grep -q "compile"; then
    cd ..
fi

cd src
python3 -m PyInstaller --onefile --noconfirm --name=cs_timer_ripoff_MacOS_Intel --clean --distpath=../ cs_timer_ripoff.py
for f in *.spec; do
    rm $f
done
rm -rf build/
rm -rf dist/
cd ..