$(document).ready(function() {

    // Initial behavior //

    $('#id_1-price').val(0); // set price to 0

    //hide vin text fields
    vin_field_list = $("[id*="+'vin'+"]");
    for (i=0;i<vin_field_list.length; i++){
        $(vin_field_list[i]).closest('.fieldWrapper').hide();
    }

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

    $('select').change(function() {
        selection = $('select').prop('value');
        rental_bike = $("[id*="+'rental_vin'+"]").closest('.fieldWrapper');
        refurbished_bike = $("[id*="+'refurbished_vin'+"]").closest('.fieldWrapper');
        if (selection == 'customer_bike'){
            $(rental_bike).hide();
            $(refurbished_bike).hide();
        }
        else if (selection == 'rental_bike'){
            $(rental_bike).show();
            $(refurbished_bike).hide();
        }
        else{
            $(refurbished_bike).show();
            $(rental_bike).hide();
        }
    })
});