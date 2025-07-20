import time
from pathlib import Path


def rename_files_by_modified_date(directory):
    path = Path(directory)
    if not path.is_dir():
        print(f"Error: {directory} is not a valid directory.")
        return

    for file in path.iterdir():
        if file.is_file():
            mod_time = file.stat().st_mtime
            timestamp = time.strftime('%Y%m%d_%H%M%S', time.localtime(mod_time))
            new_name = f"{timestamp}{file.suffix}"
            new_path = file.with_name(new_name)

            # Handle naming conflicts
            counter = 1
            while new_path.exists():
                new_name = f"{timestamp}_{counter}{file.suffix}"
                new_path = file.with_name(new_name)
                counter += 1

            print(f"Renaming: {file.name} -> {new_path.name}")
            file.rename(new_path)


if __name__ == "__main__":
    print()
    rename_files_by_modified_date("C:\\Users\\user-name\\Pictures\\2025-01-01_Holiday\\") # dir path example
