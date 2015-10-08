(function(exports){

  var EditSeedsView = Backbone.View.extend({
    el: "#seeds",
    template: _.template($("#editSeedsForm").html()),
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
      this.editor = CodeMirror.fromTextArea(document.getElementById("id_textseeds"), {
        lineNumbers: true
      });
      this.editor.setValue(this.model.toJSON().file_string);
      window.editor = this.editor;
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
