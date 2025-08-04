import os
import zipfile
import json

#-----Configs
EXPORTS_FOLDER = r'C:\Path\To\Your\ChatGPT\Exports'  #export ZIP files
EXTRACTED_FOLDER = r'C:\Path\To\Your\Extracted\Conversations'  
MASTER_JSON = r'C:\Path\To\Your\master_conversations.json'  # Output file merged convos

def main():
    """
    Merges multiple ChatGPT conversation export files into a single JSON file.
    Extracts conversations.json from ZIP files and combines them while removing duplicates.
    """
    
    # Create extraction folder if there's not already one
    if not os.path.exists(EXTRACTED_FOLDER):
        os.makedirs(EXTRACTED_FOLDER)
        print(f"Created extraction folder: {EXTRACTED_FOLDER}")

    all_conversations = []
    processed_files = 0
    error_files = 0

    print(f"Processing ChatGPT exports from: {EXPORTS_FOLDER}")
    print(f"Extracting to: {EXTRACTED_FOLDER}")
    print("-" * 50)

    # Process each ZIP file in the exp folder
    for file in os.listdir(EXPORTS_FOLDER):
        if file.lower().endswith('.zip'):
            zip_path = os.path.join(EXPORTS_FOLDER, file)
            try:
                conversations = extract_conversations_from_zip(zip_path, file)
                if conversations:
                    all_conversations.extend(conversations)
                    processed_files += 1
                    print(f"[OK] {file} - {len(conversations)} conversations")
                else:
                    print(f"[SKIP] {file} - no conversations found")
                    
            except Exception as e:
                print(f"[ERROR] {file}: {e}")
                error_files += 1

    print("-" * 50)
    print(f"Processing complete!")
    print(f"Files processed: {processed_files}")
    print(f"Files with errors: {error_files}")
    print(f"Total conversations before deduplication: {len(all_conversations)}")

    unique_conversations = remove_duplicates(all_conversations)
    
    print(f"Unique conversations after deduplication: {len(unique_conversations)}")

    save_master_json(unique_conversations)


def extract_conversations_from_zip(zip_path, filename):
    with zipfile.ZipFile(zip_path, 'r') as z:
        if 'conversations.json' not in z.namelist():
            return []
        
        z.extract('conversations.json', EXTRACTED_FOLDER)
        extracted_path = os.path.join(EXTRACTED_FOLDER, 'conversations.json')
        
        with open(extracted_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Handle different ds
        conversations = []
        if isinstance(data, list):
            conversations = data
        elif isinstance(data, dict):
            conversations = [data]

        # Rename the extr file to avoid overwriting
        archive_name = os.path.splitext(filename)[0]
        archived_path = os.path.join(EXTRACTED_FOLDER, f'{archive_name}_conversations.json')
        os.rename(extracted_path, archived_path)
        
        return conversations


def remove_duplicates(conversations):
    unique_conversations = []
    seen_ids = set()
    
    for conv in conversations:
        #different fields to identify unique convos
        conv_id = conv.get('id') or conv.get('title') or conv.get('create_time')
        
        if conv_id and conv_id not in seen_ids:
            unique_conversations.append(conv)
            seen_ids.add(conv_id)
        elif not conv_id:
            # If no id field found, include it anyway
            unique_conversations.append(conv)
    
    return unique_conversations


def save_master_json(conversations):
    with open(MASTER_JSON, 'w', encoding='utf-8') as f:
        json.dump(conversations, f, indent=2, ensure_ascii=False)
    
    print(f"Master conversation archive saved to: {MASTER_JSON}")


if __name__ == "__main__":
    main()
