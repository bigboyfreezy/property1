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
    if check_admin_agency_agent_tenant():

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


@app.route('/savecategory' , methods = ['GET','POST'])
def savecategory():
    if request.method == 'POST':
        category_name = request.form['category_name']
        agency_id = session['agency_id']

        cursor = con.cursor()
        sql = 'insert into property_category(category_name, agency_id) values(%s,%s)'

        cursor.execute(sql, (category_name, agency_id))
        con.commit()
        flash('Category Saved Successfully', 'info')
        return render_template("savecategory.html")
    else:
        return render_template('savecategory.html')

@app.route('/savetype' , methods = ['GET','POST'])
def savetype():
    if request.method == 'POST':
        type_name = request.form['type_name']
        agency_id = session['agency_id']

        cursor = con.cursor()
        sql = 'insert into unit_type(type_name, agency_id) values(%s,%s)'

        cursor.execute(sql, (type_name, agency_id))
        con.commit()
        flash('Type Saved Successfully', 'info')
        return render_template("savecategory.html")
    else:
        return render_template('savecategory.html')


@app.route('/savelocation' , methods = ['GET','POST'])
def savelocation():
    if request.method == 'POST':
        location_name = request.form['location_name']
        agency_id = session['agency_id']

        cursor = con.cursor()
        sql = 'insert into property_location(location_name, agency_id) values(%s,%s)'

        cursor.execute(sql, (location_name, agency_id))
        con.commit()
        flash('Location Saved Successfully', 'info')
        return render_template("savecategory.html")
    else:
        return render_template('savecategory.html')

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
                    flash('Wrong Email or Password', 'danger')
                    return redirect('/agent_login')
                else:
                    flash('Something went Wrong')
                    return redirect('/agent_login')

        else:
            return render_template('agent_login.html')


@app.route('/addproperty/<landlord_id>', methods = ['POST','GET'])
def addproperty(landlord_id):

    sql1 = 'select * from property_category'
    cursor1 = conn().cursor()
    cursor1.execute(sql1)
    categories = cursor1.fetchall()

    # getting locations rows
    sql2 = 'select * from property_location'
    cursor2 = conn().cursor()
    cursor2.execute(sql2)
    locations = cursor2.fetchall()
    return render_template('addproperty.html', categories=categories, locations = locations, landlord_id=landlord_id)

@app.route('/saveproperty', methods = ['POST','GET'])
def saveproperty():
    if request.method == 'POST':
           property_name = request.form['property_name']
           property_category = request.form['property_category']
           property_location = request.form['property_location']
           address = request.form['address']
           agent_id = session['agent_id']
           landlord_id = request.form['landlord_id']


           cursor = con.cursor()
           sql = 'insert into property(property_name, category_id, property_location, address,agent_id,landlord_id) values(%s,%s,%s,%s,%s,%s)'

           cursor.execute(sql,(property_name,property_category,property_location,address,agent_id,landlord_id))
           con.commit()
           flash('Property Saved Successfully','info')
           return redirect(url_for("addproperty", landlord_id = landlord_id))







@app.route('/addtenant' , methods = ['POST', 'GET'])
def addtenant():

    if check_agent():
        if request.method == "POST":
            fname = request.form['fname']
            lname = request.form['lname']
            email = request.form['email']
            tel_office = request.form['tel_office']
            tel_personal = request.form['tel_personal']
            company_name = request.form['company_name']
            password = password_generator()
            agent_id = session['agent_id']
            cursor = con.cursor()
            #check if phone already exists
            sql0 = 'select * from tenants where tel_personal = %s'
            cursor.execute(sql0,(tel_personal))
            if cursor.rowcount > 0:
                flash('Personal Phone Already in use', 'warning')
                return render_template('addtenant.html')
            else:
                sql = "insert into tenants(fname, lname, email, password, tel_office , tel_personal , company_name,agent_id) values(%s,%s,%s,%s,%s,%s,%s,%s)"
                # try:
                cursor.execute(sql,(fname, lname, email, hash_password(password), tel_office,tel_personal, company_name,agent_id))
                con.commit()
                    #send sms
                from sms import sending2
                sending2(tel_personal,password,fname,company_name)

                flash('Tenant Added Successfully', 'info')
                return render_template('addtenant.html')
                # except:
                #     flash('Tenant Add Fail', 'error')
                #     return render_template('addtenant.html' )
        else:
            return render_template('addtenant.html')
    else:
        return redirect('/agent_login')

