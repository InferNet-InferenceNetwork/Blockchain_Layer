import hashlib
import time
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from Utils.Serialization import *
from Utils.Util import load_config
from Ledger import *
import yaml


# Load the configuration
config = load_config('Config/config.yaml')


class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = hash

    
    def compute_hash(self):
        block_string = f"{self.index}{self.transactions}{self.timestamp}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def to_dict(self):
        return {
            'index': self.index,
            'transactions': [tx.to_dict() for tx in self.transactions],  # Assuming transactions can be converted to dictionaries via a to_dict method
            'timestamp': self.timestamp,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce,
            'hash': self.hash
        }
class Blockchain:
    difficulty = config['blockchain']['difficulty'] # Difficulty of our Proof of Work algorithm
    
    def __init__(self):
        self.unconfirmed_transactions = []  # data that hasn't been added
        self.chain = []
        self.create_genesis_block()
    
    def create_genesis_block(self):
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)
    
    @property
    def last_block(self):
        return self.chain[-1]
    
    def add_block(self, block, proof):
        previous_hash = self.last_block.hash
        if previous_hash != block.previous_hash:
            return False
        if not self.is_valid_proof(block, proof):
            return False
        block.hash = proof
        self.chain.append(block)
        return True
    
    def is_valid_proof(self, block, block_hash):
        return (block_hash.startswith('0' * Blockchain.difficulty) and
                block_hash == block.compute_hash())
    
    def proof_of_work(self, block):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash
    
    def add_new_transaction(self, transaction):
        print("TEST", transaction.sender)
        if  verify_signature(transaction.sender, transaction.to_dict(), transaction.signature):
            self.unconfirmed_transactions.append(transaction.to_dict())
            return True
        return False

    
    def mine(self):
        if not self.unconfirmed_transactions:
            return False
        last_block = self.last_block
        new_block = Block(index=last_block.index + 1,
                          transactions=self.unconfirmed_transactions,
                          timestamp=time.time(),
                          previous_hash=last_block.hash)
        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.unconfirmed_transactions = []
        return new_block.index
    

class Transaction:
    def __init__(self, sender, recipient, amount, signature=None):
        # Assuming sender and recipient are public key objects at initialization
        self.sender = serialize_public_key(sender)  # Serialize sender's public key
        self.recipient = serialize_public_key(recipient)  # Serialize recipient's public key
        self.amount = amount
        self.signature = signature


    def to_dict(self, include_signature=False):
        data = {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount
        }
        if include_signature and self.signature:
            data["signature"] = serialize_signature(self.signature)
        return data

    def sign(self, private_key):
        # Prepare transaction data for signing
        transaction_data = self.to_dict()  # By default, does not include the signature
        self.signature = sign_transaction(private_key, transaction_data)