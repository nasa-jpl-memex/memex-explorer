$( document ).ready(function(){
    $('#getSeeds').on('click', function() {
        $.ajax({
            type: "POST",
            data: {"action": "seeds"},
            success: function(response){
                console.log(response);
            },
        });
    });
});