@app.route('/addlandlord' , methods = ['POST', 'GET'])
def addlandlord():

    if check_agent():
        if request.method == "POST":
            fname = request.form['fname']
            lname = request.form['lname']
            email = request.form['email']
            tel_office = request.form['tel_office']
            tel_personal = request.form['tel_personal']
            company_name = request.form['company_name']

            password = password_generator()
            agent_id = session['agent_id']
            cursor = con.cursor()
            #check if phone already exists
            sql0 = 'select * from landlord where tel_personal = %s'
            cursor.execute(sql0,(tel_personal))
            if cursor.rowcount > 0:
                flash('Personal Phone Already in use', 'warning')
                return render_template('addlandlord.html')
            else:
                sql = "insert into landlord(fname, lname, email, password, tel_office , tel_personal , company_name,agent_id) values(%s,%s,%s,%s,%s,%s,%s,%s)"
                #try:
                cursor.execute(sql,(fname, lname, email, hash_password(password), tel_office,tel_personal, company_name,agent_id))
                con.commit()
                    #send sms
                from sms import sending3
                sending3(tel_personal,password,fname,company_name)

                flash('Landlord Added Successfully', 'info')
                return render_template('addlandlord.html')
                #except:
                    # flash('Landlord Add Fail', 'error')
                    # return render_template('addlandlord.html' )
        else:
            return render_template('addlandlord.html')
    else:
        return redirect('/agent_login')




@app.route('/searchtenant', methods = ['POST','GET'])
def searchtenant():
    if check_admin_agency_agent():
        if request.method == 'POST':
            email = request.form['email']
            sql = 'select * from tenants where email = %s'
            cursor = conn().cursor()
            cursor.execute(sql, (email))  # you get all rows from the latest
            # check if no agency found
            if cursor.rowcount == 0:
                return render_template('searchtenant.html', msg='No Records')
            else:
                row = cursor.fetchone()
                sql = 'select * from allocate_unit where tenant_id = %s'
                cursor = conn().cursor()
                cursor.execute(sql, (row[0]))

                sql2 = 'select * from unit'
                cursor1 = conn().cursor()
                cursor1.execute(sql2)
                unites = cursor1.fetchall()

                if cursor.rowcount == 0:
                    flash('This Tenant Has Not Been Allocated', 'danger')
                    return redirect('/searchtenant')
                else:
                    units = cursor.fetchall()
                    return render_template('searchtenant.html', row = row ,units=units, unites=unites)

        else:
            sql = 'select * from tenants order by reg_date DESC'
            cursor = conn().cursor()
            cursor.execute(sql) #you get all rows from the latest
            #check if no agency found
            if cursor.rowcount == 0:
                return render_template('searchtenant.html', msg = 'No Records')
            else:
                rows = cursor.fetchall()
                return render_template('searchtenant.html', rows= rows)
    else:
        return redirect('/agent_login')

