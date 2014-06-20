from flask import render_template
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
    form=Form()
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
    return render_template('slides.html')

@app.route('/author')
def author():
    return render_template('author.html')

@app.route('/predict', methods=['GET','POST'])
def predict():
    #set defaults for analysis

    defaultvecs = set_Defaults()
    kickdefault = defaultvecs[0]
    indiedefault = defaultvecs[1]
    
    #Process form data
    userTitle = str(request.form['input-name'])
    #return str(request.form)
    inputcat = request.form['category']
    if inputcat == 'Technology':
        indieUserCat = 19
        kickUserCat = 13
    elif inputcat == 'Art':
        indieUserCat  = 1
        kickUserCat = 0
    elif inputcat == 'Music':
        indieUserCat = 14
        kickUserCat = 10

    #userTshirt = request.form['tshirt']
    userTshirt = 0
    userVids = 0
    if userVids>0:
        userHasVid = 1
    else:
        userHasVid = 0
    userLinks = 0
    if userLinks >0:
        userHasWeb = 1
    else:
        userHasWeb=0
    userPics = 1
    userFbFriends = int(request.form['fbfriends'])

    if userFbFriends > 0:
        userConFb = 1
    else:
        userConFb = 0
    userNRewards = 5
    user500 = 2
    user200 = 2
    userDuration = int(request.form['duration'])

    userGoal = int(request.form['goal'])

    # userNRewards = request.form['nrewards']
    # user500 = request.form['big_rewards']
    # user200 = request.form['med_rewards']


    # THESE MUST BE REORDERED ALPHABETICALLY AND ADD NVIDEOS=userVids IN THERE TOO!
    indie_vector =np.array([[userConFb, userGoal, userHasVid, userHasWeb, userNRewards, userFbFriends, userPics, userLinks, userVids, userDuration, user200, user500, userTshirt, indieUserCat]])
    kick_vector = np.array([[userConFb, userGoal, userHasVid, userHasWeb, userNRewards, userFbFriends, userPics, userLinks, userVids, userDuration, user200, user500, userTshirt, kickUserCat]])


    kick_win = app.kick_predict.predict_proba(kick_vector)[0][1]

    indie_win = app.indie_predict.predict_proba(indie_vector)[0][1]


  
    #print(type(userTitle))
    #print(userCat)
    if kick_win > indie_win:
        verdict = "You should probably Kick it"
    else:
        verdict = "You should definitely GoGo"

    return render_template('predict.html',indiewin = indie_win, kickwin = kick_win, verdict = verdict)



@app.route('/eval',methods=['GET','POST'])
def eval():
    
    
    requested_loan_amount = loan_info[0]['loan_amount']
    requested_repayment_term = loan_info[0]['terms_repayment_term']
    binreqLoanAmount=int(round(loan_info[0]['loan_amount'],-2))/100

    if requested_repayment_term > 10:
        month_pred = [i for i in range(requested_repayment_term-10,requested_repayment_term+10)]
    else:
        month_pred = [(i+1) for i in range(20)]

    roundedReqAmt = int(math.floor(requested_loan_amount/100))

    if binreqLoanAmount >= 10:
        gridAmtSet = binreqLoanAmount
    else:
        gridAmtSet = 5

    amount_pred = [100*i for i in range(gridAmtSet-5,gridAmtSet+5)]
    
    #create list of tuples for (amount, month, funding prob )
    predMatrix=[]
    for amount in amount_pred:
        for month in month_pred:
            xin = np.append(continent_vec,sector_vec)
            xin = np.append(xin,np.array( [borrowers_gender,loan_info[0]['description_num_languages'],amount,posted_date_months,month ] ))

            #xin = np.array( [borrower_gender_map[loan_info[0]['borrowers_gender']],loan_info[0]['description_num_languages'],amount,country_map[loan_info[0]['location_country']], sector_map[loan_info[0]['sector']],activity_map[loan_info[0]['activity']],posted_date_months,loan_info[0]['partner_id'],month ]  )

            predprob = round(clf.predict_proba(xin)[0][0],2)
            predMatrix.append((amount, month, predprob) )
    
    # write to tsv file
    ofile  = open('static/data.tsv', "wb")
    writer = csv.writer(ofile,delimiter='\t')

    writer.writerow(['day','hour', 'value'])
    for row in predMatrix:
                writer.writerow(row)
    ofile.close()

    amount_pred_str = str(amount_pred)
    month_pred_str = str(month_pred)

    return render_template('eval.html',loan_info=loan_info,loan_id=loan_id,roundedReqAmt=roundedReqAmt,requested_repayment_term=requested_repayment_term,gridAmtSet=gridAmtSet,amount_pred_str=amount_pred_str,month_pred_str=month_pred_str,binreqLoanAmount=binreqLoanAmount)


    return render_template('eval.html')


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
    userTshirt = 0    
    userVids = 0
    if userVids>0:
        userHasVid = 1
    else:
        userHasVid = 0
    userLinks = 0
    if userLinks >0:
        userHasWeb = 1
    else:
        userHasWeb=0
    userPics = 1
    userFbFriends = 25
    if userFbFriends > 0:
        userConFb = 1
    else:
        userConFb = 0
    userDuration = 30
    userGoal = 1000
    userNRewards = 5
    user500 = 1
    user200 = 1

    indie_vector =np.array([[userTshirt, userFbFriends, user200, userHasWeb, userConFb, userHasVid, userDuration, userGoal, userNRewards, userPics, userLinks, user500, userCat]])
    kick_vector = np.array([[userTshirt, userFbFriends, user200, userGoal, userConFb, userHasVid, userDuration, userPics, userHasWeb, userNRewards, userLinks, user500, userCat]])
    veclist = [kick_vector, indie_vector]

    return veclist




   