import requests
from bs4 import BeautifulSoup
import uuid
from html_to_markdown import convert
import pypandoc
import os
import shutil
import urllib.parse
from pypandoc.pandoc_download import download_pandoc

# download_pandoc()

class ScrapeEbanglaLibrary:
    def __init__(self, url):
        self.url = url
        self.user_id = str(uuid.uuid4())
        self.create_user_folder()
        self.fetch_list_html()
        self.title = ""
        self.author = "Unknown Author"
        self.pdf_urls = {}

    def fetch_list_html(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')

        book_name = soup.find('a', id="ld-focus-mode-course-heading").text.strip()
        split = book_name.split("–")
        self.title = split[0].strip()
        self.author = split[-1].strip()
        return soup

    def fetch_pdf_urls(self):
        soup = self.fetch_list_html()
        pdf_urls = {}
        link_items = soup.find_all("div", class_="ld-lesson-item")
        for link_item in link_items:
            link = link_item.find("a", class_="ld-lesson-item-preview-heading")
            title = link.find("div", class_="ld-lesson-title").text
            pdf_urls[title.strip()] = link.get("href")
        self.pdf_urls = pdf_urls
    
    def fetch_pdf_content(self, title, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.find("div", class_="ld-tabs-content")
        with open(self.file_name(title), "w") as f:
            f.write(convert(str(content)))
        # print(f"Saved {title} as md file")
    
    def file_name(self, name):
        return "md/" + self.user_id + "/" + name + ".md"

    def create_user_folder(self):
        if not os.path.exists(f"md/{self.user_id}"):
            os.makedirs(f"md/{self.user_id}")
        if not os.path.exists(f"epub/{self.user_id}"):
            os.makedirs(f"epub/{self.user_id}")

    def md_to_epub(self):
        for title, url in self.pdf_urls.items():
            self.fetch_pdf_content(title, url)
        
        input_files = list(map(self.file_name, self.pdf_urls.keys()))

        try:
            output = pypandoc.convert_file(
                input_files,
                to='epub',
                outputfile=f"epub/{self.user_id}/{self.title}.epub",
                extra_args=[
                    '--metadata', f'title={self.title}', 
                    '--metadata', f'author={self.author}', 
                    '--toc'
                ],
                sort_files=False
            )
            assert output == ''
            # print(f"Successfully converted to {self.title}.epub")
        except Exception as e:
            print(f"Failed to convert to {self.title}.epub")
            print(e)
            raise

    def clean_up(self):
        if os.path.exists(f"md/{self.user_id}"):
            shutil.rmtree(f"md/{self.user_id}")

    def get_epub_path(self):
        """Returns the path to the generated epub file"""
        epub_dir = f"epub/{self.user_id}"
        epub_filename = f"{self.title}.epub"
        epub_path = f"{epub_dir}/{epub_filename}"
        return epub_path

    def download_epub(self):
        epub_path = self.get_epub_path()
        download_link = urllib.parse.quote(epub_path)
        # print(f"Download your epub file here: {download_link}")
        return download_link
