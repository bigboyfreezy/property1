import pymysql
from flask import *
from connection import conn
from crypt import verify_password,hash_password
from test import password_generator

con = pymysql.connect(host='localhost', user='root', password='', database='property')

app = Flask(__name__)
app.secret_key = 'A+4#s_T%P8g0@o?6'

# Admin routes.................

@app.route('/')
def index():
    if check_admin_agency_agent():

        return render_template('index.html')
    else:
       return redirect('/main')


@app.route ('/main')
def main():
    return render_template('main.html')



@app.route('/logout')
def logout():
    if check_admin():
        session.pop('admin_id')
        session.pop('email')
        session.pop('fname')
        session.pop('lname')
        return redirect('/main')
    elif check_agency():
        session.pop('agency_id')
        session.pop('email')
        session.pop('fname')
        session.pop('lname')
        return redirect('/main')
    else:
        session.clear()
        return redirect('/main')


@app.route('/profile')
def profile():
    if check_admin():
        sql = 'select * from admin where admin_id = %s'
        cursor = conn().cursor()
        session_key = session['admin_id']
        cursor.execute(sql, (session_key))
        row = cursor.fetchone()
        return render_template('profile.html', row=row)
    else:
        return redirect('/login')


@app.route('/changepassword', methods = ['POST', 'GET'])
def changepassword():
    if check_admin():
        if request.method == 'POST':
            session_key = session['admin_id']
            currentpassword = request.form['currentpassword']
            newpassword = request.form['newpassword']
            confirmpassword = request.form['confirmpassword']

            sql = 'select * from admin where admin_id = %s'
            cursor = conn().cursor()
            cursor.execute(sql, (session_key))
            if cursor.rowcount==0:
                return redirect('/logout')
            else:
                # fetchpassword..just one
                row = cursor.fetchone()
                hashed_password = row[4]
                # verify the hashed and the password if they match
                status = verify_password(hashed_password, currentpassword)
                if status == True:
                    # if new pass is not the same as confirm pass then they dont math and u render the template
                    if newpassword !=confirmpassword:
                        flash('The password dont match', 'danger')
                        return render_template('changepassword.html')
                    else:
                        con = pymysql.connect(host='localhost', user='root', password='', database='property')
                        sql = 'UPDATE admin SET password = %s where admin_id = %s'
                        cursor = con.cursor()
                        cursor.execute(sql,(hash_password(newpassword), session_key))
                        con.commit()
                        flash('Password Changed')
                        return render_template('changepassword.html')

                else:
                    return render_template('changepassword.html', msg = 'Current password is incorrect')


        else:
            return render_template('changepassword.html')
    else:
       return redirect('/login')

# request.form then




@app.route('/login', methods = ['POST','GET'])
def login():

        if request.method == "POST":
            email = request.form['email']
            password = request.form['password']

            #check if email exists
            sql = "select * from admin where email = %s"
            cursor = conn().cursor()
            cursor.execute(sql,(email))

            if cursor.rowcount == 0:
                return render_template('login.html', error = 'Email does not exist')
            else:
                row = cursor.fetchone()
                hashed_password = row[4]
                #verify
                status = verify_password(hashed_password, password)
                if status == True:
                    #create session
                    session['email'] = row[3]
                    session['admin_id'] = row[0]
                    session['fname'] = row[1]
                    session['lname'] = row[2]
                    return redirect('/')








                elif status == False:
                    return render_template('login.html', error='Login failed')
                else:
                    return render_template('login', error='something went wrong')
        else:
            return render_template('login.html')

