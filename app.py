from flask import Flask,render_template,request
import ibm_db

app=Flask(__name__)


conn = ibm_db.connect("database=bludb;hostname=1bbf73c5-d84a-4bb0-85b9-ab1a4348f4a4.c3n41cmd0nqnrk39u98g.databases.appdomain.cloud;port=32286;uid= cwd82900;password= LVYepyczmohk8k5i;security= SSL;sslcertificate = DigiCertGlobalRootCA.crt","","")
if conn:
    print("CONNECTION SUCCESSFUL")
else:
    print("NOT SUCCESS")


@app.route("/")
def index():
    return render_template('register.html')

@app.route("/register",methods=['POST','GET'])
def register():
   
    email = request.form['email']
    name = request.form['username']
    password = request.form['password']

    rd = [email,name,password]
    print(rd)

    sql = "select * from register_table where email = ?"
    stmt = ibm_db.prepare(conn, sql)
    ibm_db.bind_param(stmt, 1, email)
    ibm_db.execute(stmt)
    account = ibm_db.fetch_assoc(stmt)
    print(account)
    if account:
        msg = "Already Registered"
        return render_template('login.html',msg = msg)
            # return "Not registerd"
    else:
        sql = 'insert into register_table values (?, ?, ?)'
        stmt = ibm_db.prepare(conn, sql)

        ibm_db.bind_param(stmt, 1, email)
        ibm_db.bind_param(stmt, 2, name)
        ibm_db.bind_param(stmt, 3, password)
        ibm_db.execute(stmt)
        msg = "Successfully registered use same credentials for login"
        return render_template('login.html',msg=msg)


@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == 'POST': 
        name = request.form.get('username')
        password = request.form.get('password')
        # Check if credentials exist in DB2
        
        sql1 = "SELECT * FROM REGISTER_TABLE WHERE USERNAME = ? AND PASSWORD = ?"
        stmt = ibm_db.prepare(conn,sql1)
        ibm_db.bind_param(stmt, 1,name)
        ibm_db.bind_param(stmt, 2, password)
        ibm_db.execute(stmt)
        row = ibm_db.fetch_assoc(stmt)
        # ibm_db.close(conn)

        if row:
            msg1 = "Login Successfull"
            return render_template('login.html',msg=msg1)
        else:
            msg2 = "Invalid credentials, Please try again"
            return render_template('login.html',msg=msg2)
        
    return render_template('login.html')

if __name__=='__main__':
    app.run(debug=True)