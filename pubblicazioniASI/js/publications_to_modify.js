var oTable;


$(document).ready(function() {
	$('#form').submit( function() {
		var sData = $('input', oTable.fnGetNodes()).serialize();
		return true;
	} );

    var table = $("#publications");
	oTable = table.dataTable({"sPaginationType": "full_numbers", "bStateSave": true, "iDisplayLength": 50});

	$(document).on("click", ".delete", function() {
	            var pub_id = $(this).attr("id").replace("delete-", "");
	            if (confirm("Are you sure to remove the publication ?")) {

                  var parent = $("#"+pub_id);
                  $.ajax({
                         type: "post",
                         url: "/remove_publication",
                         data: "id="+pub_id,
                         beforeSend: function() {
                                 table.block({
                                         message: "",
                                         css: {
                                                 border: "none",
                                                 backgroundColor: "none"
                                         },
                                         overlayCSS: {
                                                 backgroundColor: "#fff",
                                                 opacity: "0.5",
                                                 cursor: "wait"
                                         }
                                 });
                         },
                         success: function(response) {
                                 table.unblock();
                                 var get = response.split(",");
                                 if(get[0] == "error") {
                                      alert("error removing publication: " +pub_id);
                                 }
                                 if(get[0] == "success") {
                                         $(parent).fadeOut(200,function() {
                                                 $(parent).remove();
                                                });
                                 }
                         }

                });

			 }
              else {
            return false;
         }
   });



   $('.editable_category').editable('/publications_update_category', {
        loadurl : "/json_projects_missions?onlycategories=true",
        id      : 'id',
        name    : 'category',
        type    : 'selectmulti',
        submit  : 'OK',
        submitdata : function(value, setting) {
        var array_val = new Array();
        var values = $(this).find('select').val();
        array_val['categories'] = values.join();
        return array_val;
        }});


   $('.editable_projects').editable('/publications_update_projects', {
        loadurl : "/json_projects",
        id      : 'id',
        name    : 'projects',
        type    : 'selectmulti',
        submit  : 'OK',
        submitdata : function(value, setting) {
        var array_val = new Array();
        var values = $(this).find('select').val();
        array_val['projects'] = values.join();
        return array_val;
        }});


});





