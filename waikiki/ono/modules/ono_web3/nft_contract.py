import os
from re import M
from web3 import Web3
import solcx

_chain_id = 1901
_gas = 6721975

url = "http://127.0.0.1:8124"
provider = Web3.HTTPProvider(url)
w3 = Web3(provider)


def create_nft_contract(my_address, my_private_key, my_title, my_symbol):
    print("[create_nft_contract] isConnected = ", w3.isConnected())

    CURRENT_DIR = os.path.dirname(__file__)

    # https://solcx.readthedocs.io/en/latest/using-the-compiler.html#compiling-files
    compiled_sol = solcx.compile_files([CURRENT_DIR + "\\contracts\\MakeNft.sol",
                                        CURRENT_DIR + "\\contracts\\tokens\\erc721-enumerable.sol",
                                        CURRENT_DIR + "\\contracts\\tokens\\erc721-metadata.sol",
                                        CURRENT_DIR + "\\contracts\\tokens\\erc721-token-receiver.sol",
                                        CURRENT_DIR + "\\contracts\\tokens\\erc721.sol",
                                        CURRENT_DIR + "\\contracts\\tokens\\nf-token-enumerable.sol",
                                        CURRENT_DIR + "\\contracts\\tokens\\nf-token-metadata.sol",
                                        CURRENT_DIR + "\\contracts\\tokens\\nf-token.sol",
                                        CURRENT_DIR + "\\contracts\\ownership\\ownable.sol",
                                        CURRENT_DIR + "\\contracts\\utils\\erc165.sol",
                                        CURRENT_DIR + "\\contracts\\utils\\address-utils.sol",
                                        CURRENT_DIR + "\\contracts\\utils\\supports-interface.sol"
                                        ],
                                       output_values=[
                                           "abi", "bin", "bin-runtime"]
                                       )

    my_index = CURRENT_DIR + "\\contracts\\MakeNft.sol:newNFT"
    my_index = my_index.replace("\\", "/")

    account_from = {
        'private_key': my_private_key,
        'address': my_address
    }

    # account_from = {
    #     'private_key': '7914b9f670e443d261b8f8198114d7517a3eae1ff38f6ffaf779d8f76bbf08eb',
    #     'address': '0xc4bf49aAA6A3928292D02f92cA4D2358b74C8B6C'
    # }

    newNFT_contract = w3.eth.contract(
        abi=compiled_sol[my_index]["abi"],
        bytecode=compiled_sol[my_index]["bin"],
        bytecode_runtime=compiled_sol[my_index]["bin-runtime"])

    # print("newNFT_contract = ", newNFT_contract)
    # print("abi = ", compiled_sol[my_index]["abi"])

    # global _abi
    # _abi = compiled_sol[my_index]["abi"]

    construct_txn = newNFT_contract.constructor(_nftName=my_title, _nftSymbol=my_symbol).buildTransaction(
        {
            'chainId': _chain_id,
            'gasPrice': w3.eth.gas_price,
            'gas': _gas,
            'from': my_address,
            'nonce': w3.eth.get_transaction_count(my_address),
            # 'from': account_from['address'],
            # 'nonce': w3.eth.get_transaction_count(account_from['address']),
        }
    )

    # print("construct_txn = ", construct_txn)

    tx_create = w3.eth.account.sign_transaction(
        construct_txn, account_from['private_key'])
    tx_hash = w3.eth.send_raw_transaction(tx_create.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    print(f'Contract deployed at address: { tx_receipt.contractAddress }')

    # global _contract_address
    # _contract_address = tx_receipt.contractAddress

    response = {
        "contract_address": tx_receipt.contractAddress,
        "abi": compiled_sol[my_index]["abi"]
    }

    return response


def mint_item(my_address, my_private_key, my_contract_address, my_abi, to_address, token_id, ipfs_uri):
    print("[mint_item] isConnected = ", w3.isConnected())

    account_from = {
        'private_key': my_private_key,
        'address': my_address
    }

    # account_from = {
    #     'private_key': '7914b9f670e443d261b8f8198114d7517a3eae1ff38f6ffaf779d8f76bbf08eb',
    #     'address': '0xc4bf49aAA6A3928292D02f92cA4D2358b74C8B6C'
    # }

    # address _to, uint256 _tokenId, string calldata _uri
    # to_address = '0xc4bf49aAA6A3928292D02f92cA4D2358b74C8B6C'
    # token_id = 2
    # uri = 'https://ipfs.io/ipfs/QmV1r8QEiQSLPgFfqiTG4RsW2ythjCKHr9LpKgoGB2pvXt'

    nft_contract = w3.eth.contract(address=my_contract_address, abi=my_abi)

    print("[1] ", to_address)
    print("[2] ", token_id)
    print("[3] ", ipfs_uri)


    nft_contract_tx = nft_contract.functions.mint(to_address, int(token_id), ipfs_uri).buildTransaction(
        {
            'chainId': _chain_id,
            'gasPrice': w3.eth.gas_price,
            'gas': _gas,
            'from': account_from['address'],
            'nonce': w3.eth.get_transaction_count(account_from['address']),
        }
    )

    tx_create = w3.eth.account.sign_transaction(
        nft_contract_tx, account_from['private_key'])
    tx_hash = w3.eth.send_raw_transaction(tx_create.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    # print(f'Tx successful with hash: { tx_receipt.transactionHash.hex() }')

    response = {
        "result": "succesful",
        "tx_receipt": tx_receipt.transactionHash.hex()
    }

    return response


def testSearch(item):
    print("[testSearch] : ", item)
    print("[testSearch] isConnected = ", w3.isConnected())

    my_info = {
        "accounts": w3.eth.accounts,
        "chain_id": w3.eth.chain_id,
        "balance": "",
        "block_number": w3.eth.get_block_number(),
        "get_transaction_count": "",
        "get_transaction": w3.eth.get_transaction(item)['input']
    }
    print(my_info)

    return my_info


# def makeNftConract():
#     contract = w3.eth.contract(
#         abi='',
#         bytecode=''
#     )

#     tx_hash = contract.deploy(
#         transaction={'from': w3.eth.accounts[0]}
#     )

#     tx_receipt = w3.eth.getTransactionReceipt(tx_hash)


# backup
# def create_nft_contract():
#     print("[create_nft_contract] isConnected = ", w3.isConnected())

#     # solcx.compile_files(["./MakeNft.sol"])
#     # compiled_sol = solcx.compile_standard(
#     #     {
#     #         "language": "Solidity",
#     #         "sources": {"SimpleStorage.sol": {"content": "MakeNft.sol"}},
#     #         "settings": {
#     #             "outputSelection": {
#     #                 "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
#     #             }
#     #         },
#     #     },
#     #     solc_version="0.8.6",
#     # )

#     CURRENT_DIR = os.path.dirname(__file__)

#     # https://solcx.readthedocs.io/en/latest/using-the-compiler.html#compiling-files
#     compiled_sol = solcx.compile_files([CURRENT_DIR + "\\contracts\\MakeNft.sol",
#                                         CURRENT_DIR + "\\contracts\\tokens\\erc721-enumerable.sol",
#                                         CURRENT_DIR + "\\contracts\\tokens\\erc721-metadata.sol",
#                                         CURRENT_DIR + "\\contracts\\tokens\\erc721-token-receiver.sol",
#                                         CURRENT_DIR + "\\contracts\\tokens\\erc721.sol",
#                                         CURRENT_DIR + "\\contracts\\tokens\\nf-token-enumerable.sol",
#                                         CURRENT_DIR + "\\contracts\\tokens\\nf-token-metadata.sol",
#                                         CURRENT_DIR + "\\contracts\\tokens\\nf-token.sol",
#                                         CURRENT_DIR + "\\contracts\\ownership\\ownable.sol",
#                                         CURRENT_DIR + "\\contracts\\utils\\erc165.sol",
#                                         CURRENT_DIR + "\\contracts\\utils\\address-utils.sol",
#                                         CURRENT_DIR + "\\contracts\\utils\\supports-interface.sol"
#                                         ],
#                                        output_values=[
#                                            "abi", "bin", "bin-runtime"]
#                                        )


#     my_index = CURRENT_DIR + "\\contracts\\MakeNft.sol:newNFT"
#     my_index = my_index.replace("\\", "/")

#     # compiled_sol[my_index]["abi"]
#     # compiled_sol[my_index]["bin"]
#     # compiled_sol[my_index]["bin-runtime"]

#     # 3
#     account_from = {
#         'private_key': '7914b9f670e443d261b8f8198114d7517a3eae1ff38f6ffaf779d8f76bbf08eb',
#         'address': '0xc4bf49aAA6A3928292D02f92cA4D2358b74C8B6C'
#     }

#     # 4
#     newNFT_contract = w3.eth.contract(
#         abi=compiled_sol[my_index]["abi"],
#         bytecode=compiled_sol[my_index]["bin"],
#         bytecode_runtime=compiled_sol[my_index]["bin-runtime"])

#     print("newNFT_contract = ", newNFT_contract)

#     # print("abi = ", compiled_sol[my_index]["abi"])
#     global _abi
#     _abi = compiled_sol[my_index]["abi"]

#     # 5          여기에 constructor parameter
#     construct_txn = newNFT_contract.constructor(_nftName="my1", _nftSymbol="my_s_1").buildTransaction(
#         {
#             'chainId': 1901,
#             'gasPrice': w3.eth.gas_price,
#             'gas': 6721975,
#             'from': account_from['address'],
#             'nonce': w3.eth.get_transaction_count(account_from['address']),
#         }
#     )

#     print("construct_txn = ", construct_txn)

#     # 6. sign tx with pk
#     tx_create = w3.eth.account.sign_transaction(
#         construct_txn, account_from['private_key'])

#     # 7. send tx and wait for recipt
#     tx_hash = w3.eth.send_raw_transaction(tx_create.rawTransaction)
#     tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

#     print(f'Contract deployed at address: { tx_receipt.contractAddress }')
#     global _contract_address
#     _contract_address = tx_receipt.contractAddress

#     my_info = {
#         "accounts": "",
#         "chain_id": "",
#         "balance": "",
#         "block_number": "",
#         "get_transaction_count": "",
#         "get_transaction": ""
#     }

#     # my_info = {
#     #     "accounts" : w3.eth.accounts,
#     #     "chain_id" : w3.eth.chain_id,
#     #     "balance" : w3.eth.get_balance(w3.eth.accounts[0]),
#     #     "block_number" : w3.eth.get_block_number(),
#     #     "get_transaction_count" : w3.eth.get_transaction_count(w3.eth.accounts[0]),
#     #     "get_transaction": w3.eth.get_transaction(item)
#     # }
#     print(my_info)

#     return my_info

# def mint_item():
#     print("[mint_item] isConnected = ", w3.isConnected())

#     # 3
#     account_from = {
#         'private_key': '7914b9f670e443d261b8f8198114d7517a3eae1ff38f6ffaf779d8f76bbf08eb',
#         'address': '0xc4bf49aAA6A3928292D02f92cA4D2358b74C8B6C'
#     }

#     # print("[ abi ] ", _abi)
#     print("[ **contract id ] ", _contract_address)
#     contract_address = _contract_address#'0x0B58eC6281b6a1ece845e1dF59f9FAbFC3FE5129'
#     #address _to, uint256 _tokenId, string calldata _uri
#     to_address = '0xc4bf49aAA6A3928292D02f92cA4D2358b74C8B6C'
#     token_id = 2
#     uri = 'https://ipfs.io/ipfs/QmV1r8QEiQSLPgFfqiTG4RsW2ythjCKHr9LpKgoGB2pvXt'

#     # 4
#     ddd = w3.eth.contract(address = contract_address, abi = _abi)

#     print("[** ddd ] ", ddd)


#     # 5
#     ddd_tx = ddd.functions.mint(to_address, token_id, uri).buildTransaction(
#         {
#             'chainId': 1901,
#             'gasPrice': w3.eth.gas_price,
#             'gas': 6721975,
#             # 'to': account_from['address'],
#             'from': account_from['address'],
#             'nonce': w3.eth.get_transaction_count(account_from['address']),
#         }
#     )

#     # 6
#     tx_create = w3.eth.account.sign_transaction(ddd_tx, account_from['private_key'])

#     # 7
#     tx_hash = w3.eth.send_raw_transaction(tx_create.rawTransaction)
#     tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

#     # print(f'Tx successful with hash: { tx_receipt.transactionHash.hex() }')

#     my_info = {
#         "accounts": "",
#         "chain_id": "",
#         "balance": "",
#         "block_number": "",
#         "get_transaction_count": "",
#         "get_transaction": ""
#     }

#     return my_info
