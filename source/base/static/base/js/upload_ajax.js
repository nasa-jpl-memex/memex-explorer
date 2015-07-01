$(document).ready(function(){
  (function(){

    var uploadAjax = document.getElementById("upload_data");
    var progressBar = $("#progress");
    var uploadProgress = $("#upload_progress");
    var percentage = $("#upload_percentage");
    var success = false;
    var uploading = false;

    var nameErrorSelector = $("#name_error");
    var fileErrorSelector = $("#file_error");

    var xhr = new XMLHttpRequest();

    function pageClose(){
      var closeMessage = "The upload is complete. Close this window?";
      if (confirm(closeMessage)){
        window.close();
      }
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
      var url = window.location.href;
      if (url.indexOf("settings") > -1){
        return url.split("/").slice(0, -3).join("/") + "/"
      } else {
        split_url = url.split("/").slice(0, -2);
        split_url.push("datasets");
        return split_url.join("/") + "/"
      }

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
      if (isInArray(indexName, jsonResponse.index_slugs) || isInArray(indexName, jsonResponse.index_names) || isInArray(indexName, jsonResponse.crawl_names) || isInArray(indexName, jsonResponse.crawl_names)){
        return false;
      } else {
        return true;
      }
    }

    xhr.upload.addEventListener("progress", updateProgress, false);
    xhr.open('POST', window.location.href, true);
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
      var formError = false;
      nameErrorSelector.attr("hidden", true);
      fileErrorSelector.attr("hidden", true);
      uploading = true;
      if (!!nameErrorSelector.length){
        if (isUnique(uploadAjax.name.value) == false){
          nameErrorSelector.attr("hidden", false);
          nameErrorSelector.html("* Index by this name already exists");
          uploading = false;
          formError = true;
        } else if (Boolean(uploadAjax.name.value) == false){
          nameErrorSelector.attr("hidden", false);
          nameErrorSelector.html("* Please provide a name for the index");
          uploading = false;
          formError = true;
        }
      }
      if (Boolean(uploadAjax.uploaded_data.files[0]) == false){
        fileErrorSelector.attr("hidden", false);
        fileErrorSelector.html("* Please provide a zipfile to upload");
        uploading = false;
        formError = true;
      }
      if (formError != false){
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
