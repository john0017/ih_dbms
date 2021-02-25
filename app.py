from flask import Flask, render_template, url_for, request, abort, redirect, session, flash
from flask_bootstrap import Bootstrap
import pandas as pd
import mysql.connector
import uuid
from functools import wraps
from datetime import timedelta


app = Flask(__name__)
Bootstrap(app)

app.config["SECRET_KEY"]="jithinj"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(seconds=5)


def auth_request(f):
    @wraps(f)
    def req_authenticator(*args, **kwargs):
        if not 'username' in session:
            flash("Please log in to continue!")
            return redirect(url_for('userlogin'))
        else:
            return f(*args, **kwargs)
    return req_authenticator
            
def conn_df_init():
    try:
        conn = mysql.connector.connect(user="root", password='IrishHomes2021!',
                                    database="Test_DB"
                                    ) 
        print("Connection Successful!")
        data = pd.read_sql("SELECT * FROM test_table1", conn, index_col="Idx")
        data.fillna("N/A", inplace=True)
        print("Dataframe Initialized!")
        return data
    except:
        print("error connecting to SQL DB")
    finally:
        conn.close()
        print("Connection Closed!")

def sql_update(council_, status_, address_, postcode_, rowUid_):
    updateQuery = """
            UPDATE test_table1 
            
            SET 
            Council = %s,
            Status = %s,
            PropertyTown = %s,
            Postcode = %s
            
            WHERE uID= %s
    """
    values = (council_, status_, address_, postcode_, rowUid_)
    try:
        conn = mysql.connector.connect(user="root", password='IrishHomes2021!',
                                    database="Test_DB"
                                    )
        print("Connection Successful!")
        cursor=conn.cursor(prepared=True)
        cursor.execute(updateQuery, values)
        conn.commit()
        print("\n\nUpdate Successful!")
    except:
        print("Update Failed")
    finally:
        cursor.close()
        conn.close()
        print("Connection Closed!")

def sql_addNew(council_, status_, address_, postcode_, rowUid_):
    addNewQuery = """
            INSERT INTO test_table1 
         
            (Council, Status, PropertyTown, Postcode, uID)
            
            VALUES
            (%s,%s,%s,%s,%s)          
    """
    values = (council_, status_, address_, postcode_, rowUid_)
    try:
        conn = mysql.connector.connect(user="root", password='IrishHomes2021!',
                                    database="Test_DB"
                                    )
        print("Connection Successful!")
        cursor=conn.cursor(prepared=True)
        cursor.execute(addNewQuery, values)
        conn.commit()
        print("\n\n Record Added!")
    except:
        print("Update Failed")
    finally:
        cursor.close()
        conn.close()
        print("Connection Closed!")
        
def sql_delete(rowUid_):
    delQuery = """
            DELETE FROM test_table1 
         
            WHERE uID = %s         
    """
    values = (rowUid_,)
    try:
        conn = mysql.connector.connect(user="root", password='IrishHomes2021!',
                                    database="Test_DB"
                                    )
        print("Connection Successful!")
        cursor=conn.cursor(prepared=True)
        cursor.execute(delQuery, values)
        conn.commit()
        print("\n\n Record Deleted!")
    except:
        print("Update Failed")
    finally:
        cursor.close()
        conn.close()
        print("Connection Closed!")
                       


# home
@app.route('/', methods=['GET', 'POST'])
@auth_request
def home():
    data = conn_df_init()
    if "username" in session:
        print("you active")
    else:
        print("you out")
    return render_template("draft.html", 
                           data=data, 
                           statusOptions = data.Status.unique(),
                           statusName="All")


@app.route('/login', methods=['GET', 'POST'])
def userlogin():
    return render_template("login.html")

@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
    if request.method=="POST":
        user_email = request.form["email"]
        user_pass = request.form["password"]
        session['username']=user_email
        session.permanent = True
        flash('Welcome, '+ session['username']+"!")
        
        return redirect(url_for("home"))
        

# edit table
@app.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method =="POST":
        rowUid_ = request.form["uID"]
        council_ = request.form["council"]
        status_ = request.form["status_"]
        address_ = request.form["Address"]
        town_ = request.form["Town"]
        postcode_ = request.form["Postcode"]
        # print(rowUid_, town_, postcode_, council_, "\n\n")
        sql_update(council_, status_, address_, postcode_, rowUid_)
        # return redirect(url_for("home"))
        return redirect(request.referrer) #return to the same page from where the user called
    return "poop"

# add new
@app.route('/addNew', methods=['GET', 'POST'])
def addNew():
    if request.method =="POST":
        council_ = request.form["council"]
        status_ = request.form["status_"]
        address_ = request.form["Address"]
        purchasePrice_ = request.form["PurchaseP"]
        postcode_ = request.form["Postcode"]
        rowUid_ = str(uuid.uuid4())
        
        sql_addNew(council_, status_, address_, postcode_, rowUid_)
        # return " ", 204
        return redirect(url_for("home"))

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method=="POST":
        rowUid_ = request.form["id"]
        # print(rowUid_)
        sql_delete(rowUid_)
        return redirect(url_for("home"))
    
@app.route('/filterBy/<status>', methods=['GET', 'POST'])
def statusFilter(status):
    data=conn_df_init()
    
    statusOptions = data.Status.unique()
    if status not in statusOptions:
        abort(404)
    else:
        dataFiltered = data.loc[data.Status==status]
        return render_template("draft.html", data=dataFiltered, statusOptions=statusOptions, statusName=status)

@app.route('/customFilter', methods=['GET', 'POST'])
def customFilter():
    data=conn_df_init()
    
    if request.method == "POST":
        council_ = request.form.getlist('MSPortfolio')
    
    print(council_)
    
    return "", 204
    
    # return render_template("draft.html",
    #                        statusoptions=statusOptions,
    #                        portfolioOptions=portfolioOptions,
    #                        countyOptions=countyOptions,
    #                        bedOptions=bedOptions,
    #                        councilOptions=councilOptions
    #                        )

@app.route('/thisProp/<id>', methods=['GET', 'POST'])
def thisProp(id):
    data=conn_df_init()
    prop_ = data[data["uID"]==id]
    return render_template("thisProp.html", id=id, prop_=prop_)

if __name__ == '__main__':
    app.run(debug='True')
