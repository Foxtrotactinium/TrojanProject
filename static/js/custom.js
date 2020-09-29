$(document).ready(function () {
    $('.setbutton').click(function () {
        $('input[name=' + $(this).data("partid") + ']').val($(this).data("value"));
        $("#submit-id-save").click();
    });

    $('#completeAll').click(function (){
        $(".setbutton").each(function() {
            $('input[name=' + $(this).data("partid") + ']').val($(this).data("value"));
        });
        $("#submit-id-save").click();
    });

    $('#id_obsolete').click(function () {
        const checked = $(this).is(':checked');
        if (checked) {
            if (!confirm('Are you sure you want to make this part obsolete?')) {
                $(this).prop("checked", false);
            }
        } else if (!confirm('Are you sure you want to remove this part from being obsolete?')) {
            $(this).prop("checked", true);
        }
    });

    $('[data-href]').click(function () {
        // window.location = $(this).data('href');
        window.open($(this).data('href'));
        // return false;
    });

    $('[data-id]').click(function () {
        $("#id_part").val($(this).data('id'));
    });

    $('[data-aid]').click(function () {
        $("#id_activity").val($(this).data('aid'));
    });

    $('[data-sid]').click(function () {
        $("#id_supplier").val($(this).data('sid'));
    });

    $('.low-stock-button').click(function () {
        $("tr:not(.table-danger)").toggle();
    });

    $("#button-id-add-stock").click(function () {
        const input = prompt('How much to add ?', '0');
        const num = parseInt(input);

        const htmlSelector = $("#id_stockOnHand");

        const previous = htmlSelector.val();
        const previous_num = parseInt(previous);

        htmlSelector.val(previous_num + num);
        $("#submit-id-save").click();
    });

});




