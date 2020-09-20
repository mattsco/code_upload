import dataiku
import pandas as pd
from flask import request
from datetime import datetime

client = dataiku.api_client()

var = dataiku.get_custom_variables()
archive_folder = var["archive_folder"] 
tracking_folder = var["tracking_folder"] 
default_file_extension = var["default_file_extension"] 
file_list = var["file_list"] 
ext_list = var["extension"] 
extension_dict = dict(zip(eval(file_list),eval(ext_list)))

@app.route('/upload-to-dss', methods = ['POST'])
def upload_to_dss():
    
    selected_file = request.form.get('selected_file')
    
    #get file
    f = request.files.get('file')
    if f is None:
        return json.dumps({"status":"No file sent to backend"})
    initial_filename = f.filename
    extension = os.path.splitext(initial_filename)[1]
    if extension != extension_dict[selected_file]:
        return json.dumps({"status":"Extension must be '%s', '%s' was found"%(default_file_extension, extension)})

    
    #get user
    request_headers = dict(request.headers)
    user = client.get_auth_info_from_browser_headers(request_headers)["authIdentifier"]
    #user = client.get_auth_info()["authIdentifier"]
    
    #get time
    now = datetime.now()
    date = now.strftime("%Y-%m-%d-%H-%M-%S")
  
    
    selected_month = request.form.get('selected_month')
    comment = request.form.get('comment')
    
    dss_filename = '%s_%s_%s%s' %(date, selected_file, user, extension)
    
    #Save uploaded file
    try:
        dataiku.Folder(archive_folder).upload_stream(dss_filename, f)
        status = "ok"
    except Exception as e:
        print("fail")
        status = str(e)

    #Write metadata
    submission = {"status":status, "date":date, "user":user, "initial_filename":f.filename, "dss_filename":dss_filename}
    submission["file_type"] = selected_file 
    submission["selected_month"] = selected_month 
    submission["comment"] = comment

    try:
        dataiku.Folder(tracking_folder).upload_stream("%s_%s_%s.json"%(date, selected_file, user), json.dumps(submission))
        status = "ok"

    except Exception as e:
        print("Submission failed")
        status = str(e)
    
        
    return json.dumps(submission)


