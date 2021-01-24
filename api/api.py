import flask
from flask import request, abort
import json
from utility.carddetails import Card
from utility.paymentgatway import ExternalPayment

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route("/ProcessPayment", methods=['POST'])
def payment():
    if request.method == 'POST':
        data = request.get_data(as_text=True)
        if not data:
            abort(400)
        request_data = json.loads(data)
        # card data into our class
        card_data = Card()
        print(f'request data {request_data}')
        #Card-Data
        try:
            if not card_data.verify_input(**request_data):
                print("card data invalid")
                abort(400)
        except:
            abort(400)

        #Payment
        try:
            payment_status = ExternalPayment(card_data.Amount, card_data)
            payment_sccessfull = payment_status.make_payment()
            if payment_sccessfull:
                return {"status code": 200}, 200
            else:
                abort(400)
        except:
            abort(500)
    else:
        abort(400)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5002)
