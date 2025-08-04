import os
import shutil
from datetime import datetime

#----- Configs
BACKUP_SOURCE = [
    r'C:\Path\To\Your\Projects',          # Add project folders 
    r'C:\Path\To\Your\Documents',         # Add document folders 
    r'C:\Path\To\Your\Important\Files',   # Add other important folders as many as needed
    
]

BACKUP_DESTINATION = r'D:\Backups'  # Change to your backup drive/folder

# Folders/files to exclude from backup
EXCLUDE_PATTERNS = [
    'node_modules', 
    '.git', 
    '__pycache__', 
    '.DS_Store', 
    'Thumbs.db', 
    '.vscode', 
    '.idea', 
    'venv', 
    'env', 
    'build', 
    'dist',
    '.tmp',
    'temp',
    'cache'
]

def main():
    """
    Automates backup of specified folders to an external drive or backup location.
    Creates timestamped backup folders and excludes common development artifacts.
    """
    
    print("Starting automated backup process...")
    print(f"Backup destination: {BACKUP_DESTINATION}")
    
    valid_sources = validate_source_folders()
    if not valid_sources:
        print("No valid source folders found. Please update BACKUP_SOURCE paths.")
        return
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_folder = os.path.join(BACKUP_DESTINATION, f"backup_{timestamp}")
    
    try:
        os.makedirs(backup_folder, exist_ok=True)
        print(f"Created backup folder: {backup_folder}")
    except Exception as e:
        print(f"Error creating backup folder: {e}")
        return
    
    # Backup each src folder
    total_files = 0
    total_size = 0
    
    for source_folder in valid_sources:
        folder_name = os.path.basename(source_folder.strip('\\/'))
        destination_folder = os.path.join(backup_folder, folder_name)
        
        print(f"\nBacking up: {source_folder}")
        print(f"To: {destination_folder}")
        
        files_copied, size_copied = backup_folder_recursive(source_folder, destination_folder)
        total_files += files_copied
        total_size += size_copied
        
        print(f"Completed: {files_copied} files, {format_size(size_copied)}")
    
    print("\n" + "="*50)
    print("BACKUP COMPLETED SUCCESSFULLY!")
    print(f"Total files backed up: {total_files}")
    print(f"Total size: {format_size(total_size)}")
    print(f"Backup location: {backup_folder}")
    print("="*50)


def validate_source_folders():

    valid_sources = []
    
    for folder in BACKUP_SOURCE:
        if os.path.exists(folder) and os.path.isdir(folder):
            valid_sources.append(folder)
            print(f"✓ Source folder found: {folder}")
        else:
            print(f"✗ Source folder not found: {folder}")
    
    return valid_sources


def should_exclude_path(path):
    path_lower = path.lower()
    return any(pattern.lower() in path_lower for pattern in EXCLUDE_PATTERNS)


def backup_folder_recursive(source_dir, destination_dir):
    files_copied = 0
    total_size = 0
    
    try:
        for root, dirs, files in os.walk(source_dir):
            if should_exclude_path(root):
                continue
            
            rel_path = os.path.relpath(root, source_dir)
            if rel_path == '.':
                target_dir = destination_dir
            else:
                target_dir = os.path.join(destination_dir, rel_path)
            
            os.makedirs(target_dir, exist_ok=True)
            
            for file in files:
                source_file = os.path.join(root, file)
                
                if should_exclude_path(source_file):
                    continue
                
                target_file = os.path.join(target_dir, file)
                
                try:
                    shutil.copy2(source_file, target_file)
                    file_size = os.path.getsize(source_file)
                    total_size += file_size
                    files_copied += 1
                    
                    # Progress indicator 
                    if files_copied % 100 == 0:
                        print(f"  Copied {files_copied} files...")
                        
                except Exception as e:
                    print(f"  Warning: Could not copy {source_file}: {e}")
                    
    except Exception as e:
        print(f"Error backing up {source_dir}: {e}")
    
    return files_copied, total_size


def format_size(size_bytes):
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.2f} {size_names[i]}"


if __name__ == "__main__":
    main()
