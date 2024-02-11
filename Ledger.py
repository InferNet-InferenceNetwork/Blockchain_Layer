
from Utils.Serialization import *
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
def prepare_data_for_signing(transaction):
    # Assuming transaction is a dictionary that includes 'sender', 'recipient', 'amount', and excludes 'signature' for verification
    transaction_copy = {key: transaction[key] for key in transaction if key != 'signature'}
    return str(transaction_copy).encode()

def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

def sign_transaction(private_key, transaction):
    transaction = str(transaction).encode()
    signature = private_key.sign(
        transaction,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

def verify_signature(public_key_str, transaction, signature):
    # Deserialize the public key from string
    public_key = deserialize_public_key(public_key_str)

    # Prepare transaction data for verification
    data_to_verify = prepare_data_for_signing(transaction)
    try:
        public_key.verify(
            signature,
            data_to_verify,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception as e:
        print(f"Verification failed: {e}")  # Better error handling
        return False
