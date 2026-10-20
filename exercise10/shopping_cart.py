from flask import Flask, jsonify, request
app = Flask(__name__)
cart = []
@app.route("/cart", methods=["GET"])
def get_cart():
    return jsonify(cart)
@app.route("/cart", methods=["POST"])
def add_to_cart():
    item = request.get_json(silent=True)
    if not isinstance(item, dict):
        return jsonify({"error": "JSON object required"}), 400
    cart.append(item)
    return jsonify(cart), 201
@app.route("/health")
def health():
    return jsonify({"status": "healthy"})
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
