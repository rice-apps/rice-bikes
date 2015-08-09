$(document).ready(function() {
    // Form Submit Event: Check the correct checkboxes

    $('form').submit(function(){
        for (i=0;i<categories.length;i++){
            category_div = categories[i];

            was_used_show = $(category_div).find("[id^='was_used_show']");
            if (was_used_show.prop('checked')) {
                console.log(i + 'was checked!');
                was_used_hidden = $(category_div).find("[id^='was_used_hidden']");
                was_used_hidden.prop('disabled', true);
            }
        }
    });
});