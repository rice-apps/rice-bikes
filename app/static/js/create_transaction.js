$(document).ready(function() {

    $('#id_1-price').val(0);

    $('.checkbox').change(function() {

        // This is explicitly for prices with format ($<integer>)
        raw_text = $(this).closest('.fieldWrapper').text();
        text = raw_text.split(/\s+/)[1];
        task_price = parseInt(text.substring(2, text.length-1));

        was_checked = (this.checked);
        if(!was_checked) {
            this.checked = true;
            $('#id_1-price').val(parseInt($('#id_1-price').val()) + task_price);
        }
        else{
            this.checked = false;
            $('#id_1-price').val(parseInt($('#id_1-price').val()) - task_price);
        }
    });
});