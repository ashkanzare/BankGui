import sqlite3

database_path = 'Shetab/shetab_network.db'


# function for create database
def create_database():
    # Create a database or connect to one
    conn = sqlite3.connect(database_path)

    # Create a cursor
    c = conn.cursor()

    # Create table
    try:
        c.execute("""CREATE TABLE costumers (
                  first_name text,
                  last_name text,
                  person_id text,
                  card_number text,
                  password text,
                  cvv2 text,
                  exp_month text,
                  exp_year text,
                  balance integer         
    
                 )  """)

        # Commit changes
        conn.commit()
    except conn.OperationalError:
        pass

    # Close connection
    conn.close()


# function for add to the database
def add_costumer():
    # Create a databse or connect to one
    conn = sqlite3.connect(database_path)

    # Create a cursor
    c = conn.cursor()

    c.execute(
        "INSERT INTO costumers VALUES (:first_name, :last_name, :person_id, :card_number, :password, :cvv2, "
        ":exp_month, "
        ":exp_year, :balance)",
        {
            'first_name': input('First Name: '),
            'last_name': input('Last Name: '),
            'person_id': input('Person ID: '),
            'card_number': input('Card Number: '),
            'password': input('Password: '),
            'cvv2': input('cvv2: '),
            'exp_month': input('EXP Month: '),
            'exp_year': input('EXP Year: '),
            'balance': input('Balance: ')
        })

    # Commit changes
    conn.commit()

    print('Your account created successfully!')
    # Close connection
    conn.close()


# function for get data from database
def query():
    # Create a databse or connect to one
    conn = sqlite3.connect(database_path)

    # Create a cursor
    c = conn.cursor()

    # Query the database
    c.execute("SELECT *, oid FROM costumers")
    records = c.fetchall()

    # Commit changes
    conn.commit()

    # Close connection
    conn.close()


# Function to delete a record
def delete():
    # Create a databse or connect to one
    conn = sqlite3.connect(database_path)

    # Create a cursor
    c = conn.cursor()

    # Delete a record
    c.execute("DELETE from costumers WHERE oid= " + input('Enter oid to delete: '))

    # Commit changes
    conn.commit()

    # Close connection
    conn.close()


# Function to validate data
def validate_data(data, pay):
    # Create a databse or connect to one
    conn = sqlite3.connect(database_path)

    # assign our entrys
    card_number = data['.!entrycard'] + data['.!entrycard2'] + data['.!entrycard3'] + data['.!entrycard4']
    password = data['.!entrycard5']
    cvv2 = data['.!entrycard6']
    exp_month = data['.!entrycard7']
    exp_year = data['.!entrycard8']
    data_list = [card_number, password, cvv2, exp_month, exp_year]

    # Create a cursor
    c = conn.cursor()

    # check if card info are correct
    # try: # if get error active this
    c.execute("SELECT *, oid FROM costumers WHERE card_number = " + card_number)
    records = c.fetchall()
    if records:
        records = records[0]
        records_list = [records[i] for i in range(3, 8)]
        if records_list == data_list:
            # Commit changes
            conn.commit()

            # Close connection
            conn.close()

            return purchase(card_number, pay)
        else:
            return 'اطلاعات وارد شده نادرست است', 'red'
    else:
        # Commit changes
        conn.commit()

        # Close connection
        conn.close()

        return 'اطلاعات وارد شده نادرست است', 'red'
    # except:  # if get error active this
    #     return 'اطلاعات وارد شده نادرست است', 'red'


# Function that get card number and return balance
def purchase(card_number, pay):
    # Create a database or connect to one
    conn = sqlite3.connect(database_path)

    # Create a cursor
    c = conn.cursor()

    # Query the database
    c.execute("SELECT balance FROM costumers WHERE card_number = " + card_number)
    records = c.fetchall()
    # todo: connect to maktab bank data base and update account if account was in maktab database
    if records[0][0] - pay >= 100000:
        c.execute("""UPDATE costumers SET
            balance = :balance
            WHERE card_number = :card_number""",
                  {
                      'balance': records[0][0] - pay,
                      'card_number': card_number
                  })
        # Commit changes
        conn.commit()

        # Close connection
        conn.close()

        return 'پرداخت با موفقیت انجام شد', 'green'
    else:
        # Commit changes
        conn.commit()

        # Close connection
        conn.close()

        return 'موجودی حساب کافی نیست', 'red'


def main():
    create_database()
    check = input('Do you want to create an account?(Y/N) ')
    if check.lower() in ['y', 'yes']:
        add_costumer()
        query()


if __name__ == '__main__':
    database_path = 'shetab_network.db'
    main()
