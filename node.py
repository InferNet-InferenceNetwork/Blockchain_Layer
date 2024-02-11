from flask import Flask, request , jsonify
from Core import *
app = Flask(__name__)

# Instantiate your Blockchain here
blockchain = Blockchain()

@app.route('/new_transaction', methods=['POST'])
def new_transaction():
    tx_data = request.get_json()
    print( tx_data)
    required_fields = ["sender", "recipient", "amount" , "signature"]

    # Check if the POSTed data contains the required fields
    if not all(field in tx_data for field in required_fields):
        return "Invalid transaction data", 400

    # Assuming your Blockchain class has an add_new_transaction method
    # that returns True if the transaction was successfully added
    tx = Transaction( deserialize_public_key( tx_data["sender"]) , deserialize_public_key( tx_data["recipient"]) , tx_data["amount"] , deserialize_signature( tx_data["signature"] )  )
    added = blockchain.add_new_transaction(tx)
    if added:
        return jsonify({"message": "Transaction will be added to Block {index}".format(index=blockchain.last_block.index + 1)}), 201
    else:
        return "Error adding transaction", 500

# Assuming a Blockchain class instance is already created named `blockchain`
# and it has an attribute `chain` which is a list of blocks.

@app.route('/get_chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)  # If your block is an object with properties
    return jsonify(length=len(chain_data), chain=chain_data), 200

@app.route('/mine', methods=['GET'])

##TODO: Implement mine method
def mine():
    # Ensure there are unconfirmed transactions to mine
    if not blockchain.unconfirmed_transactions:
        return "No transactions to mine", 400
    
    # Simulate the mining process, e.g., finding a nonce that satisfies the blockchain's difficulty level
    last_block = blockchain.last_block
    nonce, proof = blockchain.proof_of_work(last_block)
    
    # Include a reward for the miner
    blockchain.add_reward_transaction(miner_address="MINER'S WALLET ADDRESS")
    
    # Assuming your Blockchain class has a method to create a new block
    new_block = blockchain.create_new_block(nonce, proof, last_block.hash)
    
    if blockchain.add_block(new_block):
        # Notify network nodes of the new block, in a real blockchain network
        return jsonify({"message": "New block created", "block_number": new_block.index, "transactions": new_block.transactions, "nonce": new_block.nonce, "previous_hash": new_block.previous_hash}), 200
    else:
        return "Error creating new block", 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)