import os
import json
from ecdsa import SigningKey, SECP256k1
import hashlib

WALLET_DIR = "wallets"

if not os.path.exists(WALLET_DIR):
    os.makedirs(WALLET_DIR)

def generate_wallet(name):
    private_key = SigningKey.generate(curve=SECP256k1)
    public_key = private_key.get_verifying_key()
    address = hashlib.sha256(public_key.to_string()).hexdigest()

    wallet_data = {
        "private_key": private_key.to_string().hex(),
        "public_key": public_key.to_string().hex(),
        "address": address
    }

    with open(f"{WALLET_DIR}/{name}.wallet", "w") as f:
        json.dump(wallet_data, f)

    print(f"✅ Wallet '{name}' aangemaakt met adres: {address}")
    return private_key, public_key, address

def load_wallet(name):
    path = f"{WALLET_DIR}/{name}.wallet"
    if not os.path.exists(path):
        raise Exception("❌ Wallet niet gevonden")

    with open(path, "r") as f:
        data = json.load(f)

    private_key = SigningKey.from_string(bytes.fromhex(data["private_key"]), curve=SECP256k1)
    public_key = private_key.get_verifying_key()
    address = data["address"]
    print(f"🔓 Wallet '{name}' geladen met adres: {address}")
    return private_key, public_key, address

def list_wallets():
    return [f.split(".")[0] for f in os.listdir(WALLET_DIR) if f.endswith(".wallet")]
