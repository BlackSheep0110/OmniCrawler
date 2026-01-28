import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import time
import re
import config
from utils import Logger

class Crawler:
    def __init__(self, logger=None):
        self.logger = logger if logger else Logger()

    def is_domain_relevant(self, base_url):
        try:
            domain = urlparse(base_url).netloc
        except:
            return False
            
        if not domain:
            return False

        for black in config.BLACKLISTED_DOMAINS:
            if black in domain:
                self.logger.log(f"Domain blacklisted: {domain}", "SKIP")
                return False

        if not config.STRICT_MODE:
            self.logger.log(f"Domain accepted (Strict Mode OFF): {domain}", "SUCCESS")
            return True

        try:
            response = requests.get(base_url, headers=config.HEADERS, timeout=config.TIMEOUT)
            if response.status_code != 200:
                return False
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            site_title = soup.title.string if soup.title else ""
            meta_desc = ""
            desc_tag = soup.find('meta', attrs={'name': 'description'})
            if desc_tag:
                meta_desc = desc_tag.get('content', '')
            
            check_text = (site_title + " " + meta_desc).lower()
            keywords_lower = [k.lower() for k in config.TARGET_KEYWORDS]
            
            is_relevant = any(k in check_text for k in keywords_lower)
            
            if is_relevant:
                self.logger.log(f"Target found: {site_title.strip()[:40]}...", "SUCCESS")
                return True
            else:
                self.logger.log(f"Irrelevant content: {domain}", "SKIP")
                return False
        except Exception as e:
            return False

    def is_likely_article(self, url, domain):
        if domain not in url:
            return False
        if len(url) < 30: 
            return False
        
        exclude = [
            'wp-admin', 'login', 'register', 'cart', 'checkout', 'contact', 'about', 
            'feed', 'comment', 'tag', 'search', 'page', 'xml', 'jpg', 'png', 
            'pdf', 'zip', 'privacy-policy', 'terms'
        ]
        
        url_lower = url.lower()
        if any(ex in url_lower for ex in exclude):
            return False
        return True

    def find_next_page(self, soup, current_url):
        next_btn = soup.find('a', attrs={'rel': 'next'})
        if not next_btn:
            next_btn = soup.find('a', class_=re.compile(r'(next|forward|pagination-next|page-link)', re.I))
        if not next_btn:
            next_btn = soup.find('a', string=re.compile(r'(بعدی|Next|Old|Older|»|›)', re.I))
            
        if next_btn and next_btn.has_attr('href'):
            next_link = urljoin(current_url, next_btn['href'])
            if next_link != current_url:
                return next_link
        return None

    def crawl_hub_pages(self, start_url, domain):
        collected = set()
        current_url = start_url
        page = 1
        
        while current_url and page <= config.MAX_HUB_PAGES:
            try:
                response = requests.get(current_url, headers=config.HEADERS, timeout=10)
                if response.status_code != 200:
                    break
                
                soup = BeautifulSoup(response.text, 'html.parser')
                found = 0
                for a in soup.find_all('a', href=True):
                    full = urljoin(current_url, a['href'])
                    if self.is_likely_article(full, domain) and full not in collected:
                        collected.add(full)
                        found += 1
                
                if found == 0:
                    break
                
                next_page = self.find_next_page(soup, current_url)
                if next_page and next_page != current_url:
                    current_url = next_page
                    page += 1
                    time.sleep(1)
                else:
                    break
            except:
                break
        return collected

    def parse_sitemap(self, sitemap_url, depth=0):
        """Recursively extracts links from sitemaps and sitemap indices."""
        links = set()
        if depth > 2: # Prevent infinite recursion
            return links

        try:
            res = requests.get(sitemap_url, headers=config.HEADERS, timeout=10)
            if res.status_code != 200:
                return links
            
            # Check if content is XML
            if 'xml' in res.headers.get('Content-Type', '') or res.text.strip().startswith('<?xml'):
                soup = BeautifulSoup(res.content, 'xml')
                locs = soup.find_all('loc')
                
                for loc in locs:
                    url = loc.text.strip()
                    # If the link is another sitemap (ends in .xml), recurse into it
                    if url.endswith('.xml') or 'sitemap' in url.lower():
                        # self.logger.log(f"Entering sub-sitemap: {url}", "DEBUG")
                        sub_links = self.parse_sitemap(url, depth + 1)
                        links.update(sub_links)
                    else:
                        links.add(url)
        except Exception as e:
            pass
            
        return links

    def get_site_articles(self, base_url):
        domain = urlparse(base_url).netloc
        protocol = urlparse(base_url).scheme
        found_links = set()
        sitemap_found = False
        
        # Check standard Sitemaps
        for sm in ['sitemap.xml', 'sitemap_index.xml', 'post-sitemap.xml', 'article-sitemap.xml', 'news-sitemap.xml']:
            try:
                sm_url = f"{protocol}://{domain}/{sm}"
                # Use HEAD request first to check existence? No, just GET safely inside parse_sitemap
                
                # We try to parse the sitemap
                links = self.parse_sitemap(sm_url)
                
                if links:
                    self.logger.log(f"Sitemap parsed: {sm_url} ({len(links)} actual links)", "SITEMAP")
                    sitemap_found = True
                    found_links.update(links)
                    break # Stop if we found a valid main sitemap
            except:
                continue
            
        if not sitemap_found or len(found_links) < 5:
            if not sitemap_found:
                self.logger.log(f"No sitemap, switching to deep crawl: {domain}", "CRAWL")
            
            potential_hubs = set()
            paths = [
                '/blog', '/articles', '/news', '/mag', '/magazine', 
                '/category/blog', '/archive', '/latest', '/posts'
            ]
            for path in paths:
                potential_hubs.add(urljoin(base_url, path))
            
            hubs = list(potential_hubs)[:15]
            for hub in hubs:
                found_links.update(self.crawl_hub_pages(hub, domain))
            
        return list(found_links)