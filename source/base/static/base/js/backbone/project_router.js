(function(exports){

  var ProjectRouter = Backbone.Router.extend({
    routes: {
      "": "index",
    },
    index: function(){
      var project = $("#project_id").val();
      var modelCollection = new CrawlModels.CrawlModelCollection();
      var crawlCollection = new Crawls.CrawlCollection();
      modelCollection.fetch({
        url: modelCollection.url += "?project=" + project,
      });
      // Create the views only if the crawls were successfully fetched.
      crawlCollection.fetch({
        url: crawlCollection.url += "?project=" + project,
        success: function(){
          var crawlCollectionView = new Crawls.CrawlCollectionView(crawlCollection);
          var crawlFormView = new Crawls.AddCrawlView(crawlCollection, modelCollection, crawlCollectionView);
        },
      });
    },
  });


  $(document).ready(function(){
    var appRouter = new ProjectRouter();
    Backbone.history.start();
  });

})(this.projectRouter = {});
