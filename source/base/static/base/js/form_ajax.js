(function(exports){

  exports.formSubmit = function(formElement){
    return $.ajax({
      method: "POST",
      data: formToJson(formElement),
      success: function(response){
        console.log(response);
      },
      failure: function(response){
        console.log(response);
      }
    });
  }

  exports.formToJson = function(formElement){
    var objects = {};
    var formData = formElement.serializeArray();
    _.each(formData, function(formObject){
      objects[formObject.name] = formObject.value;
    });
    return objects;
  }

})(this.ajaxForms = {});