@app.route('/rented')
def rented():
    sql = 'select * from allocate_unit where status = %s'
    cursor = con.cursor()
    cursor.execute(sql,('yes'))
    if cursor.rowcount == 0:
        flash('No Rented Houses', 'Info')
        return redirect('/rented')
    else:

        #take it as a list append it then tuple it so that it can be used as laceholder
        list=[]
        units = cursor.fetchall()
        for unit in units:
            list.append(unit[1])
        sql1 = 'select * from unit where unit_id IN %s'
        cursor1 = con.cursor()
        cursor1.execute(sql1,[tuple(list)])
        houses = cursor1.fetchall()




        sql2 = 'select * from property '
        cursor2 = con.cursor()
        cursor2.execute(sql2)
        propers = cursor2.fetchall()

        sql3 = 'select * from unit_type '
        cursor3 = con.cursor()
        cursor3.execute(sql3)
        types = cursor3.fetchall()


        return render_template('rented.html', houses = houses, propers = propers, types= types )







@app.route('/tenant_in_unit/<unit_id>')
def tenant_in_unit(unit_id):
    sql = 'select * from allocate_unit where unit_id = %s and status = %s'
    cursor = con.cursor()
    cursor.execute(sql,(unit_id,'yes'))
    row = cursor.fetchone()

    sql1 = 'select * from tenants where tenant_id = %s'
    cursor = con.cursor()
    cursor.execute(sql1,(row[2]))
    row = cursor.fetchone()
    return render_template('tenants.html', row= row)




@app.route('/deallocate/<allocate_id>')
def deallocate(allocate_id):
    status = 'no'
    sql = 'update allocate_unit set status = %s where allocate_id = %s'
    cursor = con.cursor()
    cursor.execute(sql,(status, allocate_id))
    con.commit()
    return redirect('/searchtenant')



@app.route('/searchlandlord', methods = ['POST','GET'])
def searchlandlord():
    if check_agent():
        if request.method == 'POST':
            email = request.form['email']
            sql = 'select * from landlord where email = %s'
            cursor = conn().cursor()
            cursor.execute(sql, (email))  # you get all rows from the latest
            # check if no agency found
            if cursor.rowcount == 0:
                return render_template('searchlandlord.html', msg='No Records')
            else:
                rows = cursor.fetchall()
                return render_template('searchlandlord.html', rows=rows)

        else:
            sql = 'select * from landlord order by reg_date DESC'
            cursor = conn().cursor()
            cursor.execute(sql) #you get all rows from the latest
            #check if no agency found
            if cursor.rowcount == 0:
                return render_template('searchlandlord.html', msg = 'No Records')
            else:
                rows = cursor.fetchall()
                return render_template('searchlandlord.html', rows= rows)
    else:
        return redirect('/agent_login')




@app.route('/searchproperty', methods = ['POST','GET'])
def searchproperty():
    if check_agent():
        if request.method == 'POST':
            property_name = request.form['property_name']
            sql = 'select * from property where property_name = %s'
            cursor = conn().cursor()
            cursor.execute(sql, (property_name))  # you get all rows from the latest
            # check if no agency found
            if cursor.rowcount == 0:
                return render_template('searchproperty.html', msg='No Records')
            else:
                rows = cursor.fetchall()
                return render_template('searchproperty.html', rows=rows)

        else:
            sql = 'select * from property order by reg_date DESC '
            cursor = conn().cursor()
            cursor.execute(sql) #you get all rows from the latest
            #check if no agency found
            if cursor.rowcount == 0:
                return render_template('searchproperty.html', msg = 'No Records')
            else:
                rows = cursor.fetchall()
                return render_template('searchproperty.html', rows= rows)
    else:
        return redirect('/agent_login')


@app.route('/deletetenant/<tenant_id>')
def deletetenant(tenant_id):
    if check_agent():
        sql = 'delete from tenants where tenant_id = %s'
        cursor = con.cursor()
        cursor.execute(sql,(tenant_id))
        con.commit()
        flash('Deleted successfully', 'info')
        return redirect('/searchtenant')
    else:
       return  redirect('/agency_login')

