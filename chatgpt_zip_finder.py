import os
import zipfile
import shutil
from datetime import datetime

#------ Configs
SOURCE_FOLDER = r'C:\Path\To\Your\Source\Folder'  
DEST_FOLDER = r'C:\Path\To\Your\Destination\Folder'  

def main():
    """
    Finds ZIP files containing ChatGPT conversation exports and organizes them by date.
    Looks for ZIP files with 'conversations.json' inside and renames them with standardized naming.
    """
    
    # Create destination folder if there's not already one
    if not os.path.exists(DEST_FOLDER):
        os.makedirs(DEST_FOLDER)
        print(f"Created destination folder: {DEST_FOLDER}")

    processed_count = 0
    skipped_count = 0
    error_count = 0

    print(f"Scanning for ChatGPT exports in: {SOURCE_FOLDER}")
    print(f"Organizing files to: {DEST_FOLDER}")
    print("-" * 50)

    for root, dirs, files in os.walk(SOURCE_FOLDER):
        for file in files:
            if file.lower().endswith('.zip'):
                zip_path = os.path.join(root, file)
                try:
                    with zipfile.ZipFile(zip_path, 'r') as z:
                        if 'conversations.json' in z.namelist():
                            date = extract_date_from_filename(file)
                            
                            #Fallback to file modification time if no date
                            if not date:
                                timestamp = os.path.getmtime(zip_path)
                                date = datetime.fromtimestamp(timestamp)

                            new_name = f"ChatGPT_Export_{date.strftime('%Y-%m-%d')}.zip"
                            dest_path = os.path.join(DEST_FOLDER, new_name)
                            
                            # Handle duplicates
                            dest_path = get_unique_filename(dest_path)

                            shutil.copy(zip_path, dest_path)
                            print(f"[OK] {os.path.basename(zip_path)} --> {os.path.basename(dest_path)}")
                            processed_count += 1
                        else:
                            print(f"[SKIP] {os.path.basename(zip_path)} (no conversations.json found)")
                            skipped_count += 1

                except zipfile.BadZipFile:
                    print(f"[ERROR] {os.path.basename(zip_path)} (bad zip file)")
                    error_count += 1
                except Exception as e:
                    print(f"[ERROR] {os.path.basename(zip_path)} ({str(e)})")
                    error_count += 1

    print("-" * 50)
    print(f"Processing complete!")
    print(f"Processed: {processed_count}")
    print(f"Skipped: {skipped_count}")
    print(f"Errors: {error_count}")


def extract_date_from_filename(filename):
    parts = filename.split('-')
    
    for part in parts:
        if len(part) == 4 and part.isdigit():
            idx = parts.index(part)
            try:
                date_str = '-'.join(parts[idx:idx+3])
                return datetime.strptime(date_str, "%Y-%m-%d")
            except (ValueError, IndexError):
                continue
    
    return None


def get_unique_filename(dest_path):
    if not os.path.exists(dest_path):
        return dest_path
    
    base_path = os.path.splitext(dest_path)[0]
    extension = os.path.splitext(dest_path)[1]
    count = 1
    
    while True:
        new_path = f"{base_path}_{count}{extension}"
        if not os.path.exists(new_path):
            return new_path
        count += 1


if __name__ == "__main__":
    main()
