$( document ).ready(function() {

  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) == (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  var csrftoken = getCookie('csrftoken');

/*
 * Crawl Dashboard interactions
 */

var buttons = {
  play: $('#playButton'),
  stop: $('#stopButton'),
  restart: $('#restartButton'),
  kill: $('#forceStopButton'),
  images: $('#dumpImages'),
  cca: $('#common-crawl-dump'),
}

var states = {
  "NOT STARTED": {
    "disabled": [
      "stop",
      "restart",
      "kill",
      "images",
      "cca",
    ],
    "enabled": [
      "play",
    ]
  },
  "STARTING": {
    "disabled": [
      "stop",
      "restart",
      "kill",
      "images",
      "cca",
      "play",
    ],
    "enabled": [],
  },
  "STARTED": {
    "disabled": [
      "play",
      "restart",
      "images",
      "cca",
    ],
    "enabled": [
      "stop",
      "kill",
    ],
  },
  "SUCCESS": {
    "disabled": [
      "play",
      "stop",
      "kill",
    ],
    "enabled": [
      "restart",
      "images",
      "cca",
    ],
  },
  "FAILURE": {
    "disabled": [
      "stop",
      "restart",
      "kill",
      "images",
      "cca",
      "play",
    ],
    "enabled": [],
  },
  "FORCE STOPPED": {
    "disabled": [
      "stop",
      "restart",
      "kill",
      "images",
      "cca",
      "play",
    ],
    "enabled": [],
  },
}


function disable(element){
  element.attr("disabled", true);
}


function enable(element){
  element.attr("disabled", false);
}


  $( document ).ready(function() {
    $('[data-toggle="tooltip"]').tooltip();
  });

  $("#dumpImages").attr("disabled", true);

  $('#common-crawl-dump').on('click', function() {
     $( '#status' ).text( "DUMPING" );
     this.disabled = true;
     $('#playButton').attr("disabled", true);
     $('#stopButton').attr("disabled", true);
     $('#common-crawl-dump').attr("disabled", false);

    $("#nutchButtons").append('<i id="imageSpinner" class="fa fa-refresh fa-spin" style="font-size:20;"></i>')
    $.ajax({
        type: "POST",
        data: {"action": "ccadump"},
        success: function(response) {
          sweetAlert("Success", "Crawled data has been successfully dumped in CCA format!", "success");
          $("#imageSpinner").remove()
          $('#playButton').attr("disabled", false);
        },
        failure: function() {
          sweetAlert("Error", "Dump in CCA format has failed.", "error");
          $("#imageSpinner").remove()
        }
      });
  });


  $('#playButton').on('click', function() {

    $( '#status' ).text( "STARTING" );
    this.disabled = true;
    $('#stopButton').attr("disabled", false);
    $('#rounds').attr("disabled", true);

    val = $("#rounds")? $("#rounds").val() : 0,

    $.ajax({
      type: "POST",
      data: {
        "action": "start",
        "rounds": val,
      },
      success: function(response) {
        $('#getCrawlLog').attr("disabled", false);
        $('#forceStopButton').attr("disabled", false);
        console.log(response);
        if (response.status != "error") $( '#status' ).text(response.status);
        else console.log(response)},
      failure: function() {
        $( '#status' ).text( "Error (could not start crawl)" );
      }
    });
  });


  $('#stopButton').on('click', function() {

    $( '#status' ).text( "STOPPING" );
    this.disabled = true;

    $.ajax({
      type: "POST",
      data: {
        "action": "stop",
      },
      success: function(response) {
        console.log(response);
        if (response.status != "error") $( '#status' ).text(response.status);
        else console.log(response)},
      failure: function() {
        $( '#status' ).text( "Error (could not stop crawl)" );
      }
    });
  });

  function forceStop(){
    $( '#status' ).text( "STOPPING" );
    this.disabled = true;

    $.ajax({
      type: "POST",
      data: {
        "action": "force_stop",
      },
      success: function(response) {
        console.log(response);
        if (response.status != "error") $( '#status' ).text(response.status);
        else console.log(response)},
      failure: function() {
        $( '#status' ).text( "Error (could not stop crawl)" );
      }
    });
    return "success"
  }

  $('#forceStopButton').on('click', function() {
    swal({
      title: "Are you sure?",
      text: "This will corrupt all crawl data, and you will be unable to restart the crawl.",
      type: "warning",
      showCancelButton: true,
      confirmButtonColor: '#DD6B55',
      confirmButtonText: 'Yes, stop it!',
      cancelButtonText: "No, cancel!",
      closeOnConfirm: false,
      closeOnCancel: false
    },
    function(isConfirm){
      if (isConfirm){
        forceStop();
        swal("Stopped", "Your crawl has been stopped.", "success");
      } else {
        swal("Cancelled", "You cancelled the force-stop process", "error");
      }
    })
  })

  $('#restartButton').on('click', function() {

    $( '#status' ).text( "RESTARTING" );
    this.disabled = true;

    val = $("#rounds")? $("#rounds").val() : 0,

    $.ajax({
      type: "POST",
      data: {
        "action": "start",
        "rounds": val,
      },
      success: function(response) {
        console.log(response);
        if (response.status != "error") $( '#status' ).text(response.status);
        else console.log(response)},
      failure: function() {
        $( '#status' ).text( "Error (could not restart crawl)" );
      }
    });
  });

  function statusCall(){
    return $.ajax({
      type: "POST",
      data: {"action": "status"},
      success: function(response){
        $( '#status' ).text(response.status);
        $( '#roundsLeft' ).text(response.rounds_left);
        $( '#stats-pages' ).text(response.pages_crawled);
        if ('harvest_rate' in response) {
          $( '#stats-harvest' ).text(response.harvest_rate);
          if (response.harvest_rate > 0) {
            $('#getSeeds').attr("disabled", false);
          }
        }
        if (response.status == "STOPPED"){
          $('#stopButton').attr("disabled", true);
          $('#restartButton').attr("disabled", false);
          $('#forceStopButton').attr("disabled", true);
          $('#dumpImages').attr("disabled", false);
        } else if (response.status == "STARTED") {
          $('#stopButton').attr("disabled", false);
          $('#rounds').attr("disabled", true);
        } else if (response.status == "SUCCESS") {
          $('#stopButton').attr("disabled", true);
          $('#forceStopButton').attr("disabled", true);
          $('#restartButton').attr("disabled", false);
          $('#rounds').attr("disabled", false);
        } else if (response.status == "FORCE STOPPED") {
          $('#restartButton').attr("disabled", true);
          $('#stopButton').attr("disabled", true);
          $('#forceStopButton').attr("disabled", true);
          $('#rounds').attr("disabled", true);
        } else if (response.status == "DUMPING") {
          $('#stopButton').attr("disabled", true);
          $('#forceStopButton').attr("disabled", true);
          $('#restartButton').attr("disabled", false);
          $('#rounds').attr("disabled", false);
        }
      }
    });
  }

  statusCall();

  setInterval(function(){
    statusCall();
  }, 5000);

  $("#gotoSolr").on('click', function(){
    solr_url = "http://" + window.location.hostname + ":8983/solr/#"
      window.open(solr_url, '_blank');
  });

  $("#dumpImages").on('click', function(){
    $("#nutchButtons").append('<i id="imageSpinner" class="fa fa-refresh fa-spin" style="font-size:20;"></i>')
    $.ajax({
      type: "POST",
      data: {"action": "dump"},
      success: function(response) {
        sweetAlert("Success", "Images have been successfully dumped!", "success");
        $("#imageSpinner").remove()
      },
      failure: function() {
        sweetAlert("Error", "Image dump has failed.", "error");
        $("#imageSpinner").remove()
      }
    });
  });


});
