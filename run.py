import os
import sys
import json
import shutil
import subprocess
import platform


def scan_for_venvs(start_directory,maxx=3):
    print(f"Scanning {start_directory} for virtual environments...")
    i = 0
    found = []
    for root, dirs, files in os.walk(start_directory):
        if i == maxx:
            break
        if 'activate' in files or 'activate.bat' in files or 'Activate.ps1' in files:
            if any(x in root.lower() for x in ['bin', 'scripts']):
                venv_path = os.path.abspath(os.path.join(root, '..'))
                print(f"  Found venv: {venv_path}")
                found.append(venv_path)
                i += 1
                dirs.clear()
    return found


def copy_tree_into_subfolder(destination_parent, subfolder_name="copied_project"):
    source_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    destination_folder = os.path.join(destination_parent, subfolder_name)

    src_real = os.path.realpath(source_dir)
    dst_real = os.path.realpath(destination_folder)
    if src_real == dst_real or dst_real.startswith(src_real + os.sep):
        raise RuntimeError(f"Refusing to copy: destination {dst_real} is inside source {src_real}")

    os.makedirs(destination_folder, exist_ok=True)

    def ignore_patterns(dir, names):
        return [n for n in names if n in {"__pycache__", ".git", ".venv", "venv"}]

    shutil.copytree(source_dir, destination_folder, dirs_exist_ok=True, ignore=ignore_patterns)
    print(f"Copied tree from {source_dir} -> {destination_folder}")
    return destination_folder



def venv_paths(venv_dir):
    if platform.system() == "Windows":
        return {
            "python":  os.path.join(venv_dir, "Scripts", "python.exe"),
            "pip":     os.path.join(venv_dir, "Scripts", "pip.exe"),
            "activate": os.path.join(venv_dir, "Scripts", "Activate.ps1"),
            "kind":    "windows",
        }

    return {
        "python":  os.path.join(venv_dir, "bin", "python"),
        "pip":     os.path.join(venv_dir, "bin", "pip"),
        "activate": os.path.join(venv_dir, "bin", "activate"),
        "kind":    "posix",
    }


def venv_env(venv_dir):
    
    paths = venv_paths(venv_dir)
    env = os.environ.copy()
    venv_bin = os.path.dirname(paths["python"])
    env["VIRTUAL_ENV"] = venv_dir
    env["PATH"] = venv_bin + os.pathsep + env.get("PATH", "")
    env.pop("PYTHONHOME", None)
    return env


def run(cmd, cwd=None, env=None, check=True, capture=False):
    printable = " ".join(cmd) if isinstance(cmd, (list, tuple)) else str(cmd)
    print(f"\n$ {printable}" + (f"   (cwd={cwd})" if cwd else ""))
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            env=env,
            check=check,
            text=True,
            capture_output=capture,
        )
        if capture and result.stdout:
            print(result.stdout.rstrip())
        return result
    except FileNotFoundError as e:
        raise RuntimeError(f"Executable not found: {cmd[0]}") from e
    except subprocess.CalledProcessError as e:
        if capture and e.stdout:
            print(e.stdout.rstrip())
        if capture and e.stderr:
            print(e.stderr.rstrip(), file=sys.stderr)
        raise RuntimeError(f"Command failed (exit {e.returncode}): {printable}") from e


def main():
    venvs = scan_for_venvs(os.path.expanduser("~"))
    with open("venvs.json", "w", encoding="utf-8") as f:
        json.dump(venvs, f, indent=2)

    if not venvs:
        print("No virtual environments found. Nothing to do.")
        return

    first_venv = venvs[0]
    print(f"\nUsing first venv: {first_venv}")
    paths = venv_paths(first_venv)

    for label in ("python", "pip"):
        if not os.path.exists(paths[label]):
            print(f"ERROR: {paths[label]} does not exist — venv looks broken/incomplete.")
            sys.exit(1)

    destination_parent = os.path.dirname(first_venv)
    print(f"Destination parent (venv's parent): {destination_parent}")
    project_dir = copy_tree_into_subfolder(destination_parent, subfolder_name="copied_project")

    placement_script = os.path.join(project_dir, "placement.py")
    receiver_script  = os.path.join(project_dir, "receiver.py")
    requirements     = os.path.join(project_dir, "requirements.txt")

    for label, p in (("placement.py", placement_script),
                     ("receiver.py",  receiver_script),
                     ("requirements.txt", requirements)):
        if not os.path.exists(p):
            print(f"ERROR: expected {label} at {p} — copy looks incomplete.")
            sys.exit(1)

    env = venv_env(first_venv)
    print(f"VIRTUAL_ENV = {env['VIRTUAL_ENV']}")

    try:
        run([paths["python"], placement_script], cwd=project_dir, env=env)

        run([paths["pip"], "install", "-r", requirements], cwd=project_dir, env=env)

        
        run([sys.executable, receiver_script], cwd=project_dir, env=env)

        print("\nAll steps completed successfully.")
    except RuntimeError as e:
        print(f"\nERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()