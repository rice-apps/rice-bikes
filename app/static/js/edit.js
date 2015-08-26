$(document).ready(function() {

    // sort tasks into category divs and reveal the category divs
    tasks = $("#task_container").children()
    num_tasks = tasks.length
    for (var i=0; i<num_tasks; i++){
        task = tasks[i]
        category = $(task).attr('category');
        category = process_string(category);
        new_div = $(task).clone().prop('id', $(task).attr('id') + '_sorted');
        $("#" + category).append(new_div);
        $("#" + category).show();
        $(task).remove();
    }

    // sort parts into part categories

    parts = $("#part_container").children()
    for (var i=0; i<parts.length; i++){
        part = parts[i]
        category = $(part).attr('category');
        category = process_string(category);
        new_div = $(part).clone().prop('id', $(part).attr('id') + '_sorted');
        $("#" + category).append(new_div);
        $("#" + category).show();
        $(part).remove();
    }

    // change cost based on number
    $(".number").on("change", function(){
        var old_value = $(this).parent().find('.old_number').attr('old_value')
        console.log("Before, " +  old_value);

        var price = $(this).parent().find('.price').val();

        var cost_change;
        if (old_value == 0){
            cost_change = price * ($(this).val());
        }
        else{
            cost_change = price * ($(this).val() - old_value);
        }
        var new_cost = parseInt($("#id_cost").val()) + cost_change;

        $("#id_cost").val(new_cost);
        $(this).parent().find('.old_number').attr('old_value', $(this).val());

        console.log("After, " +  $(this).parent().find('.old_number').attr('old_value'));

    });

    $(".price").on("change", function(){
        var old_value = $(this).parent().find('.old_price').attr('old_value')
        console.log("Before, " +  old_value);

        var number = $(this).parent().find('.number').val();

        var cost_change;
        if (old_value == 0){
            cost_change = number * ($(this).val());
        }
        else{
            cost_change = number * ($(this).val() - old_value);
        }
        var new_cost = parseInt($("#id_cost").val()) + cost_change;

        $("#id_cost").val(new_cost);
        $(this).parent().find('.old_price').attr('old_value', $(this).val());

        console.log("After, " +  $(this).parent().find('.old_price').attr('old_value'));

    });


    $(".buy_back_price").on("change", function(){
        var old_value = $(this).parent().find('.old_price').attr('old_value')
        var cost_change = $(this).val() - old_value;

        var new_cost = parseInt($("#id_cost").val()) + cost_change;
        $("#id_cost").val(new_cost);

        $(this).parent().find('.old_price').attr('old_value', $(this).val());

    });


//    $('form').submit(function(){
//        $("#id_cost").prop("disabled", false);
//    });


});