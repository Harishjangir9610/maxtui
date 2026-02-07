import subprocess
import os
import sys

def run_maturin_build():
    cmd = [
        sys.executable,
        "-m",
        "maturin",
        "build",
        "--release",
    ]

    env = os.environ.copy()
    env["CARGO_TARGET_DIR"] = "target"
    env["PYO3_USE_ABI3_FORWARD_COMPATIBILITY"] = "1"

    try:
        subprocess.run(cmd, check=True, env=env)
        print("✅ Build completed successfully!")
    except subprocess.CalledProcessError as e:
        print("❌ Build failed!")
        exit(e.returncode)

if __name__ == "__main__":
    run_maturin_build()
    