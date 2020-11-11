import sys
from cx_Freeze import setup, Executable

if __name__ == "__main__":
    options = {
        "build_exe": {
            "packages": [
                "src",
            ],
            "path": sys.path + [".."],
            "include_files": []
        }
    }

    base = None

    print(sys.platform)

    if sys.platform == "win32":
        base = "Console"

    setup(name="CLike to Delphi Transpiler",
          version="0.1",
          description="Transpiles CLike code to Delphi code for xEdit scripts.",
          options=options,
          executables=[Executable("CLikeToDelphi.py", base=base)])
