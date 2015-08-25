(function(exports){

  exports.CrawlModel = Backbone.Model.extend({
    urlRoot: "/api/crawl_models/",
    defaults: {
      id: 0,
      slug: "",
      name: "",
      project: 0,
      features: "",
      model: "",
    },
  });


  exports.CrawlModelCollection = Backbone.Collection.extend({
    url: "/api/crawl_models/",
    model: exports.CrawlModel,
  });


  exports.CrawlView = Backbone.View.extend({
    el: "#crawlTable",
    template: _.template($("#crawlTableItem").html()),
    initialize: function(model){
      var that = this;
      this.model = model;
      this.render();
    },
    render: function(){
      this.$el.append(this.template(this.model.toJSON()));
    },
  });


  exports.AddCrawlView = BaseViews.FormView.extend({});


  exports.CrawlCollectionView = Backbone.View.extend({});

})(this.CrawlModels = {});
