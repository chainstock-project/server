# pip install bs4
import requests
from bs4 import BeautifulSoup
import subprocess
from datetime import datetime
import pytz
from apscheduler.schedulers.background import BlockingScheduler

def update_stock_data():
    #kospi
    kospi_stock_codes = []
    kospi_stock_names = []
    kospi_stock_amounts = []
    req = requests.get('https://finance.naver.com/sise/sise_market_sum.naver?sosok=0')
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    end_page_alink = soup.select_one("#contentarea > div.box_type_l > table.Nnavi > tr > td.pgRR > a")
    end_page = int(end_page_alink.get('href')[41:])

    for page in range(1,end_page+1):
        req = requests.get('https://finance.naver.com/sise/sise_market_sum.naver?sosok=0&page='+str(page))
        html = req.text

        soup = BeautifulSoup(html, 'html.parser')
        stock_code_alinks = soup.select('#contentarea > div.box_type_l > table.type_2 > tbody > tr > td:nth-child(2) > a')
        for stock_code_alink in stock_code_alinks:
            kospi_stock_codes.append(stock_code_alink.get('href')[22:])

        stock_name_alinks = soup.select('#contentarea > div.box_type_l > table.type_2 > tbody > tr > td:nth-child(2) > a')
        for stock_name_alink in stock_name_alinks:
            kospi_stock_names.append(stock_name_alink.get_text())

        stock_amounts_tds = soup.select('#contentarea > div.box_type_l > table.type_2 > tbody > tr > td:nth-child(3)')
        for stock_amounts_td in stock_amounts_tds:
            kospi_stock_amounts.append(stock_amounts_td.get_text().replace(',', ""))
        print("kospi : ", "stock_code_count=", len(kospi_stock_codes), " stock_amount_count=", len(kospi_stock_amounts))

    #kosdaq
    kosdaq_stock_codes = []
    kosdaq_stock_names = []
    kosdaq_stock_amounts = []
    req = requests.get('https://finance.naver.com/sise/sise_market_sum.naver?sosok=1')
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    end_page_alink = soup.select_one("#contentarea > div.box_type_l > table.Nnavi > tr > td.pgRR > a")
    end_page = int(end_page_alink.get('href')[41:])

    for page in range(1,end_page+1):
        req = requests.get('https://finance.naver.com/sise/sise_market_sum.naver?sosok=1&page='+str(page))
        html = req.text

        soup = BeautifulSoup(html, 'html.parser')
        stock_code_alinks = soup.select('#contentarea > div.box_type_l > table.type_2 > tbody > tr > td:nth-child(2) > a')
        for stock_code_alink in stock_code_alinks:
            kosdaq_stock_codes.append(stock_code_alink.get('href')[22:])

        stock_name_alinks = soup.select('#contentarea > div.box_type_l > table.type_2 > tbody > tr > td:nth-child(2) > a')
        for stock_name_alink in stock_name_alinks:
            kosdaq_stock_names.append(stock_name_alink.get_text())

        stock_amounts_tds = soup.select('#contentarea > div.box_type_l > table.type_2 > tbody > tr > td:nth-child(3)')
        for stock_amounts_td in stock_amounts_tds:
            kosdaq_stock_amounts.append(stock_amounts_td.get_text().replace(',', ""))
        print("kosdaq : ", "stock_code_count=", len(kosdaq_stock_codes), " stock_amount_count=", len(kosdaq_stock_amounts))

    stock_date=datetime.now(tz=pytz.timezone('Asia/Seoul')). strftime("%Y-%m-%d")

    cmd = ["blockchaind", "tx", "blockchain", "create-stock-data"]

    # kospi blockchain에 업데이트
    market_type = "kospi"
    for  i in range(len(kospi_stock_codes)):
        cmd.extend([kospi_stock_codes[i], kospi_stock_names[i], market_type, kospi_stock_amounts[i], stock_date])

    # kosdaq blockchain에 업데이트
    market_type = "kosdaq"
    for  i in range(len(kosdaq_stock_codes)):
        cmd.extend([kosdaq_stock_codes[i], kosdaq_stock_names[i], market_type, kosdaq_stock_amounts[i], stock_date])

    cmd.extend(["-y", "--from", "root", "--gas=auto","--keyring-backend","test", "--chain-id", "stock-chain"])
    subprocess.call(cmd)

if __name__=="__main__":
    #schduler 실행
    update_stock_data()
    print("start scheduler")
    sched = BlockingScheduler(daemon=True, timezone="Asia/Seoul")
    sched.add_job(update_stock_data,'cron', hour=18)
    sched.start()