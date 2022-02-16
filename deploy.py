from solcx import compile_standard, install_solc
import json
from web3 import Web3
from dotenv import load_dotenv
import os

load_dotenv()

install_solc("0.6.0")

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()


compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

print("[Info]\tContract read and compiled!")

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = json.loads(
    compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["metadata"]
)["output"]["abi"]

#Intializing Web3 and Providing the local Ganache Chain as my test chain.
#Use your own chain here.
w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/3d07b066df0047dfbdc67c5215892a97"))
chain_id = 4

#The address which I have access to the private key for.
my_address = "0x912e8d8bA2a4d8634A3E351D93088dC2212242D6"

#Creating a contract object
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

#Getting the nonce
nonce = w3.eth.getTransactionCount(my_address)

#Building a transaction from contract
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "from": my_address,
        "gasPrice": w3.eth.gas_price,
        "nonce": nonce,
    }
)

#Signing a transaction
signed_txn = w3.eth.account.sign_transaction(transaction,os.getenv("PRIVATE_KEY"))
print("[Transaction]\tTransaction Signed!")

#Sending the Signed Transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
print("[Transaction]\tSending Transaction!")

#Getting the receipt.
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

#Printing the result:
print(f"[Success]\tContract Deployed to: {tx_receipt.contractAddress}")

#Interaction with deployed contract. Creating a refrence from the chain.
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

print("----------------------------------------------------------------------------")

#Getting Intial Value
print(f"[Retrieve]\t Stored Value {simple_storage.functions.retrieve().call()}")


data = input("Enter a number to store on the contract:\t")
#Updating transaction
updated_transaction = simple_storage.functions.store(int(data)).buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce + 1,
    }
)

#Signing a transaction
signed_updated_txn = w3.eth.account.sign_transaction(updated_transaction,os.getenv("PRIVATE_KEY"))
print("[Update]\tUpdated Transaction Signed!")

#Sending the Signed Transaction
updated_tx_hash = w3.eth.send_raw_transaction(signed_updated_txn.rawTransaction)
print("[Update]\tSending Updated Transaction!")

#Getting the receipt.
updated_tx_receipt = w3.eth.wait_for_transaction_receipt(updated_tx_hash)

#Rechecking our new value.
print(f"[Retrieve]\t Stored Value {simple_storage.functions.retrieve().call()}")


#To undestand the line os.getenv("PRIVATE_KEY"). Its basically a environment variable storing the private key for my address.
#I am using the package dotenv to load the .env file (which i git ignored) at the start of the script.
#To workaround this: Create a .env file in VSCode and write export PRIVATE_KEY = 0xyour_private_key
#Remember to add "0x" before the key.