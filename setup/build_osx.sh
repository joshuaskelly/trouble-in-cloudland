rm -rf dist

/Library/Frameworks/Python.framework/Versions/2.7/bin/pyinstaller ../main.py \
	--onefile \
	--noconsole \
	--name="Trouble in CloudLand" \
	--icon=./resources/TroubleInCloudLand_Icon_Perspective.icns

rm -rf build
cp -R ../data/ ./dist/data
