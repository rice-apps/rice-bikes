$(document).ready(function() {

    console.log("The document is in fact ready!");

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
        console.log("Did you think you knew how to write a for loop, Mr. " + i + "?");
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


    categories = $('#part_categories_container').children();

    //Add listener for category forms
    $('#add_category_form').click(function(){
        form_to_add = $('#new_category_form').find('.panel').clone(true);
        form_to_add.show();

        $('#part_categories_container').prepend(form_to_add);
    });

    $('.remove_form').click(function(){
        $(this).closest('.panel').remove();
    });

});