@app.route('/agentchange', methods = ['POST', 'GET'])
def agentchange():
    if check_agent():
        if request.method == 'POST':
            session_key = session['agent_id']
            currentpassword = request.form['currentpassword']
            newpassword = request.form['newpassword']
            confirmpassword = request.form['confirmpassword']

            sql = 'select * from agent where agent_id = %s'
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
                        return render_template('agentchange.html')
                    else:
                        con = pymysql.connect(host='localhost', user='root', password='', database='property')
                        sql = 'UPDATE agent SET password = %s where agent_id = %s'
                        cursor = con.cursor()
                        cursor.execute(sql,(hash_password(newpassword), session_key))
                        con.commit()
                        flash('Password Changed','info')
                        return render_template('agentchange.html')

                else:
                    flash('current Password is not correct','danger')
                    return render_template('agentchange.html')


        else:
            return render_template('agentchange.html')
    else:
       return redirect('/login')


@app.route('/profileagent')
def profileagent():
    if check_agent():
        sql = 'select * from agent where agent_id = %s'
        cursor = conn().cursor()
        session_key = session['agent_id']
        cursor.execute(sql, (session_key))
        row = cursor.fetchone()
        return render_template('profileagent.html', row=row)
    else:
        return redirect('/login')




@app.route('/edit_tenant/<tenant_id>', methods = ['POST', 'GET'])
def edit_tenant(tenant_id):

 if check_agent():
        if request.method == "POST":
            fname = request.form['fname']
            lname = request.form['lname']
            email = request.form['email']
            tel_office = request.form['tel_office']
            tel_personal = request.form['tel_personal']
            company_name = request.form['company_name']
            active = request.form['active']

            cursor = con.cursor()
            sql = 'update tenants set fname = %s, lname = %s, email = %s, tel_office = %s, tel_personal = %s, company_name= %s, active = %s where tenant_id= %s'
            cursor.execute(sql, (fname, lname, email, tel_office, tel_personal, company_name, active, tenant_id))
            con.commit()
            flash('Update Successful' 'info')
            return redirect('/searchtenant')
        else:
            sql = 'select * from tenants where tenant_id = %s'
            cursor = conn().cursor()
            cursor.execute(sql, (tenant_id))
            if cursor.rowcount == 0:
                flash('Tenant does not exist', 'danger')
                return redirect('/searchtenant')
            else:
                row = cursor.fetchone()
                return render_template('edit_tenant.html', row =row)
 else:
       return  redirect('/agent_login')


@app.route('/editlandlord/<landlord_id>', methods = ['POST', 'GET'])
def editlandlord(landlord_id):

 if check_agent():
        if request.method == "POST":
            fname = request.form['fname']
            lname = request.form['lname']
            email = request.form['email']
            tel_office = request.form['tel_office']
            tel_personal = request.form['tel_personal']
            company_name = request.form['company_name']
            active = request.form['active']

            cursor = con.cursor()
            sql = 'update landlord set fname = %s, lname = %s, email = %s, tel_office = %s, tel_personal = %s, company_name= %s, active = %s where landlord_id= %s'
            cursor.execute(sql, (fname, lname, email, tel_office, tel_personal, company_name, active, landlord_id))
            con.commit()
            flash('Update Successful' 'info')
            return redirect('/searchlandlord')
        else:
            sql = 'select * from landlord where lardlord_id = %s'
            cursor = conn().cursor()
            cursor.execute(sql, (landlord_id))
            if cursor.rowcount == 0:
                flash('Landlord does not exist', 'danger')
                return redirect('/searchlandlord')
            else:
                row = cursor.fetchone()
                return render_template('editlandlord.html', row =row)
 else:
       return  redirect('/agent_login')




