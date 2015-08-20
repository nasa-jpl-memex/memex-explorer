(function(exports){

  exports.Crawl = Backbone.Model.extend({
    urlRoot: "/api/crawls/",
    defaults: {
      id: 1,
      slug: "",
      seeds_list: "",
      status: "",
      config: "",
      index_name: "",
      url: "",
      pages_crawled: 0,
      harvest_rate: 0.0,
      location: "",
      name: "",
      description: "",
      crawler: "",
      rounds_left: 0,
      project: 0,
      crawl_model: 0,
    },
  });


  exports.CrawlCollection = Backbone.Collection.extend({
    url: "/api/crawls/",
    model: exports.Crawl,
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


  exports.CrawlCollectionView = Backbone.View.extend({
    el: "#crawlTableDiv",
    template: _.template($("#crawlTableHeader").html()),
    modelView: exports.CrawlView,
    initialize: function(collection){
      var that = this;
      this.collection = collection;
      this.collection.fetch({
        url: that.collection.url += "?project=" + $("#project_id").val(),
        success: function(){
          that.render();
        },
      });
    },
    render: function(){
      // Render each model in ProjectCollection into a separate backbone view,
      // with one model per view.
      var that = this;
      this.$el.append(this.template());
      this.collection.each(function(model){
        var singleView = new that.modelView(model);
      });
    },
  });

})(this.Crawls = {});
