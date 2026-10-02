# E-commerce Product Scraper

A Python web scraping project that collects product information from an e-commerce website and saves the data in both **CSV** and **Excel** formats.

## What This Project Does

The scraper collects basic product information such as:

* Product name
* Price
* Rating
* Fast shipping status
* Review count
* Product URL

It then visits each product page and collects additional details:

* SKU
* Brand name
* Colors
* Styles
* Product bullets/features
* Availability
* Description
* Technical specifications

The data from the listing pages and product detail pages is then merged using the **product URL**.

## Output

The project generates:

* `products.csv` — basic product information
* `detail.csv` — product detail information
* `final_products.csv` — merged product data
* `final_products.xlsx` — final data in Excel format

## Technologies Used

* Python
* Requests
* BeautifulSoup
* CSV
* OpenPyXL

## Features

* Scrapes multiple product pages
* Handles missing data
* Uses request timeout and retry logic
* Handles pagination
* Removes duplicate detail records through URL-based merging
* Cleans scraped text
* Exports the final dataset to CSV and Excel

## How to Run

Install the required libraries:

```bash
pip install requests beautifulsoup4 openpyxl
```

Then run:

```bash
python main.py
```

The final CSV and Excel files will be created in the project folder.

## Project Purpose



This project is part of my Python web scraping practice.
