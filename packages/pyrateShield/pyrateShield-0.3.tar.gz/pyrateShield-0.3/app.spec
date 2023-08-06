# -*- mode: python ; coding: utf-8 -*-

added_files = [
	('pyrateshield/constants.yml', 'pyrateshield'),
	('pyrateshield/gui/styles.yml', 'pyrateshield/gui'),
	('pyrateshield/gui/icon.png', 'pyrateshield/gui'),
	('pyrateshield/radtracer/MCNP.pickle', 'pyrateshield/radtracer'),
	('pyrateshield/pyshield/isotopes.yml', 'pyrateshield/pyshield'),
	('pyrateshield/pyshield/physics/attenuation.xls', 'pyrateshield/pyshield/physics'),
	('pyrateshield/pyshield/physics/buildup.xls', 'pyrateshield/pyshield/physics'),
	('pyrateshield/pyshield/physics/isotopes.yml', 'pyrateshield/pyshield/physics'),
	('pyrateshield/pyshield/physics/materials.yml', 'pyrateshield/pyshield/physics'),
	('pyrateshield/pyshield/physics/physics.yml', 'pyrateshield/pyshield/physics'),
]

block_cipher = None


a = Analysis(['pyrateshield/app.py'],
             pathex=['.'],
             binaries=[],
             datas=added_files,
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='pyrateshield',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None,
		  icon='./icon.ico')

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='pyrateshield')
