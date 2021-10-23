
# Payment Gate With Tkinter

PaymentGate is a simple payment gate run by tkinter


## Screenshots

### Empty View
![App Screenshot](https://s4.uupload.ir/files/screenshot_(125)_ohs2.png)
### Filled View
![App Screenshot](https://s4.uupload.ir/files/screenshot_(126)_h3z.png)


## Features

- Generate random numpad every time
- Generate random captcha 
- Show bank logo base on first 8 card number digits

  
## Run Locally

Clone the project

```bash
  git clone https://github.com/ashkanzare/BankGui.git
  cd BankGui
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Run app with

```bash
  python main.py

```

Type Y/y to create an account and enter your card number and balance to use it in payment gate
(type n/N if you already have an account)
```bash
>>> Do you want to create an account?(Y/N) Y
>>> First Name: ashkan
>>> Last Name: zare
>>> Person ID: 123456789
>>> Card Number: 1111222233334444
>>> Password: *****
>>> cvv2: 1111
>>> EXP Month: 10
>>> EXP Year: 00
>>> Balance: 100000

Your account created successfully!

```

Then app will ask you for your payment amount

```bash
>>> Payment amount? 1250000

Your payment gate is up...
```
Then if everythings work fine, the payment gate will load up like below:

![App Screenshot](https://s4.uupload.ir/files/screenshot_(127)_8kie.png)
