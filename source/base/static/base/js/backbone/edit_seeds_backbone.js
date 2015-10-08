(function(exports){

  var EditSeedsView = Backbone.View.extend({
    el: "#seeds",
    form: "#editSeedsForm",
    template: _.template($("#editSeedsTemplate").html()),
    initialize: function(model){
      this.model = model;
      var that = this;
      this.model.set({id: $("#seeds_pk").val()}).fetch({
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
      this.model.save({
        success: function(){
          alert("Success!")
        }
      })
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
      var seedsView = new EditSeedsView(seedsList);
    },
  });

  $(document).ready(function(){
    var appRouter = new EditSeedsRouter();
    Backbone.history.start();
  });

})(this.EditSeeds = {});
