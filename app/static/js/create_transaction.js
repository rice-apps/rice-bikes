$(document).ready(function() {

    $('#id_1-price').val(0);

    $('input:checkbox').change(function() {

        // This is explicitly for prices with format ($<integer>)
        raw_text = $(this).closest('.fieldWrapper').text();

        text = raw_text.split(/\s+/)[1];
        task_price = parseInt(text.substring(2, text.length-1));

        console.log($(this));

        is_checked = $(this).prop('checked');

        if(is_checked) {
            $('#id_1-price').val(parseInt($('#id_1-price').val()) + task_price);
        }
        else{
            $('#id_1-price').val(parseInt($('#id_1-price').val()) - task_price);
        }
    });
});