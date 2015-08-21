(function(exports){

  var ProjectRouter = Backbone.Router.extend({
    routes: {
      "": "index",
    },
    index: function(){
      var modelCollection = new CrawlModels.CrawlModelCollection();
      var crawlCollection = new Crawls.CrawlCollection();
      modelCollection.fetch();
      window.modelCollection = modelCollection;
      var crawlCollectionView = new Crawls.CrawlCollectionView(crawlCollection);
      var crawlFormView = new Crawls.AddCrawlView(crawlCollection, modelCollection);
    },
  });


  $(document).ready(function(){
    var appRouter = new ProjectRouter();
    Backbone.history.start();
  });

})(this.projectRouter = {});
