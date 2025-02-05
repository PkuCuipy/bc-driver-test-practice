# BC Driver Test Practice App

A simple web application for practicing BC driver's license test questions. Questions are scraped from unofficial practice test website and presented in an easy-to-use, ads-free interface.

## Link

https://pkucuipy.github.io/bc-driver-test-practice/

## Usage

- Use mouse or arrow keys (← →) to navigate between questions
- Click on an answer to check if it's correct
- Press 'S' or click the screenshot button to save the current question


## Features

- 362 practice questions with images
- Instant feedback on answers
- Keyboard navigation (← →)
- Screenshot capture functionality (button or 'S' key)
- No server required - runs entirely in browser


## File Structure

- `data-scraper.py` - Python script to download questions and images
- `index.html` - Main application
- `html2canvas.min.js` - Library for screenshot functionality
- `questions.json` - Scraped question data
- `images/` - Scraped question images

## License

MIT

## Disclaimer

This is an unofficial practice tool. Questions are sourced from publicly available practice tests. For official test preparation, please refer to [ICBC's website](https://www.icbc.com).