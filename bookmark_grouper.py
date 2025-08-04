from bs4 import BeautifulSoup
import re
import os

#----- Configs
BOOKMARKS_MD = r'C:\Path\To\Your\bookmarks_cleaned.md'  
OUTPUT_HTML = r'C:\Path\To\Your\bookmarks_grouped.html'  

# Categorization groups --> customize these categories like you wanna
BOOKMARK_GROUPS = {
    'Programming & Development': [
        'python', 'javascript', 'nodejs', 'react', 'angular', 'vue', 'html', 'css',
        'stackoverflow', 'w3schools', 'freecodecamp', 'github', 'gitlab', 'docs'
    ],
    
    'Data Science & AI': [
        'data analysis', 'machine learning', 'deep learning', 'pandas', 'numpy',
        'scikit-learn', 'tensorflow', 'keras', 'jupyter', 'anaconda'
    ],
    
    'Cloud & DevOps': [
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'ci/cd', 'jenkins',
        'terraform', 'ansible', 'cloud'
    ],
    
    'Security & Hacking': [
        'hackthebox', 'tryhackme', 'ctf', 'cybersecurity', 'pentesting',
        'vulnerability', 'security', 'kali', 'metasploit', 'burp'
    ],
    
    'Learning & Education': [
        'courses', 'tutorials', 'udemy', 'coursera', 'edx', 'khan academy',
        'learning', 'education', 'certification', 'training'
    ],
    
    'Tools & Utilities': [
        'tools', 'utilities', 'software', 'productivity', 'automation',
        'scripting', 'terminal', 'command line', 'text editor'
    ],
    
    'Documentation & References': [
        'docs', 'documentation', 'manual', 'reference', 'api', 'guide',
        'cheatsheet', 'handbook', 'specification'
    ],
    
    'Community & Forums': [
        'reddit', 'forum', 'discord', 'slack', 'community', 'discussion',
        'chat', 'social', 'networking'
    ],
    
    'News & Media': [
        'news', 'articles', 'blog', 'podcast', 'video', 'youtube',
        'medium', 'dev.to', 'hacker news'
    ],
    
    'Shopping & E-commerce': [
        'amazon', 'ebay', 'shop', 'store', 'buy', 'purchase', 'deal',
        'discount', 'sale', 'price', 'review'
    ],
    
    'Entertainment': [
        'games', 'gaming', 'movie', 'music', 'streaming', 'netflix',
        'entertainment', 'fun', 'hobby'
    ],
    
    'Finance & Investing': [
        'finance', 'investing', 'stock', 'crypto', 'bitcoin', 'trading',
        'money', 'budget', 'bank', 'payment'
    ],
    
    'Health & Fitness': [
        'health', 'fitness', 'exercise', 'nutrition', 'wellness',
        'medical', 'doctor', 'hospital', 'diet'
    ],
    
    'Travel & Transportation': [
        'travel', 'flight', 'hotel', 'booking', 'vacation', 'trip',
        'map', 'navigation', 'transport'
    ],
    
    'Accounts & Login': [
        'account', 'login', 'profile', 'settings', 'authentication',
        'password', 'security', 'user', 'dashboard'
    ],
    
    'Work & Business': [
        'work', 'business', 'corporate', 'company', 'office', 'meeting',
        'project', 'management', 'email', 'calendar'
    ]
}

def main():
  
    if not os.path.exists(BOOKMARKS_MD):
        print(f"Error: Bookmarks file not found at {BOOKMARKS_MD}")
        print("Please run the bookmark analyzer script first.")
        return
    
    print(f"Reading bookmarks from: {BOOKMARKS_MD}")
    
    bookmarks = parse_bookmarks_from_markdown()
    
    if not bookmarks:
        print("No bookmarks found in the input file.")
        return
    
    print(f"Found {len(bookmarks)} bookmarks to categorize...")
    
    grouped_bookmarks = categorize_bookmarks(bookmarks)
    
    generate_grouped_html(grouped_bookmarks)
    
    print(f"Grouped bookmarks saved to: {OUTPUT_HTML}")


def parse_bookmarks_from_markdown():
    bookmarks = []
    
    try:
        with open(BOOKMARKS_MD, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                # Match markdown link format: - [title](url)
                match = re.match(r'^\s*-\s*\[(.*?)\]\((.*?)\)', line.strip())
                if match:
                    title, url = match.groups()
                    bookmarks.append({
                        'title': title.strip(),
                        'url': url.strip(),
                        'line': line_num
                    })
    except Exception as e:
        print(f"Error reading bookmarks file: {e}")
        return []
    
    return bookmarks


def categorize_bookmarks(bookmarks):
    grouped = {}
    
    for bookmark in bookmarks:
        category = find_best_category(bookmark)
        
        if category not in grouped:
            grouped[category] = []
        
        grouped[category].append(bookmark)
    
    sorted_grouped = {}
    for category in sorted(grouped.keys()):
        sorted_grouped[category] = sorted(grouped[category], key=lambda x: x['title'].lower())
    
    return sorted_grouped


def find_best_category(bookmark):

    # Combine title and URL for analysis
    search_text = f"{bookmark['title']} {bookmark['url']}".lower()
    
    # Check each category for keyword matches
    best_category = 'Misc'  
    max_matches = 0
    
    for category, keywords in BOOKMARK_GROUPS.items():
        matches = sum(1 for keyword in keywords if keyword.lower() in search_text)
        
        if matches > max_matches:
            max_matches = matches
            best_category = category
    
    return best_category


def generate_grouped_html(grouped_bookmarks):
    total_bookmarks = sum(len(bookmarks) for bookmarks in grouped_bookmarks.values())
    
    try:
        with open(OUTPUT_HTML, 'w', encoding='utf-8') as out:
            write_html_header(out, total_bookmarks)
            for category, bookmarks in grouped_bookmarks.items():
                write_category_section(out, category, bookmarks)
            write_html_footer(out)        
    except Exception as e:
        print(f"Error writing HTML file: {e}")


def write_html_header(out, total_bookmarks):
    """Writes the HTML file header."""
    out.write('<!DOCTYPE NETSCAPE-Bookmark-file-1>\\n')
    out.write('<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">\\n')
    out.write('<TITLE>Grouped Bookmarks</TITLE>\\n')
    out.write('<H1>Grouped Bookmarks</H1>\\n')
    out.write(f'<p>Total bookmarks: {total_bookmarks}</p>\\n')
    out.write('<DL><p>\\n')


def write_category_section(out, category, bookmarks):
    """Writes a category section with its bookmarks."""
    out.write(f'<DT><H3>{category} ({len(bookmarks)})</H3>\\n')
    out.write('<DL><p>\\n')
    
    for bookmark in bookmarks:
        safe_title = escape_html(bookmark['title'])
        safe_url = escape_html(bookmark['url'])
        out.write(f'<DT><A HREF="{safe_url}">{safe_title}</A>\\n')
    out.write('</DL><p>\\n')

def write_html_footer(out):
    """Writes the HTML file footer."""
    out.write('</DL><p>\\n')

def escape_html(text):
    return (text.replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&#x27;'))

def print_categorization_summary(grouped_bookmarks):
    print("\\nCategorization Summary:")
    print("-" * 40)
    
    for category, bookmarks in sorted(grouped_bookmarks.items()):
        print(f"{category}: {len(bookmarks)} bookmarks")
    
    total = sum(len(bookmarks) for bookmarks in grouped_bookmarks.values())
    print(f"\\nTotal: {total} bookmarks")

if __name__ == "__main__":
    main()
