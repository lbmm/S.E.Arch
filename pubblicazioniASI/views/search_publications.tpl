%setdefault(username, False)
%setdefault(is_admin, False)

% include header_template.tpl js_array=["/js/library/bootstrap-tokenfield.min.js", "/js/double_calendar.js"], css_array=["/static/library/bootstrap-tokenfield.css", "/static/addon.css"], username=username


<script type="text/javascript">


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

</script>



<div id="Content">
<h1>Search publications</h1>

    <form method="post" action="/search_publications">
    <fieldset>
      <table>



       <tr>
          <td >
            Authors (*)
          </td>
          <td class="input-group input-group-sm" >
              <input type="text" id="tokenfield_authors" class="form-control"  name="authors" value="" >
          </td>
          <td>  <i>Authors condition:</i> </td>
          <td>
          <div id="radio_authors"> 
            <input type="radio" id="radio1" name="radio_authors" value="AND"><label for="radio1">AND</label>
            <input type="radio" id="radio2" name="radio_authors" checked="checked" value="OR"><label for="radio2">OR</label>
           </div>

           </td>

        </tr>

        <tr>
          <td >
            Title (*)
          </td>
          <td colspan="2" >
             <textarea rows="1" class="form-control" cols="50" name="title">  </textarea>
          </td>
          <td>

            <button id="opener" onclick="return false;">?</button>

          </td>
        </tr>

        <tr>
          <td >
            time period: start
          </td>
          <td colspan="2">
            <input type="text"  class="form-control" name="start_date" id="datepicker" value="{{start_date}}">
          </td>
          <td class="error">
            {{errors['start_date_error']}}
          </td>
        </tr>

        <tr>
          <td >
            time period: end
          </td>
          <td colspan="2">
            <input type="text" class="form-control" name="end_date" id="datepicker1" value="{{end_date}}">
          </td>
          <td class="error">
            {{errors['end_date_error']}}
          </td>


        <tr>
          <td >
            area - category
          </td>
          <td class="input-group input-group-sm">
            <input  class="form-control"  type="text" id="tokenfield_projects_missions" value="" name="projects_missions">
          </td>

             <td>  <i>Area/Category condition:</i> </td>
          <td>
          <div id="radio_category">
            <input type="radio" id="radio_category1" name="radio_category" value="AND"><label for="radio_category1">AND</label>
            <input type="radio" id="radio_category2" name="radio_category" value="OR" checked="checked"><label for="radio_category2">OR</label>
           </div>

           </td>


        </tr>

        <tr>
          <td >
            missions/projects
          </td>
          <td class="input-group input-group-sm" >
            <input  class="form-control" type="text" id="tokenfield_projects" value="" name="projects">
          </td>
            <td>  <i> Projects/Mission condition:</i> </td>
         <td>
          <div id="radio_projects">
            <input type="radio" id="radio_projects1" name="radio_projects" value="AND"><label for="radio_projects1">AND</label>
            <input type="radio" id="radio_projects2" name="radio_projects" value="OR" checked="checked"><label for="radio_projects2">OR</label>
           </div>

           </td>

        </tr>

        <tr>
          <td >
            publication type
          </td>
          <td class="input-group input-group-sm" >
            <input class="form-control" type="text" name="type" id="tokenfield_types" value="">
          </td>
              <td>  <i> Publication type condition:</i> </td>
           <td>

          <div id="radio_type">
            <input type="radio" id="radio_type1" name="radio_type" value="AND"><label for="radio_type1">AND</label>
            <input type="radio" id="radio_type2" name="radio_type" value="OR" checked="checked"><label for="radio_type2">OR</label>
           </div>

           </td>

        </tr>

         <tr>
          <td >
            Doi (*)
          </td>
          <td >
            <input  type="text" class="form-control" name="doi" value="">
          </td>
          </tr>

           <tr>
          <td >
            ISBN (*)
          </td>
          <td >
            <input  type="text" class="form-control" name="isbn" value="">
          </td>
          </tr>

           <tr>
          <td >
            ISSN (*)
          </td>
          <td >
            <input  type="text"  class="form-control" name="issn" value="">
          </td>
          </tr>

         <tr>
          <td >
            keywords (*)
          </td>
          <td >
            <input  type="text" class="form-control"  name="keywords" value="">
          </td>

            <td>  <i> Keywords condition:</i> </td>
          <td>

          <div id="radio_keywords">
            <input type="radio" id="radio_keywords1" name="radio_keywords" value="AND"><label for="radio_keywords1">AND</label>
            <input type="radio" id="radio_keywords2" name="radio_keywords" value="OR" checked="checked"><label for="radio_keywords2">OR</label>
           </div>

           </td>

        </tr>


        <tr> <td colspan='3'> &nbsp; </td> </tr>
        <tr> <td> &nbsp; </td>
        <td colspan="2">
         <button type="submit" name="search" >search</button>
        </td>
        </tr>

      </table>
      </fieldset>
    </form>


    <div id="dialog" title="Title search HOWTO">
         <p> <b>search with the exact phrase</b> :<i> "your phrase" </i>
          <br>
               <b>with at least one of the words</b> : <i>words to search</i>

         </p>
     </div>

<br>

 <p>  <i> (*) search does support Perl regular expressions and it is case not sensitive </i> </p>

% include common_footer.tpl  username=username, is_admin=is_admin
