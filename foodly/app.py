from flask import*
import pyrebase
from functools import wraps

#from adminapp import register
app = Flask(__name__)

app.secret_key = 'Fo**-+8/'
#pyrebaseconfiguration/firebase
firebase_config = {
    "apiKey": "",
    "authDomain": "",
    "databaseURL": "",
    "projectId": " ",
    "storageBucket": "",
    "messagingSenderId": " ",
    "appId": " ",
}
firebase = pyrebase.initialize_app(firebase_config)
Auth = firebase.auth()
db = firebase.database()
st= firebase.storage()

#----------------------------------------------------
def login_requiredadmin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' in session :
            return redirect(url_for('admindashboard'))
        return f(*args, **kwargs)
    return decorated_function

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


#----------------------------------------------------users
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
            return redirect(url_for('admindashboard'))
    else:
        return redirect(url_for('landing'))


@app.route("/resturants")
def resturants():
    if "user" in session:
        if session["admin"] == False:
            all_resturants=[]
            ar=db.child("resturants").get()
            for r in ar.each():
                r.val()["resturantimageurl"]=st.child("resturants/" + r.key()+"/"+"profile.png").get_url(None)
                all_resturants.append(r.val())
            return render_template('resturants.html',all_resturants=all_resturants) 
        else:
            return redirect(url_for('landing'))
    else:
        return redirect(url_for('login'))

@app.route("/userprofile",methods=['POST','GET'])
def userprofile():
    if "user" in session:
        if session["admin"] == False:
            if request.method == 'POST':

                if 'file' in request.files:
                    file = request.files['file']
                    if file.filename != '':
                        st.child("users/" + session['user']+"/"+"profile.png").put(file)
                username = request.form['username']
                address = request.form['address']
                phone = request.form['phone']
                if len(username)!=0:
                    db.child("users").child(session["user"]).update({"username": username})
                if len(address)!=0:
                    db.child("users").child(session["user"]).update({"useraddress": address})
                if len(phone)!=0:
                    db.child("users").child(session["user"]).update({"userphone": phone})

            userprofileimage=st.child("users/" + session['user']+"/"+"profile.png").get_url(None)

            username=db.child("users").child(session["user"]).child("username").get()
            return render_template('profile.html',username=username.val().upper(),userprofileimage=userprofileimage) 
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

@app.route("/payment")
def payment():
    if "user" in session:
        if session["admin"] == False:
            totalprice=request.args.get('totalprice')
            return render_template('payment.html',totalprice=totalprice)

        else:
            return redirect(url_for('landing'))
    else:
        return redirect(url_for('login'))

@app.route("/yourorders")
def yourorders():
    if "user" in session:
        if session['admin'] == False:
            ao=db.child("users").child(session["user"]).child("yourorders").get()
            all_items=[]
            for o in ao.each():
                #print(o.val(),"usercheckout")
                all_items.append(o.val())
            totalprice=0
            for pr in all_items:
                totalprice+=float(pr['price'])*float(pr['quantity'])
            return render_template('yourorders.html',totalprice=totalprice,all_items=all_items) 
        else:
            return redirect(url_for('landing'))
    else:
        return redirect(url_for('login'))

@app.route("/usercheckout",methods=['POST','GET'])
def usercheckout():
    if "user" in session:
        if session['admin'] == False:
            userid=session['user']
            if request.method == 'POST':
                totalprice=request.form['totalprice']
                return redirect(url_for('payment',totalprice=totalprice))
                
            
            ao=db.child("users").child(session["user"]).child("yourorders").get()
            all_items=[]
            for o in ao.each():
                #print(o.val(),"usercheckout")
                all_items.append(o.val())
            totalprice=0
            for pr in all_items:
                totalprice+=float(pr['price'])*float(pr['quantity'])

            return render_template('usercheckout.html',all_items=all_items,userid=userid,totalprice=totalprice) 
        else:
            return redirect(url_for('landing'))
    else:
        return redirect(url_for('login'))


