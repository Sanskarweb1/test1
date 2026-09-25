# 🧰 Test1 Toolbox

A multi-tool desktop app built with **Python + PySide6**. One window, eight tools, zero bullshit.

## ✨ Tools

| Tool | What it does |
|------|--------------|
| 🎨 QR Code | Generate QR codes from text/URLs, save as PNG |
| 🔐 Password | Cryptographically secure passwords with custom options |
| #️⃣ Hash | MD5, SHA1, SHA256, SHA512 hashes |
| 📝 Base64 | Encode / decode Base64 |
| 🆔 UUID | Generate v4 UUIDs |
| 🌈 Color Picker | Pick colors, get HEX/RGB/HSL |
| 📖 Text Tools | Case conversion, reverse, sort, dedupe lines |
| 🎲 Random String | Generate random strings for keys/tokens |

## 📦 Download

Grab the binary for your OS from the [Releases](../../releases) page:

- 🐧 `test1-linux`
- 🪟 `test1-windows.exe`
- 🍎 `test1-macos`

No Python install needed. Just download and run.

## 🔨 Build from source

```sh
pip install -r requirements.txt
python main.py
```

📦 Bundle with PyInstaller

```sh
pip install pyinstaller
pyinstaller --onefile --windowed --collect-all PySide6 main.py
```