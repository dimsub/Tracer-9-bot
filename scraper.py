import os
import requests

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Yad2 API endpoint for motorcycles
URL = "https://yad2.co.il"
HEADERS = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15"}

def check_marketplace():
    try:
        response = requests.get(URL, headers=HEADERS, timeout=10)
        data = response.json()
        listings = data.get("data", {}).get("feed", {}).get("feed_items", [])
        
        for item in listings:
            price = item.get("price", 0)
            # Filter budget: 25,000 to 35,000 ILS
            if 25000 <= price <= 35000:
                year = item.get("year", "N/A")
                hand = item.get("hand", "N/A")
                km = item.get("kilometers", "N/A")
                item_id = item.get("id", "")
                link = f"https://yad2.co.il{item_id}"
                
                msg = f"🏍️ *Tracer Found!*\n💰 Price: {price:,} ILS\n📅 Year: {year} | Hand: {hand}\n📍 KM: {km:,}\n🌐 [View Listing]({link})"
                
                # Send to Telegram
                tel_url = f"https://telegram.org{TELEGRAM_TOKEN}/sendMessage"
                requests.post(tel_url, json={"chat_id": TELEGRAM_CHAT_ID, "text": msg, "parse_mode": "Markdown"})
    except Exception as e:
        print(f"Error checking site: {e}")

if __name__ == "__main__":
    check_marketplace()
