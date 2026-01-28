import requests
from bs4 import BeautifulSoup
import os
import re
import config
from utils import clean_filename

class Downloader:
    def __init__(self, stats_callback=None, logger=None):
        self.visited_urls = set()
        self.stats = {
            "articles_saved": 0,
            "failed_urls": 0
        }
        self.stats_callback = stats_callback 
        self.logger = logger

        if not os.path.exists(config.ARTICLES_FOLDER):
            os.makedirs(config.ARTICLES_FOLDER)

    def log(self, msg, status="INFO"):
        if self.logger:
            self.logger.log(msg, status)

    def clean_soup(self, soup):
        """Removes unwanted elements (nav, footer, ads) from the HTML."""
        # Remove standard unwanted tags
        for tag in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'form', 'iframe', 'noscript']):
            tag.decompose()
        
        # Remove elements by common 'noise' classes
        noise_patterns = re.compile(r'(sidebar|comment|widget|related|menu|navigation|breadcrumb|share|social|popup|cookie|hidden)', re.I)
        for tag in soup.find_all(class_=noise_patterns):
            tag.decompose()
            
        return soup

    def scrape_article_content(self, url):
        # 0. MEDIA FILTER: Skip images and non-html files immediately
        # لیست پسوندهای ممنوعه (عکس، فیلم، فایل فشرده و...)
        ignored_extensions = (
            '.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.bmp', '.ico', 
            '.mp4', '.mp3', '.avi', '.mov', 
            '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.zip', '.rar', '.exe'
        )
        # بررسی می‌کنیم آیا انتهای لینک به یکی از این پسوندها ختم می‌شود یا خیر
        if url.lower().strip().endswith(ignored_extensions):
            self.log(f"Skipping media file: {url}", "SKIP")
            return

        if url in self.visited_urls:
            return
        self.visited_urls.add(url)
        
        try:
            # Add verify=False if SSL errors occur, though verify=True is standard
            response = requests.get(url, headers=config.HEADERS, timeout=config.TIMEOUT)
            response.encoding = response.apparent_encoding
            
            # Check content type header to ensure it's text/html
            content_type = response.headers.get('Content-Type', '').lower()
            if 'image' in content_type or 'application' in content_type and 'html' not in content_type:
                 self.log(f"Skipping non-HTML content ({content_type}): {url}", "SKIP")
                 return

            if response.status_code != 200:
                self.log(f"Failed HTTP {response.status_code}: {url}", "ERROR")
                self.stats["failed_urls"] += 1
                return

            # Prefer lxml for speed
            try:
                soup = BeautifulSoup(response.text, 'lxml')
            except:
                soup = BeautifulSoup(response.text, 'html.parser')

            # 1. CLEANUP: Remove noise before extraction
            soup = self.clean_soup(soup)

            # 2. Extract Title
            title = soup.find('h1') or soup.find('title')
            if not title:
                self.log(f"No title found: {url}", "SKIP")
                return
            
            title_text = title.get_text(strip=True).replace("/", "-")
            
            # 3. Smart Content Extraction (Updated for Elementor/PageBuilders)
            content_text = ""
            
            # Priority 1: Look for specific article containers
            # Added 'elementor-widget-text-editor' and 'elementor-widget-theme-post-content' for the site you mentioned
            target_classes = re.compile(r'(post-content|entry-content|article-body|content-area|single-post|blog-post|elementor-widget-text-editor|elementor-widget-theme-post-content)', re.I)
            
            candidates = soup.find_all(['div', 'article', 'section'], class_=target_classes)
            
            if candidates:
                # If multiple candidates found (e.g. multiple elementor widgets), join them
                for candidate in candidates:
                    paragraphs = candidate.find_all(['p', 'h2', 'h3', 'h4', 'ul', 'li'])
                    for p in paragraphs:
                        text = p.get_text(strip=True)
                        if len(text) > 30: # Minimum length to be considered a sentence
                            content_text += text + "\n\n"
            
            # Priority 2: Fallback - Find the dense text cluster
            if len(content_text) < 150:
                # self.log(f"Strategy A weak (len={len(content_text)}), scanning body paragraphs: {url}", "DEBUG")
                body = soup.find('body')
                if body:
                    # Get all paragraphs that are NOT empty
                    paragraphs = [p for p in body.find_all('p') if len(p.get_text(strip=True)) > 40]
                    
                    # Heuristic: The main content usually has the largest cluster of p tags sharing a parent
                    if paragraphs:
                        content_text = ""
                        for p in paragraphs:
                            content_text += p.get_text(strip=True) + "\n\n"

            # 4. Final Validation & Save
            if len(content_text) > 100: # Lowered threshold to catch smaller articles
                filename = clean_filename(title_text)
                file_path = os.path.join(config.ARTICLES_FOLDER, filename)
                
                if len(file_path) > 250:
                    filename = f"Article_{len(self.visited_urls)}.txt"
                    file_path = os.path.join(config.ARTICLES_FOLDER, filename)

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(f"URL: {url}\nTitle: {title_text}\n{'='*50}\n\n{content_text}")
                
                self.stats["articles_saved"] += 1
                
                if self.stats_callback and self.stats["articles_saved"] % 5 == 0:
                    self.stats_callback(self.stats["articles_saved"])
            else:
                self.log(f"Content too short/not found ({len(content_text)} chars): {url}", "SKIP")
                self.stats["failed_urls"] += 1

        except Exception as e:
            # self.log(f"Error scraping {url}: {e}", "ERROR")
            self.stats["failed_urls"] += 1