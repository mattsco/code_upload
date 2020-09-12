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
    file_list.forEach(function(country){
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

let updateSection = document.getElementById('update-section');
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

$(document).ready(function(){
    $('input[type=radio]').click(function(){
        if (this.value === "true") {
            uploadSection.style.display="block";
            countrySection.style.display="none";
        }
        else {
            uploadSection.style.display="none";
            countrySection.style.display="block";    
        }
    });
});


$('#upload-button').click(function() {
    
    if (document.getElementById('country-select').value == ""){
        uploadResults.innerHTML = "You must select a country first"
        uploadResults.style.color = "red"
        submitSection.style.display = "none"
        return
    }
    if (document.getElementById('listed-select').value == ""){
        uploadResults.innerHTML = "You must select the type of customer (listed/unlisted)"
        uploadResults.style.color = "red"
        submitSection.style.display = "none"
        return
    }
    
    selected_country = document.getElementById('country-select').value
    customer_type = document.getElementById('listed-select').value
    
    let newFile = $('#new-file')[0].files[0];
    let form = new FormData();
    form.append('file', newFile);
    form.append('country', selected_country);
    form.append('customer_type', customer_type);
    
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
                uploadResults.innerHTML = "Upload successful - Please submit your results"
                uploadResults.style.color = "green"
                submitSection.style.display = "block"
                                
                results["update"] = "yes"
                results["countries"] = [selected_country]
                results["customer_type"] = customer_type
                
                submit_dict = {}
                submit_txt = ''
                for (result_key in results) {
                    if (result_key != "status"){
                        submit_dict[result_key] = results[result_key]
                        submit_txt = submit_txt + result_key + " : " + results[result_key] + "<br>"
                    }
                }
                window["submit_params"] = submit_dict
                submitParams.innerHTML = submit_txt
            }
            else {
                uploadResults.innerHTML = "Upload failed - " + results["status"]
                uploadResults.style.color = "red"
                submitSection.style.display = "none"
            }
        },
        error: function (jqXHR, status, errorThrown) {
            console.error("upload_to_dss function failed");
            console.error(jqXHR.responseText);
            uploadResults.innerHTML = "Upload failed - " + jqXHR.responseText
            uploadResults.style.color = "red"
            submitSection.style.dispaly = "none"
        }
    });
    
})


$('#validate-button').click(function() {
    //final_submit_dict = window["submit_params"]
    //final_submit_dict["comments"] = commentsInput.value
    
    select_countries = []
    window["global_countries"].forEach(function(country){
        if ( $(`#${country}`).is(':checked')) {
            select_countries.push(country)
        }
    })
    
    $.getJSON(getWebAppBackendUrl('/prepare_submission_without_update'),
                function(data) {
        data["countries"] = select_countries
        data["update"] = "no"
        
        submit_txt = ''
        for (data_key in data) {
            submit_txt = submit_txt + data_key + " : " + data[data_key] + "<br>"
        }
        
        window["submit_params"] = data
        submitParams.innerHTML = submit_txt
        submitSection.style.display = "block"

    });
})


$('#submit-button').click(function() {
    final_submit_dict = window["submit_params"]
    final_submit_dict["comments"] = commentsInput.value
    console.log(final_submit_dict)
    
    $.getJSON(getWebAppBackendUrl('/submit'),
              {"submission":JSON.stringify(final_submit_dict)},
                function(data) {
        countrySection.style.display = "none"
        uploadSection.style.display = "none"
        commentsInput.style.display = "none"
        commentsTitle.style.display = "none"
        submitButton.style.display = "none"
        updateSection.style.display = "none"
        submitResults.style.display = "block"
        submitParams.innerHTML = submitParams.innerHTML + "comments : " + commentsInput.value
        
        if (data["status"] == "ok"){
            submitResults.innerHTML = "Submission accepted. Please refresh for a new submission"
            submitResults.style.color = "green"
        }
        else {
            submitResults.innerHTML = "Submission failed. Please refresh for a new submission <br>" + data["status"]
            submitResults.style.color = "red"
        }
    });
    
})
