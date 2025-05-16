from flask import Flask, render_template, request, jsonify
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        place = request.json.get("place")
        reviews = scrape_reviews(place)
        return jsonify(reviews)
    return render_template("index.html")

def scrape_reviews(place):
    reviews_list = []

    # Start the Playwright browser
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            # Detect if it's a short URL or a place name
            if place.startswith("https://") or place.startswith("http://"):
                url = place
            else:
                # Perform a search if it's a plain place name
                search_url = f"https://www.google.com/maps/search/{place.replace(' ', '+')}/"
                page.goto(search_url, timeout=60000)

                # Wait for the search results to load
                page.wait_for_selector(".Nv2PK", timeout=30000)

                # Click on the first result if available
                page.locator(".Nv2PK").first.click()
                page.wait_for_timeout(5000)

                # Extract the actual place URL
                url = page.url

            # Navigate to the place URL
            page.goto(url, timeout=60000)

            # Open the reviews section if not already open
            try:
                reviews_button = page.locator("button[aria-label*='reviews'], button[aria-label*='Reviews']").first
                reviews_button.click()
                page.wait_for_timeout(5000)
            except Exception as e:
                print(f"Error opening reviews: {e}")

            # Scroll to load more reviews
            for _ in range(10):
                page.mouse.wheel(0, 1000)
                page.wait_for_timeout(2000)

            # Get the HTML and parse with BeautifulSoup
            soup = BeautifulSoup(page.content(), "html.parser")
            review_elements = soup.select(".jftiEf")

            for element in review_elements[:10]:  # Limit to 10 reviews
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

            if not reviews_list:
                print("No reviews found. Selector might be incorrect or page not fully loaded.")

        except Exception as e:
            print(f"Error while scraping: {e}")

        finally:
            browser.close()

    return reviews_list


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Render's PORT or default to 5000 for local
    app.run(host="0.0.0.0", port=port, debug=True)