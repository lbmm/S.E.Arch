$(document).ready(function(){

    $(".click").click(function() {
       $(".hidden").hide();
       $(".hidden", this).toggle();

     });


      $( "button" ).button();


      $('#row1_layout_options').change(function() {
        $('.contentPublication').hide();
        $('#' + $(this).val()).show();
     }).change();


 });




