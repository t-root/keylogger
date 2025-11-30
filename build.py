import subprocess
import sys
import os
import glob
import shutil

required_packages = [
    "pyinstaller",
    "requests",
    "keyboard"
]

def install_package(package):
    try:
        __import__(package)
    except ImportError:
        print(f"[INFO] Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

for pkg in required_packages:
    install_package(pkg)

def make_exe(py_file, output_dir):
    py_file = os.path.abspath(py_file)
    exe_name = os.path.splitext(os.path.basename(py_file))[0] + ".exe"

    os.makedirs(output_dir, exist_ok=True)

    print(f"[INFO] Creating EXE for {py_file} ...")

    subprocess.call([
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--noconsole",
        "--hidden-import=email.mime.multipart",
        "--hidden-import=email.mime.text", 
        "--hidden-import=email.mime.application",
        "--hidden-import=requests",
        "--hidden-import=keyboard",
        "--hidden-import=threading",
        "--distpath", output_dir,
        py_file
    ])

    spec_file = os.path.splitext(py_file)[0] + ".spec"
    temp_build_dir = os.path.join(os.getcwd(), "build")
    if os.path.exists(spec_file):
        os.remove(spec_file)
    if os.path.exists(temp_build_dir):
        shutil.rmtree(temp_build_dir)

    print(f"[DONE] EXE created: {os.path.join(output_dir, exe_name)}")

if __name__ == "__main__":
    py_files = glob.glob("*.py")
    current_script = os.path.basename(__file__)
    output_dir = os.path.join(os.getcwd(), "build-exe")

    for py_file in py_files:
        if py_file != current_script:
            make_exe(py_file, output_dir)