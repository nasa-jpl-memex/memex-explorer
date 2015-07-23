(function(exports){

  exports.displayError = function(inputDiv, error){
    $("#div_id_" + inputDiv).addClass("has-error");
    $("#error_id_" + inputDiv).attr("hidden", false).html(error);
  }

  exports.removeError = function(inputDiv){
    $("#div_id_" + inputDiv).removeClass("has-error");
    $("#error_id_" + inputDiv).attr("hidden", true).html("");
  }

})(this.crispyFormErrors = {});
