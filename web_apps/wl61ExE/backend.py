import dataiku
import pandas as pd
from flask import request
import ast
from datetime import datetime

archive_folder = ""
tracking_folder = ""
countries = ""
default_file_extension = ""

client = dataiku.api_client()

@app.route('/load_params')
def load_params():
    
    global archive_folder, tracking_folder, countries, default_file_extension
    archive_folder = request.args.get('archive_folder')
    tracking_folder = request.args.get('tracking_folder')
    countries = ast.literal_eval(request.args.get('countries'))
    default_file_extension = request.args.get('default_file_extension')
    
    print("archive_folder:%s, tracking_folder:%s, default_file_extension:%s"%(archive_folder, tracking_folder, default_file_extension))
    print(countries)

    return json.dumps({"status": "ok"})


@app.route('/upload-to-dss', methods = ['POST'])
def upload_to_dss():
    
    #get file
    f = request.files.get('file')
    if f is None:
        return json.dumps({"status":"No file sent to backend"})
    initial_filename = f.filename
    extension = os.path.splitext(initial_filename)[1]
    if extension != default_file_extension:
        return json.dumps({"status":"Extension must be '%s', '%s' was found"%(default_file_extension, extension)})

    
    #get user
    request_headers = dict(request.headers)
    user = client.get_auth_info_from_browser_headers(request_headers)["authIdentifier"]
    #user = client.get_auth_info()["authIdentifier"]
    
    #get time
    now = datetime.now()
    day = now.strftime("%Y%m%d")
    hour = now.strftime("%H%M%S")
       
    country = request.form.get('country')
    customer_type = request.form.get('customer_type')
    dss_filename = '%s_%s_%s_%s_%s%s' %(day, hour, country, customer_type, user, extension)
    
    
    try:
        dataiku.Folder(archive_folder).upload_stream(dss_filename, f)
        status = "ok"
    except Exception as e:
        print("fail")
        status = str(e)

    return json.dumps({"status":status, "day":day, "hour":hour, "user":user, "initial_filename":f.filename, "dss_filename":dss_filename})


@app.route('/prepare_submission_without_update')
def prepare_submission_without_update():
    
    now = datetime.now()
    day = now.strftime("%Y%m%d")
    hour = now.strftime("%H%M%S")
    
    request_headers = dict(request.headers)
    user = client.get_auth_info_from_browser_headers(request_headers)["authIdentifier"]

    return json.dumps({"day": day, "hour":hour, "user":user})


@app.route('/submit')
def submit():
    
    submission = ast.literal_eval(request.args.get('submission'))
    print(submission)
    
    results = {}
        
    try:
        dataiku.Folder(tracking_folder).upload_stream("%s_%s_%s.json"%(submission["day"], submission["hour"], submission["user"]), json.dumps(submission))
        status = "ok"

    except Exception as e:
        print("Submission failed")
        status = str(e)

    return json.dumps({"status":status})