@app.route("/resturants/<resturantid>", methods=['GET', 'POST'])
def resturantsinfo(resturantid):
    if "user" in session:
        if session['admin'] == False:
            if request.method == 'POST':
                json_data = request.get_json()
                
                db.child("users").child(session['user']).child("yourorders").set(json_data)
            #menu show karunga
            rn=db.child("resturants").child(resturantid).child("resturantname").get()
            rc=db.child("resturants").child(resturantid).child("resturantcuisine").get()
            all_menus=[]
            am=db.child("resturants").child(resturantid).child("resturantmenu").get()
            
            if am.val()!=None:
                for m in am.each():
                    
                    m.val()["menuimageurl"]=st.child("resturants/"+resturantid+"/menu/"+m.key()+".png").get_url(None)
                    all_menus.append(m.val())
                

            return render_template('resturantinfo.html',all_menus=all_menus,resturantname=rn.val(),resturantcuisine=rc.val())
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
            
            
            return redirect(url_for('index'))
        except:
            
            return render_template('login.html',block_none="block")

    return render_template('login.html',block_none="none")


@app.route("/register",methods=['GET', 'POST'])
@registration_required
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        try:
            user = Auth.create_user_with_email_and_password(email, password)
           
            session['user'] = user['localId']  
            session['admin'] = False
            user_data = {"username": name,"userphone":"","useraddress":""}
            db.child("users").child(session['user']).set(user_data)
            return redirect(url_for('index'))

        except :
            return render_template('register.html',block_none="block")

    return render_template('register.html',block_none="none")

#-----------------------------------------------------------------------resturantadmin
@app.route("/resturantactiveorders")
def resturantactiveorders():

    if "user" in session:     
        if session['admin'] == True:
            ao=db.child("users").child(session["user"]).child("yourorders").get()
            all_items=[]
            for o in ao.each():
                #print(o.val(),"usercheckout")
                all_items.append(o.val())
            return render_template('resturantactiveorders.html') 
        else:
            return redirect(url_for('landing'))
    else:
        return redirect(url_for('landing'))


@app.route("/resturantsdashboard")
def resturantsstats():

    if "user" in session:     
        if session['admin'] == True:
            return render_template('resturantsstats.html') 
        else:
            return redirect(url_for('landing'))
    else:
        return redirect(url_for('landing'))


@app.route("/resturantsdashboard/addmenu",methods=['POST','GET'])
def resturantaddmenu():

    if session['admin'] == True:     
        if "user" in session:
            if request.method == 'POST':
                itemname = request.form['itemname']
                itemprice = request.form['itemprice']
                itemdescription = request.form['itemdescription']
                if 'file' in request.files:
                    file = request.files['file']
                    st.child("resturants/" + session['user']+"/menu/"+itemname+".png").put(file)
                db.child("resturants").child(session['user']).child("resturantmenu").child(itemname).set({"itemname":itemname,"itemprice": itemprice,"itemdescription": itemdescription})
            all_menus=[]
            am=db.child("resturants").child(session['user']).child("resturantmenu").get()
            
            if am.val()!=None:
                for m in am.each():
                    
                    m.val()["menuimageurl"]=st.child("resturants/"+session['user']+"/menu/"+m.key()+".png").get_url(None)
                    all_menus.append(m.val())
                



            return render_template('addmenu.html',all_menus=all_menus) 
        else:
            return redirect(url_for('landing'))
    else:
        return redirect(url_for('landing'))


