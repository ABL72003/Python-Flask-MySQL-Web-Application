#import modules - used from class project minus the pygal becuase I dont need charts
from flask import Flask, render_template, request, flash, url_for, redirect
import mysql.connector
from mysql.connector import errorcode

app =Flask(_name_)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = 'secretkey'
app.secret_key = 'secretkey'


def get_db_connection():

    mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            #figure out when Im back home
            #port="6603",
            database="hr"
    )


    return mydb



@app.route("/")
def index():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT d.id, d.firstName, d.lastName, d.relationship,
        e.emp_id, CONCAT(e.firstName, ' ', e.lastName) AS employeeName
        FROM dependents d
        JOIN employees e ON d.employee_id = e.emp_id
        ORDER BY d.id;
    """

    cursor.execute(query)
    dependents = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("index.html", dependents=dependents)


# now we add the edit dependent
