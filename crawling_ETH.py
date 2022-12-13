from database.CRUD_tx import CRUD_tx
from web3 import Web3
import datetime
import requests
from web3.types import FilterParams
from requests.adapters import Retry


w3 = Web3(Web3.HTTPProvider('https://ethereum-mainnet-rpc.allthatnode.com'))
startBlockNum = 16000000
latestBlockNum = w3.eth.get_block_number()
print(f'latest : {latestBlockNum}')
db = CRUD_tx()

'''
for block_number in range(startBlockNum, latestBlockNum + 1):
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getBlockByNumber",
        "params": [hex(block_number), True],
        "id": 1
    }
    print(block_number)
    response = requests.post('https://ethereum-mainnet-rpc.allthatnode.com', json=payload)
    block = response.json()["result"]
    dt = datetime.datetime.fromtimestamp(int(block['timestamp'], 16))

    for tx in block['transactions']:
        value = int(tx['value'], 16) / (10**18)
        if value >= 10:
            data = [tx['from'], tx['to'], value, str(dt)]
            db.insertDB(schema='public',table='test_tb',data=data)

'''

missed_file = open('missed.txt', 'w')

for block_number in range(startBlockNum+126489, 16132581):
    try:
        block = w3.eth.getBlock(block_number, True)
        transactions = block.transactions
        dt = datetime.datetime.fromtimestamp(block.timestamp)
        for tx in transactions:
            if (tx['value']/(10**18)) >= 30:
                data = [tx['from'], tx['to'], tx['value']/(10**18), str(dt), block_number]
                db.insertDB(schema='testschema',table='ETH',data=data)
    except:
        print(f"Your database missed block number {block_number}")
        missed_file.write(f'{block_number}\n')

missed_file.close()


       
