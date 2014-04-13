# -*- mode: python -*-
a = Analysis(['../main.py'],
             pathex=['/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7',
                     '/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/pygame',
                     '/Users/joshua/Github/TroubleInCloudLand/setup',],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          Tree('../data', prefix='data'),
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Trouble in CloudLand',
          debug=False,
          strip=None,
          upx=True,
          console=False,
          icon='resources/TroubleInCloudLand_Icon_Perspective.icns')
app = BUNDLE(exe,
             name='Trouble in CloudLand.app',
             icon='./resources/TroubleInCloudLand_Icon_Perspective.icns')
