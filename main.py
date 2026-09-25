"""
Test1 Toolbox — A multi-tool desktop app built with PySide6.
"""
import sys
import os
import hashlib
import base64
import uuid
import secrets
import string
import random
from io import BytesIO
from datetime import datetime

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QTextEdit, QSpinBox, QSlider,
    QCheckBox, QComboBox, QListWidget, QListWidgetItem, QFileDialog,
    QMessageBox, QFrame, QSizePolicy, QColorDialog
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap, QImage, QColor, QFont, QIcon

try:
    import qrcode
except ImportError:
    qrcode = None


# ============================================================
# Shared styling
# ============================================================

STYLE = """
QMainWindow, QWidget { background: #1e1e2e; color: #e0e0e0; font-family: 'Segoe UI', sans-serif; font-size: 14px; }
QListWidget { background: #2a2a3e; border: none; padding: 8px; font-size: 15px; outline: none; }
QListWidget::item { padding: 12px; border-radius: 6px; margin: 2px 0; }
QListWidget::item:selected { background: #7c3aed; color: white; }
QListWidget::item:hover:!selected { background: #35355a; }
QPushButton { background: #7c3aed; color: white; border: none; padding: 10px 20px; border-radius: 6px; font-weight: 600; }
QPushButton:hover { background: #8b5cf6; }
QPushButton:pressed { background: #6d28d9; }
QPushButton:disabled { background: #444; color: #888; }
QLineEdit, QTextEdit, QSpinBox, QComboBox {
    background: #2a2a3e; color: #e0e0e0; border: 1px solid #3a3a4e;
    border-radius: 6px; padding: 8px; font-size: 14px;
}
QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QComboBox:focus { border: 1px solid #7c3aed; }
QLabel { background: transparent; }
QLabel#title { font-size: 22px; font-weight: 700; color: #ffffff; padding: 10px 0; }
QLabel#subtitle { color: #a0a0b0; font-size: 13px; padding-bottom: 10px; }
QCheckBox { color: #e0e0e0; }
QSlider::groove:horizontal { height: 6px; background: #2a2a3e; border-radius: 3px; }
QSlider::handle:horizontal { background: #7c3aed; width: 16px; margin: -6px 0; border-radius: 8px; }
QSlider::sub-page:horizontal { background: #7c3aed; border-radius: 3px; }
"""


# ============================================================
# QR Code Generator
# ============================================================

