from bs4 import BeautifulSoup
import requests
import os

#----Configs
BOOKMARKS_HTML = r'C:\Path\To\Your\bookmarks.html'  
CLEANED_MD = r'C:\Path\To\Your\bookmarks_cleaned.md'  

def main():
    """
    Analyzes browser bookmarks HTML file and creates a cleaned md version.
    Optionally checks for dead links.
    """
    
    if not os.path.exists(BOOKMARKS_HTML):
        print(f"Error: Bookmarks file not found at {BOOKMARKS_HTML}")
        print("Please export your bookmarks from your browser and update the BOOKMARKS_HTML path.")
        return

    print(f"Reading bookmarks from: {BOOKMARKS_HTML}")
    
    with open(BOOKMARKS_HTML, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    bookmarks = []

    
    for a in soup.find_all('a'):
        href = a.get('href')
        name = a.text.strip()
        add_date = a.get('add_date')
        
        if href:  
            bookmarks.append({
                'name': name, 
                'url': href, 
                'add_date': add_date
            })

    print(f"Found {len(bookmarks)} bookmarks.")

   
    check_dead = True 
    
    if check_dead:
        print("Checking for dead links... (this may take a while)")
        for i, bm in enumerate(bookmarks, 1):
            bm['dead'] = is_dead_link(bm['url'])
            if i % 10 == 0:  
                print(f"Checked {i}/{len(bookmarks)} links...")

    
    print(f"Writing cleaned bookmarks to: {CLEANED_MD}")
    
    with open(CLEANED_MD, 'w', encoding='utf-8') as f:
        f.write("# Cleaned Bookmarks\n\n")
        f.write(f"Generated on: {os.path.basename(__file__)}\n")
        f.write(f"Total bookmarks: {len(bookmarks)}\n\n")
        
        for bm in bookmarks:
            status = ""
            if check_dead:
                status = " (DEAD)" if bm.get('dead') else " (LIVE)"
            
            f.write(f"- [{bm['name']}]({bm['url']}){status}\n")
    
    print(f"Successfully saved cleaned bookmarks to: {CLEANED_MD}")


def is_dead_link(url):

    try:
        response = requests.head(url, timeout=5, allow_redirects=True)
        return response.status_code >= 400
    except Exception:
        return True


if __name__ == "__main__":
    main()
