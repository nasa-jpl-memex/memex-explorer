var tad = tad || {};

(function(){

  function submit_query(){
    return $.ajax({
      type: "POST",
      data: {
        "action"                : "post",
        "target-filters"        : "{" + $("#target-filters").val() + "}",
        "baseline-filters"      : "{" + $("#baseline-filters").val() + "}",
        "analysis-start-date"   : $("#analysis-start-date").val(),
        "analysis-end-date"     : $("#analysis-end-date").val(),
        "constant-baseline"     : $("#constant-baseline").is(":checked"),
        "scale-baseline"        : $("#scale-baseline").is(":checked"),
        "index"                 : $("#index").val(),
        "time_field"            : $("#time-field").val()
      },
      success: function(response){
        $("#raw-response").text(JSON.stringify(response, null, 2));
        task_id = response['result']['task-id'];
        if (task_id)
        {
          $("#response").html(
            "Looks like things worked! Here's your magical task ID:<br />" +
            "<b>" + task_id + "</b>");
          $("#task-id").text(task_id);
          $("#raw-response").text(JSON.stringify(response, null, 2));
          setTimeout(get_results, 1000);
        }
        else
        {
          $("#response").html("Something failed! Hopefully something in the response is useful.<br />" + response['result']['error']); 
          $("#raw-response").html('<span style="color: red;">' + JSON.stringify(response, null, 2) + '</span>');
        }
      },
      error: function(response){
        $("#response").html("Something failed! Hopefully something in the response is useful."); 
        $("#raw-response").html('<span style="color: red;">' + JSON.stringify(response, null, 2) + '</span>');
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
        $("#raw-response").text(JSON.stringify(response['result'], null, 2));
        if ((response['result']['status'] != 'Finished') && (!response['result']['error']))
          setTimeout(get_results, 1000);
        else
          $("#response").html(
            response['pvalue_plot']['script'] + response['pvalue_plot']['div'] +
            response['count_plot']['script'] + response['count_plot']['div']);
      },
      error: function(response){
        $("#response").html("Something failed! Hopefully something in the response is useful.") 
        $("#raw-response").html('<span style="color: red;">' + JSON.stringify(response, null, 2) + '</span>');
      }
    });
  }

  $(document).ready(function(){
    $("#run-detector").click(function(){
      submit_query();
    });
  });

})();

$(function() {
    $.datepicker.setDefaults({
        dateFormat: 'yy-mm-dd'
    });
});

$(function() {
    $("#analysis-start-date").datepicker();
});

$(function() {
    $("#analysis-end-date").datepicker();
});
