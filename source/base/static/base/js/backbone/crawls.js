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


  exports.AddCrawlView = BaseViews.FormView.extend({
    el: "#addProjectContainer",
    modal: "#newProjectModal",
    form: "#addProjectForm",
    formFields: [
      "name",
      "crawl_model",
      "rounds_left",
      "seeds_list",
      "crawler",
    ],
    template: _.template($("#addProjectTemplate").html()),
    initialize: function(crawlCollection, modelCollection){
      var that = this;
      this.crawlCollection = crawlCollection;
      this.modelCollection = modelCollection;
    },
    render: function(){

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
      this.collection.fetch({
        url: that.collection.url += "?project=" + that.project,
        success: function(){
          that.render();
        },
      });
    },
    render: function(){
      // Render each model in ProjectCollection into a separate backbone view,
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
