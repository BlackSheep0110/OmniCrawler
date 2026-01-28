"""
Configuration settings for OmniCrawler.
This file allows the user to customize the target topic.
"""
import os

# ==========================================
# 🎯 TOPIC SETTINGS (تنظیمات موضوع)
# ==========================================
# If STRICT_MODE is True, the scraper only downloads pages containing these keywords.
STRICT_MODE = True

# کلمات کلیدی هدف (می‌توانید تغییر دهید)
TARGET_KEYWORDS =  [
    "هوش مصنوعی", "AI", "Machine Learning", "Deep Learning", 
    "Artificial Intelligence", "برنامه‌نویسی", "پایتون"
]

# ==========================================
# ⚙️ SYSTEM SETTINGS (تنظیمات سیستم)
# ==========================================

# Output Directories
OUTPUT_FOLDER = "Scraped_Data"
ARTICLES_FOLDER = os.path.join(OUTPUT_FOLDER, "Articles")
QUEUE_FILE = "download_queue.txt"
LOG_FILE = "scraper_report.log"  # <--- این خط باعث رفع ارور می‌شود

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
}

BLACKLISTED_DOMAINS = [
    'youtube.com', 'instagram.com', 'twitter.com', 'linkedin.com', 
    'facebook.com', 'google.com', 'yahoo.com', 'wikipedia.org', 
    'aparat.com', 'divar.ir', 'sheypoor.com', 'torob.com', 
    'digikala.com', 'ninisite.com', 'civilica.com', 'emalls.ir', 'jobinja.ir',
    'microsoft.com', 'adobe.com', 'github.com', 'gitlab.com'
]

TIMEOUT = 15
MAX_HUB_PAGES = 15
MAX_WORKERS = 5