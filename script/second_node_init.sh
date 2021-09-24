#!/bin/bash
#sudo yum -y install git
#git clone https://github.com/chainstock-project/blockchain
#cd blockchain
#bash script/second_node_init.bash

APP="blockchain"
APP_DAEMON="blockchaind"
APP_HOME=$HOME/.$APP
FIRST_NODE_REST_API="3.128.172.135"

sudo yum -y install jq
wget https://golang.org/dl/go1.17.linux-amd64.tar.gz    
sudo tar -xzf go1.17.linux-amd64.tar.gz -C /usr/local
rm -rf go1.17.linux-amd64.tar.gz
GOPATH=$HOME/go
PATH=$PATH:/usr/local/go/bin:$GOPATH/bin
mkdir $GOPATH $GOPATH/bin $GOPATH/src $GOPATH/pkg

# blockchain app install
make
$APP_DAEMON init second-node --home=$APP_HOME
wget -qO- $FIRST_NODE_REST_API:26657/genesis | jq -r .result.genesis > $APP_HOME/config/genesis.json
NODE_ID=$(wget -qO- $FIRST_NODE_REST_API:26657/status | jq -r .result.node_info.id)
sed "s#persistent_peers = \"\"#persistent_peers = \"$NODE_ID@$FIRST_NODE_REST_API:26656\"#" -i $APP_HOME/config/config.toml
$APP_DAEMON start

# last height
PHEIGHT=$(wget -qO- 127.0.0.1:26657/dump_consensus_state | jq -r .result.peers[0].peer_state.round_state.height)