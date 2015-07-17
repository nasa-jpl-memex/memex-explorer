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
        $("#response").html(response["plot"]["script"] + response["plot"]["div"]);
        //$("#response").text('Looks like it worked! Task ID: ' + task_id);
        $("#task-id").text(task_id)
      },
      error: function(response){
        $("#response").text(JSON.stringify(response))
      },
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
        $("#response").text(JSON.stringify(response))
      },
      error: function(response) {
        $("#response").text("The progress ping failed.\n" + JSON.stringify(response))
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
