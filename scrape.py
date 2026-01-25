import requests
from bs4 import BeautifulSoup
from html_to_markdown import convert
import pypandoc
from pypandoc.pandoc_download import download_pandoc

download_pandoc()

def fetch_html(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    with open("html/response.html", "w") as f:
        f.write(str(soup))
    print(f"Saved {url}")

url = 'https://www.ebanglalibrary.com/lessons/%e0%a6%85%e0%a7%8d%e0%a6%af%e0%a6%be-%e0%a6%95%e0%a6%bf%e0%a6%a1%e0%a6%a8%e0%a7%8d%e0%a6%af%e0%a6%be%e0%a6%aa%e0%a6%bf%e0%a6%82-%e0%a7%a7/'
# fetch_html(url)

def fetch_pdf_urls():
    soup = BeautifulSoup(open("html/response.html"), 'html.parser')
    pdf_urls = {}

    link_items = soup.find_all("div", class_="ld-lesson-item")
    for link_item in link_items:
        link = link_item.find("a", class_="ld-lesson-item-preview-heading")
        title = link.find("div", class_="ld-lesson-title").text
        pdf_urls[title.strip()] = link.get("href")
    return pdf_urls

def fetch_pdf_content( title, url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    content = soup.find("div", class_="ld-tabs-content")
    with open(f"md/{title}.md", "w") as f:
        f.write(convert(str(content)))
    print(f"Saved {title}")

pdf_urls = fetch_pdf_urls()
# # print(pdf_urls.)
# url = 'https://www.ebanglalibrary.com/lessons/%e0%a6%85%e0%a7%8d%e0%a6%af%e0%a6%be-%e0%a6%95%e0%a6%bf%e0%a6%a1%e0%a6%a8%e0%a7%8d%e0%a6%af%e0%a6%be%e0%a6%aa%e0%a6%bf%e0%a6%82-%e0%a7%a7/'

# # fetch_pdf_content('টেস্ট', url)
# for title, url in pdf_urls.items():
#     fetch_pdf_content(title, url)


def file_name(name):
    return "md/" + name + ".md"

def md_to_epub():
    input_files = list( map( file_name, pdf_urls.keys() ) )
    output = pypandoc.convert_file(
        input_files,
        to='epub',
        outputfile="অ্যা কিডন্যাপিং.epub",
        extra_args=['--metadata', 'title="অ্যা কিডন্যাপিং"', '--toc'], # Example of adding metadata and TOC,
        sort_files=False
    )
    print(f"Successfully converted to অ্যা কিডন্যাপিং.epub")

md_to_epub()