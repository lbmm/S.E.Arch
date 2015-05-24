$(document).ready(function() {
        var table = $("#contracts");
        var oTable = table.dataTable({"sPaginationType": "full_numbers", "bStateSave": true});



        $('.editable_projects').editable('/contracts_update_projects', {
        loadurl : "/json_projects",
        id      : 'contract_id',
        name    : 'project',
        type    : 'select',
        submit  : 'OK',
        submitdata : function(value, setting) {
        var array_val = new Array();
        var value = $(this).find('select').val();
        return value;
        }});



        $(document).on("click", ".delete", function() {
                var contract_id = $(this).attr("id").replace("delete-", "");
                if (confirm("Are you sure to remove contract: " + contract_id)) {

                var parent = $("#"+contract_id);
                $.ajax({
                        type: "post",
                        url: "/remove_contract",
                        data: "contract="+contract_id,
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
                                     alert("error removing contract: " +contract_id);
                                }
                                if(get[0] == "success") {
                                        $(parent).fadeOut(200,function() {
                                                $(parent).remove();
                                        });
                                }
                        }
                });

              }else{
              return false;
              }
        });



});
