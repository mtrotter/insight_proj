from flask import render_template, session
from app import app, host, port, user, passwd, db
from app.helpers.database import con_db, query_db
import flask_wtf
from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig
from wtforms.validators import Required
from flask_wtf import Form
import wtforms
from wtforms import SelectField, TextField, TextAreaField, IntegerField
from flask import request
from app.helpers.filters import format_currency
import jinja2
import pickle
import numpy as np
from flask import render_template, _app_ctx_stack, jsonify, request
from operator import itemgetter
import math
import random
import csv
import os 
# To create a database connection, add the following
# within your view functions:
# con = con_db(host, port, user, passwd, db)


#ROUTING/VIEW FUNCTIONS

#@app.route('/index')
#def index():

#    return render_template('index.html')
@app.route('/', methods=['POST','GET'])
@app.route('/home', methods=['POST','GET'])
def home():
    form=request.form

    
        #session[key] = value

    










    return render_template('home.html',form=form)


# @app.route('/test')
# def index():
#     return render_template('test.html')



# def process(string):
#     """
#     This is essentially the main query/processing function that acts on the input. In this example, a dictionary of
#     links and text is returned, which is then combined to form a HTML link using jQuery. Modify the dictionary and the
#     JS functions as per your needs.
#     :param string: string
#     :return: dict
#     """
#     if len(string) is 3:
#         return {
#             'results': [{'link': '#', 'text': 'Character {i}: {s}'.format(i=i + 1, s=s)} for i, s in enumerate(string)]

#         }
#     else:
#         raise ValueError

# @app.route('/results', methods=['POST'])
# def results():
#     """
#     The values from the input fields/text areas/check boxes, etc. on the main page are retrieved using request.form.
#     The keys for the dictionary are the same as that used in the JS function (line 36 in index.html).
#     """
#     return jsonify(process(request.form['input']))


@app.route('/slides')
def slides():
    return render_template('myslides.html')

@app.route('/author')
def author():
    return render_template('author.html')
@app.route('/more')
def more():
    return render_template('more.html')

@app.route('/predict', methods=['GET','POST'])
def predict():
    #set defaults for analysis
    #print(request.form)
    #print(request.form['fbcon'])
   # defaultvecs = set_Defaults()
    #kickdefault = defaultvecs[0]
    #indiedefault = defaultvecs[1]

    for key, value in request.form.iteritems():
        if key == 'input-name':
            session[key] = (value)
        else:
            session[key]=float(value)

   # session['bodylen_kick']=3600
    #session['bodylen_ind']=6600
    IndieBodyLen = session['bodylen']
    KickBodyLen = session['bodylen']
    #print(session)


    if int(session["fbcon"]) == 1:
        userFbCon=1
        #print('yes')
    else:
         userFbCon=0
    #print(request.form)

    #Process form data
    #userTitle = str(session['input-name'])
   
    inputcat = session['category']
    if inputcat == 2: #technology
        indieUserCat = 19
        session['indieUserCat']=19
        kickUserCat = 13
        session['kickUserCat']=13
    elif inputcat == 1: #art
        indieUserCat  = 1
        session['indieUserCat']=1
        kickUserCat = 0
        session['kickUserCat']=0
    elif inputcat == 3: #music
        indieUserCat = 14
        session['indieUserCar']=14
        kickUserCat = 10
        session['kickUserCat']=10
    elif inputcat >3:
        indieUserCat = 8 #arbitrary lie
        session['indieUserCat']=8
        kickUserCat = 8 #arbitrary lie
        session['kickUserCat']=8
    
    userTshirt = session['tshirt']
    userTshirt = 0
    userVids = int(session['nvids'])
    if userVids>0:
        session['hasvid'] = 1
        userHasVid=1
    else:
        userHasVid = 0
        session['hasvid']=0
    userLinks = int(session['nlinks'])
    if userLinks >0:
        userHasWeb = 1
        session['hasweb']=1
    else:
        userHasWeb=0
        session['hasweb']=0
   
    userPics = int(session['npics'])
    userFbFriends = int(session['fbfriends'])
    
    if userFbFriends > 0:
        userConFb = 1
    else:
        userConFb = 0
    userNRewards = session['perks']
    user500 = 0
    user200 = 0
    session['u500']=0
    session['u200']=0
    if session['perks']>2:
        user500=1
        user200=1
        session['u500']=1
        session['u200']=1

    userDuration = int(session['duration'])

    userGoal = float(session['goal'])

    #userNRewards = session['perks']
    # user500 = session['big_rewards']
    # user200 = session['med_rewards']

    #print(session['duration'])
    # THESE MUST BE REORDERED ALPHABETICALLY AND ADD NVIDEOS=userVids IN THERE TOO!
    indie_vector =np.array([[KickBodyLen, userConFb, userGoal, userHasVid, userHasWeb, indieUserCat, userNRewards, userFbFriends, userPics, userLinks, userVids, userDuration, user200, user500, userTshirt]])
    kick_vector = np.array([[IndieBodyLen, userConFb, userGoal, userHasVid, userHasWeb, kickUserCat, userNRewards, userFbFriends, userPics, userLinks, userVids, userDuration, user200, user500, userTshirt]])
    #print(indie_vector)

    kick_win = app.kick_classify.predict_proba(kick_vector)[0][1]

    indie_win = app.indie_classify.predict_proba(indie_vector)[0][1]

    #print(indie_win)
  
    #print(type(userTitle))
    if kick_win > indie_win:
        verdict = "If it was me, I'd Kick it"
    else:
        verdict = "Looks like you should definitely GoGo"

    kick_cash = app.kick_regress.predict(kick_vector)*userGoal
    indie_cash = app.indie_regress.predict(indie_vector)*userGoal




    



   

    return render_template('predict.html', indiewin = indie_win, kickwin = kick_win, kickcash = kick_cash, indiecash = indie_cash, verdict = verdict)