@app.route('/addagency' , methods = ['POST', 'GET'])
def addagency():
    if check_admin():
        if request.method == "POST":
            fname = request.form['fname']
            lname = request.form['lname']
            email = request.form['email']
            tel_office = request.form['tel_office']
            tel_personal = request.form['tel_personal']
            company_name = request.form['company_name']
            password = password_generator()
            admin_id = session['admin_id']
            cursor = con.cursor()
            #check if phone already exists
            sql0 = 'select * from agency where tel_personal = %s'
            cursor.execute(sql0,(tel_personal))
            if cursor.rowcount > 0:
                flash('Personal Phone Already in use', 'warning')
                return render_template('addagency.html')
            else:
                sql = "insert into agency(fname, lname, email, password, tel_office , tel_personal , company_name,admin_id) values(%s,%s,%s,%s,%s,%s,%s,%s)"
                try:
                    cursor.execute(sql,(fname, lname, email, hash_password(password), tel_office,tel_personal, company_name,admin_id))
                    con.commit()
                    #send sms
                    from sms import sending
                    sending(tel_personal,password,fname)

                    flash('Agency Added Successfully', 'info')
                    return render_template('addagency.html')
                except:
                    flash('Agency Add Fail', 'error')
                    return render_template('addagency.html' )
        else:
            return render_template('addagency.html')
    else:
        return redirect('/login')







@app.route('/search_agencies', methods = ['POST','GET'])
def search_agencies():
    if check_admin():
        if request.method == 'POST':
            email = request.form['email']
            sql = 'select * from agency where email = %s'
            cursor = conn().cursor()
            cursor.execute(sql, (email))  # you get all rows from the latest
            # check if no agency found
            if cursor.rowcount == 0:
                return render_template('search_agencies.html', msg='No Records')
            else:
                rows = cursor.fetchall()
                return render_template('search_agencies.html', rows=rows)

        else:
            sql = 'select * from agency order by reg_date DESC'
            cursor = conn().cursor()
            cursor.execute(sql) #you get all rows from the latest
            #check if no agency found
            if cursor.rowcount == 0:
                return render_template('search_agencies.html', msg = 'No Records')
            else:
                rows = cursor.fetchall()
                return render_template('search_agencies.html', rows= rows)

    else:
       return redirect('/login')



@app.route('/delete_agency/<agency_id>')
def delete_agency(agency_id):
    if check_admin():

        sql = 'delete from agency where agency_id = %s'
        cursor = con.cursor()
        cursor.execute(sql,(agency_id))
        con.commit()
        flash('Deleted successfully', 'info')
        return redirect('/search_agencies')
    else:
       return redirect('/login')


@app.route('/edit_agency/<agency_id>', methods = ['POST', 'GET'])
def edit_agency(agency_id):
    if check_admin():
        if request.method == "POST":
            fname = request.form['fname']
            lname = request.form['lname']
            email = request.form['email']
            tel_office = request.form['tel_office']
            tel_personal = request.form['tel_personal']
            company_name = request.form['company_name']
            active = request.form['active']

            cursor = con.cursor()
            sql = 'update agency set fname = %s, lname = %s, email = %s, tel_office = %s, tel_personal = %s, company_name= %s, active = %s where agency_id= %s'
            cursor.execute(sql, (fname, lname, email, tel_office, tel_personal, company_name, active, agency_id))
            con.commit()
            flash('Update Successful' 'info')
            return redirect('/search_agencies')
        else:
            sql = 'select * from agency where agency_id = %s'
            cursor = conn().cursor()
            cursor.execute(sql, (agency_id))
            if cursor.rowcount == 0:
                flash('Agency does not exist', 'danger')
                return redirect('/search_agencies')
            else:
                row = cursor.fetchone()
                return render_template('edit_agency.html', row =row)

    else:
        return redirect('/login')








#    ==================== Agency routes ======================

@app.route('/agency_login', methods = ['GET','POST'])
def agency_login():

        if request.method == "POST":
            email = request.form['email']
            password = request.form['password']

            #check if email exists
            sql = 'select * from agency where email = %s'
            cursor = conn().cursor()
            cursor.execute(sql,(email))
            if cursor.rowcount == 0:
                flash('Email does not exist', 'danger')
            else:
                row = cursor.fetchone()
                hashed_password = row[4]
                status = verify_password(hashed_password, password)
                #verify
                if status == True:
                    # create session
                    session['email'] = row[3]
                    session['agency_id'] = row[0]
                    session['fname'] = row[1]
                    session['lname'] = row[2]
                    return redirect('/')

                elif status == False:
                    flash('Login Failed', 'danger')
                    return redirect('/agency_login')
                else:
                    flash('Something went Wrong')
                    return redirect('/agency_login')

        else:
            return render_template('agency_login.html')



