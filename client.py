import requests
import json
from Core import *


# The URL where your Flask app is running
FLASK_APP_URL = 'http://127.0.0.1:5000'



def send_transaction(transaction ):
   
    # Send the transaction to the Flask app
    json = transaction.to_dict( 
        include_signature = True
                               )
    print(json)
    response = requests.post(f"{FLASK_APP_URL}/new_transaction", json= json)
    print(response)
    
    return response.json()

def get_blockchain():
    # Request the blockchain from the Flask app
    response = requests.get(f"{FLASK_APP_URL}/get_chain")
    return response.json()

# Example usage
alice_private_key, alice_public_key = generate_keys()
bob_private_key, bob_public_key = generate_keys()
amount = 10
# Construct the transaction

transaction = Transaction(sender=alice_public_key, recipient=bob_public_key, amount=10)
transaction.sign(alice_private_key)



# Send a transaction
transaction_response = send_transaction(transaction )
print("Transaction response:", transaction_response)

# Get the blockchain
blockchain_response = get_blockchain()
print("Blockchain response:", blockchain_response)