@app.route("/eval", methods=['POST','GET'])
def eval():

    
    #NOTE loan amount = goal
    #repayment term = duration for indie, perks for kick
    print(session)
    indicator = request.form['button']
    #print(type(session['goal']))
    
   
    
    requested_loan_amount = float(session['goal'])
   
    if indicator == "Indiegogo":
        requested_repayment_term = float(session['bodylen'])
        xlabelstr = "Story Length"
        print session['bodylen']
        siteind = 1
    else:
        requested_repayment_term = float(session['perks'])
        print session['perks']
        xlabelstr = "Number of Perks Offered"
        siteind = 0
   
  
   # if requested_repayment_term >=2000:
    if siteind ==  1: #indiegogo
         month_pred = [500*(i+1) for i in range(20)]
         gridxpad = -1
         friendbin = 500
         midpoint = 500
    # elif requested_repayment_term >=1000:
    #      month_pred = [100*(i+1) for i in range(20)]
    #      gridxpad = -1
    #      friendbin = 100
    #      midpoint = 1000
    # elif requested_repayment_term >=500:
    #      month_pred = [50*(i+1) for i in range(20)]
    #      gridxpad = -1.0
    #      friendbin = 50
    #      midpoint = 500
    # elif requested_repayment_term >= 250:
    #   #  month_pred = [15*i +(requested_repayment_term-100) for i in range(20)]
    #      month_pred = [25*(i+1) for i in range(20)]
    #      gridxpad = -1.1
    #      friendbin =15
    #      midpoint = 150
    else:
        month_pred = [5*(i+1) for i in range(20)]
        gridxpad = -1.25
        friendbin = 5
        midpoint = 50


    if requested_loan_amount >=50000:
        interval = 5000
    elif requested_loan_amount >=1000:
        interval = 1000
    elif requested_loan_amount >=500:
        interval = 100
    else:
        interval = 50

    binreqLoanAmount=int(round(requested_loan_amount,-2)/interval)
    roundedReqAmt = int(math.floor(requested_loan_amount/interval))

    if binreqLoanAmount >= 10:
        gridAmtSet = binreqLoanAmount
    else:
        gridAmtSet = 5
   

    amount_pred = [interval*(i+1) for i in range(gridAmtSet-5,gridAmtSet+5)]
   

    print gridAmtSet
    #print(indicator)
    #create list of tuples for (amount, month, funding prob )
    predMatrix=[]
    for amount in amount_pred:
        for month in month_pred:
            
            #month = duration, amount = goal
            indie_vector =np.array([[session['bodylen_ind'], session['fbcon'], amount, session['hasvid'], session['hasweb'], session['indieUserCat'], session['perks'], session['fbfriends'], session['npics'], session['nlinks'], session['nvids'], month, session['u200'], session['u500'], session['tshirt']]])
            kick_vector = np.array([[session['bodylen_kick'], session['fbcon'], amount, session['hasvid'], session['hasweb'], session['kickUserCat'], month, session['fbfriends'], session['npics'], session['nlinks'], session['nvids'], session['duration'], session['u200'], session['u500'], session['tshirt']]])

            #print(kick_vector)
            #xin = np.append(continent_vec,sector_vec)
            #xin = np.append(xin,np.array( [borrowers_gender,loan_info[0]['description_num_languages'],amount,posted_date_months,month ] ))

            
            #xin = np.array( [borrower_gender_map[loan_info[0]['borrowers_gender']],loan_info[0]['description_num_languages'],amount,country_map[loan_info[0]['location_country']], sector_map[loan_info[0]['sector']],activity_map[loan_info[0]['activity']],posted_date_months,loan_info[0]['partner_id'],month ]  )
            if indicator =="Indiegogo":
                predprob = round(app.kick_classify.predict_proba(kick_vector)[0][1],2)
            else:
                predprob = round(app.indie_classify.predict_proba(kick_vector)[0][1],2)
                
            #predprob = round(app.indie_classify.predict_proba(indie_vector)[0][1],1)
            #print(predprob)
            predMatrix.append((amount, month, predprob) )
    print(indicator)
    # write to tsv file
    ofile  = open('app/static/data.tsv', "wb")
    writer = csv.writer(ofile,delimiter='\t')

    writer.writerow(['day','hour', 'value'])
    for row in predMatrix:
                writer.writerow(row)
    ofile.close()

    amount_pred_str = str(amount_pred)
    month_pred_str = str(month_pred)
    print(amount_pred_str)
    print(month_pred_str)

    
    return render_template('eval.html', interval = interval, otherthing = siteind, roundedReqAmt=roundedReqAmt,requested_repayment_term=requested_repayment_term,gridAmtSet=gridAmtSet,amount_pred_str=amount_pred_str,month_pred_str=month_pred_str,binreqLoanAmount=binreqLoanAmount, gridxpad= gridxpad, friendbin = friendbin)

