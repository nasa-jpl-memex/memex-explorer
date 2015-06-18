$(document).ready(function(){
  (function(){

    var uploadAjax = document.getElementById("upload_data");
    var csrf_token = uploadAjax.csrfmiddlewaretoken.value;

    function deleteIndex(){
      return $.ajax({
        type: "POST",
        url: window.location.href + "delete/",
        data: {csrfmiddlewaretoken: csrf_token},
        success: function(){
          window.close(); 
        },
        failure: function(){
          return "error";
        }
      });
    }

    $('#deleteIndexButton').click(function(){
      swal({
        title: "Are you sure?",
        text: "This will delete the index and all files associated with the index.",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: '#DD6B55',
        confirmButtonText: 'Yes, delete it!',
        cancelButtonText: "No, cancel!",
        closeOnConfirm: false,
        closeOnCancel: false
      },
      function(isConfirm){
        if (isConfirm){
          deleteIndex();
        } else {
          swal("Cancelled", "You cancelled the delete process", "error");
        }
      })
    });


  })();
});
