# -*- mode: python -*-
a = Analysis(['..\\main.py'],
             pathex=['.'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
             
for d in a.datas:
    if 'pyconfig' in d[0]: 
        a.datas.remove(d)
        break

pyz = PYZ(a.pure)
exe = EXE(pyz,
          Tree('..\\data', prefix='data'),
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Trouble in CloudLand.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False,
          icon='resources\\TroubleInCloudLand_Icon_Perspective.ico')
