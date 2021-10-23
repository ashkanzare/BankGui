from Shetab import shetab
from PaymentGate import PaymentGate

if __name__ == '__main__':
    shetab.main()
    PaymentGate.main(int(input('Payment amount? ')))