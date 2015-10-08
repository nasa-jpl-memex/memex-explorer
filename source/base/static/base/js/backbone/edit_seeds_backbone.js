(function(exports){

  var EditSeedsView = Backbone.View.extend({
    el: "#seeds",
    form: "#editSeedsForm",
    template: _.template($("#editSeedsTemplate").html()),
    initialize: function(model){
      this.model = model;
      var that = this;
      this.model.fetch({
        success: function(){
          that.render();
          that.setEditor();
        }
      });
    },
    render: function(){
      this.$el.append(this.template(this.model.toJSON()));
    },
    setEditor: function(){
      this.editor = CodeMirror.fromTextArea(document.getElementById("id_seeds"), {
        lineNumbers: true
      });
      this.loadSeeds();
    },
    editSeeds: function(event){
      var that = this;
      event.preventDefault();
      var newSeeds = JSON.stringify($("#id_seeds").val().replace("\r", "").split("\n"))
      this.model.set("seeds", newSeeds);
    },
    loadSeeds: function(){
      this.editor.setValue(this.model.toJSON().file_string);
    },
    events: {
      "submit #editSeedsForm": "editSeeds",
      "click #reset": "loadSeeds",
    },
  });


  var EditSeedsRouter = Backbone.Router.extend({
    routes: {
      "": "index",
    },
    index: function(){
      var seedsList = new Seeds.Seeds();
      var seedsListPk = $("#seeds_pk").val();
      seedsList.urlRoot = seedsList.urlRoot + seedsListPk + "/";
      var seedsView = new EditSeedsView(seedsList);
    },
  });

  $(document).ready(function(){
    var appRouter = new EditSeedsRouter();
    Backbone.history.start();
  });

})(this.EditSeeds = {});
