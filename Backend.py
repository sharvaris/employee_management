import re
import pymysql
import Read_yaml_file as db_conn
from flask import Flask, jsonify, request, abort, render_template
def set_parameters():
    '''Sets connection parameters from the yaml file'''
    data = db_conn.yaml_db_conn_loader("db_conn.yaml")
    for parameter,value in data.items():
        if parameter == 'host':
            host = value
        elif parameter == 'user':
            user = value
        elif parameter == 'passwd':
            passwd = value
        else:
            db = value
    return host,user,passwd,db

def connect_to_db():
    '''Creates database (if not exists) and connects to it'''
    try:
        (host,user,passwd,db) = set_parameters()
        connection = pymysql.connect(host=host,user=user,passwd=passwd,autocommit=True,local_infile=1)
        cursor = connection.cursor()
        CreateDB = """create DATABASE if not EXISTS {};"""
        cursor.execute(CreateDB.format(db))
        cursor.execute("use {}".format(db))
        return cursor
    except Exception as err:
        print("Something went wrong: {}".format(err))
        return 0

app = Flask(__name__)

@app.route('/login',methods=['POST'])
def email_validation():
    '''Validates email address'''
    user_id = request.json['id']
    password = request.json['password']
    cursor = connect_to_db()
    if cursor!=0:
        query = '''SELECT emp_name,password from employee_data where login_id = {}'''
        result = cursor.execute(query.format(user_id))
        result = cursor.fetchone()
        emp_name_from_db = result[1]
        pass_from_db = result[5]
        if len(result) ==0:
            return jsonify({'status':404})
        elif pass_from_db==password:
            return jsonify({'status':403})
        else:
            return jsonify({'status':200,'user_name':emp_name_from_db})

if __name__ == '__main__':
 app.run(port=5000)






