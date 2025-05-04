# otp
simple tool to encrypt / decrypt a .txt with a random or given One Time Pad

## Usage
either run it with python or run the .exe

Encrypt: 
```
python3 otp.py encrypt input.txt [optional_pad.txt]
```
```
.\otp.exe encrypt input.txt [optional_pad.txt]
```
Decrypt:
```

## rebuild the .exe
from windows CMD :
```
pip3 install pyinstaller
pyinstaller --onefile otp.py
```
