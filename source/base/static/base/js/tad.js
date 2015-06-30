var tad = tad || {};

(function(){

  function tadUpdate(){
    return $.ajax({
      type: "POST",
      data: {
        "get": "data",
      },
      success: function(response){
        console.log(response);
      },
      error: function(response){
        console.log("Failure");
      },
    });
  }

  $(document).ready(function(){
    tadUpdate();
  });

})();
