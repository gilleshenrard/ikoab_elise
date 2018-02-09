/**
 * Compare le regex envoyé à la valeur de ID, et impacte le form-group et le tip en conséquence
 * @param {string} regex
 * @param {string} id
 */
function checkValues(regex, id){
    if (regex.test($("#id_"+id).val())) {
        $("#group_"+id).removeClass("has-danger");
        $("#group_"+id).addClass("has-success");
        $("#fb_"+id).removeClass("glyphicon-remove");
        $("#fb_"+id).addClass("glyphicon-ok");
        //$("#tip_"+id).addClass("hidden");
        //return true;
    } else {
        $("#group_"+id).removeClass("has-success");
        $("#group_"+id).addClass("has-danger");
        $("#fb_"+id).removeClass("glyphicon-ok");
        $("#fb_"+id).addClass("glyphicon-remove");
        //$("#tip_"+id).removeClass("hidden");
        //return false;
    }
}

$(document).ready(function(){
    /**
     * Valide la valeur du numéro de chassis
     * Structure : 12345-12345-12345-12345
     */
    $("#id_firstname").focusout(function(){
        checkValues(/^[A-z -]{0,32}$/, "firstname");
    });
});