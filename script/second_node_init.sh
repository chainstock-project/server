#!/bin/bash
#sudo yum -y install git
#git clone https://github.com/chainstock-project/blockchain
#cd blockchain
#bash script/second_node_init.bash


sudo yum -y install jq
sudo yum -y install git

wget https://golang.org/dl/go1.17.linux-amd64.tar.gz    
sudo tar -xzf go1.17.linux-amd64.tar.gz -C /usr/local       
rm -rf go1.17.linux-amd64.tar.gz
GOPATH=$HOME/go
PATH=$PATH:/usr/local/go/bin:$GOPATH/bin
mkdir $GOPATH $GOPATH/bin $GOPATH/src $GOPATH/pkg
echo "export PATH=$PATH:/usr/local/go/bin:$GOPATH/bin" >> ~/.bashrc
# blockchain app install
git clone https://github.com/chainstock-project/blockchain
cd blockchain
make

FIRST_NODE="3.12.83.66"
blockchaind init ec2-node
wget -qO- $FIRST_NODE:26657/genesis | jq -r .result.genesis > ~/.blockchain/config/genesis.json
NODE_ID=$(wget -qO- $FIRST_NODE:26657/status | jq -r .result.node_info.id)
sed "s#persistent_peers = \"\"#persistent_peers = \"$NODE_ID@$FIRST_NODE:26656\"#" -i ~/.blockchain/config/config.toml
blockchaind start

# last height
PHEIGHT=$(wget -qO- $FIRST_NODE:26657/dump_consensus_state | jq -r .result.peers[0].peer_state.round_state.height)
