from flask import Flask, render_template, request, url_for

import requests
import pandas as pd 
import datetime
import time


app = Flask(__name__)

first_date = datetime.datetime(2019,1,7)
current_date = datetime.datetime.now()#.strftime('%Y-%m-%d')
trading_days = int((current_date - first_date).days * 0.7)
calendar_days = (current_date - first_date).days

@app.route('/')
def get_investors():

    investors = ['Grant','Paul','Bret','Dave','Stef','Nan','Jon']
    return render_template('Investors.html',investors=investors)

@app.route('/<string:investor_name>/metrics/')
def investors_metrics(investor_name):

    login = requests.get('https://www.myfxbook.com/api/login.json?email=robbieslaney@gmail.com&password=Trader1')
    session = login.json()['session']
    account = requests.get('https://www.myfxbook.com/api/get-my-accounts.json?session={}'.format(session))
    info = account.json()
    accounts = info['accounts']
    TP3 = []
    for item in accounts:
        if item['name'] == 'Jon M':
            TP3.append(item)
        
    balance = TP3[0]['balance']
    profits = TP3[0]['profit']
    investors_profits = profits * 0.5 
    deposits = TP3[0]['deposits']
    investors_net_gain_percentage = investors_profits / deposits
    investors_net_gain_percentage = investors_profits / deposits
    calendar_daily_gain = investors_net_gain_percentage/ calendar_days
    trading_daily_gain = investors_net_gain_percentage/ trading_days
    gain = TP3[0]['gain'] /100
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    if investor_name == 'Grant':
        grant_deposits = 75000
        grant_profits = investors_profits * 0.68
        grant_balance = grant_deposits + grant_profits
        grant_gain = grant_profits/grant_deposits
        #daily_gain = grant_profits/calendar_days
        return render_template('metrics_by_investor.html', balance=balance, profits=profits,deposit = deposits,
                            investor_id=investor_name,my_deposits = grant_deposits,
                            gain=gain,date=date, my_balance = grant_balance,my_profit=grant_profits, my_gain=grant_gain,
                            trading_daily_gain = trading_daily_gain,daily_gain = calendar_daily_gain)

    elif investor_name == 'Dave':
        dave_deposits = 5000
        dave_profits = investors_profits * 0.0453
        dave_balance = dave_deposits + dave_profits
        dave_gain = dave_profits/dave_deposits
        #daily_gain = dave_profits/calendar_days
        return render_template('metrics_by_investor.html', balance=balance, profits=profits,deposit = deposits,
                            investor_id=investor_name,my_deposits = dave_deposits,
                            gain=gain,date=date, my_balance = dave_balance,my_profit=dave_profits, my_gain=dave_gain,
                            trading_daily_gain = trading_daily_gain, daily_gain = calendar_daily_gain)
  
    elif investor_name == 'Paul':
        paul_deposits = 10000
        paul_profits = investors_profits * 0.0907
        paul_balance = paul_deposits + paul_profits
        paul_gain = paul_profits/paul_deposits
        #daily_gain = paul_profits/calendar_days
        return render_template('metrics_by_investor.html', balance=balance, profits=profits,deposit = deposits,
                            investor_id=investor_name,my_deposits = paul_deposits,
                            gain=gain,date=date, my_balance = paul_balance,my_profit=paul_profits, my_gain=paul_gain,
                            trading_daily_gain = trading_daily_gain, daily_gain = calendar_daily_gain)

    elif investor_name == 'Bret':
        bret_deposits = 2800
        bret_profits = investors_profits * 0.0254
        bret_balance = bret_deposits + bret_profits
        bret_gain = bret_profits/bret_deposits
        #daily_gain = bret_profits/calendar_days
        return render_template('metrics_by_investor.html', balance=balance, profits=profits,deposit = deposits,
                            investor_id=investor_name,my_deposits = bret_deposits,
                            gain=gain,date=date, my_balance = bret_balance,my_profit=bret_profits, my_gain=bret_gain,
                            trading_daily_gain = trading_daily_gain, daily_gain = calendar_daily_gain)
    
    elif investor_name == 'Stef':
        steff_deposits = 7500
        steff_profits = investors_profits * 0.068
        steff_balance = steff_deposits + steff_profits
        steff_gain = steff_profits/steff_deposits
        #daily_gain = steff_profits/calendar_days
        return render_template('metrics_by_investor.html', balance=balance, profits=profits,deposit = deposits,
                            investor_id=investor_name,my_deposits = steff_deposits,
                            gain=gain,date=date, my_balance = steff_balance,my_profit=steff_profits, my_gain=steff_gain,
                            trading_daily_gain = trading_daily_gain, daily_gain = calendar_daily_gain)

    elif investor_name == 'Nan':
        nan_deposits = 5000
        nan_profits = investors_profits * 0.04053
        nan_balance = nan_deposits + nan_profits
        nan_gain = nan_profits/nan_deposits
        #daily_gain = nan_profits/calendar_days
        return render_template('metrics_by_investor.html', balance=balance, profits=profits,deposit = deposits,
                            investor_id=investor_name,my_deposits = nan_deposits,
                            gain=gain,date=date, my_balance = nan_balance,my_profit=nan_profits, my_gain=nan_gain,
                            trading_daily_gain = trading_daily_gain, daily_gain = calendar_daily_gain)
    
    elif investor_name == 'Jon':
        jon_deposits = 5000
        jon_profits = investors_profits * 0.04053
        jon_balance = jon_deposits + jon_profits
        jon_gain = jon_profits/jon_deposits
        #daily_gain = jon_profits/calendar_days
        return render_template('metrics_by_investor.html', balance=balance, profits=profits,deposit = deposits,
                            investor_id=investor_name,my_deposits = jon_deposits,
                            gain=gain,date=date, my_balance = jon_balance,my_profit=jon_profits, my_gain=jon_gain,
                            trading_daily_gain = trading_daily_gain, daily_gain = calendar_daily_gain)

@app.route('/info')
def get_metrics():

    login = requests.get('https://www.myfxbook.com/api/login.json?email=robbieslaney@gmail.com&password=Trader1')
    session = login.json()['session']
    account = requests.get('https://www.myfxbook.com/api/get-my-accounts.json?session={}'.format(session))
    info = account.json()
    accounts = info['accounts']
    TP3 = []
    for item in accounts:
        if item['name'] == 'Jon M':
            TP3.append(item)
        
    balance = TP3[0]['balance']
    profits = TP3[0]['profit']
    deposits = TP3[0]['deposits']
    pips = TP3[0]['pips']
    profit_factor = TP3[0]['profitFactor']
    abs_gain = TP3[0]['absGain']
    commissions = TP3[0]['commission']
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    return render_template('metrics.html', balance = balance, profits=profits, deposits=deposits,
                            commissions = commissions,abs_gain=abs_gain, 
                            date = date, pips = pips, profit_factor= profit_factor)



if __name__ == '__main__':
    app.secret_key = 'supersecretkey'
    app.debug = False
    app.run(host='0.0.0.0', port=8000)
