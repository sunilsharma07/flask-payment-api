class BasePaymentGateway:
    def __init__(self, retry_up=0):
        self.retry_up = retry_up
        self.gateway = None

    def connect(self, gateway=None, details=None):
        if gateway != None:
            if self.authenticate(details):
                return True
        return False

    def authenticate(self, details=None):
        if details != None:
            return True
        return False

    def pay(self, amount, user_details=None, gateway=None):
        if gateway is None:
            gateway = self.gateway
        while self.retry_up + 1 > 0:
            if self.connect(gateway, user_details):
                print("payment of {} in gateway {} sucessful".format(amount, self.gateway))
                return True
            self.retry_up -= 1
        return False


class CheapPaymentGateway(BasePaymentGateway):
    def __init__(self, retry_up=0):
        super(CheapPaymentGateway, self).__init__(retry_up)
        self.gateway = "CheapPaymentGateway"


class ExpensivePaymentGateway(BasePaymentGateway):
    def __init__(self, retry_up=1):
        super(ExpensivePaymentGateway, self).__init__(retry_up)
        self.gateway = "ExpensivePaymentGateway"


class PremiumPaymentGateway(BasePaymentGateway):
    def __init__(self, retry_up=3):
        super(PremiumPaymentGateway, self).__init__(retry_up)
        self.gateway = "PremiumPaymentGateway"


class ExternalPayment:
    def __init__(self, amount, card_details=None):
        self.amount = amount
        self.card_details = card_details

    def make_payment(self):
        try:
            payment_mode = None
            if self.amount <= 20:
                payment_mode = CheapPaymentGateway()
            elif 20 < self.amount < 500:
                payment_mode = ExpensivePaymentGateway()
            elif self.amount >= 500:
                payment_mode = PremiumPaymentGateway()
            else:
                return False
            status = payment_mode.pay(self.amount, self.card_details)
            return status
        except:
            return False
