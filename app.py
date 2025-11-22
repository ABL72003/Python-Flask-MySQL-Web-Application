#import modules - used from class project minus the pygal becuase I dont need charts
from flask import Flask, render_template, request, flash, url_for, redirect
import mysql.connector
from mysql.connector import errorcode

app = Flask(__name__)
app.config["DEBUG"] = True
app.secret_key = 'secretkey'


def get_db_connection():

    mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            #figure out when Im back home
            port="6603",
            database="hr"
    )


    return mydb



@app.route("/")
def index():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT d.dependent_id AS id, d.first_name AS firstName, d.last_name AS lastName, d.relationship, e.employee_id AS emp_id, CONCAT(e.first_name, ' ', e.last_name) AS employeeName
    FROM dependents d
    JOIN employees e ON d.employee_id = e.employee_id
    ORDER BY d.dependent_id;"""

    cursor.execute(query)
    dependents = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("index.html", dependents=dependents)




#delte get from class project with modification becuasue there is a seperate screen that pops up 

#delte post
@app.route("/delete/<int:id>", methods=["POST"])
def delete_post(id):
    dep = get_dependent(id)

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM dependents WHERE dependent_id = %s;", (id,))
    connection.commit()
    flash(f"Dependent {dep['firstName']} {dep['lastName']} deleted successfully!")
    cursor.close()
    connection.close()
    return redirect(url_for("index"))







# now we add the get dependent

def get_dependent(id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
    SELECT d.dependent_id AS id, d.first_name AS firstName, d.last_name AS lastName, d.relationship, e.employee_id AS emp_id,
    CONCAT(e.first_name, ' ', e.last_name) AS employeeName
    FROM dependents d JOIN employees e ON d.employee_id = e.employee_id
    WHERE d.dependent_id = %s; """, 
    (id,))

    dep = cursor.fetchone()

    cursor.close()
    connection.close()
    return dep

#edit get
@app.route("/edit/<int:id>", methods=["GET"])
def edit(id):
    dependent = get_dependent(id)
    return render_template("edit.html", dependent=dependent)

#edit post
#took code from class project and simplied what I thought I could as it was a very long function.
#get into from form submitted
@app.route("/edit/<int:id>", methods=["POST"])
def edit_post(id):
    first = request.form.get("firstName")
    last = request.form.get("lastName")
    relationship = request.form.get("relationship")

    if not first:
        flash("First name is required.")
        return redirect(url_for("edit", id=id))
    elif not last:
        flash("Last name is required.")
        return redirect(url_for("edit", id=id))
    elif not relationship:
        flash("Relationship is required.")
        return redirect(url_for("edit", id=id))


    connection = get_db_connection()
    cursor = connection.cursor()
#query to update the database with new information given from user
    update_query = """
    UPDATE dependents
    SET first_name = %s, last_name = %s, relationship = %s
    WHERE dependent_id = %s; """
    cursor.execute(update_query, (first, last, relationship, id))
    connection.commit()

    cursor.close()
    connection.close()

    flash("Dependent updated successfully!")
    return redirect(url_for("index"))


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)