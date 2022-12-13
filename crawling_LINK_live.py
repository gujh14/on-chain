from database.CRUD_tx import CRUD_tx
from web3 import Web3
import json
import datetime

w3 = Web3(Web3.HTTPProvider('https://ethereum-mainnet-rpc.allthatnode.com'))
abi = json.loads('[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"},{"name":"_data","type":"bytes"}],"name":"transferAndCall","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_subtractedValue","type":"uint256"}],"name":"decreaseApproval","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_addedValue","type":"uint256"}],"name":"increaseApproval","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"remaining","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"},{"indexed":false,"name":"data","type":"bytes"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"}]')
LINK = '0x514910771AF9Ca656af840dff83E8264EcF986CA'
LINK = Web3.toChecksumAddress(LINK)
contract = w3.eth.contract(LINK, abi=abi)
db = CRUD_tx()

token_name = contract.functions.name().call() 
token_symbol = contract.functions.symbol().call() 

print('Name:', token_name)
print('Symbol:', token_symbol)

latest = 16129999

while 1:
    try:
        if latest <= w3.eth.get_block_number():
            event_filter = contract.events.Transfer.createFilter(fromBlock=latest)
            events = event_filter.get_new_entries()
            block = w3.eth.getBlock(latest, True)
            dt = datetime.datetime.fromtimestamp(block.timestamp)

            for event in events:
                try:
                    if event['event'] == 'Transfer':
                        if (event['args']['_value']/(10**18)) >= 1000:
                            data = [event['args']['_from'], event['args']['_to'], event['args']['_value']/(10**18), str(dt), latest]
                            db.insertDB(schema='testschema',table='LINK',data=data)
                except Exception as e:
                    print(f"Your database missed LINK in block number {event['latest']} because of ",e)

            latest = latest + 1

        elif latest > w3.eth.get_block_number():
            continue
    
    except Exception as e:
        print(f"Your database missed block number {latest}", e)
    