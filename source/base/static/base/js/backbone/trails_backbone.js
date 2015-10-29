(function(exports){

  exports.Trail = Backbone.Model.extend({
    urlRoot: "/api/datawake",
    defaults: {
      docid: "",
      trail_id: 0,
      domain_name: "",
      urls: [],
      urls_string: "",
    },
  });


  exports.TrailsCollection = Backbone.Collection.extend({
    url: "/api/datawake",
    model: exports.Trail,
  });


  exports.TrailView = Backbone.View.extend({
    el: "#trails",
    template: _.template($("#trailItem").html()),
    initialize: function(model){
      var that = this;
      this.model = model;
      this.render();
    },
    render: function(){
      this.$el.append(this.template(this.model.toJSON()));
    },
    events: {},
  });


  exports.TrailFormView = BaseViews.FormView.extend({
    el: "#trailSeedsCreation",
    modal: "#trailModal",
    form: "#trailForm",
    formFields: [
      "seedsname",
    ],
    template: _.template($("#trailFormBody").html()),
    initialize: function(collection){
      this.render();
      this.editor = CodeMirror.fromTextArea(document.getElementById("id_trailseeds"), {
        lineNumbers: false,
        readOnly: true,
      });
      this.editor.setSize("100%", 400);
    },
    render: function(){
      this.$el.html(this.template());
    },
  });


  exports.TrailsCollectionView = BaseViews.CollectionView.extend({
    el: "#trailHeader",
    template: _.template($("#trailHead").html()),
    modelView: exports.TrailView,
    initialize: function(collection){
      this.collection = collection;
      var that = this;
      this.collection.fetch({
        success: function(){
          that.render();
        },
      });
    },
    render: function(){
      // Render each model in collection into a separate backbone view,
      // with one model per view.
      var that = this;
      if(this.collection.length){
        this.$el.append(this.template());
        this.collection.each(function(model){
          var singleView = new that.modelView(model);
        });
      }
    },
  });

})(this.Trails = {});
