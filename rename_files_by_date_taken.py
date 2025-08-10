import time
from pathlib import Path
import exifread
from datetime import datetime
import pytz
# pip install pywin32
from win32com.propsys import propsys, pscon

def get_date_taken(filename: Path):
    ext = filename.suffix.lower()

    if ext in ('.jpg', '.jpeg', '.heic'):
        with open(filename, 'rb') as image:
            exif = exifread.process_file(image, stop_tag="EXIF DateTimeOriginal", details=False)
            if "EXIF DateTimeOriginal" in exif:
                dt_str = str(exif["EXIF DateTimeOriginal"])
                try:
                    dt_obj = datetime.strptime(dt_str, "%Y:%m:%d %H:%M:%S")
                    return dt_obj
                except ValueError:
                    pass
    # For videos - read Windows "Date Encoded" property
    elif ext in ('.mp4', '.mov', '.avi', '.mkv', '.wmv'):
        properties = propsys.SHGetPropertyStoreFromParsingName(str(filename))
        dt = properties.GetValue(pscon.PKEY_Media_DateEncoded).GetValue()
        if dt:
            if not isinstance(dt, datetime):
                # Convert to datetime if it's a FILETIME-like object
                dt = datetime.fromtimestamp(int(dt))
            # Assign timezone info (UTC from Windows metadata)
            dt = dt.replace(tzinfo=pytz.UTC)
            return dt

    return None


def rename_files_by_modified_date(directory):
    path = Path(directory)
    if not path.is_dir():
        print(f"Error: {directory} is not a valid directory.")
        return

    for file in path.iterdir():
        if file.is_file():
            date_taken = get_date_taken(file)
            if date_taken:
                timestamp = date_taken.strftime('%Y%m%d_%H%M%S')
            else:
                # Fallback if no EXIF date is found
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
    rename_files_by_modified_date("C:\\Users\\user-name\\Pictures\\2025-01-01_Holiday\\")
