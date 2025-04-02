import time
from wallet_manager import generate_wallet, load_wallet, list_wallets
from wallet import sign_message
from blockchain import Blockchain
from ecdsa import VerifyingKey, SECP256k1

# Maak een nieuwe blockchain
coin = Blockchain()
coin.load_chain()
print("📂 Blockchain succesvol geladen.\n")
print("👛 Kies een wallet:")
wallets = list_wallets()
for i, name in enumerate(wallets):
    print(f"{i + 1}. {name}")
print(f"{len(wallets) + 1}. Nieuwe wallet aanmaken")

keuze = input("👉 Nummer: ")

if keuze == str(len(wallets) + 1):
    naam = input("Naam voor nieuwe wallet: ")
    private_key, public_key, address = generate_wallet(naam)
else:
    index = int(keuze) - 1
    naam = wallets[index]
    private_key, public_key, address = load_wallet(naam)

print(f"\n✅ Actieve wallet: {naam} ({address})")

def send_transaction(to, amount):
    message = f"{address}:{to}:{amount}"
    signature = sign_message(private_key, message).hex()
    tx = {
        "from": address,
        "to": to,
        "amount": amount,
        "signature": signature,
        "public_key": public_key.to_string().hex()
    }
    try:
        coin.add_transaction(tx)
        print(f"✅ Transactie toegevoegd ({amount} → {to})")
    except Exception as e:
        print(f"❌ Fout: {e}")

def mine_block():
    coin.mine_pending_transactions(address)
    print("🎉 Je hebt een blok gemined!")
    print(f"💰 Je saldo is nu: {coin.get_balance(address)}")

def show_balance():
    print(f"💳 Wallet {address}")
    print(f"💰 Saldo: {coin.get_balance(address)}")

def menu():
    while True:
        print("\n📜 MENU")
        print("1. Saldo bekijken")
        print("2. Transactie verzenden")
        print("3. Blok minen")
        print("4. Blockchain checken")
        print("0. Afsluiten")

        keuze = input("👉 Kies een optie: ")

        if keuze == "1":
            show_balance()
        elif keuze == "2":
            ontvanger = input("Ontvanger adres: ")
            bedrag = float(input("Bedrag: "))
            send_transaction(ontvanger, bedrag)
        elif keuze == "3":
            mine_block()
            coin.save_chain()
        elif keuze == "4":
            print("📦 Lengte ketting:", len(coin.chain))
            print("🧱 Laatste blok hash:", coin.get_latest_block().hash)
        elif keuze == "0":
            print("👋 Tot de volgende keer!")
            break
        else:
            print("❗ Ongeldige keuze")

if __name__ == "__main__":
    menu()
