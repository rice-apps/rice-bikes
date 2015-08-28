$(document).ready(function() {

    // INITIAL BEHAVIOR

    //hide vin text fields
    vin_field_list = $("[id*="+'vin'+"]");
    for (i=0;i<vin_field_list.length; i++){
        $(vin_field_list[i]).closest('.fieldWrapper').hide();
    }


    // EVENT HANDLERS AND HELPER FXNS

    var fill_fields = function(){
        $('*[id*="first_name"]').prop('value','NOT');
        $('*[id*="last_name"]').prop('value','APPLICABLE');
        $('*[id*="email"]').prop('value','mrp9@rice.edu');
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



});