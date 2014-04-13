rm -rf dist

arch -i386 /Library/Frameworks/Python.framework/Versions/2.7/bin/pyinstaller "Trouble in CloudLand.osx.spec"

rm -rf build
