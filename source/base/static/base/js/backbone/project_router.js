(function(exports){

  var ProjectRouter = Backbone.Router.extend({
    routes: {
      "": "index",
    },
    index: function(){
      var collection = new Crawls.CrawlCollection();
      var collectionView = new Crawls.CrawlCollectionView();
      var formView = new Crawls.CrawlFormView()
    },
  });


  $(document).ready(function(){
    var appRouter = new ProjectRouter();
    Backbone.history.start();
  });

})(this.projectRouter = {});
