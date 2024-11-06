from urllib.request import urlopen
import re
import json
from bs4 import BeautifulSoup
import psycopg2
from config import load_config
import requests
import os
import logging


log_dir = '/var/log/pythonScripts'
log_file = 'spellingbee.log'
log_path = os.path.join(log_dir, log_file)

# Ensure the log directory exists
if not os.path.exists(log_dir):
    os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    filename=log_path,
    level=logging.INFO,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',
)

slack_webhook_url = 'https://hooks.slack.com/services/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'

def main(): 
    game_data = get_html_content()  # Should be JSON-compatible structure or string
    if game_data is None:
        raise ValueError("No data returned from get_html_content().")

    if isinstance(game_data, str):
        game_data = json.loads(game_data)
    
    letters = game_data["today"]["validLetters"]
    answers = game_data['today']['answers']
    weekday = game_data['today']['displayWeekday']
    date = game_data['today']['displayDate']
    pangrams = game_data['today']['pangrams']
    centerletter = game_data['today']['centerLetter']
    sql = """INSERT INTO spellingbee (letters, answers, pangrams, weekday, date)
             VALUES(%s,%s,%s,%s,%s)"""
    config = load_config()
    try:
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:
                # execute the INSERT statement
                cur.execute(sql, (letters, answers, pangrams, weekday, date))
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
        """Send a Slack notification when IP changes."""
    payload = {
        "text": f"""It's {weekday} on the {date}. You know what that means! 
                    The Letters today are: {letters} with the Center Letter being {centerletter}
                    This make the Pangrams: {pangrams}
                    and the Words: {answers}"""
     }      
    try:
        response = requests.post(slack_webhook_url, json=payload, headers={'Content-Type': 'application/json'})
        if response.status_code == 200 :
            print("Notification sent successfully.")
            logging.info('Notification sent successfully.')
        else:
            print(f"Failed to send notification. Status code: {response.status_code}, Response: {response.text}")
            logging.error(f"Failed to send notification. Status code: {response.status_code}, Response: {response.text}")
    except requests.RequestException as e:
        print(f"Error sending notification: {e}")
        logging.error(f"Error sending notification: {e}")



def get_html_content():
    url = "https://www.nytimes.com/puzzles/spelling-bee"
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, 'html.parser')
    script_content = str(soup.find("script", string=re.compile(r"window\.gameData")))
    match = re.search(r'window\.gameData\s*=\s*({.*})', script_content, re.DOTALL)
    if match:
        game_data_json = match.group(1)  # Extract JSON part
        try:
            # Parse JSON data into a Python dictionary
            game_data = json.loads(game_data_json)
            letters = game_data["today"]["validLetters"]
            answers = game_data['today']['answers']
            weekday = game_data['today']['displayWeekday']
            date = game_data['today']['displayDate']
            pangrams = game_data['today']['pangrams']
            
            return game_data
        except json.JSONDecodeError:
            print("Error decoding JSON.")
    else:
        print("Could not find gameData JSON in the script tag.")

    print("Another day, another Spelling Bee. Here's the results")

main()