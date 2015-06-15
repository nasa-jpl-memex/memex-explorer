$(document).ready(function(){
(function(){

  var uploadAjax = document.getElementById("upload_ajax");
  var indexName = document.getElementById("name");
  var submitButton = document.getElementById("submit");

  uploadAjax.onsubmit = function(event){
    event.preventDefault();
  }

  var uploadedFiles = document.getElementById("uploaded_files");
  var files = uploadedFiles.files;
  var formData = new FormData();

  window.uploadAjax = uploadAjax;

})();
});
