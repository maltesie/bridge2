@echo off

if exist python3env\ (
  echo using existing python3env...
) else (
  python3 -m venv python3env
  call python3env\Scripts\activate
  pip install --no-cache-dir --upgrade pip
  pip install --no-cache-dir -r requirements.txt
)

python3env\Scripts\python.exe bridge.py
