import requests
from requests_html import HTML
import time
import pandas as pd

#base_url = 'https://stackoverflow.com/questions/tagged/'
#tag = "python"
#query_filter = "Votes"
#url = f"{base_url}{tag}?tab={query_filter}"

def extract(url):
    r = requests.get(url)
    if r.status_code not in range(200, 299):
        return []
    html_str = r.text
    html = HTML(html=html_str)
    question_summaries = html.find(".question-summary")
    
    return question_summaries

#question_summaries = extract(url)
#print(question_summaries)
#print(question_summaries[0].text)

#columns = ['votes', 'vote_title', 'num_answers', 'views', 'question', 'short_desc', 'tags', 'date', 'user', 'user_details']
#this_row = list(question_summaries[0].text.split("\n"))
#print(this_row)
#for column, row_v in zip(columns, this_row):
#    print(column, row_v)

#classes_needed = ['.question-hyperlink', '.vote', '.tags']
#this_question_element = question_summaries[0]
#this_question_element.find('.question-hyperlink', first=True).text
#this_question_element.find('.vote', first=True).text.replace('\nvotes', '')

def clean_scraped_data(text, keyname=None):
    if keyname == 'votes':
        return text.replace('\nvotes', '')
    return text

def parse_tagged_page(question_summaries):
    #question_summaries = extract(url)
    key_names = ['question', 'votes', 'tags']
    classes_needed = ['.question-hyperlink', '.vote', '.tags']
    datas = []
    for q_el in question_summaries:
        question_data = {}
        for i, _class in enumerate(classes_needed):
            sub_el = q_el.find(_class, first=True)
            keyname = key_names[i]
            question_data[keyname] = clean_scraped_data(sub_el.text, keyname=keyname)
        datas.append(question_data)
    return datas

def extract_data_from_url(url):
    question_summaries = extract(url)
    datas = parse_tagged_page(question_summaries)

    return datas

#print(extract_data_from_url(url))

def scrape_tag(tag = "python", query_filter = "Votes", max_pages=50, pagesize=25):
    base_url = 'https://stackoverflow.com/questions/tagged/'
    datas = []
    for p in range(max_pages):
        page_num = p + 1
        url = f"{base_url}{tag}?tab={query_filter}&page={page_num}&pagesize={pagesize}"
        datas += extract_data_from_url(url)
        time.sleep(1.2)

    return datas

datas = scrape_tag(tag='python')
#print(len(datas))
df = pd.DataFrame(datas)
df.to_csv("python.csv", index=False)