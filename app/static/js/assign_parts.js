$(document).ready(function() {

    categories = $('#all_part_categories').children();

    var form_num = categories.length;

    $('#add_form').click(function(){
        console.log(form_num);
        fields_disabled = $('#new_form').clone(true).prop('id', "new_form_disabled_" + form_num);
        fields_hidden =  $('#new_form').clone(true).prop('id', "new_form_hidden_" + form_num).prop('hidden', true);

        inputs = fields_disabled.find('[class*=form-control]').prop('disabled', 'true');

        $('#all_part_categories').append(fields_disabled);
        $('#all_part_categories').append(fields_hidden);

        form_num += 1;

        // clear fields in new_form
        $('#new_form').find('[class*=form-control]').prop('value','');
        $('#new_form').find('[type=checkbox]').prop('checked','')

    });


});