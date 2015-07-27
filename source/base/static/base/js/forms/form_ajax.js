(function(exports){

  exports.toFormData = function(formElement){
    var objects = new FormData();
    var formData = formElement.serializeArray();
    _.each(formData, function(formObject){
      objects[formObject.name] = formObject.value;
      objects.append(formObject.name, formObject.value)
    });
    return objects;
  }

  exports.toJson = function(formElement){
    var objects = {};
    var formData = formElement.serializeArray();
    _.each(formData, function(formObject){
      objects[formObject.name] = formObject.value;
    });
    return objects;
  }

  exports.xhrFactory = function(url){
    var xhr = new XMLHttpRequest();
    xhr.open('POST', url, true);
    xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    xhr.onload = function(){
      if ((xhr.status === 200) || (xhr.status === 302)){
        success = true;
      } else {
        crispyFormErrors.showFormErrors(xhr.response);
        success = false;
      }
    }
    return xhr;
  }

})(this.ajaxForms = {});
