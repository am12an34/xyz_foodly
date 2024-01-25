from flask import*
import pyrebase
from functools import wraps
app = Flask(__name__)

app.secret_key = 'Fo**-+8/'
#pyrebaseconfiguration
firebase_config = {
    "apiKey": "AIzaSyBE8OPJ0Z_yVcJTDlN4kKX_yLx3SvYmrrQ",
    "authDomain": "foodly-a5923.firebaseapp.com",
    "databaseURL": " ",
    "projectId": " ",
    "storageBucket": " ",
    "messagingSenderId": " ",
    "appId": " ",
}
firebase = pyrebase.initialize_app(firebase_config)
Auth = firebase.auth()
#----------------------------------------------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' in session:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def registration_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' in session:
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
        return render_template('resturants.html') 
    else:
        return redirect(url_for('login'))

@app.route("/resturants")
def resturants():
    if "user" in session:
        return render_template('resturants.html') 
    else:
        return redirect(url_for('login'))

@app.route("/resturants/resturantinfo")
def resturantsinfo():
        if "user" in session:
            return render_template('resturantinfo.html')
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
            print(session['user'])
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
            return redirect(url_for('index'))

        except :
            return render_template('register.html',block_none="block")

    return render_template('register.html',block_none="none")
@app.route("/resturantsregister")
def landing():
        return render_template('adminsignup.html') 
@app.route('/logout')
def logout():

    session.pop('user', None)
    return redirect(url_for('login'))

@app.after_request
def add_no_cache(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response  

#----------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
