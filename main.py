"""
A simple script that retrieve data from hugo.team site
and store them keeping its format by using bold (**) for <strong> tag, 
italics (_) for <em> tag and line breaks (\n) for <br/> tag

Jijel in 27 Jumada al Alkhir(6) 1440
         04 March 2019
By Oussama Heloulou
"""

from bs4 import BeautifulSoup
import requests
import re
import json


BASE_URL = 'https://www.hugo.team'
TEMPLATES_PAGE = 'https://www.hugo.team/meeting-note-templates'
OUTPUT = list()

def get_template_urls(templates_page):
    source = requests.get(templates_page)
    source.encoding = 'utf-8'
    soup = BeautifulSoup(source.text, 'html.parser')
    anchor_tags = soup.find_all('a', {'class': 'link-block-29'})[:21]
    template_urls = []
    for anchor in anchor_tags:
        url = BASE_URL + anchor['href']
        template_urls.append(url)
    return template_urls


def get_template_data(template_url):
    source = requests.get(template_url)
    source.encoding = 'utf-8'
    soup = BeautifulSoup(source.text, 'html.parser')
    title = soup.find('div', {'class': 'div-block-594'}).text
    title = re.sub(r'(Template)', r" \1", title, re.MULTILINE).strip().replace("  ", " ")
    description = soup.find('h2', {'class': 'heading-40'}).text
    text_block = soup.find('div', {'class': 'rich-text-block-9'})
    text = ''
    for element in text_block:
        sub_elements = element.findChildren()
        for sub_element in sub_elements:
            text += format_tag_text(sub_element)
    
    return {'title': title, 'description': description, 'text': text}


def format_tag_text(tag):
    if tag.name == 'br':
        return '\n'
    elif tag.name == 'em':
        return f'_{tag.text}_'
    elif tag.name == 'strong':
        return f'**{tag.text}**'
    else:
        return ''


template_urls = get_template_urls(TEMPLATES_PAGE)

for template in template_urls:
    print(template)
    template_data = get_template_data(template)
    OUTPUT.append(template_data)

# print(OUTPUT)
with open('output.json', 'w', encoding='utf-8') as output_file:
    json.dump(OUTPUT, output_file, ensure_ascii=False, indent=4)
