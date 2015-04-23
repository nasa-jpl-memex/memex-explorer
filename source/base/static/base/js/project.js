$(document).ready(function(){
  $("#createIndex").on('click', function(){
    $.ajax({
      type: "POST",
      data: {"action": "create_index"},
      success: function(response) {
        sweetAlert("Success", "Elastic Search index created!", "success");
        $("#imageSpinner").remove()
      },
      failure: function() {
        sweetAlert("Error", "Index creation has failed.", "error");
        $("#imageSpinner").remove()
      }
    });
  });
});
