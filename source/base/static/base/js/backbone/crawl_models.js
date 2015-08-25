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


  exports.CrawlModelView = Backbone.View.extend({
    el: "#crawlModelTable",
    template: _.template($("#crawlModelTableItem").html()),
    initialize: function(model){
      var that = this;
      this.model = model;
      this.render();
    },
    render: function(){
      this.$el.append(this.template(this.model.toJSON()));
    },
  });


  exports.AddCrawlModelView = BaseViews.FormView.extend({
    el: "#addCrawlModelContainer",
    modal: "#addCrawlModelModal",
    form: "#addCrawlModelForm",
    project: $("#project_id").val(),
    formFields: [
      "name",
      "crawl_model",
      "rounds_left",
      "seeds_list",
      "crawler",
    ],
  });


  exports.CrawlModelCollectionView = Backbone.View.extend({
    el: "#crawlModelTableDiv",
    project: $("#project_id").val(),
    tableTemplate: _.template($("#crawlModelTableHeader").html()),
    noCrawlsTemplate: _.template($("#emptyCrawlModelTable").html()),
    modelView: exports.CrawlModelView,
    initialize: function(collection){
      var that = this;
      this.collection = collection;
      this.render();
    },
    render: function(){
      // Render each model in CrawlCollection into a separate Backbone view,
      // with one model per view.
      var that = this;
      if (this.collection.models.length){
        this.$el.html(this.tableTemplate());
        this.collection.each(function(model){
          var singleView = new that.modelView(model);
        });
      } else {
        this.$el.append(this.noCrawlModelsTemplate());
      }
    },
  });

})(this.CrawlModels = {});
