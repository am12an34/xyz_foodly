from flask import*
from functools import wraps
app = Flask(__name__)

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

@app.route("/")
def index():
    return redirect(url_for('login'))
    
@app.route("/login")
@login_required
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        #database er kaaj korbo...
        
    return render_template('login.html')

@app.route("/register")
@registration_required
def register():
    return render_template('signup.html',block_none="none")

#----------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
