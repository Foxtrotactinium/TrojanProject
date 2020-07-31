$(document).ready(function()
{
    $('[data-href]').click(function()
    {
        window.location = $(this).data('href');
        return false;
    });

    $('[data-id]').click(function()
    {
        $("#id_part").val($(this).data('id'));
    });

    $('[data-aid]').click(function()
    {
        $("#id_activity").val($(this).data('aid'));
    });

    $('[data-sid]').click(function()
    {
        $("#id_supplier").val($(this).data('sid'));
    });

});




