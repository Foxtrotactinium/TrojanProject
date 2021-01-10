$(document).ready(function () {
    $('.setbutton').click(function () {
        $('input[name=' + $(this).data("partid") + ']').val($(this).data("value"));
        $("#submit-id-save").click();
    });

    $('#completeAll').click(function () {
        $(".setbutton").each(function () {
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
//        window.location = $(this).data('href');
        window.open($(this).data('href'));
//         return false;
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

    $(".orderingForm").each(function (index, elem) {
        // REF:
        // https://dev.to/nemecek_f/django-how-to-let-user-re-order-sort-table-of-content-with-drag-and-drop-3nlp
        let tblId = $(this).data('tblid');
        let btnId = $(this).data('btnid');

        const groups = document.getElementById(tblId);
        let sortable = Sortable.create(groups, {
            handle: '.handle',
            chosenClass: 'table-primary',
            onChange: () => {
                saveOrderingButton.disabled = false;
            }
        });

        const saveOrderingButton = document.getElementById(btnId);
        const formInput = $(elem).children('.orderingInput');


        function saveOrdering() {
            const rows = document.getElementById(tblId).querySelectorAll('tr');
            let ids = [];
            for (let row of rows) {
                ids.push(row.dataset.lookup);
            }
            $(formInput).val(ids.join(','));
            elem.submit();
        }

        saveOrderingButton.addEventListener('click', saveOrdering);
    });

    $("form.silent_form").submit(function () {
        alert("Updated");
        return false;
    });

});




