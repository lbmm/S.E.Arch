% include header_template.tpl js_array=["/js/double_calendar.js"], css_array=[], username=username

<script type="text/javascript">

 $(function() {
      $( "button" ).button();

});
</script>


<div id="Content">


<h1>Modify publications</h1>

    <form method="post" action="/modify_publications">
      <table>

        <tr>
          <td >
            Title (*)
          </td>
          <td colspan="2" >
             <textarea rows="1" cols="50" name="title">  </textarea>
          </td>
        </tr>

        <tr>
          <td >
            start date
          </td>
          <td>
            <input type="text" name="start_date" id="datepicker" value="{{start_date}}">
          </td>
          <td class="error">
	        {{errors['start_date_error']}}
          </td>

        </tr>

        <tr>
          <td >
            end date
          </td>
          <td>
            <input type="text" name="end_date" id="datepicker1" value="{{end_date}}">
          </td>
          <td class="error">
	        {{errors['end_date_error']}}
          </td>
        </tr>

        <tr> <td> &nbsp; </td>
        <td>
         <button type="submit" name="search" >search</button>
        </td>
        </tr>
      </table>

    </form>


% include admin_menu.tpl
