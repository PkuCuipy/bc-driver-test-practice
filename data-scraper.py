import requests
from bs4 import BeautifulSoup
import json
import time
import os
from urllib.parse import urljoin

class BCDriverTestScraper:
    def __init__(self, base_url="https://bc.driver-test.com/exam/"):
        self.base_url = base_url
        self.session = requests.Session()
        self.questions = []

    def get_question_page(self, question_number):
        url = f"{self.base_url}{question_number}"
        response = self.session.get(url)
        if response.status_code != 200:
            print(f"Failed to get question {question_number}: {response.status_code}")
            return None
        return response.text

    def extract_image_url(self, soup):
        img_tag = soup.find('img', {'class': 'img-fluid'})
        if img_tag and 'src' in img_tag.attrs:
            return urljoin("https://bc.driver-test.com", img_tag['src'])
        return None

    def download_image(self, image_url, question_number):
        if not image_url:
            return None
        
        # Create images directory if it doesn't exist
        os.makedirs('images', exist_ok=True)
        
        # Extract file extension from URL
        ext = image_url.split('.')[-1]
        filename = f"images/question_{question_number}.{ext}"
        
        response = self.session.get(image_url)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                f.write(response.content)
            return filename
        return None

    def parse_question(self, html_content, question_number):
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Get question title
        question_title = soup.find('h5', {'class': 'card-title'})
        if not question_title:
            return None
            
        # Get correct answer from Vue.js data
        script_tags = soup.find_all('script')
        correct_answer = None
        for script in script_tags:
            if script.string and 'const answer =' in script.string:
                correct_answer = script.string.split('const answer =')[1].split(';')[0].strip().strip('"')
                break
                
        # Get choices
        choices = []
        choice_items = soup.find_all('li', {'class': 'list-group-item'})
        for item in choice_items:
            input_tag = item.find('input')
            if input_tag and 'value' in input_tag.attrs:
                choices.append(input_tag['value'])

        # Get image URL and download it
        image_url = self.extract_image_url(soup)
        image_path = self.download_image(image_url, question_number) if image_url else None

        return {
            'id': question_number,
            'question': question_title.text.strip(),
            'choices': choices,
            'correct_answer': correct_answer,
            'image_path': image_path,
            'image_url': image_url
        }

    def scrape_questions(self, start=1, end=362):
        for i in range(start, end + 1):
            print(f"Scraping question {i}...")
            html_content = self.get_question_page(i)
            if html_content:
                question_data = self.parse_question(html_content, i)
                if question_data:
                    self.questions.append(question_data)
            time.sleep(1)  # Be nice to the server

    def save_to_json(self, filename='bc_driver_test_questions.json'):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                'questions': self.questions,
                'total_questions': len(self.questions),
                'scraped_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }, f, ensure_ascii=False, indent=2)

def main():
    scraper = BCDriverTestScraper()
    scraper.scrape_questions()
    scraper.save_to_json()

if __name__ == "__main__":
    main()
