from cx_Freeze import setup, Executable

exe = Executable(
    script="Main.py",
    base="Win32GUI",
    icon="data/icon.ico",
    targetName="Urbancity.exe",
    compress= True
)
options = {"packages": ["pygame", "dbm"], "excludes": ["tkinter"],
           "include_files": ["data/"],
           "optimize": 2,
           "compressed": True,
           "include_msvcr": True
           }
setup(
    name="Urbancity",
    version="2.0",
    author="Kristjan Küngas, Kristen Kotkas",
    description="2016 Python Pygame project, https://bitbucket.org/urbancity/urbancity",
    options={"build_exe": options},
    executables=[exe]
)
