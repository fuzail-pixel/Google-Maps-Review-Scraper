# Google-Maps-Review-Scraper

A full stack web application for scraping Google Maps reviews based on business links or place names, with a responsive dashboard.

## 📖 Overview

This project allows users to extract reviews from Google Maps for any business or place. It supports both direct Google Maps URLs and plain place names, providing an easy way to gather valuable customer feedback for analysis, marketing, or competitive research.

## ✨ Features

* Scrape reviews using either place names or Google Maps links.
* Extracts author names, ratings, and review texts.
* Simple, clean, and responsive web interface.
* Supports pagination and dynamic loading for extensive reviews.
* Error handling and timeouts for reliability.

## 🛠️ Technologies Used

* **Backend:** Flask, Playwright (Python)
* **Frontend:** HTML, CSS, JavaScript (Fetch API)
* **Parsing:** BeautifulSoup (Python)

## 🚀 Getting Started

### Prerequisites

Make sure you have the following installed:

* Python 3.9+
* Google Chrome or Chromium browser

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/fuzail-pixel/Google-Maps-Review-Scraper.git
   cd Google-Maps-Review-Scraper
   ```

2. **Create a Virtual Environment (Optional but Recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows, use: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright Browsers**

   ```bash
   playwright install
   ```

### Running the Application

Start the Flask server:

```bash
flask run
```

By default, the server runs on `http://localhost:5000`.

### Usage

* Open `http://localhost:5000` in your browser.
* Enter a place name or Google Maps link to start scraping.
* Reviews will be displayed on the page once extracted.

## 🤝 Contributing

Contributions are welcome! Feel free to fork this repo, create a new branch, and submit a pull request.

## 📄 License

This project is licensed under the GPL-3.0 License.

## 📧 Contact

Feel free to reach out on [LinkedIn](https://linkedin.com/in/fuzail-rehman-31a755241/) or [GitHub](https://github.com/fuzail-pixel) if you have any questions or feedback.

---

Thanks for using the Google-Maps-Review-Scraper! 😊
