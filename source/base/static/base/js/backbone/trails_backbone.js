(function(exports){

  exports.Trail = Backbone.Model.extend({
    urlRoot: "/api/datawake",
    defaults: {
      trail: {},
      domain: "",
      user: "",
      urls: [],
    },
  });


  exports.TrailsCollection = Backbone.Collection.extend({
    url: "/api/datawake",
    model: exports.Trail,
  });


  exports.TrailView = Backbone.View.extend({
    initialize: function(){
      null;
    },
    render: function(){
      null;
    },
  });


  exports.TrailsCollectionView = BaseViews.CollectionView.extend({
    modelView: exports.TrailView,
  });

})(this.Trails = {});
