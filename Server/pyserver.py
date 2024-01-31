import os
from flask import Flask, request, render_template
import json 
import re
import pymysql.cursors
from datetime import date, datetime

db = pymysql.connect(host="localhost", user="root", password="", database="test", charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor)
cursor = db.cursor()
   
# Setup flask server
app = Flask(__name__) 
  
# Setup url route which will calculate
# total sum of array.
@app.route('/arraymqtt', methods = ['POST'])
def mqtt_receiver(): 
    data = request.get_json() 
    #data1 = data.payload.decode()
    data1 = json.loads(data)
    data2 = data1[0]
    arr = re.split('{|,|}',data2)
    data31 = arr[1]
    data32 = arr[2]
    data33 = arr[3]
    data34 = arr[4]
    data35 = arr[5]
    data36 = arr[6]
    data37 = arr[7]
    arr1 = re.split('{|: |}',data31)
    arr2 = re.split('{|: |}',data32)
    arr3 = re.split('{|: |}',data33)
    arr4 = re.split('{|: |}',data34)
    arr5 = re.split('{|: |}',data35)
    arr6 = re.split('{|: |}',data36)
    arr7 = re.split('{|: |}',data37)
    print(arr1[1])
    print(arr2[1])
    print(arr3[1])
    print(arr4[1])
    print(arr5[1])
    print(arr6[1])
    print(arr7[1])
    sql = """INSERT INTO forecasting (voltage, current_A, power_W, energy_Wh, frequency_Hz, power_factor, alarm) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    cursor.execute(sql, (arr1[1], arr2[1], arr3[1], arr4[1], arr5[1], arr6[1], arr7[1]))
    db.commit()

    # Return data in json format 
    return json.dumps({"result":"ok"})

files_store = "C:\\xampp\\htdocs\\server-side"
@app.route("/upload", methods=['POST'])
def upload_file():
    storage = os.path.join(files_store, "uploads/")
    print(storage)
    
    if not os.path.isdir(storage):
        os.mkdir(storage)

    try:
        for file_rx in request.files.getlist("file"):
            name = file_rx.filename
            destination = "/".join([storage, name])
            file_rx.save(destination)
            sql = """INSERT INTO tbl_files (filename) VALUES (%s)"""
            cursor.execute(sql, (name))
            db.commit()
        
        return "200"
    except Exception:
        return "500"
   
if __name__ == "__main__": 
    app.run(host='172.20.10.4', port=5000)