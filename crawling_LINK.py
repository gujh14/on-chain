from database.CRUD_tx import CRUD_tx
from web3 import Web3
import json
import datetime

w3 = Web3(Web3.HTTPProvider('https://ethereum-mainnet-rpc.allthatnode.com'))
block = w3.eth.getBlock('latest', True) 
transactions = block.transactions
abi = json.loads('[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"},{"name":"_data","type":"bytes"}],"name":"transferAndCall","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_subtractedValue","type":"uint256"}],"name":"decreaseApproval","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_addedValue","type":"uint256"}],"name":"increaseApproval","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"remaining","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"},{"indexed":false,"name":"data","type":"bytes"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"}]')
LINK = '0x514910771AF9Ca656af840dff83E8264EcF986CA'
LINK = Web3.toChecksumAddress(LINK)
contract = w3.eth.contract(LINK, abi=abi)
db = CRUD_tx()

token_name = contract.functions.name().call() 
token_symbol = contract.functions.symbol().call() 

print('Name:', token_name)
print('Symbol:', token_symbol)

i = 15000000
while i < 16000000:
    try:
        transfer_filter = contract.events.Transfer.createFilter(fromBlock=i, toBlock=i+9999)
        events = transfer_filter.get_all_entries()
        print(f'start {i}')
        for event in events:
            try:
                if event['event'] == 'Transfer':
                    if (event['args']['value']/(10**18)) >= 1000:
                        blockNumber = event['blockNumber']
                        block = w3.eth.getBlock(blockNumber, True)
                        dt = datetime.datetime.fromtimestamp(block.timestamp)
                        data = [event['args']['from'], event['args']['to'], event['args']['value']/(10**18), str(dt), blockNumber]
                        db.insertDB(schema='testschema',table='LINK',data=data)
            except Exception as e:
                print(f"Your database missed LINK in block number {event['blockNumber']} because of ",e)
        i = i+10000
    except Exception as e :
            result = (f"LINK {i} err",e)
        