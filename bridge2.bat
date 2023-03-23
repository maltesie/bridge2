@echo off

if exist python3env\ (
  echo using existing python3env...
) else (
  python3 -m venv python3env
  call python3env\Scripts\activate
  python3env\Scripts\python.exe -m pip install --no-cache-dir --upgrade pip
  python3env\Scripts\python.exe -m pip install --no-cache-dir -r requirements.txt
)

python3env\Scripts\python.exe bridge2.py
