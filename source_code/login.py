from flask import Flask
from flask import request
import pymysql as mysql

app = Flask(__name__)
@app.route('/login', methods=['GET'])
def login():
    try:
        # connect to data base
        con = mysql.connect(host="172.19.0.1", port=3306, user="ruthvik", password="ruthvik", database="login")
        username = request.args.get('username')
        password = request.args.get('password')
        sql = "select * from userinfo where username='" + username + "' and password='" + password + "'"
        print(username)
        print(password)
        print(sql)
        # get cursor object
        c = con.cursor()
        # getdata
        c.execute(sql)
        rows=c.fetchall()
        print(len(rows))
        if len(rows)==0:
            return "False"

        # close database connection
        con.close()

    except Exception as e:
        print(e)
        return "False"
    return "True"
@app.route('/register', methods=['GET'])
def register():
    try:
        #connect to data base
        con=mysql.connect(host="172.19.0.1",  port=3306, user="ruthvik", password="ruthvik", database="login")
        username = request.args.get('username')
        password = request.args.get('password')
        email = request.args.get('email')
        phone = request.args.get('mobile_no')
        sql = "insert into userinfo values('"+username+"','"+password+"','"+email+"','"+phone+"')"
        print(username)
        print(password)
        print(email)
        print(phone)

        #get cursor object
        c=con.cursor()
        #execute Query
        c.execute(sql)
        con.commit()
        #close database connection
        con.close()

    except Exception as e:
        print(e)
        return "False"
    return "True"


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=5000)
