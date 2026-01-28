OmniCrawler 🕷️

OmniCrawler is a robust, modular, and general-purpose web scraping framework designed to build datasets from the web. Whether you are researching AI, Real Estate, Finance, or Medical data, OmniCrawler helps you discover relevant domains and bulk-download articles.

Developed by: Ahmad Salami Far

It operates in an Auto-Pilot mode:

Discovery: Scans ANY input file (Text, Word, Logs, etc.) for links, filters relevant domains, and maps articles.

Extraction: Automatically switches to multithreaded downloading of clean text content.

OmniCrawler (خزشگر هوشمند وب)

OmniCrawler یک فریم‌ورک متن‌باز و قدرتمند برای استخراج داده از وب است. این ابزار به هیچ موضوع خاصی محدود نیست و توسط احمد سلامی‌فر توسعه یافته است.

✨ Key Features / ویژگی‌های کلیدی

🔄 Auto-Pilot Mode: Automatically runs discovery and then switches to download mode without user intervention.

حالت خلبان خودکار: اجرای پشت‌سرهم فاز کشف و دانلود بدون نیاز به دخالت کاربر.

💾 Smart Resume & Checkpoint: Saves found links instantly. If the internet cuts off or the app crashes, you can resume exactly where you left off.

ذخیره لحظه‌ای و قابلیت ادامه: لینک‌ها بلافاصله ذخیره می‌شوند. اگر برق برود یا برنامه بسته شود، در اجرای بعدی از همان‌جا ادامه می‌دهد.

📂 Universal Input Reader: Extracts links from dirty/messy text files, logs, code, or Word documents (.docx).

ورودی نامحدود: استخراج لینک از فایل‌های متنی شلوغ، فایل‌های ورد و لاگ‌های سیستم با استفاده از الگوریتم‌های هوشمند پاکسازی.

📝 File Logging: Keeps a detailed history of operations in scraper_report.log.

گزارش‌گیری فایل: ثبت دقیق تمام وقایع و خطاها در فایل لاگ برای بررسی‌های بعدی.

Topic Agnostic: Fully customizable via config.py.

بدون محدودیت موضوع: تنها با تغییر کلمات کلیدی، هدف ربات را مشخص کنید (مثلاً  هوش مصنوعی، بورس).

🚀 Quick Start / شروع سریع

1. Installation (نصب)

git clone [https://github.com/ahmadsalamifar/OmniCrawler.git](https://github.com/ahmadsalamifar/OmniCrawler.git)
cd OmniCrawler
pip install -r requirements.txt


2. Configuration (تنظیمات)

Open config.py and set TARGET_KEYWORDS.
فایل config.py را باز کنید و کلمات کلیدی هدف خود را بنویسید (مثلاً "کانکس"، "هوش مصنوعی").

3. Usage (نحوه اجرا)

Just drop your input files (files containing links) into the folder and run:
فایل‌های حاوی لینک (هر فایلی با هر پسوندی) را در پوشه بریزید و فقط دستور زیر را اجرا کنید:

python main.py


The script will find links, filter them, save the queue, and automatically start downloading.

برنامه لینک‌ها را پیدا می‌کند، فیلتر می‌کند و به صورت خودکار دانلود را شروع می‌کند.

Manual Modes (حالت‌های دستی - اختیاری)

If you want to run specific phases manually:
اگر می‌خواهید فازها را جداگانه اجرا کنید:

Only Find Links (فقط جستجو):

python main.py --mode discovery


Only Download (فقط دانلود از لیست آماده):

python main.py --mode download


📂 Project Structure / ساختار پروژه

config.py: Settings (Keywords, threads, timeouts).

main.py: The brain of the scraper (Auto-switching logic).

scraper_report.log: Detailed logs of what happened.

download_queue.txt: The queue of found links (Auto-saved).

Scraped_Data/: Where downloaded articles are saved.

Note: Built for educational purposes. Please respect robots.txt.