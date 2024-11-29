import requests
from bs4 import BeautifulSoup
from mongodb_integration import MongoDBHandler

class NailibScraper:
    def __init__(self):
        self.base_url = 'https://nailib.com'
        self.mongo_handler = MongoDBHandler()

    def scrape(self):
        response = requests.get(f"{self.base_url}/math-ai-sl-ia-samples")
        soup = BeautifulSoup(response.text, 'html.parser')
        
        samples = soup.find_all('div', class_='sample-class')  # Adjust class name as needed
        
        for sample in samples:
            data = self.extract_data(sample)
            self.mongo_handler.upsert_data(data)

    def extract_data(self, sample):
        title = sample.find('h2').text.strip()
        subject = "Math AI SL"
        description = sample.find('p', class_='description').text.strip()
        
        sections = {
            "Introduction Guidance": "",
            "Mathematical Information usage": "",
            "Mathematical Processes applied": "",
            "Interpretation of Findings": "",
            "Validity and Limitations": "",
            "Academic Honesty guidelines": ""
        }
        
        # Extract section data as needed
        # Example: sections["Introduction Guidance"] = sample.find(...).text.strip()

        word_count = len(description.split())
        read_time = f"{word_count // 200} mins"

        file_link = sample.find('a', class_='download-link')['href'] if sample.find('a', class_='download-link') else None
        
        return {
            "title": title,
            "subject": subject,
            "description": description,
            "sections": sections,
            "word_count": word_count,
            "read_time": read_time,
            "file_link": file_link,
            "publication_date": None  # Adjust as necessary
        }

if __name__ == "__main__":
    scraper = NailibScraper()
    scraper.scrape()