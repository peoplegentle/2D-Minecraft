# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Users\\Jeong\\Downloads\\2D Minecraft\\2D Minecraft\\2D Minecraft.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\Jeong\\Downloads\\2D Minecraft\\2D Minecraft\\images', 'images'), ('C:\\Users\\Jeong\\Downloads\\2D Minecraft\\2D Minecraft\\sounds', 'sounds'), ('C:\\Users\\Jeong\\Downloads\\2D Minecraft\\2D Minecraft\\music', 'music'), ('C:\\Users\\Jeong\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\site-packages\\pgzero\\data', 'pgzero\\data')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='2D Minecraft',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Users\\Jeong\\Downloads\\2D Minecraft\\2D Minecraft\\images\\icon.ico'],
)
