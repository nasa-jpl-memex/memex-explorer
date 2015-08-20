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
    model: Crawl,
  });


  exports.CrawlView = Backbone.View.extend({});


  exports.AddCrawlView = BaseViews.FormView.extend({});


  exports.CrawlCollectionView = BaseViews.CollectionView.extend({
    modelView: exports.CrawlView,
  });

})(this.crawls = crawls);
