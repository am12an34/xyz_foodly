from flask import*
import pyrebase
from functools import wraps
#from adminapp import register
app = Flask(__name__)

app.secret_key = 'Fo**-+8/'
#pyrebaseconfiguration/firebase
firebase_config = {
    "apiKey": "AIzaSyBE8OPJ0Z_yVcJTDlN4kKX_yLx3SvYmrrQ",
    "authDomain": "foodly-a5923.firebaseapp.com",
    "databaseURL": "https://foodly-a5923-default-rtdb.firebaseio.com",
    "projectId": " ",
    "storageBucket": "foodly-a5923.appspot.com",
    "messagingSenderId": " ",
    "appId": " ",
}
firebase = pyrebase.initialize_app(firebase_config)
Auth = firebase.auth()
db = firebase.database()

#----------------------------------------------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' in session :
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def registration_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' in session :
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


#----------------------------------------------------
@app.route("/landing")
def landing():
        return render_template('landingpage.html') 


@app.route("/")
def index():
    if "user" in session:
        if session['admin'] == False:
            return redirect(url_for('resturants')) 
        elif session['admin'] == True:
            return redirect(url_for('resturantindex'))
    else:
        return redirect(url_for('landing'))



@app.route("/resturants")
def resturants():
    if "user" in session:
        if session["admin"] == False:
            return render_template('resturants.html') 
        else:
            return redirect(url_for('landing'))
    else:
        return redirect(url_for('login'))

@app.route("/userprofile")
def userprofile():
    if "user" in session:
        if session["admin"] == False:
            return render_template('profile.html') 
        else:
            return redirect(url_for('landing'))
    else:
        return redirect(url_for('login'))


@app.route("/previousorder")
def previousorderuser():
    if "user" in session:
        if session["admin"] == False:
            return render_template('previousorderuser.html') 
        else:
            return redirect(url_for('landing'))
    else:
        return redirect(url_for('login'))

@app.route("/yourorders")
def yourorders():
    if "user" in session:
        if session['admin'] == False:
            return render_template('yourorders.html') 
        else:
            return redirect(url_for('landing'))
    else:
        return redirect(url_for('login'))

@app.route("/resturants/resturantinfo")
def resturantsinfo():
    if "user" in session:
        if session['admin'] == False:
            return render_template('resturantinfo.html')
        else:
            return redirect(url_for('landing'))
    else:
        return redirect(url_for('login'))
      

    
@app.route("/login",methods=['GET', 'POST'])
@login_required
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            user = Auth.sign_in_with_email_and_password(email, password)
            session['user'] = user['localId']
            session['admin'] = False
            print(session)
            return redirect(url_for('index'))
        except:
            
            return render_template('login.html',block_none="block")

    return render_template('login.html',block_none="none")


@app.route("/register",methods=['GET', 'POST'])
@registration_required
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            user = Auth.create_user_with_email_and_password(email, password)
            print(user)
            session['user'] = user['localId']  
            session['admin'] = False
            return redirect(url_for('index'))

        except :
            return render_template('register.html',block_none="block")

    return render_template('register.html',block_none="none")

#-----------------------------------------------------------------------
@app.route("/resturantsdashboard/addmenu")
def resturantaddmenu():

    if session['admin'] == True:     
        if "user" in session:
            return render_template('addmenu.html') 
        else:
            return redirect(url_for('landing'))
    else:
        return redirect(url_for('landing'))

@app.route("/resturantsdashboard")
def resturantindex():

    if "user" in session:     
        if session['admin'] == True:
            return render_template('resturantsdashboard.html') 
        else:
            return redirect(url_for('landing'))
    else:
        return redirect(url_for('landing'))



@app.route("/resturantsregister",methods=['GET', 'POST'])
@registration_required
def resturantsregister():
        if request.method == 'POST':
                email = "admin."+request.form['email']
                password = request.form['password']
                resturantname=request.form['resturantname']
                resturantcuisine=request.form['resturantcuisine']
                try:
                    user = Auth.create_user_with_email_and_password(email, password)
                    #print(user)
                    session['user'] = user['localId']
                    session['admin'] = True
                    #resturant_data = {"resturantcuisine": resturantcuisine}
                    #db.child("resturants").child(resturantname).set(resturant_data)
                    return redirect(url_for('resturantindex'))
                except :
                    return render_template('resturantsregister.html',block_none="block")

        return render_template('resturantsregister.html',block_none="none")

@app.route("/resturantslogin",methods=['GET', 'POST'])
@login_required
def resturantslgoin():
        if request.method == 'POST':
                email = "admin."+request.form['email']
                password = request.form['password']
                print(email)
                print(password)
                try:
                    user = Auth.sign_in_with_email_and_password(email, password)
                    session['user'] = user['localId']
                    session['admin'] = True
                    return redirect(url_for('resturantindex'))
                except :
                    return render_template('resturantslogin.html',block_none="block")

        return render_template('resturantslogin.html',block_none="none")


#-----------------------------------------------------------------------

@app.route('/logout')
def logout():

    session.pop('user', None)
    return redirect(url_for('landing'))

'''@app.after_request
def add_no_cache(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response  
'''
#----------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)

