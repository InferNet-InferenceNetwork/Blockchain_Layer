#TODO: Fix imports
from Core import *
from Ledger import *
# Generate keys for Alice and Bob
alice_private_key, alice_public_key = generate_keys()
bob_private_key, bob_public_key = generate_keys()
blockchain = Blockchain()
transaction = Transaction(sender=alice_public_key, recipient=bob_public_key, amount=10)
transaction.sign(alice_private_key)
# Attempt to add the transaction to the blockchain
print( transaction.to_dict())
blockchain.add_new_transaction(transaction)
if blockchain.add_new_transaction(transaction):
    blockchain.mine()
    "mined"
else:
    print("Failed to add transaction.")
for block in blockchain.chain:
    print(f"Index: {block.index}")
    print(f"Transactions: {block.transactions}")
    print(f"Timestamp: {block.timestamp}")
    print(f"Current Hash: {block.hash}")
    print(f"Previous Hash: {block.previous_hash}\n")