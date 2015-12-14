from cx_Freeze import setup, Executable

target = Executable(
    script="Main.py",
    icon="data/icon.ico"
)

options = {"packages": ["pygame", "dbm"], "excludes": ["tkinter"],
           "include_files": ["data/", "Classes.py", "Methods.py"]}

setup(
    name="Urbancity",
    options={"build_exe": options},
    executables=[target]
)
