(function(exports){

  var Project = Backbone.Model.extend({
    urlRoot: "/api/projects/",
    defaults: {
      name: "",
      description: "",
      url: "",
      slug: "",
    },
  });


  var ProjectCollection = Backbone.Collection.extend({
    url: "/api/projects/",
    model: Project,
  });


  var ProjectView = Backbone.View.extend({
    el: "#projects",
    template: _.template($("#indexProjectItem").html()),
    initialize: function(model){
      this.model = model;
      _.bindAll(this, 'render');
      var that = this;
      this.render();
    },
    render: function(){
      this.$el.append(this.template(this.model.toJSON()));
    },
  });


  var AddProjectView = BaseViews.FormView.extend({
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


  var ProjectCollectionView = BaseViews.CollectionView.extend({
    modelView: ProjectView,
  });


  var IndexRouter = Backbone.Router.extend({
    routes: {
      "": "index",
    },
    index: function(){
      var projectCollection = new ProjectCollection();
      var collectionView = new ProjectCollectionView(projectCollection);
      var addProjectView = new AddProjectView(projectCollection);
    },
  });


  $(document).ready(function(){
    var appRouter = new IndexRouter();
    Backbone.history.start();
  });

})(this.projects = {});
