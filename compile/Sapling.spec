# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['C:\\Users\\pelie\\Documents\\eDx\\Python\\Project Sapling\\project_sapling.py'],
             pathex=['C:\\Users\\pelie\\Documents\\eDx\\Python\\Project Sapling'],
             binaries=[],
             datas=[('C:\\Users\\pelie\\Documents\\eDx\\Python\\Project Sapling\\logo', '.\\logo')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Sapling',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=['ucrtbase.dll', 'VCRUNTIME140.dll'],
          runtime_tmpdir=None,
          console=True )