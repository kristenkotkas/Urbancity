from cx_Freeze import setup, Executable

exe = Executable(
    script="Main.py",
    base="Win32GUI",
    icon="data/icon.ico",
    targetName="Urbancity.exe",
    compress= True
)
options = {"packages": ["pygame", "dbm"], "excludes": ["tkinter"],
           "include_files": ["data/", "Classes.py", "Methods.py"],
           "optimize": 2,
           "compressed": True,
           "include_msvcr": True
           }
setup(
    name="Urbancity",
    version="1.0.0",
    author="Kristjan Küngas, Kristen Kotkas",
    description="2015 Python Pygame project, https://bitbucket.org/kristjanhk/pygame-projekt",
    options={"build_exe": options},
    executables=[exe]
)