@app.route('/process', methods=['GET','POST'])
def process():
    #input_string = request.form['input-name']  
    #print request.form #This request has the data from the form in home.html

    #user_cat = request.form['category']
   
    userTitle = request.form['input-name']
    userCat = request.form['category']
    





    # Create database connection

    con = con_db(host, port, user, passwd, db)

    # Add custom filter to jinja2 env
    jinja2.filters.FILTERS['format_currency'] = format_currency

    var_dict_whole = {
        "category": request.args.get("category"),
        "goal": request.args.get("goal", '0'),
        "tshirt": request.args.get("tshirt", '0'),
        "nlinks": request.args.get("nlinks", '0'),
        "order_by": request.args.get("order_by", "goal"),
        "sort": request.args.get("sort", "DESC")
    }
    var_dict = {
        "category": request.args.get("category"),
        "goal": request.args.get("goal", '0'),
        "tshirt": request.args.get("tshirt", '0'),
        "nlinks": request.args.get("nlinks", '0'),
        "order_by": request.args.get("order_by", "goal"),
        "sort": request.args.get("sort", "DESC")
    }

    # Query the database
    data = query_db(con, var_dict_whole, usercat=user_cat)
   # data_for_sort = query_db_usercat(con, var_dict, user_cat)
    # Add data to dictionary
    #var_dict["data"] = data_for_sort
    var_dict_whole["data"]=data

   # return render_template('process.html', form = request.form)
    return render_template('process.html', settings=var_dict, sort_settings=var_dict_whole)


def set_Defaults():
    #userTitle = str(request.form['input-name'])
    kick_vector = np.zeros((1,13))
    indievector = np.zeros((1,13))

        
    userCat = 0
    userTshirt = 1   
    userVids = 3
    if userVids>0:
        userHasVid = 1
    else:
        userHasVid = 0
    userLinks = 3
    if userLinks >0:
        userHasWeb = 1
    else:
        userHasWeb=0
    userPics = 1
    userFbFriends = 250
    if userFbFriends > 0:
        userConFb = 1
    else:
        userConFb = 0
    userDuration = 30
    userGoal = 3000
    userNRewards = 15
    user500 = 3
    user200 = 2

    indie_vector =np.array([[userTshirt, userFbFriends, user200, userHasWeb, userConFb, userHasVid, userDuration, userGoal, userNRewards, userPics, userLinks, user500, userCat]])
    kick_vector = np.array([[userTshirt, userFbFriends, user200, userGoal, userConFb, userHasVid, userDuration, userPics, userHasWeb, userNRewards, userLinks, user500, userCat]])
    veclist = [kick_vector, indie_vector]

    return veclist




   
