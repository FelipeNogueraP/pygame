import sys
from cx_Freeze import setup, Executable

# Incluye los archivos de assets en el paquete
build_exe_options = {
    "packages": ["pygame", "random", "os", "platform"],
    "include_files": ["assets/"],
}

# Base es "Win32GUI" si el sistema es Windows
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Explota los globos",
    version="1.0",
    description="Juego de explotar globos",
    options={"build_exe": build_exe_options},
    executables=[Executable("Juego con fondo.py", base=base)]
)
