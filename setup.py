from distutils.core import setup
import py2exe, sys, os

includes  = [
 "encodings",
 "encodings.utf_8",
]
 
options = {
 "bundle_files": 1,                 # create singlefile exe
 "compressed": 1,                 # compress the library archive
 "optimize": 2,                 # do optimize
 "includes": includes,
}
 
setup(
 name = "MSDM Key checker for Windows8.x & 10 (OEM KEY)",
 options = {"py2exe" : options},
 console = [
	{
	'script': "MSDMWinKey.py",
	"icon_resources": [(1, "MSDMWinKey.ico")],
	}
	],
 zipfile = None,
)