(function(exports){

  exports.FormView = Backbone.View.extend({
    modal: "",
    form: "",
    formFields: [],
    clearErrors: function(){
      var that = this;
      _.each(this.formFields, function(field){
        $(that.form).find("#div_id_" + field).removeClass("has-error");
        $(that.form).find("#error_id_" + field).attr("hidden", true).html("")
      });
    },
    showFormErrors: function(errors){
      // This code is particular to the JSON response given by the REST api.
      var errorsArray = Object.keys(errors);
      var that = this;
      _.each(errorsArray, function(field){
        $(that.form).find("#div_id_" + field).addClass("has-error");
        $(that.form).find("#error_id_" + field).attr("hidden", false).html(errors[field][0]);
      });
    },
    formSuccess: function(){
      $(this.modal).modal('hide');
      $(this.form)[0].reset();
    },
  });

})(this.baseViews = {});
