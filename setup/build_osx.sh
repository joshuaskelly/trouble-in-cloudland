rm -rf dist

# Build the app
python2.7-32 /Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/pyinstaller-1.5/pyinstaller.py ./Trouble\ in\ CloudLand.osx.spec

# Put the icon in the bundle
cp ./resources/TroubleInCloudLand_Icon_Perspective.icns ./Trouble\ in\ CloudLand.app/Contents/Resources/App.icns

# Cleanup
mkdir dist
mv Trouble\ in\ CloudLand ./dist
mv Trouble\ in\ CloudLand.app/ ./dist

rm -rf *.log
rm -rf warnTrouble\ in\ CloudLand.osx.txt
rm -rf build

