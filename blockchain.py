import time
import json
from block import Block
from wallet import get_address, verify_signature

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 3
        self.pending_transactions = []
        self.mining_reward = 100

    def create_genesis_block(self):
        return Block(0, [], time.time(), "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction):
        if not transaction.get("from") or not transaction.get("to") or not transaction.get("amount"):
            raise Exception("Transactie ongeldig: ontbrekende velden")

        if transaction["from"] != "network":
            if not transaction.get("signature") or not transaction.get("public_key"):
                raise Exception("Transactie ongeldig: geen handtekening of public key")

            # Verifieer handtekening
            message = f'{transaction["from"]}:{transaction["to"]}:{transaction["amount"]}'
            if not verify_signature(transaction["public_key"], bytes.fromhex(transaction["signature"]), message):
                raise Exception("Transactie ongeldig: ongeldige handtekening")

        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self, miner_address):
        block = Block(
            index=len(self.chain),
            transactions=self.pending_transactions,
            timestamp=time.time(),
            previous_hash=self.get_latest_block().hash
        )
        block.mine_block(self.difficulty)
        self.chain.append(block)

        # Reset transacties, geef beloning
        self.pending_transactions = [{
            "from": "network",
            "to": miner_address,
            "amount": self.mining_reward
        }]

    def get_balance(self, address):
        balance = 0
        for block in self.chain:
            for tx in block.transactions:
                if tx["to"] == address:
                    balance += tx["amount"]
                if tx["from"] == address:
                    balance -= tx["amount"]
        return balance

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i - 1]
            if curr.hash != curr.calculate_hash():
                return False
            if curr.previous_hash != prev.hash:
                return False
        return True

    # ✅ Nieuwe methodes toegevoegd hieronder:
    def save_chain(self, filename="chain.json"):
        data = []
        for block in self.chain:
            data.append({
                "index": block.index,
                "transactions": block.transactions,
                "timestamp": block.timestamp,
                "previous_hash": block.previous_hash,
                "nonce": block.nonce,
                "hash": block.hash
            })
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print(f"💾 Blockchain opgeslagen als '{filename}'")

    def load_chain(self, filename="chain.json"):
        try:
            with open(filename, "r") as f:
                data = json.load(f)
            self.chain = []
            for block_data in data:
                block = Block(
                    index=block_data["index"],
                    transactions=block_data["transactions"],
                    timestamp=block_data["timestamp"],
                    previous_hash=block_data["previous_hash"],
                    nonce=block_data["nonce"]
                )
                block.hash = block_data["hash"]
                self.chain.append(block)
            print(f"📂 Blockchain geladen uit '{filename}'")
        except FileNotFoundError:
            print(f"⚠️ Geen opgeslagen blockchain gevonden – nieuw gestart")

if __name__ == "__main__":
    print("✅ Blockchain-module is correct geladen")
