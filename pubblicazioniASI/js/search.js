 $(function() {


       $('#tokenfield_authors').tokenfield({
       autocomplete: {
       source: {{!authors}},
       delay: 100
       },
       showAutocompleteOnFocus: true
      })

       $('#tokenfield_types').tokenfield({
       autocomplete: {
       source: {{!types}},
       delay: 100
       },
       showAutocompleteOnFocus: true
      })




      $('#tokenfield_projects_missions').tokenfield({
       autocomplete: {
       source: {{!projects_missions}},
       delay: 100
       },
       showAutocompleteOnFocus: true
      })


      $('#tokenfield_projects').tokenfield({
       autocomplete: {
       source: {{!projects}},
       delay: 100
       },
       showAutocompleteOnFocus: true
      })


    $( "#radio_authors" ).buttonset();

    $( "#radio_category" ).buttonset();

    $( "#radio_projects" ).buttonset();

    $( "#radio_type" ).buttonset();

    $( "#radio_keywords" ).buttonset();

    $( "button" ).button();


    $( "#dialog" ).dialog({
      autoOpen: false,
    });

    $( "#opener" ).click(function() {
      $( "#dialog" ).dialog( "open" );
    });



});
