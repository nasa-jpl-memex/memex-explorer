$(document).ready(function () {

    $("#upload_file").change(function ()
    {
        if($("#upload_file").val()) {
            $('#column_name_x').prop("readonly", true);
            $('#column_name_y').prop("readonly", true);
        }
        else {
            $('#column_name_x').prop("readonly", false);
            $('#column_name_y').prop("readonly", false);

            $('#column_name_x').val('');
            $('#column_name_y').val('');
        }
    });
});