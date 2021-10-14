# app.py
from flask import Flask
from flask import request
import subprocess
import os
from apscheduler.schedulers.background import BackgroundScheduler
from update_stock_data import update_stock_data

#schduler 실행
sched = BackgroundScheduler(daemon=True, timezone="Asia/Seoul")
sched.add_job(update_stock_data,'cron', hour=18,minute=5, day_of_week="mon-fri")
sched.start()

app = Flask(__name__)
@app.route('/') # 접속하는 url
def index():
    result = """
    /register\n
    """
    return result 

@app.route('/register')
def signin():
    address = request.args.get('address', default='address', type=str)
    name = request.args.get('name', default='root', type=str)
    if address == 'address':
        return "Invalid address", 400
    elif name == 'root':
        return "Invalid name", 400
    else:
        subprocess.call(['blockchaind', 'tx', 'blockchain', 'create-user', address, name, '--from', 'root', '--chain-id', 'stock-chain', '--keyring-backend', 'test', '-y'], stderr=subprocess.STDOUT, universal_newlines=True)
        return "Run transaction", 200

if __name__=="__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)