class QRTool(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        title = QLabel("🎨 QR Code Generator")
        title.setObjectName("title")
        layout.addWidget(title)

        layout.addWidget(QLabel("Enter text or URL:"))
        self.input = QTextEdit()
        self.input.setPlaceholderText("https://github.com/Sanweb1/test1")
        self.input.setMaximumHeight(80)
        layout.addWidget(self.input)

        btn_row = QHBoxLayout()
        gen_btn = QPushButton("Generate")
        gen_btn.clicked.connect(self.generate)
        save_btn = QPushButton("Save PNG")
        save_btn.clicked.connect(self.save)
        btn_row.addWidget(gen_btn)
        btn_row.addWidget(save_btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        self.preview = QLabel("QR preview will appear here")
        self.preview.setAlignment(Qt.AlignCenter)
        self.preview.setMinimumHeight(280)
        self.preview.setStyleSheet("background: #2a2a3e; border-radius: 8px; padding: 10px; color: #666;")
        layout.addWidget(self.preview)

        layout.addStretch()
        self.current_pixmap = None

    def generate(self):
        text = self.input.toPlainText().strip()
        if not text:
            return
        if qrcode is None:
            self.preview.setText("qrcode library not installed")
            return
        img = qrcode.make(text)
        buf = BytesIO()
        img.save(buf, format="PNG")
        qimg = QImage.fromData(buf.getvalue())
        self.current_pixmap = QPixmap.fromImage(qimg).scaled(
            260, 260, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.preview.setPixmap(self.current_pixmap)

    def save(self):
        if self.current_pixmap is None:
            QMessageBox.warning(self, "Nothing to save", "Generate a QR code first.")
            return
        path, _ = QFileDialog.getSaveFileName(self, "Save QR", "qrcode.png", "PNG (*.png)")
        if path:
            self.current_pixmap.save(path)


# ============================================================
# Password Generator
# ============================================================

class PasswordTool(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        title = QLabel("🔐 Password Generator")
        title.setObjectName("title")
        layout.addWidget(title)

        len_row = QHBoxLayout()
        len_row.addWidget(QLabel("Length:"))
        self.length_lbl = QLabel("16")
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(4, 64)
        self.slider.setValue(16)
        self.slider.valueChanged.connect(lambda v: self.length_lbl.setText(str(v)))
        len_row.addWidget(self.slider)
        len_row.addWidget(self.length_lbl)
        layout.addLayout(len_row)

        opts = QHBoxLayout()
        self.use_upper = QCheckBox("Uppercase")
        self.use_upper.setChecked(True)
        self.use_lower = QCheckBox("Lowercase")
        self.use_lower.setChecked(True)
        self.use_digits = QCheckBox("Digits")
        self.use_digits.setChecked(True)
        self.use_symbols = QCheckBox("Symbols")
        self.use_symbols.setChecked(True)
        for w in (self.use_upper, self.use_lower, self.use_digits, self.use_symbols):
            opts.addWidget(w)
        layout.addLayout(opts)

        self.output = QLineEdit()
        self.output.setReadOnly(True)
        self.output.setStyleSheet("font-family: 'Consolas', monospace; font-size: 16px; padding: 15px;")
        layout.addWidget(self.output)

        btn_row = QHBoxLayout()
        gen = QPushButton("Generate Password")
        gen.clicked.connect(self.generate)
        copy = QPushButton("Copy")
        copy.clicked.connect(self.copy)
        btn_row.addWidget(gen)
        btn_row.addWidget(copy)
        btn_row.addStretch()
        layout.addLayout(btn_row)

        layout.addStretch()
        self.generate()

    def generate(self):
        pool = ""
        if self.use_upper.isChecked(): pool += string.ascii_uppercase
        if self.use_lower.isChecked(): pool += string.ascii_lowercase
        if self.use_digits.isChecked(): pool += string.digits
        if self.use_symbols.isChecked(): pool += "!@#$%^&*()-_=+[]{};:,.<>?"
        if not pool:
            self.output.setText("Select at least one character type")
            return
        length = self.slider.value()
        self.output.setText("".join(secrets.choice(pool) for _ in range(length)))

    def copy(self):
        QApplication.clipboard().setText(self.output.text())


# ============================================================
# Hash Generator
# ============================================================

class HashTool(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        title = QLabel("#️⃣ Hash Generator")
        title.setObjectName("title")
        layout.addWidget(title)

        layout.addWidget(QLabel("Input text:"))
        self.input = QTextEdit()
        self.input.setMaximumHeight(100)
        layout.addWidget(self.input)

        self.results = {}
        for algo in ("md5", "sha1", "sha256", "sha512"):
            row = QHBoxLayout()
            row.addWidget(QLabel(f"{algo.upper()}:"), 0)
            field = QLineEdit()
            field.setReadOnly(True)
            field.setStyleSheet("font-family: 'Consolas', monospace; font-size: 12px;")
            copy_btn = QPushButton("Copy")
            copy_btn.setMaximumWidth(80)
            copy_btn.clicked.connect(lambda _, f=field: QApplication.clipboard().setText(f.text()))
            row.addWidget(field, 1)
            row.addWidget(copy_btn, 0)
            layout.addLayout(row)
            self.results[algo] = field

        calc = QPushButton("Calculate Hashes")
        calc.clicked.connect(self.calculate)
        layout.addWidget(calc)

        self.input.textChanged.connect(self.calculate)
        layout.addStretch()

    def calculate(self):
        text = self.input.toPlainText().encode("utf-8")
        for algo, field in self.results.items():
            field.setText(hashlib.new(algo, text).hexdigest())


# ============================================================
# Base64 Tool
# ============================================================

class Base64Tool(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        title = QLabel("📝 Base64 Encoder / Decoder")
        title.setObjectName("title")
        layout.addWidget(title)

        layout.addWidget(QLabel("Input:"))
        self.input = QTextEdit()
        self.input.setMaximumHeight(150)
        layout.addWidget(self.input)

        row = QHBoxLayout()
        enc = QPushButton("Encode →")
        enc.clicked.connect(lambda: self.process("encode"))
        dec = QPushButton("← Decode")
        dec.clicked.connect(lambda: self.process("decode"))
        row.addWidget(enc)
        row.addWidget(dec)
        row.addStretch()
        layout.addLayout(row)

        layout.addWidget(QLabel("Output:"))
        self.output = QTextEdit()
        self.output.setMaximumHeight(150)
        layout.addWidget(self.output)

        layout.addStretch()

    def process(self, mode):
        text = self.input.toPlainText()
        try:
            if mode == "encode":
                self.output.setPlainText(base64.b64encode(text.encode()).decode())
            else:
                self.output.setPlainText(base64.b64decode(text.encode()).decode())
        except Exception as e:
            self.output.setPlainText(f"Error: {e}")


# ============================================================
# UUID Generator
# ============================================================

class UUIDTool(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        title = QLabel("🆔 UUID Generator")
        title.setObjectName("title")
        layout.addWidget(title)

        row = QHBoxLayout()
        row.addWidget(QLabel("How many?"))
        self.count = QSpinBox()
        self.count.setRange(1, 100)
        self.count.setValue(5)
        row.addWidget(self.count)
        btn = QPushButton("Generate")
        btn.clicked.connect(self.generate)
        row.addWidget(btn)
        row.addStretch()
        layout.addLayout(row)

        self.output = QTextEdit()
        self.output.setStyleSheet("font-family: 'Consolas', monospace; font-size: 14px;")
        layout.addWidget(self.output)

        self.generate()

    def generate(self):
        n = self.count.value()
        lines = [str(uuid.uuid4()) for _ in range(n)]
        self.output.setPlainText("\n".join(lines))


# ============================================================
# Color Picker
# ============================================================

class ColorTool(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        title = QLabel("🌈 Color Picker")
        title.setObjectName("title")
        layout.addWidget(title)

        pick = QPushButton("Pick a Color")
        pick.clicked.connect(self.pick)
        layout.addWidget(pick)

        self.swatch = QLabel()
        self.swatch.setMinimumHeight(120)
        self.swatch.setStyleSheet("background: #7c3aed; border-radius: 8px;")
        layout.addWidget(self.swatch)

        self.hex_lbl = self._make_row(layout, "HEX")
        self.rgb_lbl = self._make_row(layout, "RGB")
        self.hsl_lbl = self._make_row(layout, "HSL")

        layout.addStretch()

    def _make_row(self, layout, name):
        row = QHBoxLayout()
        row.addWidget(QLabel(f"{name}:"), 0)
        field = QLineEdit()
        field.setReadOnly(True)
        field.setStyleSheet("font-family: 'Consolas', monospace;")
        copy = QPushButton("Copy")
        copy.setMaximumWidth(80)
        copy.clicked.connect(lambda _, f=field: QApplication.clipboard().setText(f.text()))
        row.addWidget(field, 1)
        row.addWidget(copy, 0)
        layout.addLayout(row)
        return field

    def pick(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.swatch.setStyleSheet(f"background: {color.name()}; border-radius: 8px;")
            self.hex_lbl.setText(color.name())
            self.rgb_lbl.setText(f"rgb({color.red()}, {color.green()}, {color.blue()})")
            h, s, l, _ = color.getHsl()
            self.hsl_lbl.setText(f"hsl({h}, {int(s/2.55)}%, {int(l/2.55)}%)")


# ============================================================
# Text Tools
# ============================================================

class TextTool(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        title = QLabel("📖 Text Tools")
        title.setObjectName("title")
        layout.addWidget(title)

        layout.addWidget(QLabel("Input:"))
        self.input = QTextEdit()
        self.input.setMaximumHeight(180)
        self.input.textChanged.connect(self.stats)
        layout.addWidget(self.input)

        self.stats_lbl = QLabel("0 chars • 0 words • 0 lines")
        self.stats_lbl.setStyleSheet("color: #a0a0b0; padding: 5px;")
        layout.addWidget(self.stats_lbl)

        layout.addWidget(QLabel("Actions:"))
        grid = QHBoxLayout()
        actions = [
            ("UPPER", lambda t: t.upper()),
            ("lower", lambda t: t.lower()),
            ("Title Case", lambda t: t.title()),
            ("Reverse", lambda t: t[::-1]),
            ("Trim Spaces", lambda t: "\n".join(line.strip() for line in t.splitlines())),
            ("Remove Duplicates", lambda t: "\n".join(dict.fromkeys(t.splitlines()))),
            ("Sort Lines", lambda t: "\n".join(sorted(t.splitlines()))),
        ]
        for name, fn in actions:
            b = QPushButton(name)
            b.clicked.connect(lambda _, f=fn: self.apply(f))
            grid.addWidget(b)
        layout.addLayout(grid)

        layout.addStretch()

    def apply(self, fn):
        self.input.setPlainText(fn(self.input.toPlainText()))

    def stats(self):
        t = self.input.toPlainText()
        chars = len(t)
        words = len(t.split())
        lines = t.count("\n") + 1 if t else 0
        self.stats_lbl.setText(f"{chars} chars • {words} words • {lines} lines")


# ============================================================
# Random String Generator
# ============================================================

class RandomStringTool(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        title = QLabel("🎲 Random String Generator")
        title.setObjectName("title")
        layout.addWidget(title)

        row = QHBoxLayout()
        row.addWidget(QLabel("Length:"))
        self.length = QSpinBox()
        self.length.setRange(4, 256)
        self.length.setValue(32)
        row.addWidget(self.length)
        row.addWidget(QLabel("Count:"))
        self.count = QSpinBox()
        self.count.setRange(1, 50)
        self.count.setValue(5)
        row.addWidget(self.count)
        layout.addLayout(row)

        opts = QHBoxLayout()
        self.alnum = QCheckBox("Alphanumeric only")
        self.alnum.setChecked(True)
        opts.addWidget(self.alnum)
        opts.addStretch()
        layout.addLayout(opts)

        btn = QPushButton("Generate")
        btn.clicked.connect(self.generate)
        layout.addWidget(btn)

        self.output = QTextEdit()
        self.output.setStyleSheet("font-family: 'Consolas', monospace; font-size: 13px;")
        layout.addWidget(self.output)

        self.generate()

    def generate(self):
        if self.alnum.isChecked():
            pool = string.ascii_letters + string.digits
        else:
            pool = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{};:,.<>?"
        lines = [
            "".join(secrets.choice(pool) for _ in range(self.length.value()))
            for _ in range(self.count.value())
        ]
        self.output.setPlainText("\n".join(lines))


# ============================================================
# Main Window
# ============================================================

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test1 Toolbox")
        self.resize(900, 620)

        central = QWidget()
        self.setCentralWidget(central)

        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Sidebar
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(220)
        tools = [
            ("🎨 QR Code", QRTool),
            ("🔐 Password", PasswordTool),
            ("#️⃣ Hash", HashTool),
            ("📝 Base64", Base64Tool),
            ("🆔 UUID", UUIDTool),
            ("🌈 Color Picker", ColorTool),
            ("📖 Text Tools", TextTool),
            ("🎲 Random String", RandomStringTool),
        ]
        for name, _ in tools:
            self.sidebar.addItem(QListWidgetItem(name))
        self.sidebar.currentRowChanged.connect(self.switch_tool)
        root.addWidget(self.sidebar)

        # Content area
        self.content_area = QWidget()
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setContentsMargins(30, 20, 30, 20)
        root.addWidget(self.content_area, 1)

        self.tools = [cls() for _, cls in tools]
        for t in self.tools:
            t.setVisible(False)
            self.content_layout.addWidget(t)

        self.sidebar.setCurrentRow(0)

    def switch_tool(self, idx):
        for i, t in enumerate(self.tools):
            t.setVisible(i == idx)


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()