var tad = tad || {};

(function(){

  function submit_query(){
    return $.ajax({
      type: "POST",
      data: {
        "action": "post",
      },
      success: function(response){
        task_id = response['task-id'];
        $("#response").html(
            "Looks like things worked! Here's your magical task ID:<br />" +
            "<b>" + response['task-id'] + "</b>");
        $("#task-id").text(task_id)
      },
      error: function(response){
        $("#response").html("Something failed! Hopefully what follows is useful:<br />" + 
            '<span style="color: red;">' + JSON.stringify(response) + '</span>')
      }
    });
  }

  function get_results(){
    return $.ajax({
      type: "POST",
      data: {
        "action": "progress",
        "task-id": $("#task-id").text()
      },
      success: function(response) {
        $("#response").html(response['plot']['script'] + response['plot']['div'] +
          JSON.stringify(response['result']))
      },
      error: function(response){
        $("#response").html("Something failed! Hopefully what follows is useful:<br />" + 
          '<span style="color: red;">' + JSON.stringify(response) + '</span>')
      }
    });
  }

  $(document).ready(function(){
    $("#run-detector").click(function(){
      submit_query();
    });
    $("#get-status").click(function(){
      get_results();
    });
  });

})();
