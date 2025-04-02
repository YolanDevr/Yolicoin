from flask import Flask, render_template_string, request, redirect
from wallet_manager import list_wallets, load_wallet, generate_wallet
from wallet import sign_message
from blockchain import Blockchain

app = Flask(__name__)
coin = Blockchain()
coin.load_chain()

# Actieve wallet (ingeladen bij selectie)
private_key = None
public_key = None
address = None

@app.route("/", methods=["GET", "POST"])
def index():
    global private_key, public_key, address

    wallets = list_wallets()

    if request.method == "POST":
        if "wallet" in request.form:
            selected = request.form["wallet"]
            private_key, public_key, address = load_wallet(selected)
            return redirect("/wallet")
        elif "new_wallet" in request.form:
            new_name = request.form["new_wallet"]
            private_key, public_key, address = generate_wallet(new_name)
            return redirect("/wallet")

    return render_template_string("""
<!doctype html>
<html lang="en">
<head>
    <title>SELV Coin Wallet</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-dark text-white">
<div class="container mt-5">
    <h1 class="mb-4">💼 Kies een wallet</h1>

    {% if wallets %}
    <form method="post" class="mb-4">
        <div class="input-group">
            <select name="wallet" class="form-select">
                {% for w in wallets %}
                <option value="{{ w }}">{{ w }}</option>
                {% endfor %}
            </select>
            <button class="btn btn-primary" type="submit">🔓 Laden</button>
        </div>
    </form>
    {% else %}
    <div class="alert alert-warning">⚠️ Geen wallets gevonden</div>
    {% endif %}

    <hr>

    <h2 class="mb-3">➕ Nieuwe wallet aanmaken</h2>
    <form method="post">
        <div class="input-group">
            <input type="text" name="new_wallet" class="form-control" placeholder="Naam voor wallet" required>
            <button class="btn btn-success" type="submit">Aanmaken</button>
        </div>
    </form>
</div>
</body>
</html>
""", wallets=wallets)
@app.route("/wallet", methods=["GET", "POST"])
def wallet():
    global private_key, public_key, address

    if request.method == "POST":
        to = request.form["to"]
        amount = float(request.form["amount"])
        message = f"{address}:{to}:{amount}"
        signature = sign_message(private_key, message).hex()
        tx = {
            "from": address,
            "to": to,
            "amount": amount,
            "signature": signature,
            "public_key": public_key.to_string().hex()
        }
        coin.add_transaction(tx)
        return redirect("/wallet")

    balance = coin.get_balance(address)
    return render_template_string("""
<!doctype html>
<html lang="en">
<head>
    <title>SELV Wallet</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-dark text-white">
<div class="container mt-5">
    <h1 class="mb-4">💳 Wallet</h1>
    <p><strong>Adres:</strong> {{ address }}</p>
    <p><strong>Saldo:</strong> € {{ balance }}</p>

    <hr>
    <h3>📤 Transactie verzenden</h3>
    <form method="post" class="row g-2 mb-4">
        <div class="col-md-6">
            <input type="text" name="to" class="form-control" placeholder="Ontvanger adres" required>
        </div>
        <div class="col-md-4">
            <input type="number" name="amount" class="form-control" placeholder="Bedrag" required>
        </div>
        <div class="col-md-2">
            <button type="submit" class="btn btn-primary w-100">Verstuur</button>
        </div>
    </form>

    <a href="/mine" class="btn btn-warning me-2">⛏️ Mine een blok</a>
    <a href="/" class="btn btn-secondary">🔄 Wissel wallet</a>
</div>
</body>
</html>
""", address=address, balance=balance)
@app.route("/mine")
def mine():
    global address
    coin.mine_pending_transactions(address)
    coin.save_chain()
    return redirect("/wallet")
@app.route("/dashboard")
def dashboard():
    total_blocks = len(coin.chain)
    total_transactions = sum(len(block.transactions) for block in coin.chain)
    total_supply = sum(
        tx["amount"]
        for block in coin.chain
        for tx in block.transactions
        if tx["to"] != "network"
    )

    return render_template_string("""
<!doctype html>
<html lang="en">
<head>
    <title>SELV Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-dark text-white">
<div class="container mt-5">
    <h1 class="mb-4">📊 Blockchain Dashboard</h1>
<div class="row">
    <div class="col-md-4">
        <div class="card bg-secondary text-white mb-3 shadow">
            <div class="card-body">
                <h5 class="card-title">🧱 Aantal blokken</h5>
                <p class="card-text fs-3">{{ total_blocks }}</p>
            </div>
        </div>
    </div>

    <div class="col-md-4">
        <div class="card bg-secondary text-white mb-3 shadow">
            <div class="card-body">
                <h5 class="card-title">💸 Transacties</h5>
                <p class="card-text fs-3">{{ total_transactions }}</p>
            </div>
        </div>
    </div>

    <div class="col-md-4">
        <div class="card bg-secondary text-white mb-3 shadow">
            <div class="card-body">
                <h5 class="card-title">🏦 Totale muntvoorraad</h5>
                <p class="card-text fs-3">€ {{ total_supply }}</p>
            </div>
        </div>
    </div>
</div>


<a href="/" class="btn btn-light">🏠 Terug naar start</a>
</div>
</body>
</html>
""", 
total_blocks=total_blocks, 
total_transactions=total_transactions, 
total_supply=total_supply)
if __name__ == "__main__":
    app.run(debug=True)
