from distutils.core import setup
import py2exe
import sys
import os

currentDirectory = os.getcwd()

os.environ['PATH'] = '%s;%s' % (currentDirectory,os.environ['PATH'])

data_files = []
data_files.append(('',['msvcp71.dll']))
data_files.append(("",["lmcrypt.exe"]))

PROGRAM_NAME = "Scharf Inventory Interface"
PROGRAM_VERSION = "1.0"

SOURCE_FILE = "MainFrame.py"
DIST_DIR = "dist"
EXE_NAME = "ScharfInventoryInterface"
MANIFEST_NAME = "Scharf Inventory Interface"
ZIP_NAME = "scharf.dll"


# If run without args, build executables, in quiet mode.
if len(sys.argv) == 1:
    sys.argv.append("py2exe")
    sys.argv.append("-q")

class Target:
    def __init__(self, **kw):
        self.__dict__.update(kw)
        # for the versioninfo resources
        self.version = PROGRAM_VERSION
        self.company_name = "Beaker and Sons, Inc"
        self.copyright = "(c) Beaker and Sons, Inc, 2014"
        self.name = PROGRAM_NAME

#

manifest_template = '''
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
<assemblyIdentity
    version="5.0.0.0"
    processorArchitecture="x86"
    name="%(prog)s"
    type="win32"
/>
<description>%(prog)s</description>
<dependency>
    <dependentAssembly>
        <assemblyIdentity
            type="win32"
            name="Microsoft.Windows.Common-Controls"
            version="6.0.0.0"
            processorArchitecture="X86"
            publicKeyToken="6595b64144ccf1df"
            language="*"
        />
    </dependentAssembly>
</dependency>
</assembly>
'''

RT_MANIFEST = 24

exe_base = EXE_NAME

excludes = ["pywin", "pywin.debugger", "pywin.debugger.dbgcon",
            "pywin.dialogs", "pywin.dialogs.list", "tcltk",
            "_gtkagg",
            "_tkagg",
            "_cairo",
            "_cocoaagg",
            "_fltkagg",
            "_gtk",
            "_gtkcairo",
            "tcl",
            "Tkconstants",
            "Tkinter",
            "tcl",
            "curses",
            "email",
            "distutil",
            "setuptools"]

dll_excludes = ['libgdk_pixbuf-2.0-0.dll',
                'libgobject-2.0-0.dll',
                'ligdk-win32.2.0-0.dll',
                'tcl84.dll',
                'tk84.dll',
                'wxmsw26uh_v6.dll']

includes = ['MySQLdb',
            ]


windows = Target(
    # used for the versioninfo resource
    description = PROGRAM_NAME,

    # what to build
    script = SOURCE_FILE,
    icon_resources = [(1,'horn.ico')],
    other_resources = [(RT_MANIFEST, 1, manifest_template % dict(prog=MANIFEST_NAME))],
    dest_base = exe_base)

setup(options = {"py2exe": {
                          "compressed": 1,
                          "excludes": excludes,
                          "dll_excludes": dll_excludes,
                          "includes": includes,
                          "dist_dir": DIST_DIR,
                          "optimize": 0}},
    zipfile = ZIP_NAME,
    windows = [windows],
    data_files=data_files
    )


