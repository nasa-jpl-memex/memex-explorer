$(document).ready(function(){
(function(){

  var uploadAjax = document.getElementById("upload_data");
  var progressBar = $("#progress");
  var uploadProgress = $("#upload_progress");
  var percentage = $("#upload_percentage");
  var success = false;
  var uploading = false;

  var xhr = new XMLHttpRequest();

  function pageClose(){
    return swal({
      title: "Uploaded Succeeded",
      text: "Close this window?",
      type: "warning",
      showCancelButton: true,
      confirmButtonColor: '#DD6B55',
      confirmButtonText: 'Yes!',
      cancelButtonText: "No!",
      closeOnConfirm: false,
      closeOnCancel: false
    },
    function(isConfirm){
      if (isConfirm){
        window.close();
      } else {
        swal("", "", "error");
      }
    })
  }

  function updateProgress(event){
    var percentComplete = parseInt((event.loaded / event.total) * 100);
    uploadProgress.attr("aria-valuenow", percentComplete);
    uploadProgress.css("width", percentComplete + "%");
    if (percentComplete == 100){
      percentage.html("Completed");
    } else {
      percentage.html(percentComplete + "%");
    }
  }

  function disableForm(formId){
    $("#" + formId).find(":input").attr("disabled", true);
    $("#" + formId).css({
      "background-color": "#f5f5f5",
      "border-radius": "8px",
    });
  }

  function getIndicesUrl(){
    split_url = window.location.href.split("/").slice(0, -2);
    split_url.push("indices");
    return split_url.join("/") + "/"
  }

  function getObjects(){
    return $.ajax({
      type: "POST",
      url: getIndicesUrl(),
      data: {"get": "objects"},
      success: function(response){
        return response;
      }
    });
  }

  var objectsResponse = getObjects();

  function isInArray(value, array) {
    return array.indexOf(value) > -1;
  }

  function isUnique(indexName){
    var jsonResponse = objectsResponse.responseJSON;
    if (isInArray(indexName, jsonResponse.slugs) || isInArray(indexName, jsonResponse.names)){
      return false;
    } else {
      return true;
    }
  }

  xhr.upload.addEventListener("progress", updateProgress, false);
  xhr.open('POST', uploadAjax.action, true);
  xhr.onload = function(){
    if ((xhr.status === 200) || (xhr.status === 302)){
      success = true;
      uploading = false;
      pageClose();
    } else {
      success = false;
      uploading = false;
    }
  }

  uploadAjax.onsubmit = function(event){
    event.preventDefault();
    uploading = true;
    if (isUnique(uploadAjax.name.value) != true){
      console.log("Non-unique name");
      uploading = false;
      return
    } else if (Boolean(uploadAjax.name.value) != true){
      console.log("Empty Name");
      uploading = false;
      return
    } else if (Boolean(uploadAjax.uploaded_data.files[0]) != true){
      console.log("Empty Files");
      uploading = false;
      return
    }
    disableForm("upload_data");
    progressBar.attr("hidden", false);
    var zipfile = uploadAjax.uploaded_data.files[0];
    var indexName = uploadAjax.name.value;
    var csrf_token = uploadAjax.csrfmiddlewaretoken.value;

    var formData = new FormData();
    formData.append("csrfmiddlewaretoken", csrf_token);
    formData.append("name", indexName);
    formData.append("uploaded_data", zipfile, zipfile.name);

    xhr.send(formData);
  }

  window.onbeforeunload = function(event){
    if (uploading == true){
      return "Reloading or navgating away from this page will cause the upload to fail.";
    }
  }

})();
});
