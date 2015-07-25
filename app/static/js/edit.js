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

    // Form Submit Event: Check the correct checkboxes
    $('form').submit(function(){
        for (i=0;i<categories.length;i++){
            category_div = categories[i];

            was_used_show = $(category_div).find("[id^='was_used_show']");
            if (was_used_show.prop('checked')) {
                console.log(i + 'was checked!');
                was_used_hidden = $(category_div).find("[id^='was_used_hidden']");
                was_used_hidden.prop('disabled',true);
            }
        }
    });

});