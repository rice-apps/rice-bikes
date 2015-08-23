$(document).ready(function() {


    // INITIAL BEHAVIOR

    cost_el = $('*[id*="cost"]');

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

    String.prototype.splice = function( idx, rem, s ) {
        return (this.slice(0,idx) + s + this.slice(idx + Math.abs(rem)));
    };

    process_string = function(string){
        var processed_string = string;
        var offset = 0;

        for (i in string){
            i = parseInt(i);
            char = string[i];
            if (char == '(' || char == ')'){
                processed_string = processed_string.splice(i + offset, 0, "\\");
                offset += 1;
            }
        }
        return processed_string;
    }


    $('.sub_category').click(function() {
        var string = $(this).attr('category');
        var processed_string = process_string(string);

        $("." + processed_string).toggle();

    })

    $('.category').click(function() {
        var string = $(this).attr('category');
        var processed_string = process_string(string);

        $("." + processed_string).toggle();
    })

});