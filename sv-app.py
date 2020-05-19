from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

#------------ SELECT YOUR SQLITE FILE HERE ----------------------------#
db_locale = 'sw.db'


@app.route('/')
def home():
    tab_columns = tables_to_tuple(list_tables())
    return render_template('sv-home.html', tab_columns=tab_columns)


@app.route('/<table_name>')
def table_all_data(table_name):
    table_header, table_contents = table_all(table_name)
    return render_template('table_contents.html', table_header=table_header, table_contents=table_contents)


# function to list all tables within a database
def list_tables():
    connie = sqlite3.connect(db_locale)
    c = connie.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%';")
    tbls = c.fetchall()
    return (tbls)


# function to list all column names within a table
def list_columns(table_name):
    connie = sqlite3.connect(db_locale)
    c = connie.cursor()
    c.execute("SELECT name, type FROM PRAGMA_TABLE_INFO(?)", (table_name,))
    column_names = c.fetchall()
    return column_names


# turn table list into tuple with table name as key and column list as value
def tables_to_tuple(table_list):
    column_dict = {}
    for table in table_list:
        column_dict[table[0]] = list_columns(table[0])
    return column_dict


# a function that queries a table based on input and retrieves all header and data
def table_all(table_name):
    connie = sqlite3.connect(db_locale)
    sql_query = '' + 'SELECT * FROM ' + table_name
    c = connie.cursor()
    c.execute(sql_query)
    table_contents = c.fetchall()
    c.execute("SELECT name FROM PRAGMA_TABLE_INFO(?)", (table_name,))
    table_headers = c.fetchall()
    return (table_headers, table_contents)

if __name__ == '__main__':
    app.run()
