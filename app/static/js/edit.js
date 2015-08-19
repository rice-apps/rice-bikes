$(document).ready(function() {

    console.log("The document is in fact ready!");

    // sort tasks into category divs and reveal the category divs
    tasks = $("#task_container").children()
    for (i=0; i<tasks.length; i++){
        task = tasks[i]
        category = $(task).attr('category');
        new_div = $(task).clone().prop('id', $(task).attr('id') + '_sorted');
        $("#" + category).append(new_div);
        $("#" + category).show();
        $(task).remove();
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