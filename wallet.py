from ecdsa import SigningKey, SECP256k1
import hashlib

def generate_keys():
    private_key = SigningKey.generate(curve=SECP256k1)
    public_key = private_key.get_verifying_key()
    return private_key, public_key

def get_address(public_key):
    public_bytes = public_key.to_string()
    return hashlib.sha256(public_bytes).hexdigest()

def sign_message(private_key, message):
    return private_key.sign(message.encode())

def verify_signature(public_key, signature, message):
    return public_key.verify(signature, message.encode())

# Voor test
if __name__ == "__main__":
    private, public = generate_keys()
    address = get_address(public)
    print("Jouw wallet-adres:", address)

    message = "Hallo wereld"
    signature = sign_message(private, message)

    print("Geldig?", verify_signature(public, signature, message))
