$(document).ready(function() {
        var table = $("#projects_missions");
        var oTable = table.dataTable({"sPaginationType": "full_numbers", "bStateSave": true});




  $(document).on("click", ".delete", function() {
                var str = $(this).attr("id").replace("delete-", "");
                var project_info = str.split("_");
                var project_id = project_info[0]
                if (confirm("Are you sure to remove project: " + project_info[1])) {
                var parent = $("#"+project_id);
                $.ajax({
                        type: "post",
                        url: "/remove_missions_project",
                        data: "project_mission="+project_id,
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
                                     alert("error removing user: " +project_id);
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
