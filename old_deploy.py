import json
from solcx import compile_standard, install_solc
from web3 import Web3
from web3.types import ABI
from dotenv import load_dotenv
import os

load_dotenv()

with open("SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

install_solc("0.6.0")

complied_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"./SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

with open("complied_code.json", "w") as file:
    json.dump(complied_sol, file)

bytecode = complied_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

abi = complied_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chain_id = 5777
my_address = "0x5EAc3Ec70400a88d618991177B180D5EB1726c25"
private_key = os.getenv("PRIVATE_KEY")


SimpleStorage = w3.eth.contract(
    abi=abi,
    bytecode=bytecode,
)
nonce = w3.eth.getTransactionCount(my_address)

# Build A Transaction
# Sign A Transaction
# Send A Transaction

transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce}
)

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

print("Deploying contract.....")
# Send
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Contract Deployed....")

simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# call -> Simulate make a call and getting a return value, dont make state chane (blue button on remix)
# Transact -> when we make a state change,

print(simple_storage.functions.retrieve().call())

store_Transaction = simple_storage.functions.store(15).buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce + 1}
)
signed_store_txn = w3.eth.account.sign_transaction(
    store_Transaction, private_key=private_key
)
print("Updating Contract....")
store_tx_hash = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
store_tx_reciept = w3.eth.wait_for_transaction_receipt(store_tx_hash)
print("Updated!")
print(simple_storage.functions.retrieve().call())
