from flask import Flask, request
import paho.mqtt.publish as publish

app = Flask(__name__)

MACHINE_ID = "VEG001"
MQTT_BROKER = "broker.hivemq.com"
MQTT_TOPIC = "smartvegpay/VEG001/command"


@app.route("/")
def home():
    return """
    <h1>SMART VEG PAY</h1>
    <h2>Machine: VEG001</h2>

    <p>Select Amount:</p>

    <a href="/pay/20"><button>₹20</button></a><br><br>
    <a href="/pay/30"><button>₹30</button></a><br><br>
    <a href="/pay/40"><button>₹40</button></a><br><br>
    <a href="/pay/60"><button>₹60</button></a>
    """


@app.route("/pay/<int:amount>")
def payment_page(amount):

    allowed_amounts = [20, 30, 40, 60]

    if amount not in allowed_amounts:
        return "Invalid amount"

    return f"""
    <h1>SMART VEG PAY</h1>
    <h2>Machine: {MACHINE_ID}</h2>

    <h3>Selected Amount: ₹{amount}</h3>

    <form action="/test-payment" method="post">
        <input type="hidden" name="amount" value="{amount}">
        <button type="submit">
            TEST PAYMENT SUCCESS
        </button>
    </form>
    """


@app.route("/test-payment", methods=["POST"])
def test_payment():

    amount = int(request.form["amount"])

    publish.single(
        MQTT_TOPIC,
        str(amount),
        hostname=MQTT_BROKER,
        port=1883
    )

    return f"""
    <h1>TEST PAYMENT SUCCESS ✅</h1>

    <h2>Machine: {MACHINE_ID}</h2>
    <h2>Amount: ₹{amount}</h2>

    <p>Amount sent to ESP32 through MQTT.</p>

    <a href="/">Back</a>
    """


if __name__ == "__main__":
    print("SMART VEG PAY SERVER")
    print("Machine ID:", MACHINE_ID)
    print("MQTT Topic:", MQTT_TOPIC)
    print("Open in browser:")
    print("http://127.0.0.1:5000")

    app.run(host="0.0.0.0", port=5000)