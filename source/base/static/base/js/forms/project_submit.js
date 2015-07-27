(function(){
  $(document).ready(function(){

    var addProjectForm = $("#addProjectForm");

    addProjectForm.submit(function(event){
      event.preventDefault();
      var xhr = ajaxForms.xhrFactory(window.location.href + "add_project/", "addProjectForm");
      var formData = ajaxForms.toFormData(addProjectForm);

      crispyFormErrors.clearErrors(
        [
          "name",
        ],
        "addProjectForm"
      );

      xhr.send(formData);
    });

    $("#cancelSubmit").click(function(){
      crispyFormErrors.clearErrors(
        [
          "name",
        ],
        "addProjectForm"
      );
    });

  });
})();
