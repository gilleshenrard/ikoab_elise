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

/**
 * Makes an Ajax call through a POST message
 */
function update_person(){
	$.ajax({
		url : $("#id_firstname").val(),
		type : "PUT",
		data : { firstname : $("#id_firstname").val(),
				lastname : $("#id_lastname").val(),
				country : $("#id_country").val(),
				email : $("#id_email").val(),
				phone : $("#id_phone").val(),
				occupation_field : $("#id_occupation_field").val(),
				occupation : $("#id_occupation").val(),
				birthdate : $("#id_birthdate").val(),
				description : $("#id_description").val()},
		
		success : function(json) {
			console.log("SUCCESS! " + $("#id_firstname").val() + " updated!")
		},
		
		error : function(xhr, errmsg, err) {
			console.log("Oops! We have encountered an error: "+errmsg);
			console.log(xhr.status + ": " + xhr.responseText);
		}
	});
}

$(document).ready(function(){
    /**
     * Valide la valeur du numéro de chassis
     * Structure : 12345-12345-12345-12345
     */
    $("#id_firstname").focusout(function(){
        checkValues(/^[A-z -]{0,32}$/, "firstname");
    });
    
    /**
     * Impedes the default submission to replace it with Ajax
     */
    $("#badge_form").on('submit', function(event){
    	event.preventDefault();
    	console.log("Form submitted");
    	update_person();
    });
});