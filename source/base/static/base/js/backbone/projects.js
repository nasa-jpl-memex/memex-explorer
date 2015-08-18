(function(exports){

  var Project = Backbone.Model.extend({
    urlRoot: "/api/projects/",
    defaults: {
      name: "",
      description: "",
    },
  });

  var ProjectCollection = Backbone.Collection.extend({
    url: "/api/projects/",
    model: Project,
  });

  var ProjectView = Backbone.View.extend({
    initialize: function(model){
      this.model = model;
      _.bindAll(this, 'render');
      var that = this;
      this.render();
    },
    render: function(){

    },
  });

  var ProjectRouter = Backbone.Router.extend({
    routes: {
      "": "index",
    },
    index: function(){
      var projectCollection = new ProjectCollection();
      window.collection = projectCollection;
    },
  });
  var appRouter = new ProjectRouter();
  Backbone.history.start();

})(this.projects = {});
