#!/bin/sh
# blockchain app build
git clone https://github.com/chainstock-project/blockchain
make -C blockchain
blockchaind init first-node --chain-id stock-chain
echo "retreat uphold table initial liquid glow debris carbon salon expire mystery entry blue skirt differ wing general only human scout fish pipe asthma base" | blockchaind keys add root --keyring-backend test --recover
ROOT_ADDRESS=$(blockchaind keys show root -a --keyring-backend test)
blockchaind add-genesis-account $ROOT_ADDRESS 110000000000stake
blockchaind gentx root 10000000000stake --chain-id stock-chain --keyring-backend test
blockchaind collect-gentxs
sed -i 's/enable = false/enable = true/' $HOME/.blockchain/config/app.toml
sed -i 's,laddr = "tcp://127.0.0.1:26657",laddr = "tcp://0.0.0.0:26657",g' $HOME/.blockchain/config/config.toml
# blockchain app start
nohup blockchaind start > blockchain.log 2>&1&

# flask build
git clone https://github.com/chainstock-project/server.git
python3 -m venv server/venv
source server/venv/bin/activate
pip install -r server/requirements.txt
# flask start
gunicorn app:app -b 0.0.0.0:5000 -w 10 --chdir server/flask/