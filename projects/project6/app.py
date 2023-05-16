# -*- coding: utf-8 -*-
"""
Created on Sat May  6 16:01:51 2023

@author: ChatGPT3
"""

from flask import Flask, render_template, request
import pandas as pd
import locale

locale.setlocale(locale.LC_ALL, 'en_GB.UTF-8')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    # get form data
    principal = float(request.form['principal'])
    interest_rate = float(request.form['interest_rate'])
    loan_term = int(request.form['loan_term'])

    # convert interest rate to decimal
    interest_rate /= 100

    # calculate mortgage payment
    monthly_rate = interest_rate / 12
    num_payments = loan_term * 12
    mortgage_payment = (principal * monthly_rate) / (1 - (1 + monthly_rate) ** (-num_payments))

    # create payment schedule
    balance = principal
    payments = []
    for i in range(num_payments):
        interest_payment = balance * monthly_rate
        principal_payment = mortgage_payment - interest_payment
        balance -= principal_payment
        payments.append({
            'Payment Number': i + 1,
            'Payment Amount': mortgage_payment,
            'Principal Payment': principal_payment,
            'Interest Payment': interest_payment,
            'Remaining Balance': balance
        })

    # create dataframe and render table
    df = pd.DataFrame(payments)
    
    df['Payment Amount'] = df['Payment Amount'].map(lambda x: locale.currency(x, grouping=True))
    df['Principal Payment'] = df['Principal Payment'].map(lambda x: locale.currency(x, grouping=True))
    df['Interest Payment'] = df['Interest Payment'].map(lambda x: locale.currency(x, grouping=True))
    df['Remaining Balance'] = df['Remaining Balance'].map(lambda x: locale.currency(x, grouping=True))
   
    return render_template('table.html', table=df.to_html(index=False))

if __name__ == '__main__':
    app.run(debug=True)
