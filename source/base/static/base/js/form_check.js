$(document).ready(function () {

    $("#upload_file").change(function ()
    {
        if($("#upload_file").val()) {
            $('#uri').val('uri will automatically be generated');
            $("#uri").prop("readonly", true);

        }
        else {
            $("#uri").prop("readonly", false);
            $('#uri').val('');
        }
    });
});
