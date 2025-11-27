# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_submodules, collect_data_files
import os
import glob

datas = []
datas += collect_data_files('faster_whisper')
datas += collect_data_files('kss')
datas += collect_data_files('kss.pynori')


hiddenimports = []
hiddenimports += collect_submodules('requests')
hiddenimports += collect_submodules('faster_whisper')
hiddenimports += collect_submodules('kss')
hiddenimports += ["numpy", "sentencepiece"]


torch_lib = r"C:\Users\mingy\Desktop\3-2\Capstone1\venv\Lib\site-packages\torch\lib"

binaries = []

if os.path.exists(torch_lib):
    for dll in glob.glob(os.path.join(torch_lib, "*.dll")):
        binaries.append((dll, "torch/lib"))


ffmpeg_path = r"C:\Users\mingy\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0-full_build\bin\ffmpeg.exe"

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
