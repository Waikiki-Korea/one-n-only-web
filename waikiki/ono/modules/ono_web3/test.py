from web3 import Web3

def testSearch(item):
    print("[testSearch] : ", item)

    url = "http://127.0.0.1:8123"
    provider = Web3.HTTPProvider(url)
    w3 = Web3(provider)
    
    print("[testSearch] isConnected = ", w3.isConnected())
    
    my_info = {
        "accounts" : w3.eth.accounts,
        "chain_id" : w3.eth.chain_id,
        "balance" : w3.eth.get_balance(w3.eth.accounts[0]),
        "block_number" : w3.eth.get_block_number(),
        "get_transaction_count" : w3.eth.get_transaction_count(w3.eth.accounts[0]),
        "get_transaction": w3.eth.get_transaction(item)
    }
    print(my_info)

    return my_info
