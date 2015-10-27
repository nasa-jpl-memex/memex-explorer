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
    el: "trails",
    template: _.template($("#trailItem").html()),
    initialize: function(model){
      var that = this;
      this.model = model;
      this.render();
    },
    render: function(){
      this.$el.append(this.template(this.model.toJSON()));
    },
  });


  exports.TrailsCollectionView = BaseViews.CollectionView.extend({
    modelView: exports.TrailView,
  });

})(this.Trails = {});
