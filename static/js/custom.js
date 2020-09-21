$(document).ready(function()
{
    $('.setbutton').click(function() {
    $('input[name='+$(this).data("partid")+']').val( $(this).data("value"));
    });

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

    $('.low-stock-button').click(function()
    {
        $("tr:not(.table-danger)").hide();
    });

    $("#button-id-add-stock").click(function(e)
    {
    var input = prompt('How much to add ?','0');
    var num = parseInt(input);

    var previous = $("#id_stockOnHand").val();
    var previous_num = parseInt(previous);

    $("#id_stockOnHand").val(previous_num + num);
    $("#submit-id-save").click();
    });

});




