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


  var AddProjectView = baseViews.FormView.extend({
    el: "#addProjectContainer",
    modal: "#newProjectModal",
    form: "#addProjectForm",
    formFields: ["name"],
    template: _.template($("#addProjectTemplate").html()),
    initialize: function(collection){
      this.collection = collection;
      _.bindAll(this, 'render');
      this.render();
    },
    render: function(){
      this.$el.html(this.template());
    },
    addProject: function(event){
      var that = this;
      event.preventDefault();
      var formObjects = ajaxForms.toJson($("#addProjectForm"));
      var newProject = new Project(formObjects);
      this.collection.add(newProject);
      newProject.save({}, {
        success: function(response){
          var newProject = new ProjectView(
            that.collection.models[that.collection.models.length - 1]
          );
          that.formSuccess();
          that.clearErrors();
        },
        error: function(model, xhr, thrownError){
          that.showFormErrors(xhr.responseJSON);
        },
      });
    },
    events: {
      "submit #addProjectForm": "addProject",
    },
  });


  var ProjectCollectionView = Backbone.View.extend({
    initialize: function(collection){
      this.collection = collection;
      _.bindAll(this, 'render');
      var that = this;
      this.collection.fetch({
        success: function(){
          that.render();
        }
      });
    },
    render: function(){
      this.collection.each(function(project){
        var projectView = new ProjectView(project);
      });
    },
  });


  var ProjectRouter = Backbone.Router.extend({
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
    var appRouter = new ProjectRouter();
    Backbone.history.start();
  });

})(this.projects = {});