@app.route("/resturantprofile",methods=['POST','GET'])
def resturantprofile():

    if "user" in session:     
        if session['admin'] == True:
            if request.method == 'POST':
                if 'file' in request.files:
                    file = request.files['file']
                    if file.filename != '':
                        st.child("resturants/" + session['user']+"/"+"profile.png").put(file)
                resturantname = request.form['resturantname']
                resturantphone = request.form['resturantphone']
                if len(resturantname)!=0:
                    db.child("resturants").child(session["user"]).update({"resturantname": resturantname})
                if len(resturantphone)!=0:
                    db.child("resturants").child(session["user"]).update({"resturantphone": resturantphone})

    
            resturantimage=st.child("resturants/" + session['user']+"/"+"profile.png").get_url(None)
           
            resturantname=db.child("resturants").child(session["user"]).child("resturantname").get()
            resturantaddress=db.child("resturants").child(session["user"]).child("resturantaddress").get()
            resturantphone=db.child("resturants").child(session["user"]).child("resturantphone").get()

            return render_template('resturantprofile.html',resturantaddress=resturantaddress.val().capitalize(),resturantname=resturantname.val().upper(),resturantphone=resturantphone.val(),resturantimage=resturantimage)

        else:
            return redirect(url_for('landing'))
    else:
        return redirect(url_for('landing'))


@app.route("/resturantsdashboard")
def resturantindex():

    if "user" in session:     
        if session['admin'] == True:
            return redirect(url_for('resturantsstats')) 
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
                resturantaddress=request.form['resturantaddress']
                try:
                    user = Auth.create_user_with_email_and_password(email, password)
                    #print(user)
                    session['user'] = user['localId']
                    session['admin'] = True
                    resturant_data = {"resturantid":session['user'],"resturantname": resturantname,"resturantcuisine": resturantcuisine,"resturantaddress":resturantaddress}
                    db.child("resturants").child(session['user']).set(resturant_data)
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
              
                try:
                    user = Auth.sign_in_with_email_and_password(email, password)
                    session['user'] = user['localId']
                    session['admin'] = True
                    return redirect(url_for('resturantindex'))
                except :
                    return render_template('resturantslogin.html',block_none="block")

        return render_template('resturantslogin.html',block_none="none")


#-----------------------------------------------------------------------projectadmin
@app.route("/adminresturantsrequest")
def adminresturantrequest():
    if "user" in session:
        if session['projectadmin'] == True:
            return render_template('adminresturantrequest.html') 
        else:
            return redirect(url_for('landing'))
    else:
        return redirect(url_for('landing'))
@app.route("/adminresturants",methods=['POST','GET'])
def adminresturants():
    if "user" in session:
        if session['projectadmin'] == True:
            all_resturants=[]
            ar=db.child("resturants").get()
            if ar.val()!=None:
                for r in ar.each():
                    r.val()["resturantid"]=r.key()
                    r.val()["resturantimageurl"]=st.child("resturants/" + r.key()+"/"+"profile.png").get_url(None)
                    all_resturants.append(r.val())
                
            if request.method == 'POST':
                resturantid=request.form['resturantid']#databse se ura do......
                #db.child("resturants").child(resturantid).remove()
                #st.child("resturants/"+resturantid).delete()
                #Auth.delete_user(resturantid)
            return render_template('adminresturants.html',all_resturants=all_resturants) 
        else:
            return redirect(url_for('landing'))
    else:
        return redirect(url_for('landing'))

@app.route("/admindashboard")
def admindashboard():
    if "user" in session:
        if session['projectadmin'] == True:
            return redirect(url_for('adminresturants'))
        else:
            return redirect(url_for('landing'))
    else:
        return redirect(url_for('landing'))


@app.route("/adminlogin",methods=['GET', 'POST'])
@login_requiredadmin
def adminlgoin():
        if request.method == 'POST':
                email = "projectadmin."+request.form['email']
                password = request.form['password']
               
                try:
                    user = Auth.sign_in_with_email_and_password(email, password)
                    session['user'] = user['localId']
                    session['projectadmin'] = True
                    session['admin']='TrueAdmin'

                    return redirect(url_for('admindashboard'))
                except :
                    return render_template('adminlogin.html',block_none="block")

        return render_template('adminlogin.html',block_none="none")
#-----------------------------------------------------------------------

@app.route('/logout')
def logout():

    session.pop('user', None)
    return redirect(url_for('landing'))

@app.after_request
def add_no_cache(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response  

#----------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)

