import json
from datetime import datetime

#----Configs
MASTER_JSON = r'C:\Path\To\Your\master_conversations.json'  # I: merged convo file
OUTPUT_MD = r'C:\Path\To\Your\conversations_readable.md'   # O: readable md file

def main():
    """
    Converts ChatGPT conversations from JSON format to readable Markdown format.
    Creates a single markdown file with all conversations formatted for easy reading.
    """
    
    try:
        with open(MASTER_JSON, 'r', encoding='utf-8') as f:
            conversations = json.load(f)
    except FileNotFoundError:
        print(f"Error: Could not find master conversations file at {MASTER_JSON}")
        print("Please run the conversation merger script first.")
        return
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {MASTER_JSON}")
        return

    print(f"Converting {len(conversations)} conversations to readable format...")

    with open(OUTPUT_MD, 'w', encoding='utf-8') as out:
        write_header(out, len(conversations))
        
        for idx, conv in enumerate(conversations, 1):
            write_conversation(out, conv, idx)
            
            # Progress indicator 
            if idx % 10 == 0:
                print(f"Processed {idx}/{len(conversations)} conversations...")

    print(f"Conversion complete! Readable file saved to: {OUTPUT_MD}")


def write_header(out, total_conversations):
    out.write("# ChatGPT Conversations - Readable Format\n\n")
    out.write(f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    out.write(f"**Total conversations:** {total_conversations}\n\n")
    out.write("---\n\n")


def write_conversation(out, conv, idx):

    # Extract convo metadata
    title = conv.get('title', f'Conversation {idx}')
    create_time = format_timestamp(conv.get('create_time', ''))
    
    # Write convo header
    out.write(f"## {idx}. {title}\n")
    out.write(f"**Created:** {create_time}\n\n")
    
    messages = conv.get('mapping', conv.get('messages', {}))
    message_list = extract_messages(messages)
    
    if message_list:
        for role, content in message_list:
            out.write(f"**{role.title()}:** {content}\n\n")
    else:
        out.write("*No messages found in this conversation.*\n\n")
    
    out.write("---\n\n")


def format_timestamp(timestamp):
    try:
        if isinstance(timestamp, (int, float)):
            return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(timestamp, str) and timestamp.replace('.', '').isdigit():
            return datetime.fromtimestamp(float(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
        else:
            return str(timestamp) if timestamp else 'Unknown'
    except (ValueError, OSError):
        return str(timestamp) if timestamp else 'Unknown'


def extract_messages(messages):
    message_list = []
    
    if isinstance(messages, dict):
        for message_data in messages.values():
            if message_data is None:
                continue
                
            message_obj = message_data.get('message')
            if not isinstance(message_obj, dict):
                continue
                
            content = message_obj.get('content', {})
            parts = content.get('parts', [])
            role = message_obj.get('author', {}).get('role', 'unknown')
            
            for part in parts:
                if part and part.strip(): 
                    message_list.append((role, part))
                    
    elif isinstance(messages, list):
        for message in messages:
            role = message.get('role', 'unknown')
            content = message.get('content', '')
   
            if isinstance(content, dict):
                content = content.get('parts', [''])[0]
            
            if content and content.strip(): 
                message_list.append((role, content))
    
    return message_list


if __name__ == "__main__":
    main()
