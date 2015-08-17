$(document).ready(function() {

    categories = $('#all_part_categories').children();

    var form_num = categories.length;

    $('#add_form').click(function(){
        console.log(form_num);
        fields_disabled = $('#new_form').clone(true).prop('id', "new_form_disabled_" + form_num);
        fields_hidden =  $('#new_form').clone(true).prop('id', "new_form_hidden_" + form_num).prop('hidden', true);

        fields_disabled.find('.panel-body').removeClass('new-part-panel').addClass('parts-panel');
        fields_hidden.find('.panel-body').removeClass('new-part-panel').addClass('parts-panel');

        category_val = $("#new_form").find("#id_category").val();
        fields_disabled.find("#id_category").val(category_val);
        fields_hidden.find("#id_category").val(category_val);



        inputs = fields_disabled.find('[class*=form-control]').prop('disabled', 'true');

        $('#all_part_categories').prepend("<div class='form_pair'></div>");

        new_form_pair_div = $('#all_part_categories').children()[0];

        $(new_form_pair_div).append(fields_disabled);
        $(new_form_pair_div).append(fields_hidden);

        form_num += 1;

        // clear fields in new_form
        $('#new_form').find('[class*=form-control]').prop('value','');
        $('#new_form').find('[type=checkbox]').prop('checked','')

    });

    $('.remove_form').click(function(){
        $(this).closest('.form_pair').remove();
    });

});