@app.route('/edit_agent/<agent_id>', methods = ['POST', 'GET'])
def edit_agent(agent_id):

 if check_agency():
        if request.method == "POST":
            fname = request.form['fname']
            lname = request.form['lname']
            email = request.form['email']
            tel_office = request.form['tel_office']
            tel_personal = request.form['tel_personal']
            company_name = request.form['company_name']
            active = request.form['active']

            cursor = con.cursor()
            sql = 'update agent set fname = %s, lname = %s, email = %s, tel_office = %s, tel_personal = %s, company_name= %s, active = %s where agent_id= %s'
            cursor.execute(sql, (fname, lname, email, tel_office, tel_personal, company_name, active, agent_id))
            con.commit()
            flash('Update Successful' 'info')
            return redirect('/search_agencies')
        else:
            sql = 'select * from agent where agent_id = %s'
            cursor = conn().cursor()
            cursor.execute(sql, (agent_id))
            if cursor.rowcount == 0:
                flash('Agent does not exist', 'danger')
                return redirect('/search_agencies')
            else:
                row = cursor.fetchone()
                return render_template('editagent.html', row =row)
 else:
       return  redirect('/agency_login')


@app.route('/searchagent', methods = ['POST','GET'])
def searchagent():
    if check_agency():
        if request.method == 'POST':
            email = request.form['email']
            sql = 'select * from agent where email = %s'
            cursor = conn().cursor()
            cursor.execute(sql, (email))  # you get all rows from the latest
            # check if no agency found
            if cursor.rowcount == 0:
                return render_template('searchagent.html', msg='No Records')
            else:
                rows = cursor.fetchall()
                return render_template('searchagent.html', rows=rows)

        else:
            sql = 'select * from agent order by reg_date DESC'
            cursor = conn().cursor()
            cursor.execute(sql) #you get all rows from the latest
            #check if no agency found
            if cursor.rowcount == 0:
                return render_template('searchagent.html', msg = 'No Records')
            else:
                rows = cursor.fetchall()
                return render_template('searchagent.html', rows= rows)
    else:
        return redirect('/agency_login')



@app.route('/deleteagent/<agent_id>')
def deleteagent(agent_id):
    if check_agency():
        sql = 'delete from agent where agent_id = %s'
        cursor = con.cursor()
        cursor.execute(sql,(agent_id))
        con.commit()
        flash('Deleted successfully', 'info')
        return redirect('/searchagent')
    else:
       return  redirect('/agency_login')



@app.route('/addagent' , methods = ['POST', 'GET'])
def addagent():

    if check_agency():
        if request.method == "POST":
            fname = request.form['fname']
            lname = request.form['lname']
            email = request.form['email']
            tel_office = request.form['tel_office']
            tel_personal = request.form['tel_personal']
            company_name = request.form['company_name']
            password = password_generator()
            agency_id = session['agency_id']
            cursor = con.cursor()
            #check if phone already exists
            sql0 = 'select * from agent where tel_personal = %s'
            cursor.execute(sql0,(tel_personal))
            if cursor.rowcount > 0:
                flash('Personal Phone Already in use', 'warning')
                return render_template('addagent.html')
            else:
                sql = "insert into agent(fname, lname, email, password, tel_office , tel_personal , company_name,agency_id) values(%s,%s,%s,%s,%s,%s,%s,%s)"
                try:
                    cursor.execute(sql,(fname, lname, email, hash_password(password), tel_office,tel_personal, company_name,agency_id))
                    con.commit()
                    #send sms
                    from sms import sending1
                    sending1(tel_personal,password,fname,company_name)

                    flash('Agent Added Successfully', 'info')
                    return render_template('addagent.html')
                except:
                    flash('Agency Add Fail', 'error')
                    return render_template('addagent.html' )
        else:
            return render_template('addagent.html')
    else:
        return redirect('/agency_login')

@app.route('/profileagency')
def profileagency():
    if check_agency():
        sql = 'select * from agency where agency_id = %s'
        cursor = conn().cursor()
        session_key = session['agency_id']
        cursor.execute(sql, (session_key))
        row = cursor.fetchone()
        return render_template('profileagency.html', row=row)
    else:
        return redirect('/login')

