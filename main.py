import os
import glob
import re
import argparse
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
import time
import sys

# Import Modules
import config
from utils import Logger, normalize_url, get_docx_content, show_banner
from crawler import Crawler
from downloader import Downloader

def save_queue_to_file(links):
    """Helper function to save queue safely."""
    with open(config.QUEUE_FILE, 'w', encoding='utf-8') as f:
        for link in links:
            f.write(link + "\n")

def run_discovery(logger):
    """Phase 1: Discovery Mode with Auto-Save and Resume capability."""
    print(f"\n{'='*55}")
    print(f"🔍 Phase 1: Discovery Mode Started")
    print(f"{'='*55}\n")
    logger.log("Starting Discovery Phase...", "PHASE_1")

    # Step 1: Smart File Detection
    all_files = glob.glob("*.*")
    ignored_extensions = ['.py', '.pyc', '.exe', '.jpg', '.png', '.zip', '.rar', '.pdf', '.log']
    ignored_names = [config.QUEUE_FILE, "requirements.txt", ".gitignore", "LICENSE", "README.md", getattr(config, 'LOG_FILE', 'scraper.log')]
    
    input_files = []
    for f in all_files:
        ext = os.path.splitext(f)[1].lower()
        if f not in ignored_names and ext not in ignored_extensions and "Scraped_Data" not in f:
            input_files.append(f)

    if not input_files:
        logger.log("No input files found.", "ERROR")
        return False

    logger.log(f"Processing input files: {', '.join(input_files)}", "INFO")

    raw_links = []
    for file_path in input_files:
        text_content = ""
        try:
            if file_path.endswith('.docx'):
                text_content = get_docx_content(file_path)
            else:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        text_content = f.read()
                except UnicodeDecodeError:
                    with open(file_path, 'r', encoding='latin-1') as f:
                        text_content = f.read()
        except Exception as e:
            logger.log(f"Could not read {file_path}: {e}", "WARN")
            continue
        
        urls = re.findall(r'(?:https?://|www\.)[^\s\u200c,;"\'<>\]\[]+|[a-zA-Z0-9.-]+\.(?:ir|com|net|org|co)[^\s\u200c,;"\'<>\]\[]*', text_content)
        for u in urls:
            normalized = normalize_url(u)
            if normalized:
                bad_exts = ['.jpg', '.png', '.css', '.js', '.woff', '.ttf', '.svg', '.gif']
                if not any(ext in normalized.lower() for ext in bad_exts):
                    raw_links.append(normalized)

    unique_domains = set()
    for link in raw_links:
        try:
            parsed = urlparse(link)
            if parsed.netloc:
                unique_domains.add(f"{parsed.scheme}://{parsed.netloc}")
        except:
            pass

    logger.log(f"Found {len(raw_links)} raw links.", "INFO")
    logger.log(f"Identified {len(unique_domains)} unique domains to check.", "START")
    
    # Step 2: Crawl Domains
    crawler = Crawler(logger)
    
    # Load existing queue if resuming
    all_article_links = set()
    if os.path.exists(config.QUEUE_FILE):
        with open(config.QUEUE_FILE, 'r', encoding='utf-8') as f:
            existing = [l.strip() for l in f if l.strip()]
            all_article_links.update(existing)
            if existing:
                logger.log(f"Resuming with {len(existing)} pre-existing links.", "RESUME")

    try:
        for domain_url in unique_domains:
            if crawler.is_domain_relevant(domain_url):
                logger.log(f"Scanning: {domain_url}", "SCANNING")
                links = crawler.get_site_articles(domain_url)
                if links:
                    logger.log(f" + Found {len(links)} articles.", "FOUND")
                    all_article_links.update(links)
                    # === CRITICAL: Save immediately after finding links ===
                    save_queue_to_file(all_article_links)
                else:
                    logger.log(" - No articles found.", "EMPTY")
            time.sleep(1)

    except KeyboardInterrupt:
        logger.log("User interrupted the process! Saving progress...", "WARN")
        save_queue_to_file(all_article_links)
        print("\n🛑 Process stopped by user. Links saved.")
        sys.exit(0)
    except Exception as e:
        logger.log(f"Unexpected Error: {e}. Saving progress...", "CRASH")
        save_queue_to_file(all_article_links)
        return False

    # Step 3: Final Save
    if all_article_links:
        save_queue_to_file(all_article_links)
        logger.log(f"Discovery Phase Complete. Total links: {len(all_article_links)}", "SUCCESS")
        return True # Signal to start Phase 2
    else:
        logger.log("No articles found in any domain.", "FAILURE")
        return False

def run_download(logger):
    """Phase 2: Download articles from the queue file."""
    if not os.path.exists(config.QUEUE_FILE):
        logger.log(f"Queue file '{config.QUEUE_FILE}' not found.", "ERROR")
        return

    print(f"\n{'='*55}")
    print(f"🚀 Phase 2: Download Mode Started")
    print(f"{'='*55}\n")
    logger.log("Starting Download Phase...", "PHASE_2")
    
    with open(config.QUEUE_FILE, 'r', encoding='utf-8') as f:
        urls_to_scrape = [line.strip() for line in f if line.strip()]
    
    logger.log(f"Queue size: {len(urls_to_scrape)} articles.", "INFO")
    
    # PASS LOGGER TO DOWNLOADER HERE
    downloader = Downloader(
        stats_callback=lambda n: print(f"   >>> Saved {n} articles so far..."),
        logger=logger
    )
    
    try:
        with ThreadPoolExecutor(max_workers=config.MAX_WORKERS) as executor:
            executor.map(downloader.scrape_article_content, urls_to_scrape)
    except KeyboardInterrupt:
        logger.log("Download interrupted by user.", "WARN")
        return
        
    logger.log(f"Download Complete! {downloader.stats['articles_saved']} saved, {downloader.stats['failed_urls']} failed.", "SUCCESS")
    logger.log(f"Files saved to: {config.ARTICLES_FOLDER}", "INFO")

def main():
    show_banner() 
    
    parser = argparse.ArgumentParser(description="OmniCrawler: Advanced Web Scraper by Ahmad Salami Far")
    parser.add_argument('--mode', choices=['discovery', 'download', 'auto'], default='auto', 
                        help="Operation mode.")
    
    args = parser.parse_args()
    logger = Logger()

    if args.mode == 'discovery':
        run_discovery(logger)
    elif args.mode == 'download':
        run_download(logger)
    else: # Auto mode (Default)
        # 1. Run Discovery
        found_links = run_discovery(logger)
        
        # 2. If links found (or file already exists), Run Download immediately
        if found_links or (os.path.exists(config.QUEUE_FILE) and os.path.getsize(config.QUEUE_FILE) > 0):
            print("\n🔄 Switching to Download Phase automatically...")
            time.sleep(2)
            run_download(logger)
        else:
            logger.log("Skipping Phase 2 (No links found).", "INFO")

if __name__ == "__main__":
    main()