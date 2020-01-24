# from bs4 import BeautifulSoup as bs
import requests as r
import json
import datetime as dt
import re
parse_template = re.compile('(currentGames)(.)*')

## Function to scrape questions and answers from HQBuff.com
## date parameter must be a string formatted as "YYYY-MM-DD"
def scrape_qas(date):
    try:
        url = f"https://hqbuff.com/us/game/{date}/2"
        headers = {
            'User-Agent': "PostmanRuntime/7.20.1",
            'Accept': "*/*",
            'Cache-Control': "no-cache",
            'Host': "hqbuff.com",
            'Accept-Encoding': "gzip, deflate",
            'Connection': "keep-alive",
            'cache-control': "no-cache"
            }
        response = r.request("GET", url, headers=headers)
        # print(response.text)
        stringified_json = parse_template.search(response.text).group()[15:-1]
        parsed_object = json.loads(stringified_json)
        return parsed_object
    except Exception as e:
        print(f"Error scraping and parsing answer \n{e}")
        return

def save_to_file(date, data):
    with open(f'./scraped/{date}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def scrape(start_date, periods):
    start = dt.datetime.strptime(start_date, "%Y-%m-%d")
    dates = []
    for i in range(periods):
        dates += [(start + dt.timedelta(days=i)).strftime("%Y-%m-%d")]
    
    agg_question_data = []
    for date in dates:
        print(f"Scraping {date}...")
        question_data = scrape_qas(date)
        if (question_data):
            save_to_file(date, question_data)
            agg_question_data += question_data
        else:
            print("No data to add")
    return agg_question_data

print(scrape("2019-01-01", 365))
