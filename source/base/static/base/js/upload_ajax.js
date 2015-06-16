$(document).ready(function(){
(function(){

  var uploadAjax = document.getElementById("upload_data");

  uploadAjax.onsubmit = function(event){
    event.preventDefault();
    var zipfile = uploadAjax.uploaded_data.files[0];
    var indexName = uploadAjax.name.value;
    var csrf_token = uploadAjax.csrfmiddlewaretoken.value;

    var formData = new FormData();
    formData.append("csrfmiddlewaretoken", csrf_token);
    formData.append("name", indexName);
    formData.append("uploaded_data", zipfile, zipfile.name);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', uploadAjax.action, true);
    xhr.onload = function(){
      if (xhr.status === 200){
        console.log("Success");
      } else {
        console.log("Error");
      }
    }
    xhr.send(formData);
  }

})();
});
