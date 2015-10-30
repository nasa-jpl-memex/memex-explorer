(function(exports){

  // Module-wide variables
  var module = {};


  exports.Trail = Backbone.Model.extend({
    urlRoot: "/api/datawake",
    defaults: {
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
      this.trailId = this.model.toJSON()["trail_id"];
      this.render();
      this.events = {};
      this.events["click #trail_" + this.trailId] = "setForm";
    },
    render: function(){
      this.$el.append(this.template(this.model.toJSON()));
    },
    setForm: function(){
      $("#id_trailseeds").val(this.model.toJSON()["urls_string"]);
    }
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
    },
    render: function(){
      this.$el.html(this.template());
    },
    createSeeds: function(events){
      var that = this;
      event.preventDefault();
      // Convert formdata to fields necessary for creating a seeds list.
      var formObjects = this.toFormData(this.form);
      formObjects["name"] = formObjects["seedsname"];
      formObjects["textseeds"] = $("#id_trailseeds").val();
      delete formObjects["seedsname"];
      var newSeeds = new Seeds.Seeds(formObjects);
      newSeeds.save({}, {
        success: function(response){
          that.formSuccess(that.modal, that.form);
          that.clearErrors(that.formFields, that.form);
          var newSeedsView = new Seeds.SeedsView(response)
        },
        error: function(model, xhr, thrownError){
          // Convert the name of the error to seedsname, to avoid conflict with
          // the add seeds form.
          var response = xhr.responseJSON;
          response["seedsname"] = response["name"];
          delete response["name"]
          that.showFormErrors(response, that.form);
        },
      });
    },
    events: {
      "submit #trailForm": "createSeeds",
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
