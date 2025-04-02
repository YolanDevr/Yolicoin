from ecdsa import SigningKey, SECP256k1

# Genereer een private/public key-paar
private_key = SigningKey.generate(curve=SECP256k1)
public_key = private_key.get_verifying_key()

# Bericht ondertekenen
message = "Hello blockchain"
signature = private_key.sign(message.encode())

# Ondertekening controleren
verified = public_key.verify(signature, message.encode())

print("Signature geldig:", verified)
