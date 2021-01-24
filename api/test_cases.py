import json
import requests

url = "http://{}:{}".format('127.0.0.1', 5002)

def endpoint_with_request():
    response = requests.get("{}/ProcessPayment".format(url))
    print(response)
    assert response.status_code >= 400


def payment_with_empty_json():
    card_data = {}
    response = requests.post("{}/ProcessPayment".format(url), data=json.dumps(card_data),
                             headers={"Content-Type": "application/json"})

    print(response.status_code)
    assert response.status_code == 400


def payment_invalid_credit_card_detail():
    card_data_1 = {"CreditCardNumber": "1234567890123456", "CardHolder": "sunil testing", "SecurityCode": "111",
                   "ExpirationDate": "2020/1/1", "Amount": 566.7}
    card_data_2 = {"CreditCardNumber": "1234567890123456", "CardHolder": "sunil testing", "SecurityCode": "111",
                   "ExpirationDate": "2025/11/12", "Amount": 566.7}

    response_1 = requests.post("{}/ProcessPayment".format(url), data=json.dumps(card_data_1),
                               headers={"Content-Type": "application/json"})
    response_2 = requests.post("{}/ProcessPayment".format(url), data=json.dumps(card_data_2),
                               headers={"Content-Type": "application/json"})

    print(response_1.status_code)
    assert response_1.status_code == 400
    assert response_2.status_code == 200


def valid_input_data_with_differ_amount():
    card_data_1 = {"CreditCardNumber": "1234567890123456", "CardHolder": "sunil testing", "SecurityCode": "111",
                   "ExpirationDate": "2025/11/12", "Amount": 19}
    card_data_2 = {"CreditCardNumber": "1234567890123456", "CardHolder": "sunil testing", "SecurityCode": "111",
                   "ExpirationDate": "2025/11/12", "Amount": 333}
    card_data_3 = {"CreditCardNumber": "1234567890123456", "CardHolder": "sunil testing", "SecurityCode": "111",
                   "ExpirationDate": "2025/11/12", "Amount": 666}

    response_1 = requests.post("{}/ProcessPayment".format(url), data=json.dumps(card_data_1),
                               headers={"Content-Type": "application/json"})
    response_2 = requests.post("{}/ProcessPayment".format(url), data=json.dumps(card_data_2),
                               headers={"Content-Type": "application/json"})
    response_3 = requests.post("{}/ProcessPayment".format(url), data=json.dumps(card_data_3),
                               headers={"Content-Type": "application/json"})

    assert response_1.status_code == 200
    assert response_2.status_code == 200
    assert response_3.status_code == 200


def payment_card_exp_date():
    card_data_1 = {"CreditCardNumber": "1234567890123456", "CardHolder": "sunil testing", "SecurityCode": "111",
                   "ExpirationDate": "2025/1/1", "Amount": 566.7}
    card_data_2 = {"CreditCardNumber": "1234567890123456", "CardHolder": "sunil testing", "SecurityCode": "111",
                   "ExpirationDate": "2020/11/12", "Amount": 566.7}

    response_1 = requests.post("{}/ProcessPayment".format(url), data=json.dumps(card_data_1),
                               headers={"Content-Type": "application/json"})
    response_2 = requests.post("{}/ProcessPayment".format(url), data=json.dumps(card_data_2),
                               headers={"Content-Type": "application/json"})

    assert response_1.status_code == 200
    assert response_2.status_code == 400


def security_code():
    card_data_1 = {"CreditCardNumber": "1234567890123456", "CardHolder": "sunil testing", "SecurityCode": "111",
                   "ExpirationDate": "2025/1/1", "Amount": 566.7}
    card_data_2 = {"CreditCardNumber": "1234567890123456", "CardHolder": "sunil testing", "ExpirationDate": "2025/1/1",
                   "Amount": 566.7}
    card_data_3 = {"CreditCardNumber": "1234567890123456", "CardHolder": "sunil testing", "SecurityCode": 444,
                   "ExpirationDate": "2025/1/1", "Amount": 566.7}

    response_1 = requests.post("{}/ProcessPayment".format(url), data=json.dumps(card_data_1),
                               headers={"Content-Type": "application/json"})

    response_2 = requests.post("{}/ProcessPayment".format(url), data=json.dumps(card_data_2),
                               headers={"Content-Type": "application/json"})
    response_3 = requests.post("{}/ProcessPayment".format(url), data=json.dumps(card_data_3),
                               headers={"Content-Type": "application/json"})

    assert response_1.status_code == 200
    assert response_2.status_code == 200
    assert response_3.status_code == 400

# security_code()
# payment_card_exp_date()
# valid_input_data_with_differ_amount()
# endpoint_with_request()
# payment_with_empty_json()
# payment_invalid_credit_card_detail()
