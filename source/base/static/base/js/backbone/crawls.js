(function(exports){

  exports.Crawl = Backbone.Model.extend({
    urlRoot: "/api/crawls/",
    defaults: {
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
    project: $("#project_id").val(),
    filesField: "#id_seeds_list",
    formFields: [
      "name",
      "crawl_model",
      "rounds_left",
      "seeds_list",
      "crawler",
    ],
    modelView: exports.AddCrawlFormModel,
    template: _.template($("#addCrawlTemplate").html()),
    initialize: function(crawlCollection, modelCollection, collectionView){
      var that = this;
      this.crawlCollection = crawlCollection;
      this.modelCollection = modelCollection;
      this.collectionView = collectionView;
      this.on("renderCrawlForm", this.afterRender);
      this.render();
    },
    render: function(){
      var that = this;
      this.$el.html(this.template());
      this.modelCollection.each(function(model){
        var newModelOption = new that.modelView(model);
      });
      this.trigger("renderCrawlForm");
    },
    afterRender: function(){
      this.onCrawlerChange();
    },
    // Hide Crawl Model when Nutch is selected, hide Rounds when Ache is selected.
    onCrawlerChange: function(){
      var crawler = $("#addCrawlForm :input[id='cancelSubmit']");
      var nutch = $('#id_crawler_1');
      var crawl_model = $('#id_crawl_model');
      var model_div = $('#div_id_crawl_model');
      var rounds_div = $('#div_id_rounds_left');
      var rounds = $('#id_rounds_left')
      if (nutch[0].checked){
        crawl_model.prop("disabled", true);
        rounds.prop("disabled", false);
        model_div.prop("hidden", true);
        rounds_div.prop("hidden", false);
        model_div.addClass("input-greyed-out");
        model_div.removeClass("input-available");
        rounds_div.addClass("input-available");
        rounds_div.removeClass("input-greyed-out");
      } else {
        crawl_model.prop("disabled", false);
        rounds.prop("disabled", true);
        model_div.prop("hidden", false);
        rounds_div.prop("hidden", true);
        model_div.addClass("input-available");
        model_div.removeClass("input-greyed-out");
        rounds_div.addClass("input-greyed-out");
        rounds_div.removeClass("input-available");
      }
    },
    addCrawl: function(event){
      var that = this;
      event.preventDefault();
      var formObjects = this.toFormData(this.form);
      // Attach the contents of the file to the FormData object.
      var file = $(this.filesField)[0].files[0];
      if (typeof file != 'undefined'){
        formObjects.append("seeds_list", file, file.name);
      }
      var newCrawl = new exports.Crawl(formObjects);
      this.crawlCollection.add(newCrawl);
      // If model.save() is successful, clear the errors and the form, and hide
      // the modal. If model.save() had errors, show each error on form field,
      // along with the content of the error.
      newCrawl.save({}, {
        data: formObjects,
        contentType: false,
        success: function(response){
          // After success, if the size of the collection is 1, re-render the
          // collection view.
          if (that.crawlCollection.models.length == 1){
            that.collectionView.render();
          } else {
            var newCrawlView = new exports.CrawlView(
              that.crawlCollection.models[that.crawlCollection.models.length - 1]
            );
          }
          that.formSuccess(that.modal, that.form);
          that.clearErrors(that.formFields, that.form);
        },
        error: function(model, xhr, thrownError){
          that.showFormErrors(xhr.responseJSON, that.form);
        },
      });
    },
    events: {
      "submit #addCrawlForm": "addCrawl",
      "change #addCrawlForm :input[name='crawler']": "onCrawlerChange",
    },
  });


  exports.CrawlCollectionView = Backbone.View.extend({
    el: "#crawlTableDiv",
    project: $("#project_id").val(),
    tableTemplate: _.template($("#crawlTableHeader").html()),
    noCrawlsTemplate: _.template($("#emptyTable").html()),
    modelView: exports.CrawlView,
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
        this.$el.append(this.noCrawlsTemplate());
      }
    },
  });

})(this.Crawls = {});
