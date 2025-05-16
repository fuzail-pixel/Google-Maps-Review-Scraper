from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import os
import gc
import platform
from contextlib import contextmanager

app = Flask(__name__)

@contextmanager
def dummy_context():
    yield

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        place = request.json.get("place")
        reviews = scrape_reviews(place)
        return jsonify(reviews)
    return render_template("index.html")

def scrape_reviews(place):
    reviews_list = []

    is_linux = platform.system() == "Linux"
    if is_linux:
        from xvfbwrapper import Xvfb  # Import only on Linux
        display_context = Xvfb()
    else:
        display_context = dummy_context()

    with display_context:
        with sync_playwright() as p:
            # Use Firefox instead of Chromium (lower memory footprint)
            browser = p.firefox.launch(
                headless=True,
                firefox_user_prefs={
                    # Disable unnecessary features
                    "media.autoplay.default": 5,
                    "media.autoplay.blocking_policy": 2,
                    "browser.cache.disk.enable": False,
                    "browser.cache.memory.enable": False,
                    "permissions.default.image": 2,  # Block images
                    "javascript.options.mem.max": 128 * 1024 * 1024,  # Limit JS memory
                }
            )
            
            # Configure context to use less resources
            context = browser.new_context(
                viewport={"width": 800, "height": 600},  # Smaller viewport
                java_script_enabled=True,  # Keep JS enabled since we need it
                user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
            )
            
            page = context.new_page()
            
            # Intercept and block unnecessary resources
            page.route("**/*.{png,jpg,jpeg,gif,svg,pdf,mp4,webp,css,woff,woff2,ttf,otf}", lambda route: route.abort())
            page.route("**/(analytics|tracking|advertisement|ad)\\.js", lambda route: route.abort())

            try:
                if place.startswith("https://") or place.startswith("http://"):
                    url = place
                else:
                    # Go directly to search results page
                    search_url = f"https://www.google.com/maps/search/{place.replace(' ', '+')}/"
                    page.goto(search_url, timeout=30000)
                    
                    # Wait for results with reduced timeout
                    try:
                        page.wait_for_selector(".Nv2PK", timeout=15000)
                        page.locator(".Nv2PK").first.click()
                        page.wait_for_timeout(2000)  # Reduced wait time
                    except Exception as e:
                        print(f"Error finding search results: {e}")
                        # Try to proceed anyway with current page
                    
                    url = page.url

                # Navigate to main page
                page.goto(url, timeout=30000)

                # Try to open reviews
                try:
                    reviews_button = page.locator("button[aria-label*='reviews'], button[aria-label*='Reviews']").first
                    reviews_button.click()
                    page.wait_for_timeout(2000)  # Reduced wait time
                except Exception as e:
                    print(f"Error opening reviews: {e}")

                # Scroll fewer times to load some reviews
                for _ in range(5):  # Reduced from 10 to 5
                    page.mouse.wheel(0, 800)
                    page.wait_for_timeout(1000)  # Reduced wait time

                # Extract content and parse
                soup = BeautifulSoup(page.content(), "html.parser")
                review_elements = soup.select(".jftiEf")

                # Get reviews (limit to 5 instead of 10)
                for element in review_elements[:7]:
                    try:
                        author = element.select_one(".d4r55").text.strip()
                        rating = element.select_one("span[aria-label]").get("aria-label", "").strip()
                        review_text = element.select_one(".wiI7pd").text.strip()
                        reviews_list.append({
                            "author": author,
                            "rating": rating,
                            "review": review_text
                        })
                    except Exception as e:
                        print(f"Error extracting review data: {e}")

            except Exception as e:
                print(f"Error while scraping: {e}")

            finally:
                context.close()
                browser.close()
                
    # Force garbage collection
    gc.collect()
    
    return reviews_list

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)