@app.route('/editunit/<unit_id>', methods = ['POST', 'GET'])
def editunit(unit_id):

 if check_agent():
        if request.method == "POST":
            unit_code = request.form['unit_code']



            agent_id = session['agent_id']


            cursor = con.cursor()
            sql = 'update landlord set unit_code = %s, type_id= %s where unit_id= %s'
            cursor.execute(sql, (unit_code, unit_id))
            con.commit()
            flash('Update Successful' 'info')
            return redirect('/viewunit')
        else:
            sql = 'select * from unit where unit_id = %s'
            cursor = conn().cursor()
            cursor.execute(sql, (unit_id))
            if cursor.rowcount == 0:
                flash('Landlord does not exist', 'danger')
                return redirect('/viewunit')
            else:
                row = cursor.fetchone()
                return render_template('editunit.html', row =row)
 else:
       return  redirect('/agent_login')

@app.route('/deleteunit/<property_id>')
def deleteunit(property_id):
    if check_agent():
        sql = 'delete from unit where unit_id = %s'
        cursor = con.cursor()
        cursor.execute(sql,(property_id))
        con.commit()
        flash('Deleted successfully', 'info')
        return redirect(url_for('viewunit', property_id=property_id))
    else:
       return  redirect('/agency_login')



@app.route('/deletelandlord/<landlord_id>')
def deletelandlord(landlord_id):
    if check_agent():
        sql = 'delete from landlord where landlord_id = %s'
        cursor = con.cursor()
        cursor.execute(sql,(landlord_id))
        con.commit()
        flash('Deleted successfully', 'info')
        return redirect('/searchlandlord')
    else:
       return  redirect('/agency_login')

@app.route('/viewunit/<property_id>')
def viewunit(property_id):
    if check_agent():
        sql = 'select * from unit where property_id = %s'
        cursor = conn().cursor()
        cursor.execute(sql, (property_id))


        sql1 = 'select * from unit_type'
        cursor0 = conn().cursor()
        cursor0.execute(sql1)
        types = cursor0.fetchall()

        sql2 = 'select * from property_location'
        cursor1 = conn().cursor()
        cursor1.execute(sql2)
        locations = cursor1.fetchall()



        if cursor.rowcount == 0:
            return render_template('viewunit.html', msg='No records')
        else:
            rows = cursor.fetchall()
            return render_template('viewunit.html', rows=rows, property_id=property_id, locations=locations, types=types)


@app.route('/allocateunit', methods = ['POST','GET'])
def allocateunit():
    if check_agent():

        if request.method == 'POST':


            min = float(request.form['min'])
            max = float(request.form['max'])
            location_name = request.form['location_name']
            type_id = request.form['type_id']

            sql1 = 'select * from property_location '
            cursor1 = conn().cursor()
            cursor1.execute(sql1)
            locations = cursor1.fetchall()

            sql2 = 'select * from unit_type '
            cursor2 = conn().cursor()
            cursor2.execute(sql2)
            types = cursor2.fetchall()


            list = []
            status = 'yes'
            sql3 = 'select * from allocate_unit where status = %s'
            cursor3 = conn().cursor()
            cursor3.execute(sql3, (status))
            allocated = cursor3.fetchall()
            for row in allocated:
                list.append(row[1])


            if tuple(list):
                sql4 = 'select * from unit where unit_id NOT IN %s and cost between %s AND %s AND location_name = %s AND type_id = %s'
                cursor4 = conn().cursor()
                cursor4.execute(sql4, [tuple(list),min, max, location_name,type_id])
                rows = cursor4.fetchall()
            else:
                sql4 = 'select * from unit where cost between %s AND %s AND location_name = %s AND type_id = %s'
                cursor4 = conn().cursor()
                cursor4.execute(sql4,(min,max,location_name,type_id))
                rows = cursor4.fetchall()


            if cursor4.rowcount == 0:
                return render_template('allocateunit.html', msg='No Unit Found' ,locations=locations, types=types)
            else:

                return render_template('allocateunit.html', rows=rows, locations=locations, types=types)
        else:
                list = []
                status = 'yes'
                sql3 = 'select * from allocate_unit where status = %s'
                cursor3 = conn().cursor()
                cursor3.execute(sql3,(status))
                allocated = cursor3.fetchall()
                for row in allocated:
                    list.append(row[1])

                if tuple(list):
                    sql4 = 'select * from unit where unit_id NOT IN %s'
                    cursor4 = conn().cursor()
                    cursor4.execute(sql4, [tuple(list)])
                    rows = cursor4.fetchall()
                else:
                    sql4 = 'select * from unit '
                    cursor4 = conn().cursor()
                    cursor4.execute(sql4 )
                    rows = cursor4.fetchall()












                sql1 = 'select * from property_location '
                cursor1 = conn().cursor()
                cursor1.execute(sql1 )
                locations = cursor1.fetchall()

                sql2 = 'select * from unit_type '
                cursor2 = conn().cursor()
                cursor2.execute(sql2)
                types = cursor2.fetchall()

                if cursor4.rowcount == 0:
                    return render_template('allocateunit.html',)
                else:

                    return render_template('allocateunit.html', rows=rows, locations=locations, types=types)

    else:
        return redirect('/agent_login')



