from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import base64


def deserialize_public_key(public_key_str):
    return serialization.load_pem_public_key(
        public_key_str.encode('utf-8'),
        backend=default_backend()
    )

def serialize_public_key(public_key):
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode('utf-8')



    
def serialize_signature( signature):
        if signature:
            return base64.b64encode(signature).decode('utf-8')
        return None

def deserialize_signature( signature_str):
        if signature_str:
            return base64.b64decode(signature_str.encode('utf-8'))
        return None