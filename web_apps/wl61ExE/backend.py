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


var = dataiku.get_custom_variables()
archive_folder = var["archive_folder"] 
tracking_folder = var["tracking_folder"] 
default_file_extension = var["default_file_extension"] 
file_list = var["file_list"] 


@app.route('/load_params')
def load_params():

    print("archive_folder:%s, tracking_folder:%s, default_file_extension:%s"%(archive_folder, tracking_folder, default_file_extension))
    print(file_list)
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
       
    selected_file = request.form.get('selected_file')
    comment = request.form.get('comment')
    dss_filename = '%s_%s_%s_%s%s' %(day, hour, selected_file, user, extension)
    
    #Save uploaded file
    try:
        dataiku.Folder(archive_folder).upload_stream(dss_filename, f)
        status = "ok"
    except Exception as e:
        print("fail")
        status = str(e)

    #Write metadata
    submission = {"status":status, "day":day, "hour":hour, "user":user, "initial_filename":f.filename, "dss_filename":dss_filename}
    submission["file_type2"] = selected_file 
    submission["comment2"] = comment

    try:
        dataiku.Folder(tracking_folder).upload_stream("%s_%s_%s.json"%(submission["day"], submission["hour"], submission["user"]), json.dumps(submission))
        status = "ok"

    except Exception as e:
        print("Submission failed")
        status = str(e)
    
        
    return json.dumps(submission)


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
        

    return json.dumps({"status":status})
