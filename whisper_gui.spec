# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_submodules, collect_data_files
import os
import glob

datas = []
datas += collect_data_files('faster_whisper')
datas += collect_data_files('kss')
datas += collect_data_files('kss.pynori')
datas += collect_data_files('jamo')

hiddenimports = []
hiddenimports += collect_submodules('requests')
hiddenimports += collect_submodules('faster_whisper')
hiddenimports += collect_submodules('kss')
hiddenimports += ["numpy", "sentencepiece"]

binaries = []


ffmpeg_path = r"{FFMPEG_PATH}"

if os.path.exists(ffmpeg_path):
    binaries.append((ffmpeg_path, "ffmpeg"))

a = Analysis(
    ['whisper_gui.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
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
    name='whisper_gui',
    console=False,
)
