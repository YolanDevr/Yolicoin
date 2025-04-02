import hashlib
import json
import time

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash='', nonce=0):
        self.index = index
        self.transactions = transactions  # lijst van transacties (dicts)
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = {
            'index': self.index,
            'transactions': self.transactions,
            'timestamp': self.timestamp,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }
        block_string = json.dumps(data, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty):
        print("⛏️ Blok wordt gemined...")
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"✅ Blok gemined: {self.hash}")
if __name__ == "__main__":
    test_transactions = [{"from": "Alice", "to": "Bob", "amount": 10}]
    block = Block(1, test_transactions, time.time(), "0")
    block.mine_block(difficulty=3)