@app.route('/landlord_property/<landlord_id>')
def landlord_property(landlord_id):
    sql = 'select * from property where landlord_id = %s'
    cursor = conn().cursor()
    cursor.execute(sql, (landlord_id))
    #check if agency i
    sql1 = 'select * from property_category'
    cursor0 = conn().cursor()
    cursor0.execute(sql1)
    categories = cursor0.fetchall()
    #fetching location
    sql2 = 'select * from property_location'
    cursor1 = conn().cursor()
    cursor1.execute(sql2)
    locations = cursor1.fetchall()




    if cursor.rowcount == 0:
        return render_template('landlord_property.html', msg='No records')
    else:
        rows = cursor.fetchall()
        return render_template('landlord_property.html', rows=rows, categories=categories, locations=locations)

@app.route('/addunit/<property_id>')
def addunit(property_id):

    sql = 'select * from unit_type'
    cursor = conn().cursor()
    cursor.execute(sql)#you get all rows from the latest
    #check if unit type is found

    sql1 = 'select * from property where property_id = %s'
    cursor1 = conn().cursor()
    cursor1.execute(sql1, (property_id))
    row = cursor1.fetchone()



    sql2 = 'select * from property_location where category_id = %s'
    cursor2 = conn().cursor()
    cursor2.execute(sql2,(row[7]))
    locations = cursor2.fetchone()
    location_name = locations[1]




    if cursor.rowcount == 0:
        return render_template('addunit.html', msg= 'no records')
    else:
        rows = cursor.fetchall()
        return render_template('addunit.html', rows=rows, property_id = property_id, location_name = location_name)

@app.route('/saveunit', methods = ['POST','GET'])
def saveunit():
    if request.method == 'POST':
           unit_code = request.form['unit_code']
           type_id = request.form['type_id']
           property_id = request.form['property_id']
           location_name= request.form['location_name']
           description= request.form['description']
           cost = request.form['cost']

           agent_id = session['agent_id']



           cursor = con.cursor()
           sql = 'insert into unit(unit_code, agent_id, type_id, property_id,location_name,description,cost) values(%s,%s,%s,%s,%s,%s,%s)'

           cursor.execute(sql,(unit_code,agent_id,type_id,property_id,location_name,description,cost))
           con.commit()
           flash('Unit Saved Successfully','info')
           return redirect(url_for("addunit", property_id = property_id))

@app.route('/tenantallocate/<unit_id>', methods = ['POST','GET'])
def tenantallocate(unit_id):
    if request.method == 'POST':

        email = request.form['email']
        cursor = conn().cursor()
        sql = 'select * from tenants where email = %s'
        cursor.execute(sql,(email))
        if cursor.rowcount == 0:
            return render_template('tenantallocate.html',msg='Tenant Not Found',unit_id=unit_id)
        else:
            row = cursor.fetchone()
            return render_template('tenantallocate.html', row= row, unit_id=unit_id)
    else:
        return render_template('tenantallocate.html', unit_id=unit_id)

