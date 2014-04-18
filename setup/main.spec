# -*- mode: python -*-
a = Analysis(['../main.py'],
             pathex=['/Users/joshua/Github/TroubleInCloudLand/setup'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='main',
          debug=False,
          strip=None,
          upx=True,
          console=False )
app = BUNDLE(exe,
             name='main.app',
             icon=None)
