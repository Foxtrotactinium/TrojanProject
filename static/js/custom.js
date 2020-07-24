$(document).ready(function()
{
    $('[data-href]').click(function()
    {
        window.location = $(this).data('href');
        return false;
    });

    $('[data-id]').click(function()
    {
        $("#id_partsrequired").val($(this).data('id'));
    });

    $('[data-aid]').click(function()
    {
        $("#id_activityid").val($(this).data('aid'));
    });
});




