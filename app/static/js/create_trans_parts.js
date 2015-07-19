$(document).ready(function() {

    var form_num = 0;
    $('#add_form').click(function(){
        console.log(form_num);
        buttons = $('#buttons').clone(true);
        $('#buttons').remove();
        fields = $('#original_fields').clone().prop('id', $('#original_fields').attr('id') + form_num);
        $('form').append(fields);
        $('form').append(buttons);

        form_num += 1;
    });
});