/*Load project variable params
Example 
{
    "last_compute_date":"2020/07/27-21:32:00",
    "countries": "[\"India\",\"Thailand\",\"UK\"]",
    "archive_folder":"vOv1eTkv",
    "tracking_folder":"3zAYHyFW",
    "default_file_extension":".pdf"
}
*/
global_countries = []

$.ajax({
    method: "GET",
    url: "/public/api/projects/" + dataiku.defaultProjectKey + "/variables/",
    headers : {
        "Authorization" : "Basic " + btoa(dataiku.defaultAPIKey + ":" + "")
    }
}).done(function(data){

    countries = data.standard["countries"]
    window["global_countries"] = JSON.parse(countries)
    debugger;
    webapp_params = {
        archive_folder:data.standard["archive_folder"],
        tracking_folder:data.standard["tracking_folder"],
        countries:data.standard["countries"],
        file_list:data.standard["file_list"],
        default_file_extension:data.standard["default_file_extension"]
    }
    console.log(webapp_params)
    
    $.getJSON(getWebAppBackendUrl('/load_params'),
                webapp_params,
                function(data) {
        if (data.status == "ok"){console.log("Parameters loaded in backend")}
        else {console.log("Parameters loading in backend failed - Check python logs")}
    });    
    
    country_html = ""
    country_html_upload = "<option value='' selected disabled hidden>Choose a file</option>"
    data.standard["file_list"].forEach(function(country){
        var html = `
            <div class="checkbox">
                <input type="checkbox" name="${country}" id="${country}" />
                <label for="${country}">${country}</label>
            </div>`;
        var html_upload = `
            <option value="${country}">${country}</option>`;
        country_html = country_html + html
        country_html_upload = country_html_upload + html_upload
    })
    document.getElementById('countries-div').innerHTML = country_html
    document.getElementById('country-select').innerHTML = country_html_upload
});        
        

//Ensure only one country can be selected when uploading a file
$('.country-list').on('change', function() {
    $('.country-list').not(this).prop('checked', false);  
});


let countrySection = document.getElementById('countries-section');
let uploadSection = document.getElementById('upload-section');
let uploadResults = document.getElementById('message');
let submitSection = document.getElementById('submit-section');
let submitParams = document.getElementById('submit-params');
let submitButton = document.getElementById('submit-button');
let commentsInput = document.getElementById('comments');
let commentsTitle = document.getElementById('comments-title');
let submitResults = document.getElementById('submit-results');


var submit_params = {}




$('#upload-button').click(function() {
    
    if (document.getElementById('country-select').value == ""){
        uploadResults.innerHTML = "You must select a type file first"
        uploadResults.style.color = "red"
        return
    }

    
    selected_file = document.getElementById('country-select').value
    comment = commentsInput.value
    let newFile = $('#new-file')[0].files[0];
    let form = new FormData();
    form.append('file', newFile);
    form.append('country', selected_file);
    form.append('comments',  comment);
    
    $.ajax({
        type: 'post',
        url: getWebAppBackendUrl('/upload-to-dss'),
        processData: false,
        contentType: false,
        data: form,
        success: function (data) {
            results = JSON.parse(data)
            console.log(results);
            if (results["status"] == "ok"){
                uploadResults.innerHTML = "Upload successful <br>"
                uploadResults.style.color = "green"
                                
                results["file_type"] = [selected_file]
                results["comment"] = [comment]
                
                submit_dict = {}
                submit_txt = ''
                for (result_key in results) {
                    if (result_key != "status"){
                        submit_dict[result_key] = results[result_key]
                        submit_txt = submit_txt + result_key + " : " + results[result_key] + "<br>"
                    }
                }
                window["submit_params"] = submit_dict
                uploadResults.innerHTML += submit_txt
            }
            else {
                uploadResults.innerHTML = "Upload failed - " + results["status"]
                uploadResults.style.color = "red"
            }
        },
        error: function (jqXHR, status, errorThrown) {
            console.error("upload_to_dss function failed");
            console.error(jqXHR.responseText);
            uploadResults.innerHTML = "Upload failed - " + jqXHR.responseText
            uploadResults.style.color = "red"
        }
    });
    
})

