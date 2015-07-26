$(document).ready(function() {

    // Initial behavior //

    $('#id_1-cost').val(0); // set price to 0

    //hide vin text fields
    vin_field_list = $("[id*="+'vin'+"]");
    for (i=0;i<vin_field_list.length; i++){
        $(vin_field_list[i]).closest('.fieldWrapper').hide();
    }

   // checkbox click event
    $('input:checkbox').change(function() {

        // This is explicitly for prices with format ($<integer>)
        raw_text = $(this).closest('.form-group').find('.control-label').text();

        text = raw_text.split(/\s+/)[0];
        task_price = parseInt(text.substring(2, text.length-1));

        is_checked = $(this).prop('checked');

        if(is_checked) {
            $('#id_1-cost').val(parseInt($('#id_1-cost').val()) + task_price);
        }
        else{
            $('#id_1-cost').val(parseInt($('#id_1-cost').val()) - task_price);
        }
    });

    var fill_fields = function(){
        $('*[id*="first_name"]').prop('value','NOT');
        $('*[id*="last_name"]').prop('value','APPLICABLE');
        $('*[id*="email"]').prop('value','NOT@APPLICABLE.com');
    }

    var empty_fields = function(){
        $('*[id*="first_name"]').prop('value','');
        $('*[id*="last_name"]').prop('value','');
        $('*[id*="email"]').prop('value','');
    }

    // selection event
    $('#bike_type').change(function() {
        selection = $(this).prop('value');
        rental_bike = $("[id*="+'rental_vin'+"]").closest('.fieldWrapper');
        refurbished_bike = $("[id*="+'refurbished_vin'+"]").closest('.fieldWrapper');
        if (selection == 'customer_bike'){
            $(rental_bike).hide();
            $(refurbished_bike).hide();
            empty_fields();
        }
        else if (selection == 'rental_bike'){
            $(rental_bike).show();
            $(refurbished_bike).hide();
            empty_fields();
        }
        else if (selection == 'refurbished_bike') {
            $(refurbished_bike).show();
            $(rental_bike).hide();
            fill_fields();
        }
    })

    $('.category').click(function() {
        $("." + $(this).attr('category')).toggle()
    })

});