# WebRecon 🚀

WebRecon is a Python-based web reconnaissance tool designed to assist during the initial information-gathering phase of web application security testing.

The tool collects publicly accessible information from target web applications and provides visibility into common security-relevant elements such as HTTP headers, HTML forms, hidden parameters, links, exposed email addresses, and robots.txt files.

## Features

* Status Code Detection
* Server Header Identification
* Security Header Analysis

  * Content-Security-Policy (CSP)
  * Strict-Transport-Security (HSTS)
  * X-Frame-Options
  * X-Content-Type-Options
* HTML Form Discovery and Analysis
* Hidden Input Extraction
* Email Discovery using Regular Expressions
* Internal and External Link Enumeration
* robots.txt Detection
* Command-Line Interface using argparse

## Technologies Used

* Python
* Requests
* BeautifulSoup
* Regular Expressions
* argparse

## Installation

pip install -r requirements.txt

## Usage

python webrecon.py -u https://example.com

## Future Improvements

* JavaScript File Discovery
* Technology Fingerprinting
* JSON Report Generation
* Sitemap.xml Analysis
* Endpoint Extraction
* Robots.txt analysis module


## Disclaimer

This tool is intended for educational purposes and authorized security testing only.
