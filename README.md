# python-scripts
A collection of useful Python scripts for file management, data processing, and automation tasks.

## Scripts Overview
###  File Management
- **`chatgpt_zip_finder.py`** - Finds and organizes ChatGPT export ZIP files by date
- **`conversation_merger.py`** - Merges multiple ChatGPT conversation exports into one file
- **`conversation_separator.py`** - Separates master conversation file into individual markdown files
- **`json_to_readable.py`** - Converts JSON conversations to readable markdown format
- **`pc_backup_automation.py`** - Automates PC backup to external drives


###  Web & Bookmarks
- **`bookmark_analyzer.py`** - Analyzes browser bookmarks and checks for dead links
- **`bookmark_grouper.py`** - Groups bookmarks by category automatically


### Media
- **`youtube_downloader.py`** - Downloads YouTube videos/audio using yt-dlp

###  Utilities
- **`desktop_time_widget.py`** - Desktop time widget with detailed time data export


## Requirements

```bash
pip install -r requirements.txt
```

### Dependencies
- `beautifulsoup4` - For HTML parsing (bookmark scripts)
- `requests` - For web requests (bookmark analyzer)
- `yt-dlp` - For YouTube downloading
- `tkinter` - For GUI applications (usually included with Python)

## Setup Instructions

1. **Clone or download** this repository
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Configure paths** in each script's configuration section
4. **Run scripts** individually based on your needs

## Configuration

Each script contains a configuration section at the top where you need to update paths and settings for your system:

```python
# Configuration - Update these paths for your system
SOURCE_FOLDER = r'C:\Path\To\Your\Source\Folder'
DEST_FOLDER = r'C:\Path\To\Your\Destination\Folder'
```

### Important: Update Paths Before Use
- Replace all example paths with your actual directory paths
- Update URLs in the YouTube downloader with actual video URLs
- Configure bookmark file paths for browser bookmark scripts

## Usage Examples

### ChatGPT Export Organization
```bash
python chatgpt_zip_finder.py
```
Scans for ChatGPT export ZIP files and organizes them with standardized naming.

### Bookmark Management
```bash
# Step 1: Analyze bookmarks
python bookmark_analyzer.py

# Step 2: Group bookmarks by category
python bookmark_grouper.py
```

### YouTube Downloads
```bash
python youtube_downloader.py
```
Downloads videos/audio from configured URL list.

### Backup Automation
```bash
python pc_backup_automation.py
```
Creates timestamped backups of configured directories.

## Features

###  ChatGPT Tools
- **Smart date extraction** from filenames
- **Duplicate handling** with automatic numbering
- **Conversation merging** with deduplication
- **Multiple export formats** (JSON, Markdown)

###  Bookmark Management
- **Dead link detection** (optional)
- **Automatic categorization** based on content analysis
- **Multiple output formats** (HTML, Markdown)
- **Customizable categories**

###  Backup 
- **Selective file backup** with exclusion patterns
- **Progress tracking** and size reporting
- **Error handling** and logging


###  Media Tools
- **High-quality audio extraction**
- **Batch downloading** support
- **Multiple format options**
- **Progress monitoring**

## Safety Features

- **Input validation** and error handling
- **Progress indicators** for long operations
- **Backup creation** before file operations
- **Exclusion patterns** for system files

## Customization

### Adding New Categories (Bookmark Grouper)
```python
BOOKMARK_GROUPS = {
    'Your Category': ['keyword1', 'keyword2', 'keyword3'],
    # Add more categories...
}
```

### Modifying Backup Exclusions
```python
EXCLUDE_PATTERNS = [
    'node_modules', '.git', '__pycache__',
    'your_custom_exclusion'  # Add your patterns
]
```

### YouTube Download Options
```python
DOWNLOAD_OPTIONS = {
    'format': 'bestaudio/best',
    'audioformat': 'mp3',
    'preferredquality': '192',  # Adjust quality
    # Modify other options...
}
```

## Troubleshooting

### Common Issues

1. **Path not found errors**
   - Ensure all configured paths exist
   - Use absolute paths instead of relative paths
   - Check path format for your operating system

2. **Permission errors**
   - Run as administrator if needed
   - Check write permissions on destination folders
   - Ensure source files are not in use

3. **Missing dependencies**
   - Install required packages: `pip install -r requirements.txt`
   - Update pip: `pip install --upgrade pip`

4. **YouTube download issues**
   - Update yt-dlp: `pip install --upgrade yt-dlp`
   - Check if URLs are valid and accessible
   - Verify internet connection

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for improvements.

### Development Guidelines
- Follow PEP 8 style guidelines
- Add docstrings to functions
- Include error handling
- Test with various file types and scenarios


## Disclaimer!!!

- These scripts are provided as-is without warranty
- Always test with non-critical data first
- Back up important files before running organization scripts
- Respect website terms of service when downloading content

---

**Note**: Remember to update configuration paths and settings before using any script!

