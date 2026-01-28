🕷️ OmniCrawler

A High-Performance, Fault-Tolerant, and Topic-Agnostic Web Scraping Framework. > Developed by: Ahmad Salami Far

📖 Overview

OmniCrawler is a robust web scraping engine designed to build large-scale datasets from the web effortlessly. Unlike traditional scrapers bound to specific websites, OmniCrawler is general-purpose. It takes raw files containing mixed links, discovers relevant content based on your keywords, and automatically downloads clean, text-based articles.

Whether you are gathering data for AI Training (NLP), Market Research, or Academic Analysis, OmniCrawler automates the entire pipeline.

📖 معرفی پروژه

OmniCrawler (آمنی‌کراولر) یک موتور خزشگر وب قدرتمند است که برای ساخت مجموعه داده‌های بزرگ (Datasets) طراحی شده است. برخلاف ربات‌های سنتی که محدود به سایت‌های خاصی هستند، این ابزار عمومی است. این برنامه فایل‌های ورودی شما را (که حاوی لینک‌های درهم هستند) می‌خواند، محتوای مرتبط با کلمات کلیدی شما را کشف می‌کند و مقالات تمیز و متنی را دانلود می‌کند.

این ابزار برای آموزش هوش مصنوعی (NLP)، تحقیقات بازار و تحلیل‌های دانشگاهی ایده‌آل است.

✨ Key Features / ویژگی‌های کلیدی

🔄 Auto-Pilot Mode (حالت خلبان خودکار)

It runs in a dual-phase cycle automatically:

Discovery Phase: Scans inputs, filters domains, and finds article links.

Download Phase: Switches to multi-threaded downloading without user intervention.

برنامه به صورت خودکار بین فاز "کشف لینک" و "دانلود محتوا" سوییچ می‌کند و نیاز به نظارت کاربر ندارد.

💾 Smart Resume Capability (قابلیت ادامه دانلود)

Crashes or internet cuts? No problem. OmniCrawler saves the queue (download_queue.txt) in real-time. When you restart, it resumes exactly where it left off.

در صورت قطع برق یا اینترنت، لینک‌های پیدا شده از دست نمی‌روند. برنامه در اجرای بعدی دقیقاً از همان‌جایی که متوقف شده بود ادامه می‌دهد.

📂 Universal Input Parser (ورودی هوشمند و نامحدود)

Just drop any file into the folder. OmniCrawler extracts links from:

📜 Text files (.txt, logs)

📄 Word Documents (.docx)

💻 Code files (.py, .js, etc.)

فایل‌های خود را درون پوشه بریزید. برنامه لینک‌ها را از دل متن‌های شلوغ، فایل‌های ورد و حتی کدهای برنامه استخراج می‌کند.

🎯 Smart Filtering & Cleaning (فیلترینگ و تمیزسازی هوشمند)

Strict Mode: Downloads only pages matching your specific keywords.

Content Cleaning: Removes ads, navigation bars, scripts, and footer noise.

Blacklist: Automatically skips social media and irrelevant sites (YouTube, Instagram, etc.).

حذف تبلیغات، منوها و اسکریپت‌ها برای دریافت متن خالص. همچنین سایت‌های نامرتبط (مثل اینستاگرام و یوتیوب) به صورت خودکار نادیده گرفته می‌شوند.

🚀 Quick Start / شروع سریع

1. Installation (نصب)

Clone the repository and install dependencies:

git clone [https://github.com/ahmadsalamifar/OmniCrawler.git](https://github.com/ahmadsalamifar/OmniCrawler.git)
cd OmniCrawler
pip install -r requirements.txt


2. Configuration (تنظیمات)

Open config.py to customize your target.
فایل config.py را باز کنید و تنظیمات را تغییر دهید.

# config.py

# 1. Define what you are looking for (کلمات کلیدی هدف)
TARGET_KEYWORDS = ["Artificial Intelligence", "Neural Networks", "هوش مصنوعی"]

# 2. Set Mode (Strict Mode = True means stricter filtering)
STRICT_MODE = True 

# 3. Performance Settings
MAX_WORKERS = 5  # Number of simultaneous downloads


3. Usage (نحوه اجرا)

Option A: Auto Mode (Recommended)
Simply place your files (containing links) in the project folder and run:
فایل‌های حاوی لینک را در پوشه پروژه قرار دهید و دستور زیر را اجرا کنید:

python main.py


Option B: Manual Control
You can run specific phases individually:

Discovery Only: Find links but do not download yet.

python main.py --mode discovery


Download Only: Download from an existing download_queue.txt.

python main.py --mode download


📂 Project Structure / ساختار پروژه

OmniCrawler/
│
├── 📂 Scraped_Data/        # Output Folder (Where files are saved)
│   └── 📂 Articles/        # Cleaned text files (.txt)
│
├── 📜 config.py            # User Settings (Keywords, Blacklist, Threads)
├── 📜 main.py              # Entry Point (Auto-Switching Logic)
├── 📜 crawler.py           # Logic for finding & validating links
├── 📜 downloader.py        # Logic for downloading & cleaning HTML
├── 📜 utils.py             # Helpers (File reading, normalization)
├── 📜 download_queue.txt   # Database of found links (Auto-generated)
├── 📜 scraper_report.log   # Detailed execution logs
└── 📜 requirements.txt     # Python dependencies


⚠️ Disclaimer

This tool is designed for educational and research purposes.

Please respect robots.txt policies of websites.

Do not use this tool to overload servers (DDoS) or scrape copyrighted personal data without permission.

The author is not responsible for misuse of this software.

این ابزار صرفاً برای اهداف آموزشی و تحقیقاتی طراحی شده است. لطفاً از آن برای فشار آوردن به سرورها یا استخراج غیرقانونی اطلاعات استفاده نکنید.

<div align="center">

Made with 💻 and ☕ by Ahmad Salami Far

</div>
