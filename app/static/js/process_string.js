$(document).ready(function() {

    String.prototype.splice = function( idx, rem, s ) {
        return (this.slice(0,idx) + s + this.slice(idx + Math.abs(rem)));
    };

    process_string = function(string){
        var processed_string = string;
        var offset = 0;

        for (var i in string){
            var i = parseInt(i);
            char = string[i];
            if (char == '(' || char == ')'){
                processed_string = processed_string.splice(i + offset, 0, "\\");
                offset += 1;
            }
        }
        return processed_string;
    }
});