(function(exports){

  exports.CrawlModel = Backbone.Model.extend({
    urlRoot: "/api/crawl_models/",
    defaults: {
      slug: "",
      name: "",
      project: 0,
      features: "",
      model: "",
      url: "",
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
    modal: "#crawlModelModal",
    form: "#addCrawlModelForm",
    project: $("#project_id").val(),
    formFields: [
      "name",
      "model",
      "features",
    ],
    featuresField: "#id_features",
    modelField: "#id_model",
    template: _.template($("#addCrawlModelTemplate").html()),
    initialize: function(collection, collectionView){
      var that = this;
      this.collection = collection;
      this.collectionView = collectionView;
      this.render();
    },
    render: function(){
      var that = this;
      this.$el.html(this.template());
    },
    addCrawlModel: function(event){
      var that = this;
      event.preventDefault();
      var formObjects = this.toFormData(this.form);
      // Attach the contents of the file to the FormData object.
      var features = $(this.featuresField)[0].files[0];
      var model = $(this.modelField)[0].files[0];
      if (typeof features != 'undefined'){
        formObjects.append("features", features, features.name);
      }
      if (typeof model != 'undefined'){
        formObjects.append("model", model, model.name);
      }
      var newModel = new exports.CrawlModel(formObjects);
      this.collection.add(newModel);
      // If model.save() is successful, clear the errors and the form, and hide
      // the modal. If model.save() had errors, show each error on form field,
      // along with the content of the error.
      newModel.save({}, {
        data: formObjects,
        contentType: false,
        success: function(response){
          // After success, if the size of the collection is 1, re-render the
          // collection view.
          if (that.collection.models.length == 1){
            that.collectionView.render();
          } else {
            var newModelView = new exports.CrawlModelView(
              that.collection.models[that.collection.models.length - 1]
            );
            var newModelOption = new Crawls.AddCrawlFormModel(
              that.collection.models[that.collection.models.length - 1]
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
      "submit #addCrawlModelForm": "addCrawlModel",
    }
  });


  exports.CrawlModelCollectionView = Backbone.View.extend({
    el: "#crawlModelTableDiv",
    project: $("#project_id").val(),
    tableTemplate: _.template($("#crawlModelTableHeader").html()),
    noCrawlModelsTemplate: _.template($("#emptyCrawlModelTable").html()),
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
