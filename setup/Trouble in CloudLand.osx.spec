# -*- mode: python -*-
a = Analysis([os.path.join(HOMEPATH,'support/_mountzlib.py'), os.path.join(HOMEPATH,'support/useUnicode.py'), '../main.py'],
             pathex=['/Users/joshua/Github/TroubleInCloudLand/setup',
                     '/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/pygame'])
pyz = PYZ(a.pure)
exe = EXE( pyz,
          Tree('../data', prefix='data'),
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Trouble in CloudLand',
          debug=False,
          strip=False,
          upx=False,
          console=False,
          icon='resources/TroubleInCloudLand_Icon_Perspective.icns')
app = BUNDLE(exe,
             name='Trouble in CloudLand.app',
             icon='./resources/TroubleInCloudLand_Icon_Perspective.icns')
