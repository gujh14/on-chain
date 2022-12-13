from database.CRUD_tx import CRUD_tx
from web3 import Web3
import datetime
import requests


w3 = Web3(Web3.HTTPProvider('https://ethereum-mainnet-rpc.allthatnode.com'))
latest = w3.eth.get_block_number()
print(f'latest : {latest}')
db = CRUD_tx()


while 1:
    try:
        if latest <= w3.eth.get_block_number():
            block = w3.eth.getBlock(latest, True)
            transactions = block.transactions
            dt = datetime.datetime.fromtimestamp(block.timestamp)
            for tx in transactions:
                if (tx['value']/(10**18)) >= 30:
                    data = [tx['from'], tx['to'], tx['value']/(10**18), str(dt), latest]
                    db.insertDB(schema='testschema',table='ETH',data=data)
            latest = latest + 1
        elif latest > w3.eth.get_block_number():
            continue
    except Exception as e:
        print(f"Your database missed block number {latest}", e)



       
