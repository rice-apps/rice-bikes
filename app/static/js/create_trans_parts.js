$(document).ready(function() {
    submit = $(':submit').clone();
    $(':submit').remove();
    fields = $('.fieldWrapper').clone();
    $('form').append(fields);
    $('form').append(submit);
});