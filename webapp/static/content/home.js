//
// 25/01/14 HWD Creation
//

$(function() {
	var tmpl, // main template HTML
        tdata = {}; // JSON data object that feeds the template

	// Initialise page
	var initPage = function() {

	    // Load the HTML template
	    $.get("/templates/home.html", function(d) {
		    tmpl = d;
	    });

	    $(document).ajaxStop(function() {
		    var renderedPage = Mustache.to_html( tmpl, tdata );
		    $("#data").html( renderedPage );
	    })
	}();
});