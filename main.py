import time
import requests
import ast
import telegram_send
from datetime import datetime


def checkwebpage() -> bool:
    unixtime = round(time.time() * 1000)
    url = f'https://holidays.butlins.com/sw/js/bme.json?timestamp={unixtime}'
    response = requests.get(url)
    if response.status_code==200:
        dtpicker = ast.literal_eval(response.text)
        if dtpicker['REACT_APP_LATEST_ARRIVAL_DATE'] != '2021-06-18':
            return True
        else:
            return False


def send_telegram() -> None:
    message = 'The 21st June is available on the Butlins Plan My Day WebApp'
    telegram_send.send(messages=[message])


def main():
    tw1_available = False
    sleep_timer = 5

    while True:
        print(f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}: Checking whether date is available... ', end='')
        if tw1_available == False:
            if checkwebpage():
                sleep_timer = 1
                tw1_available = True
        if tw1_available:
            send_telegram()
            print('IT IS! Sending Telegram message!')
        else:
            print('Not yet.')
        time.sleep(sleep_timer*60)

if __name__ == '__main__':
    main()


