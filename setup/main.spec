# -*- mode: python -*-
a = Analysis([os.path.join(HOMEPATH,'support/_mountzlib.py'), os.path.join(HOMEPATH,'support/useUnicode.py'), '../main.py'],
             pathex=['/home/devvm/Github/TroubleInCloudLand/setup'])
pyz = PYZ(a.pure)
exe = EXE( pyz,
          Tree('../data', prefix='data'),
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('dist', 'main'),
          debug=False,
          strip=False,
          upx=True,
          console=1 )
