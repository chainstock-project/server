# app.py
from flask import Flask, render_template
from flask import request
import time
import subprocess
from datetime import datetime


#Flask 객체 인스턴스 생성
app = Flask(__name__)

@app.route('/') # 접속하는 url
def index():
    return render_template('index.html')

@app.route('/signin')
def signin():
    name = request.args.get('name', default='root', type=str)
    address = request.args.get('address', default='address', type=str)
    if name == 'root':
        return "Invalid name", 400
    elif address == 'address':
        return "Invalid address", 400
    else:
        try:
            output = subprocess.check_output(['blockchaind', 'tx', 'blockchain', 'create-user', address, name, '--from', 'root', '--log_format', 'json', '-y'])
            output = str(output, 'utf-8')

            output_split = output.split('\n')
            for i in range(len(output_split)):
                if output_split[i].startswith('code'):
                    code = output_split[i]
                if output_split[i].startswith('raw_log'):
                    raw_log = output_split[i]
                if output_split[i].startswith('  '):
                    raw_log += output_split[i]

            if code == '0': 
                return "Success signin", 200
            else:
                return raw_log, 400
        except subprocess.CalledProcessError:
            return "Invalid parameter", 400

if __name__=="__main__":
    app.run(debug=True)
    # host 등을 직접 지정하고 싶다면
    # app.run(host="127.0.0.1", port="5000", debug=True)