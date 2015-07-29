(function(exports){

  function displayError(inputDiv, error, formId){
    $("#" + formId).find("#div_id_" + inputDiv).addClass("has-error");
    $("#" + formId).find("#error_id_" + inputDiv).attr("hidden", false).html(error);
  }

  function removeError(inputDiv, formId){
    $("#" + formId).find("#div_id_" + inputDiv).removeClass("has-error");
    $("#" + formId).find("#error_id_" + inputDiv).attr("hidden", true).html("");
  }

  exports.showFormErrors = function(errorResponse, formId){
    var errorsObject = JSON.parse(errorResponse).form_errors;
    var errorsArray = Object.keys(errorsObject);
    _.each(errorsArray, function(field){
      displayError(field, errorsObject[field], formId)
    })
  }

  exports.clearErrors = function(inputs, formId){
    _.each(inputs, function(field){
      removeError(field, formId);
    })
  }

})(this.crispyFormErrors = {});
