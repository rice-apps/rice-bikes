$(document).ready(function() {


    // INITIAL BEHAVIOR

    cost_el = $('*[id*="cost"]');
    cost_el.val(0); // set price to 0


    // EVENT HANDLERS AND HELPER FXNS

   // checkbox click event
    $('input:checkbox').change(function() {

        // This is explicitly for prices with format ($<integer>)
        raw_text = $(this).closest('.form-group').find('.control-label').text();

        text = raw_text.split(/\s+/)[0];
        task_price = parseInt(text.substring(2, text.length-1));

        is_checked = $(this).prop('checked');

        if(is_checked) {
            cost_el.val(parseInt(cost_el.val()) + task_price);
        }
        else{
            cost_el.val(parseInt(cost_el.val()) - task_price);
        }
    });

    $('.category').click(function() {
        $("." + $(this).attr('category')).toggle()
    })

});