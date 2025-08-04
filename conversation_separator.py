import json
import os
import re
from datetime import datetime

#---- Configs
MASTER_JSON = r'C:\Path\To\Your\master_conversations.json'  # I: merged convos file
OUTPUT_DIR = r'C:\Path\To\Your\Separated\Conversations'     # O: folder for individual files

def main():
    """
    Separates a master conversations JSON file into individual markdown files.
    Each conversation becomes a separate file organized by date and title.
    """

    if not os.path.exists(MASTER_JSON):
        print(f"Error: Master conversations file not found at {MASTER_JSON}")
        print("Please run the conversation merger script first.")
        return
    
    # Create output dir
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Output directory: {OUTPUT_DIR}")
    
    # Load convos
    try:
        with open(MASTER_JSON, 'r', encoding='utf-8') as f:
            conversations = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {MASTER_JSON}")
        return
    
    print(f"Processing {len(conversations)} conversations...")
    print("-" * 50)
    
    # Process each convo
    successful_exports = 0
    failed_exports = 0
    
    for idx, conv in enumerate(conversations, 1):
        try:
            export_conversation(conv, idx)
            successful_exports += 1
            
            # Progress indicator
            if idx % 10 == 0:
                print(f"Processed {idx}/{len(conversations)} conversations...")
                
        except Exception as e:
            print(f"Error processing conversation {idx}: {e}")
            failed_exports += 1
    
    print("-" * 50)
    print("Processing complete!")
    print(f"Successfully exported: {successful_exports}")
    print(f"Failed exports: {failed_exports}")
    print(f"Files saved to: {OUTPUT_DIR}")


def export_conversation(conv, idx):

    # Extract metadata
    title = conv.get('title', f'Conversation {idx}')
    create_time = conv.get('create_time', '')
    date_str = format_timestamp_for_filename(create_time)
    
    safe_title = sanitize_filename(title)
    filename = f"{date_str}_{safe_title}.md"
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    # Handle duplicates
    filepath = get_unique_filepath(filepath)
    
    # Write convo to file
    with open(filepath, 'w', encoding='utf-8') as out:
        write_conversation_header(out, title, create_time)
        write_conversation_messages(out, conv)
    
    print(f"[OK] {os.path.basename(filepath)}")


def write_conversation_header(out, title, create_time):

    formatted_time = format_timestamp_for_display(create_time)
    
    out.write(f"# {title}\n\n")
    out.write(f"**Created:** {formatted_time}\n")
    out.write(f"**Exported:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    out.write("---\n\n")


def write_conversation_messages(out, conv):

    messages = conv.get('mapping', conv.get('messages', {}))
    message_list = extract_messages(messages)
    
    if not message_list:
        out.write("*No messages found in this conversation.*\n\n")
        return
    
    for role, content in message_list:
        out.write(f"## {role.title()}\n\n")
        out.write(f"{content}\n\n")
        out.write("---\n\n")


def extract_messages(messages):

    message_list = []
    
    if isinstance(messages, dict):
        for m in messages.values():
            if m is None:
                continue
            message_obj = m.get('message')
            if not isinstance(message_obj, dict):
                continue
            content = message_obj.get('content', {})
            parts = content.get('parts', [])
            role = message_obj.get('author', {}).get('role', 'unknown')
            for part in parts:
                if part and part.strip():
                    message_list.append((role, part))
                    
    elif isinstance(messages, list):
        for m in messages:
            role = m.get('role', 'unknown')
            content = m.get('content', '')
            if isinstance(content, dict):
                content = content.get('parts', [''])[0]
            if content and content.strip():
                message_list.append((role, content))
    
    return message_list


def format_timestamp_for_filename(timestamp):
    try:
        if isinstance(timestamp, (int, float)):
            return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')
        elif isinstance(timestamp, str) and timestamp.replace('.', '').isdigit():
            return datetime.fromtimestamp(float(timestamp)).strftime('%Y-%m-%d')
        else:
            return 'unknown-date'
    except (ValueError, OSError):
        return 'unknown-date'


def format_timestamp_for_display(timestamp):
    try:
        if isinstance(timestamp, (int, float)):
            return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(timestamp, str) and timestamp.replace('.', '').isdigit():
            return datetime.fromtimestamp(float(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
        else:
            return str(timestamp) if timestamp else 'Unknown'
    except (ValueError, OSError):
        return str(timestamp) if timestamp else 'Unknown'


def sanitize_filename(filename):
    sanitized = re.sub(r'[^a-zA-Z0-9 _\-]', '', filename)
    sanitized = sanitized[:50].strip() or 'Untitled'
    return sanitized


def get_unique_filepath(filepath):
    if not os.path.exists(filepath):
        return filepath
    
    base_path = os.path.splitext(filepath)[0]
    extension = os.path.splitext(filepath)[1]
    count = 1
    
    while True:
        new_path = f"{base_path}_{count}{extension}"
        if not os.path.exists(new_path):
            return new_path
        count += 1


if __name__ == "__main__":
    main()
