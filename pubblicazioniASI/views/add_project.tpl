% include header_template.tpl js_array=[], css_array=[], username=username

<div id="Content">
<h2>Add new Mission/Project</h2>

    <form method="post" action="/add_project">
      <table>
        <tr>
          <td >
            Mission/Project
          </td>
          <td>
            <input type="text" name="project" value="{{project}}">
          </td>
          <td class="error">
            {{error['name_error']}}
          </td>
        </tr>
        <tr>
           <td >Area/Category</td>
           <td>
            <select name="project_mission">
               <option value=""> --- </option>
               %for p_m in projects_missions:
                 <option value="{{p_m['id']}}">{{p_m['name']}} </option>
               % end
            </select>
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

      <input type="submit" name="submit">
    </form>


% include admin_menu.tpl
