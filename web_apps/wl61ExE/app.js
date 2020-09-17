

$.ajax({
    method: "GET",
    url: "/public/api/projects/" + dataiku.defaultProjectKey + "/variables/",
    headers : {
        "Authorization" : "Basic " + btoa(dataiku.defaultAPIKey + ":" + "")
    }
}).done(function(data){
   
    console.log("project variable:",data);
    document.getElementById('only-after').innerHTML = data.standard["only_after"]
    f_html = ""
    f_html_upload = "<option value='' selected disabled hidden>Choose a file</option>"
    data.standard["file_list"].forEach(function(f){
        var html = `
            <div class="checkbox">
                <input type="checkbox" name="${f}" id="${f}" />
                <label for="${f}">${f}</label>
            </div>`;
        var html_upload = `
            <option value="${f}">${f}</option>`;
        f_html = f_html + html
        f_html_upload = f_html_upload + html_upload
    })
    document.getElementById('file-select').innerHTML = f_html_upload
});
        

//Ensure only one file can be selected when uploading a file
$('.file-list').on('change', function() {
    $('.file-list').not(this).prop('checked', false);  
});



let uploadResults = document.getElementById('message');
let commentsInput = document.getElementById('comments');

var submit_params = {}


$('#upload-button').click(function() {
    
    if (document.getElementById('file-select').value == ""){
        uploadResults.innerHTML = "You must select a type file first"
        uploadResults.style.color = "red"
        return
    }

    
    selected_file = document.getElementById('file-select').value
    comment = commentsInput.value
    let newFile = $('#new-file')[0].files[0];
    let form = new FormData();
    form.append('file', newFile);
    form.append('selected_file', selected_file);
    form.append('comment',  comment);
    
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

