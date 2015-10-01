(function(exports){

  exports.Seeds = Backbone.Model.extend({
    urlRoot: "/api/seeds_list/",
    defaults: {
      seeds: "",
      name: "",
      slug: "",
    }
  });


  exports.SeedsCollection = Backbone.Model.extend({
    url: "/api/seeds_list/",
    model: Seeds,
  });


  exports.SeedsCollectionView = Backbone.Model.extend({
    el: "#addProjectContainer",
    modal: "#newProjectModal",
    form: "#addProjectForm",
    formFields: ["name"],
    template: _.template($("#addProjectTemplate").html()),
    initialize: function(collection){
      this.collection = collection;
      this.render();
    },
    render: function(){
      this.$el.html(this.template());
    },
    addProject: function(event){
      var that = this;
      event.preventDefault();
      var formObjects = this.toJson(this.form);
      var newProject = new Project(formObjects);
      this.collection.add(newProject);
      // If model.save() is successful, clear the errors and the form, and hide
      // the modal. If model.save() had errors, show each error on form field,
      // along with the content of the error.
      newProject.save({}, {
        success: function(response){
          var newProject = new ProjectView(
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
    events: {
      "submit #addProjectForm": "addProject",
    },
  });

})(this.Seeds = {});
