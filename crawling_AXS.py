from database.CRUD_tx import CRUD_tx
from web3 import Web3
import json
import datetime

w3 = Web3(Web3.HTTPProvider('https://ethereum-mainnet-rpc.allthatnode.com'))
block = w3.eth.getBlock('latest', True) 
transactions = block.transactions
abi = json.loads('[{"inputs":[{"internalType":"address","name":"_mainchainGateway","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"_owner","type":"address"},{"indexed":true,"internalType":"address","name":"_spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"_value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"_from","type":"address"},{"indexed":true,"internalType":"address","name":"_to","type":"address"},{"indexed":false,"internalType":"uint256","name":"_value","type":"uint256"}],"name":"Transfer","type":"event"},{"constant":true,"inputs":[{"internalType":"address","name":"_owner","type":"address"},{"internalType":"address","name":"_spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"_value","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_spender","type":"address"},{"internalType":"uint256","name":"_value","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_spender","type":"address"},{"internalType":"uint256","name":"_value","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_spender","type":"address"},{"internalType":"uint256","name":"_value","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"mainchainGateway","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint256","name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"_success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_from","type":"address"},{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint256","name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"_success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]')
AXS = '0xBB0E17EF65F82Ab018d8EDd776e8DD940327B28b'
AXS = Web3.toChecksumAddress(AXS)
contract = w3.eth.contract(AXS, abi=abi)
db = CRUD_tx()

token_name = contract.functions.name().call() 
token_symbol = contract.functions.symbol().call() 

print('Name:', token_name)
print('Symbol:', token_symbol)

i = 16000000
while i < 16130000:
    try:
        transfer_filter = contract.events.Transfer.createFilter(fromBlock=i, toBlock=i+9999)
        events = transfer_filter.get_all_entries()
        print(f'start {i}')
        for event in events:
            try:
                if event['event'] == 'Transfer':
                    if (event['args']['_value']/(10**18)) >= 1000:
                        blockNumber = event['blockNumber']
                        block = w3.eth.getBlock(blockNumber, True)
                        dt = datetime.datetime.fromtimestamp(block.timestamp)
                        data = [event['args']['_from'], event['args']['_to'], event['args']['_value']/(10**18), str(dt), blockNumber]
                        db.insertDB(schema='testschema',table='AXS',data=data)
            except Exception as e:
                print(f"Your database missed AXS in block number {event['blockNumber']} because of ",e)
        i = i+10000
    except Exception as e :
            result = (f"AXS {i} err",e)
        