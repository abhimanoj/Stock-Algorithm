import flask
from flask import request
    
from get_highest_combined_price import *
from get_only_nifty1_data import *

app = flask.Flask(__name__)
app.config["DEBUG"] = True


#--- GET API----->
@app.route('/nifty_operation',methods=['GET'])
def nifty_operation():
    resp = nifty_operation_on_highest_combined_price()
    
    return resp

#--- GET API----->
@app.route('/', methods=['GET'])
def operation_on_highest():
     
    resp=operation_on_highest_combined_price()    

    return str(resp) 

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8000)

      