@app.route('/commitallocation',methods = ['POST','GET'])
def commitallocation():
    if request.method == 'POST':
        unit_id = request.form['unit_id']
        tenant_id = request.form['tenant_id']
        cursor = con.cursor()
        sql = 'insert into allocate_unit(unit_id, tenant_id) values (%s,%s)'

        cursor.execute(sql,(unit_id,tenant_id))
        con.commit()

        flash('Allocation Successful', 'info')
        return redirect(url_for('tenantallocate', unit_id=unit_id))


#====================== Tenant Routes ======================

@app.route('/tenant_login', methods=['GET','POST'])
def tenant_login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        # check if email exists
        sql = 'select * from tenants where email = %s'
        cursor = conn().cursor()
        cursor.execute(sql, (email))
        if cursor.rowcount == 0:
            flash('Email does not exist', 'danger')
            return redirect('/agent_login')
        else:
            row = cursor.fetchone()
            hashed_password = row[4]
            status = verify_password(hashed_password, password)
            # verify
            if status == True:
                # create session
                session['email'] = row[3]
                session['tenant_id'] = row[0]
                session['fname'] = row[1]
                session['lname'] = row[2]
                return redirect('/')

            elif status == False:
                flash('Wrong Email or Password', 'danger')
                return redirect('/tenant_login')
            else:
                flash('Something went Wrong')
                return redirect('/tenant_login')

    else:
        return render_template('tenant_login.html')


@app.route('/profiletenant')
def profiletenant():
    if check_tenant():
        sql = 'select * from tenants where tenant_id = %s'
        cursor = conn().cursor()
        session_key = session['tenant_id']
        cursor.execute(sql, (session_key))
        row = cursor.fetchone()
        return render_template('profiletenant.html', row=row)
    else:
        return redirect('/tenant_login')


@app.route('/sample')
def sample():
    if check_tenant():
        status = 'yes'
        tenant_id = session['tenant_id']
        sql = 'select * from allocate_unit where status = %s and tenant_id = %s'
        cursor = con.cursor()
        cursor.execute(sql,(status,tenant_id))

        if cursor.rowcount== 0:
            return render_template('housedisplay.html', msg = "You Are Not Allocated'")
        else:
            rows = cursor.fetchall()
            list = []
            for row in rows:
                list.append(row[1])
            sql2 = 'select * from unit where unit_id IN %s'
            cursor2 = con.cursor()
            cursor2.execute(sql2,[tuple(list)]) #we are passing the row at which unit is in the allocate table and check it in the unit table to get the unit name
            units = cursor2.fetchall()

            sql3 = 'select * from unit_type'
            cursor3 = conn().cursor()
            cursor3.execute(sql3)
            types = cursor3.fetchall()

            sql4 = 'select * from property'
            cursor4 = conn().cursor()
            cursor4.execute(sql4)
            props = cursor4.fetchall()

            return render_template('housedisplay.html', units= units, types=types, props=props)
    else:
        return redirect('/tenant_login')


@app.route('/process_payment' , methods = ['POST','GET'])
def process_payment():
    if request.method == 'POST':
        phone = str(request.form['phone'])

        amount = '1'
        from payment import mpesa_payment
        mpesa_payment(phone,amount)
        flash('Please Complete Payment On Your Phone')
        return redirect('/sample')
    else:
        flash('Payment Processing Failed')




def check_tenant():
    if 'tenant_id' in session:
        return True
    else:
        return False




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

def check_agent():
    if 'agent_id' in session:
        return True
    else:
        return False
def check_agent():
    if 'agent_id' in session:
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

def check_admin_agency_agent_tenant():
    if 'admin_id' in session or 'agency_id' in session or 'agent_id' in session or 'tenant_id' in session:
        return True
    else:
        return  False

if __name__=='__main__':
    app.run(debug=True, port=8080)