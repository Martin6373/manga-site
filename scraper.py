import cloudscraper
from bs4 import BeautifulSoup
import json
import os

def scrape():
    # تجاوز حماية الموقع لمحاكاة متصفح حقيقي
    scraper = cloudscraper.create_scraper(browser={'browser': 'chrome','platform': 'windows','mobile': False})
    url = "https://mangalek.com"
    
    try:
        print("جاري سحب المانجا... انتظر قليلاً")
        res = scraper.get(url, timeout=30)
        soup = BeautifulSoup(res.text, "html.parser")
        manga_list = []

        # اختيار عناصر المانجا من الصفحة الرئيسية
        items = soup.select('.page-item-detail, .manga-item')[:24]

        for item in items:
            title_el = item.select_one('h3 a') or item.select_one('h3')
            img_el = item.select_one('img')
            
            if title_el and img_el:
                m_title = title_el.get_text(strip=True)
                m_url = title_el.find('a')['href'] if title_el.find('a') else "#"
                m_img = img_el.get('data-src') or img_el.get('src') or ""
                if m_img.startswith('//'): m_img = "https:" + m_img

                # هيكلة البيانات لتناسب ملف الـ HTML
                manga_list.append({
                    "title": m_title,
                    "img": m_img,
                    "url": m_url
                })

        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(manga_list, f, ensure_ascii=False, indent=2)
        
        print("✅ تم بنجاح! تم إنشاء ملف data.json")

    except Exception as e:
        print(f"❌ خطأ: {e}")

if __name__ == "__main__":
    scrape()
