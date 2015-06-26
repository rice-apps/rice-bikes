$(document).ready(function() {
    tasks = $("#task-container").children()
    for (i=0; i<tasks.length; i++){
        task = tasks[i]
        category = $(task).attr('category');
        new_div = $(task).clone().prop('id', $(task).attr('id') + '_sorted');
        $("#" + category).append(new_div);
        $(task).remove();
    }
});