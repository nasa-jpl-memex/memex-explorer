$(document).ready(function(){
(function(){

  var uploadAjax = document.getElementById("upload_data");

  uploadAjax.onsubmit = function(event){
    event.preventDefault();
    var zipfile = uploadAjax.uploaded_data.files[0];
    var name = uploadAjax.name;

    var formData = new FormData();
    formData.append("name", name);
    formData.append("uploaded_data", zipfile, zipfile.name);

    window.formData = formData;

    var xhr = new XMLHttpRequest();
  }

})();
});
