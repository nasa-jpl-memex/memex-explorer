(function(exports){

  exports.formSubmit = function(formData){
    return $.ajax({
      method: "POST",
      data: {
        action: "add_crawl",
        form_data: formData,
      },
      success: function(response){
        console.log(response);
      },
      failure: function(response){
        console.log(response);
      }
    });
  }

  exports.formToJson = function(formElement){
    var formDataObject = new FormData();
    var formData = formElement.serializeArray();
    _.each(formData, function(formObject){
      formDataObject[formObject.name] = formObject.value;
    });
    return formDataObject;
  }

})(this.ajaxForms = {});
