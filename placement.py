import os
import sys
import json
import shutil


def scan_for_venvs(start_directory,maxx=4):
    i = 0
    print(f"Scanning {start_directory} for virtual environments...")
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
        raise RuntimeError(
            f"Refusing to copy: destination {dst_real} is inside source {src_real}"
        )

    os.makedirs(destination_folder, exist_ok=True)

    def ignore_patterns(dir, names):
        return [n for n in names if n in {"__pycache__", ".git", ".venv", "venv"}]

    shutil.copytree(
        source_dir,
        destination_folder,
        dirs_exist_ok=True,
        ignore=ignore_patterns,
    )
    print(f"Copied tree from {source_dir} -> {destination_folder}")
    return destination_folder


def main():
    venvs = scan_for_venvs(os.path.expanduser("~"))

    with open("venvs.json", "w", encoding="utf-8") as f:
        json.dump(venvs, f, indent=2)

    if not venvs:
        print("No virtual environments found. Nothing to do.")
        return

    first_venv = venvs[0]
    print(f"\nUsing first venv: {first_venv}")

    destination_parent = os.path.dirname(first_venv)
    print(f"Destination parent (venv's parent): {destination_parent}")

    try:
        final_path = copy_tree_into_subfolder(
            destination_parent,
            subfolder_name="project_beta",  
        )
        print(f"Success. Project copied to: {final_path}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()