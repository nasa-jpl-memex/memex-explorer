(function(exports){

  var Seeds = Backbone.Model.extend({
    urlRoot: "/api/seeds_list/",
    defaults: {
      seeds: "",
      name: "",
      slug: "",
    }
  });


  var SeedsCollection = Backbone.Collection.extend({
    url: "/api/seeds_list/",
    model: Seeds,
  });


  var SeedsView = Backbone.View.extend({
    el: "#seeds",
    template: _.template($("#seedsItem").html()),
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


  var SeedsCollectionView = BaseViews.CollectionView.extend({
    modelView: SeedsView,
  });


  var SeedsRouter = Backbone.Router.extend({
    routes: {
      "": "index",
    },
    index: function(){
      var seedsCollection = new SeedsCollection();
      var seedsCollectionView = new SeedsCollectionView(seedsCollection);
      // var addProjectView = new AddProjectView(projectCollection);
    },
  });


  $(document).ready(function(){
    var appRouter = new SeedsRouter();
    Backbone.history.start();
  });

})(this.Seeds = {});