@app.route('/agencychange', methods = ['POST', 'GET'])
def agencychange():
    if check_agency():
        if request.method == 'POST':
            session_key = session['agency_id']
            currentpassword = request.form['currentpassword']
            newpassword = request.form['newpassword']
            confirmpassword = request.form['confirmpassword']

            sql = 'select * from agency where agency_id = %s'
            cursor = conn().cursor()
            cursor.execute(sql, (session_key))
            if cursor.rowcount==0:
                return redirect('/logout')
            else:
                # fetchpassword..just one
                row = cursor.fetchone()
                hashed_password = row[4]
                # verify the hashed and the password if they match
                status = verify_password(hashed_password, currentpassword)
                if status == True:
                    # if new pass is not the same as confirm pass then they dont math and u render the template
                    if newpassword !=confirmpassword:
                        flash('The password dont match', 'danger')
                        return render_template('agencychange.html')
                    else:
                        con = pymysql.connect(host='localhost', user='root', password='', database='property')
                        sql = 'UPDATE agency SET password = %s where agency_id = %s'
                        cursor = con.cursor()
                        cursor.execute(sql,(hash_password(newpassword), session_key))
                        con.commit()
                        flash('Password Changed','info')
                        return render_template('agencychange.html')

                else:
                    flash('current Password is not correct','danger')
                    return render_template('agencychange.html')


        else:
            return render_template('agencychange.html')
    else:
       return redirect('/login')


# ================= Agent routes =========================

@app.route('/agent_login', methods = ['GET','POST'])
def agent_login():
        if request.method == "POST":
            email = request.form['email']
            password = request.form['password']

            #check if email exists
            sql = 'select * from agent where email = %s'
            cursor = conn().cursor()
            cursor.execute(sql,(email))
            if cursor.rowcount == 0:
                flash('Email does not exist', 'danger')
                return redirect('/agent_login')
            else:
                row = cursor.fetchone()
                hashed_password = row[4]
                status = verify_password(hashed_password, password)
                #verify
                if status == True:
                    # create session
                    session['email'] = row[3]
                    session['agent_id'] = row[0]
                    session['fname'] = row[1]
                    session['lname'] = row[2]
                    return redirect('/')

                elif status == False:
                    flash('Login Failed', 'danger')
                    return redirect('/agent_login')
                else:
                    flash('Something went Wrong')
                    return redirect('/agent_login')

        else:
            return render_template('agent_login.html')


@app.route('/addproperty', methods = ['POST','GET'])
def addproperty():
    if request.method == 'POST':
           property_name = request.form['property_name']
           property_category = request.form['property_category']
           property_location = request.form['property_location']
           address = request.form['address']
           agent_id = 'agent_id'
           landlord_id = '1'

           cursor = con.cursor()
           sql = 'insert into property(property_name, category_id, property_location, address,agent_id,landlord_id) values(%s,%s,%s,%s,%s,%s)'

           cursor.execute(sql,(property_name,property_category,property_location,address,agent_id,landlord_id))
           con.commit()
           flash('Saved Successfully')
           return redirect('/addproperty')


    else:
#         getting categories rows
        sql1 = 'select * from property_category'
        cursor1 = conn().cursor()
        cursor1.execute(sql1)
        categories = cursor1.fetchall()

        # getting locations rows
        sql2 = 'select * from property_location'
        cursor2 = conn().cursor()
        cursor2.execute(sql2)
        locations = cursor2.fetchall()
        return render_template('addproperty.html', categories = categories, locations = locations)


def check_admin():
    if 'admin_id' in session:
        return True
    else:
        return False

def check_agency():
    if 'agency_id' in session:
        return True
    else:
        return False



def check_admin_agency():
    if 'admin_id' in session or 'agency_id' in session:
        return True
    else:
        return  False


def check_admin_agency_agent():
    if 'admin_id' in session or 'agency_id' in session or 'agent_id' in session:
        return True
    else:
        return  False

if __name__=='__main__':
    app.run(debug=True, port=8080)