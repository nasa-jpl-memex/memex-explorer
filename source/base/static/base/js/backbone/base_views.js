(function(exports){

  exports.FormView = Backbone.View.extend({
    modal: "",
    form: "",
    formFields: [],
    clearErrors: function(fields, form){
      // Clear errors from the form after it has been successfully submitted.
      var that = this;
      _.each(fields, function(field){
        $(form).find("#div_id_" + field).removeClass("has-error");
        $(form).find("#error_id_" + field).attr("hidden", true).html("")
      });
    },
    showFormErrors: function(errors, form){
      // Take the JSON response from the server containing the errors, parse them,
      // and show them on the form.
      var that = this;
      var errorsArray = Object.keys(errors);
      _.each(errorsArray, function(field){
        $(form).find("#div_id_" + field).addClass("has-error");
        $(form).find("#error_id_" + field).attr("hidden", false).html(errors[field][0]);
      });
    },
    formSuccess: function(modal, form){
      // If the submit was successful, hide the modal and reset the form.
      $(modal).modal('hide');
      $(form)[0].reset();
    },
    toFormData: function(form){
      // Convert the contents of the form to FormData, to allow for file uploads.
      var objects = new FormData();
      var formData = $(form).serializeArray();
      _.each(formData, function(formObject){
        objects[formObject.name] = formObject.value;
        objects.append(formObject.name, formObject.value)
      });
      return objects;
    },
    toJson: function(form){
      // Convert the contents of the form to JSON with key:value pairs, where the
      // key is the name of the field and the value is the value of the field.
      var objects = {};
      var formData = $(form).serializeArray();
      _.each(formData, function(formObject){
        objects[formObject.name] = formObject.value;
      });
      return objects;
    },
  });


  // View for rendering each item in a collection to a new view. Must define
  // which modelView to use to render.
  exports.CollectionView = Backbone.View.extend({
    modelView: "",
    initialize: function(collection){
      this.collection = collection;
      var that = this;
      this.collection.fetch({
        success: function(){
          that.render();
        },
      });
    },
    render: function(){
      // Render each model in collection into a separate backbone view,
      // with one model per view.
      var that = this;
      this.collection.each(function(model){
        var singleView = new that.modelView(model);
      });
    },
  });

})(this.BaseViews = {});
