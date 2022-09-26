from flask import Flask, render_template,request
from flask_mysqldb import MySQL
import yaml


app = Flask(__name__)

db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/',methods=['GET','POST'])

def index():
    if request.method == 'POST':
        hday1 = request.form
        name=hday1['name']
        date=hday1['date']
        cur = mysql.connection.cursor()
        cur.execute("insert into holiday_db.holiday(h_name,h_date) values(%s,%s)",(name,date))
        mysql.connection.commit()
        cur.close()
        return 'success'
    return render_template('index.html')


@app.route('/holiday')

def holiday():
    cur = mysql.connection.cursor()
    hday = cur.execute("SELECT * FROM holiday_db.holiday")
    
    if hday > 0:
        hday1 = cur.fetchall()
        return render_template('holiday.html', hday1=hday1)


@app.route('/leave',methods=['GET','POST'])

def leave():
    if request.method == 'POST':
        lday = request.form
        eid=lday['eid']
        name=lday['name']
        date=lday['date']
        cur = mysql.connection.cursor()
        cur.execute("insert into holiday_db.leave(e_id,l_name,l_date) values(%s,%s,%s)",(eid,name,date))
        mysql.connection.commit()
        cur.close()
        return 'success'
    return render_template('leave.html')

@app.route('/leave_list')

def leave_list():
    cur = mysql.connection.cursor()
    lday1 = cur.execute("SELECT * FROM holiday_db.leave")
    if lday1 > 0:
        lday = cur.fetchall()
        return render_template('leave_list.html', lday=lday)
    return 'NO Leave Applied'

@app.route('/cal')

def cal():
    # yy = 2022
    # mm = 9
    # print(calendar.month(yy, mm))
    return render_template('cal.html')
    
if __name__ == '__main__':
    app.run(debug = True)


