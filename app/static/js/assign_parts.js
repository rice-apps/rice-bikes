$(document).ready(function() {

    categories = $('#all_part_categories').children();

    var form_num = categories.length;

    $('#add_form').click(function(){
        console.log(form_num);
        buttons = $('#buttons').clone(true);
        $('#buttons').remove();
        fields = $('#original_fields_0').clone().prop('id', "original_fields_" + form_num);
        $('form').append(fields);
        $('form').append(buttons);

        form_num += 1;
    });


});