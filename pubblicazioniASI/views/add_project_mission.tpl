% include header_template.tpl js_array=[], css_array=[], username=username

<div id="Content">
<h2>Add new Area/Category</h2>

    <form method="post" action="/add_project_mission">
      <table>
        <tr>
          <td >
            Area/Category
          </td>
          <td>
            <input type="text" name="project_mission" value="{{project_mission}}">
          </td>
          <td class="error">
            {{error['name_error']}}
          </td>
        </tr>
        <tr>
          <td >
            external URL
          </td>
          <td>
            <input type="text" name="URL" value="{{URL}}">
          </td>
        </tr>


      </table>

      <input type="submit">
    </form>


% include admin_menu.tpl
