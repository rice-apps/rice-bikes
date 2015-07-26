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

});