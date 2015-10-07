(function(exports){

  exports.SeedsFormItem = Backbone.View.extend({
    el: "#id_seeds_object",
    template: _.template($("#crawlFormSeeds").html()),
    initialize: function(model){
      this.model = model;
      _.bindAll(this, 'render');
      this.render();
    },
    render: function(){
      this.$el.append(this.template(this.model.toJSON()));
    },
  });


  exports.AddSeedsProjectPage = Seeds.AddSeedsView.extend({
    render: function(){
      var that = this;
      this.$el.html(this.template());
      if (this.collection.models.length){
        this.collection.each(function(model){
          var singleView = new exports.SeedsFormItem(model);
        });
      }
      $(this.modal).on('hidden.bs.modal', function(event){
        if ($("#newSeedsModal").attr("aria-hidden") == "false"){
          $("body").addClass("modal-open");
        }
      });
    },
    addSeeds: function(){
      var that = this;
      event.preventDefault();
      var formObjects = this.toFormData(this.form);
      // Attach the contents of the file to the FormData object.
      var file = $(this.filesField)[0].files[0];
      if (typeof file != 'undefined'){
        formObjects.append("seeds", file, file.name);
      }
      var newSeeds = new Seeds.Seeds(formObjects);
      this.collection.add(newSeeds);
      // If model.save() is successful, clear the errors and the form, and hide
      // the modal. If model.save() had errors, show each error on form field,
      // along with the content of the error.
      newSeeds.save({}, {
        data: formObjects,
        contentType: false,
        success: function(response){
          var newSeeds = new exports.SeedsFormItem(
            that.collection.models[that.collection.models.length - 1]
          );
          that.formSuccess(that.modal, that.form);
          that.clearErrors(that.formFields, that.form);
        },
        error: function(model, xhr, thrownError){
          that.showFormErrors(xhr.responseJSON, that.form);
        },
      });
    },
  });

})(this.AddSeeds = {});
