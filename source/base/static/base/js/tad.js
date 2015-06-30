var tad = tad || {};

(function(){

  function tadUpdate(){
    return $.ajax({
      type: "POST",
      data: {
        "get": "data",
      },
      success: function(response){
        $("#tadResponse").html(response)
        console.log(response);
      },
      error: function(response){
        $("#tadResponse").html(response)
        console.log("Failure");
      },
    });
  }

  $(document).ready(function(){
    $("#tadUpdate").click(function(){
      tadUpdate();
      setInterval(function(){
        tadUpdate();
      }, 5000);
    });
  });

})();
