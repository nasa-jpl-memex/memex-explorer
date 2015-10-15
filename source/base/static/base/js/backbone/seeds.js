(function(exports){

  exports.Seeds = Backbone.Model.extend({
    urlRoot: "/api/seeds_list/",
    defaults: {
      seeds: "",
      file_string: "",
      name: "",
      slug: "",
      url: "",
    }
  });


  exports.SeedsCollection = Backbone.Collection.extend({
    url: "/api/seeds_list/",
    model: exports.Seeds,
  });


  exports.SeedsView = Backbone.View.extend({
    el: "#seeds",
    template: _.template($("#seedsItem").html()),
    initialize: function(model){
      this.model = model;
      _.bindAll(this, 'render');
      var that = this;
      this.modelObject = this.model.toJSON();
      this.deleteId = "#delete_seeds_" + this.modelObject.id
      // Reset events each time so backbone doesnt clump events together.
      this.events = {};
      this.events["submit " + this.deleteId] = "deleteSeeds"
      this.render();
    },
    render: function(){
      this.$el.append(this.template(this.model.toJSON()));
    },
    deleteSeeds: function(event){
      event.preventDefault();
      var confirmDelete = confirm("Are you sure you want to delete this seeds list?")
      if (confirmDelete == true){
        $.ajax({
          method: "DELETE",
          url: "/api/seeds_list/" + this.model.id + "/",
          success: function(response){
            window.location.reload();
          },
          error: function(response, xhr, thrownError){
            errorString = "";
            errors = response.responseJSON;
            _.each(errors.errors, function(error){
              errorString += ("\n\t" + error);
            })
            alert(errors.message + errorString);
          },
        });
      }
    },
  });


  exports.SeedsCollectionView = BaseViews.CollectionView.extend({
    modelView: exports.SeedsView,
  });


  exports.AddSeedsView = BaseViews.FormView.extend({
    el: "#addSeedsContainer",
    modal: "#newSeedsModal",
    form: "#addSeedsForm",
    filesField: "#id_seeds",
    formFields: [
      "name",
      "seeds",
    ],
    invalidLines: [],
    template: _.template($("#addSeedsTemplate").html()),
    initialize: function(collection){
      this.collection = collection;
      this.render();
      this.editor = CodeMirror.fromTextArea(document.getElementById("id_textseeds"), {
        lineNumbers: false,
      });
      this.editor.setSize("100%", 400);
    },
    render: function(){
      this.$el.html(this.template());
    },
    addSeeds: function(event){
      var that = this;
      event.preventDefault();
      var formObjects = this.toFormData(this.form);
      // Attach the contents of the file to the FormData object.
      var file = $(this.filesField)[0].files[0];
      if (typeof file != 'undefined'){
        formObjects.append("seeds", file, file.name);
      }
      var newSeeds = new exports.Seeds(formObjects);
      this.collection.add(newSeeds);
      // If model.save() is successful, clear the errors and the form, and hide
      // the modal. If model.save() had errors, show each error on form field,
      // along with the content of the error.
      newSeeds.save({}, {
        data: formObjects,
        contentType: false,
        beforeSend: function(){
          that.clearLineErrors();
        },
        success: function(response){
          var newSeeds = new exports.SeedsView(
            that.collection.models[that.collection.models.length - 1]
          );
          that.formSuccess(that.modal, that.form);
          that.clearErrors(that.formFields, that.form);
        },
        error: function(model, xhr, thrownError){
          that.showFormErrors(xhr.responseJSON, that.form);
          that.showLineErrors(xhr.responseJSON, that.form);
        },
      });
    },
    showLineErrors: function(errors){
      this.errors = errors["seeds"];
      $("#textseeds_label").html("");
      this.editor.setValue(this.errors[this.errors.length - 1]["list"]);
      var that = this;
      _.each(this.errors, function(seed){
        // Skip the initial error message.
        if((that.errors.indexOf(seed) == 0) || (that.errors.indexOf(seed) == that.errors.length - 1)){
          return;
        }
        line = that.editor.getLineHandle(Object.keys(seed));
        that.invalidLines.push(line);
        that.editor.doc.addLineClass(line, 'background', 'line-error');
      });
      this.clearFileInput();
    },
    clearLineErrors: function(){
      var that = this;
      $("#textseeds_label").html("Or, paste urls to crawl.");
      _.each(this.invalidLines, function(line){
        that.editor.doc.removeLineClass(line, 'background', 'line-error');
      });
      this.invalidLines = []
    },
    events: {
      "submit #addSeedsForm": "addSeeds",
    },
    clearFileInput: function(){
      var file = $("#id_seeds");
      file.replaceWith(file = file.clone( true ));
    }
  });

})(this.Seeds = {});
