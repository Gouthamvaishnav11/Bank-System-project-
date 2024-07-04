# from flask import Flask
from flask import Flask, render_template, request, redirect
#from sqlalchemy import SQLAlchemy 
from flask_sqlalchemy import SQLAlchemy

# Let's create the object of the Flask class
app = Flask(__name__)

# Connecting the flask app with SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///accountdetails.db'

# Creating an object of SQLAlchemy class
database = SQLAlchemy(app)

# Writing Python class to insert data into table
class Details(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    accountHolderName = database.Column(database.String(100), nullable=False)
    accountNumber = database.Column(database.String(20), unique=True, nullable=False)
    accountType = database.Column(database.String(20), nullable=False)
    accountBalance = database.Column(database.Float, nullable=False)

# First route: Index route/default route
@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # Fetch the value of account holder name, number, type, balance
        HolderName = request.form.get('accountholder')
        Number = request.form.get('accountnumber')
        Type = request.form.get('accounttype')
        Balance = request.form.get('accountbalance')
        
        # Add it to the database
        new_account = Details(
            accountHolderName=HolderName,
            accountNumber=Number,
            accountType=Type,
            accountBalance=float(Balance)
        )
        database.session.add(new_account)
        database.session.commit()

        # Returning the index.html page
        return redirect('/')
    
    else:
        # Fetching all details from the database
        alldetails = Details.query.all()
        return render_template('index.html', alldetails=alldetails)

# Second route: contact
@app.route('/contact')
def contact():
    



    # Returning the response
    return render_template('contact.html')

# Third route: about us
@app.route('/about')
def about():
    # Returning the response
    return render_template('about.html')

# Fourth route: delete a detail from database
@app.route("/delete")
def delete():
    # Extracting the id
    id_number = request.args.get('id')
    # Fetching details with id=id_number
    account_to_delete = Details.query.filter_by(id=id_number).first()

    # Deleting the details
    database.session.delete(account_to_delete)
    database.session.commit()

    # Reassign id_number
    all_details = Details.query.order_by(Details.id).all()
    for index, account in enumerate(all_details, start=1):
        account.id = index
    database.session.commit()

    # Redirect to index page
    return redirect('/')

# Fifth route: update a detail from database
@app.route("/update", methods=["GET", "POST"])
def update():
    # Getting the id for update
    id_number = request.args.get('id')
    # Fetching the details from database to update the details
    reqdetails = Details.query.filter_by(id=id_number).first()

    if request.method == "POST":
        # Fetching the updated values
        updatedaccountHolderName = request.form.get('accountholder')
        updatedaccountNumber = request.form.get('accountnumber')
        updatedaccountType = request.form.get('accounttype')
        updatedaccountBalance = request.form.get('accountbalance')

        # Changing the value of the existing task
        reqdetails.accountHolderName = updatedaccountHolderName
        reqdetails.accountNumber = updatedaccountNumber
        reqdetails.accountType = updatedaccountType
        reqdetails.accountBalance = float(updatedaccountBalance)

        # Committing the update in database
        database.session.commit()

        # Redirecting the index.html page
        return redirect('/')
    
    else:
        # Rendering the update.html page
        return render_template('update.html', reqdetails=reqdetails)

# Running the flask application
if __name__ == "__main__":
    app.run(debug=True)


