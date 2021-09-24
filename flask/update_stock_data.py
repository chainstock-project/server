# pip install bs4
import requests
from bs4 import BeautifulSoup
import subprocess
from datetime import datetime

def update_stock_data():
    #kospi
    kospi_stock_codes = []
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

        stock_amounts_tds = soup.select('#contentarea > div.box_type_l > table.type_2 > tbody > tr > td:nth-child(3)')
        for stock_amounts_td in stock_amounts_tds:
            kospi_stock_amounts.append(stock_amounts_td.get_text().replace(',', ""))

        print("kospi : ", "stock_code_count=", len(kospi_stock_codes), " stock_amount_count=", len(kospi_stock_amounts))

    #kosdaq
    kosdaq_stock_codes = []
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

        stock_amounts_tds = soup.select('#contentarea > div.box_type_l > table.type_2 > tbody > tr > td:nth-child(3)')
        for stock_amounts_td in stock_amounts_tds:
            kosdaq_stock_amounts.append(stock_amounts_td.get_text().replace(',', ""))

        print("kosdaq : ", "stock_code_count=", len(kosdaq_stock_codes), " stock_amount_count=", len(kosdaq_stock_amounts))

    # kospi blockchain에 업데이트
    date=datetime.today().strftime("%Y-%m-%d")
    stock_type = "kospi"
    cmd = ["blockchaind", "tx", "blockchain", "create-stock-data", date]
    for  i in range(len(kospi_stock_codes)):
        cmd.extend([stock_type, kospi_stock_codes[i], kospi_stock_amounts[i]])
    # kosdaq blockchain에 업데이트
    stock_type = "kosdaq"
    for  i in range(len(kosdaq_stock_codes)):
        cmd.extend([stock_type, kospi_stock_codes[i], kospi_stock_amounts[i]])
    cmd.extend(["--from", "root", "-y", "--gas=auto"])
    subprocess.call(cmd)

if __name__=="__main__":
    update_stock_data()