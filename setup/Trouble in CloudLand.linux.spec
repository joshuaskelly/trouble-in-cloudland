# -*- mode: python -*-
a = Analysis(['../main.py'],
             pathex=['/usr/lib/python2.7/dist-packages/pygame/base.so',
             		     '/home/devvm/Github/TroubleInCloudLand/setup'],
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
          upx=False,
          console=False,
          icon='resources/TroubleInCloudLand_Icon_Perspective.icns')
