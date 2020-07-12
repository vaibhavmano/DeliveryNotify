import requests
from bs4 import BeautifulSoup
import time
import os
import sys

CHAT_ID = os.environ['chat_id']
BOT_TOKEN_ID = os.environ['bot_token_id']
TRACKING_ID = os.environ['tracking_id']

def notify_systemos(message, title='iPhone SE2020'):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(message, title))



def notify_bot(message):    
    bot_url = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'
    response = requests.post(bot_url.format(BOT_TOKEN_ID, CHAT_ID, message))
    if response.status_code == 200:
        print('OK')

if __name__ == "__main__":
    """
    Code is designed to run for every 3 hours. It will check for the last updated status
    in ekart Logistics and send a push notification to your system and to your telegram chat
    """

    tracking_id = TRACKING_ID
    sleep_time = 3*60*60
    try:
        sleep_time = int(sys.argv[1])
    except:
        print('No time passed as param\nDefault time of 3 hours will be used.')
    print(sleep_time)
    while True:
        get_response = requests.get('https://ekartlogistics.com/track/{}/'.format(tracking_id))
        soup = BeautifulSoup(get_response.content, 'html.parser')
        system_message = soup.td.text
        table = soup.find_all('tr')
        message = table[3].text
        message = 'Last updated status: \n' + message
        notify_bot(message)
        try:
            notify_systemos(system_message)
        except:
            print('Does not support your OS')
        break
        time.sleep(3*60*60)


