rmdir dist /Q /S

C:\Libraries\Python27\Scripts\pyinstaller ..\main.py ^
	--onefile ^
	--noconsole ^
	--name="Trouble in CloudLand" ^
	--icon=.\resources\TroubleInCloudLand_Icon_Perspective.ico

rmdir build /Q /S
xcopy /EIQ ..\data .\dist\data
