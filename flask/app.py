# app.py
from flask import Flask
from flask import request
import subprocess
import atexit
import os
from apscheduler.schedulers.background import BackgroundScheduler
from update_stock_data import update_stock_data

#schduler 실행
sched = BackgroundScheduler(daemon=True)
# sched.add_job(update_stock_data,'cron', hour=7, day_of_week="mon-fri")
sched.add_job(update_stock_data,'interval', minutes=1)
sched.start()
atexit.register(sched.shutdown)

app = Flask(__name__)

@app.route('/') # 접속하는 url
def index():
    result = """
    /signin\n
    """
    return result

@app.route('/signin')
def signin():
    address = request.args.get('address', default='address', type=str)
    name = request.args.get('name', default='root', type=str)
    if address == 'address':
        return "Invalid address", 400
    elif name == 'root':
        return "Invalid name", 400
    else:
        try:
            output = subprocess.check_output(['blockchaind', 'tx', 'blockchain', 'create-user', address, name, '--from', 'root', '--log_format', 'json', '-y'], stderr=subprocess.STDOUT, universal_newlines=True)
            output_split = output.split('\n')
            raw_log = ''
            for i in range(len(output_split)):
                if output_split[i].startswith('code'):
                    code = output_split[i]
                elif output_split[i].startswith('raw_log'):
                    raw_log = output_split[i]
                elif output_split[i].startswith('  '):
                    raw_log += output_split[i]

            if code == '0': 
                return "Success signin", 200
            else:
                return raw_log, 400
        except subprocess.CalledProcessError as e:
            return output.split('\n')[0], 400

if __name__=="__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)