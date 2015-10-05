(function(exports){

  var SeedsRouter = Backbone.Router.extend({
    routes: {
      "": "index",
    },
    index: function(){
      seedsCollection = new Seeds.SeedsCollection();
      seedsCollectionView = new Seeds.SeedsCollectionView(seedsCollection);
      addSeedsView = new Seeds.AddSeedsView(seedsCollection);
    },
  });


  $(document).ready(function(){
    var appRouter = new SeedsRouter();
    Backbone.history.start();
  });

})();
