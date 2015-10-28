(function(exports){

  var SeedsRouter = Backbone.Router.extend({
    routes: {
      "": "index",
    },
    index: function(){
      seedsCollection = new Seeds.SeedsCollection();
      seedsCollectionView = new Seeds.SeedsCollectionView(seedsCollection);
      addSeedsView = new Seeds.AddSeedsView(seedsCollection);
      trailsCollection = new Trails.TrailsCollection();
      trailsCollectionView = new Trails.TrailsCollectionView(trailsCollection);
      window.trails = trailsCollection;
    },
  });


  $(document).ready(function(){
    var appRouter = new SeedsRouter();
    Backbone.history.start();
  });

})();
