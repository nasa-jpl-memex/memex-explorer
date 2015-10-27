(function(){

  var Trail = Backbone.Model.extend({
    urlRoot: "/api/datawake",
    defaults: {
      trail: {},
      domain: "",
      user: "",
      urls: [],
    },
  });


  var TrailsCollection = Backbone.Collection.extend({
    url: "/api/datawake",
    model: Trail,
  });


  var TrailView = Backbone.View.extend({
    initialize: function(){
      null;
    },
    render: function(){
      null;
    },
  });


  var TrailsCollectionView = BaseViews.CollectionView.extend({
    modelView: "",
  });

})(this.Trails = {});
