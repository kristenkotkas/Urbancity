import cx_Freeze

cx_Freeze.setup(
    name = "Urbancity",
    options = {"build_exe":
                   {"packages": ["pygame", "dbm"], "excludes": ["tkinter"],
                    "include_files": ["data/", "Classes.py", "Methods.py"]}},
    executables = [cx_Freeze.Executable("Main.py")]
)
