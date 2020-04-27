from cx_Freeze import setup, Executable
setup(
    name = "TurboClock",
    version = "0.1",
    description = "First release",
    executables = [Executable("main.py")],
)