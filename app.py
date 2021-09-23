# app.py
from flask import Flask, render_template
from flask import request
import subprocess
import os

#Flask 객체 인스턴스 생성
app = Flask(__name__)

@app.route('/') # 접속하는 url
def index():
    result = """
    /signin\n
    """
    return result

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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)