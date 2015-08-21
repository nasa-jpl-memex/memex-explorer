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


  exports.AddCrawlFormModel = Backbone.View.extend({
    el: "#id_crawl_model",
    template: _.template($("#crawlFormModel").html()),
    initialize: function(model){
      var that = this;
      this.model = model;
      this.render();
    },
    render: function(){
      this.$el.append(this.template(this.model.toJSON()));
    },
  });


  exports.AddCrawlView = BaseViews.FormView.extend({
    el: "#addCrawlContainer",
    modal: "#addCrawlModal",
    form: "#addCrawlForm",
    formFields: [
      "name",
      "crawl_model",
      "rounds_left",
      "seeds_list",
      "crawler",
    ],
    modelView: exports.AddCrawlFormModel,
    template: _.template($("#addCrawlTemplate").html()),
    initialize: function(crawlCollection, modelCollection){
      var that = this;
      this.crawlCollection = crawlCollection;
      this.modelCollection = modelCollection;
      this.render();
    },
    render: function(){
      var that = this;
      this.$el.html(this.template());
      this.modelCollection.each(function(model){
        var newModelOption = new that.modelView(model);
      });
    },
  });


  exports.CrawlCollectionView = Backbone.View.extend({
    el: "#crawlTableDiv",
    tableTemplate: _.template($("#crawlTableHeader").html()),
    noCrawlsTemplate: _.template($("#emptyTable").html()),
    modelView: exports.CrawlView,
    initialize: function(collection){
      var that = this;
      this.project = $("#project_id").val();
      this.collection = collection;
      this.render();
    },
    render: function(){
      // Render each model in CrawlCollection into a separate Backbone view,
      // with one model per view.
      var that = this;
      if (this.collection.models.length){
        this.$el.append(this.tableTemplate());
        this.collection.each(function(model){
          var singleView = new that.modelView(model);
        });
      } else {
        this.$el.append(this.noCrawlsTemplate());
      }
    },
  });

})(this.Crawls = {});
