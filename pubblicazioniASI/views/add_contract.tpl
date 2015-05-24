% include header_template.tpl js_array=["/js/double_calendar.js"], css_array=[], username=username

<div id="Content">
<h1>Add new Contract</h1>

    <form method="post" action="/add_contract">
      <table>
        <tr>
          <td class="error" colspan="2">
            {{error['name_error']}}
          </td>
        </tr>
        <tr>
          <td >
            Contract id
          </td>
          <td>
            <input type="text" name="contract_id" value="{{contract_id}}"> *
          </td>
          <td class="error">
            {{error['contract_id_error']}}
          </td>
        </tr>
         <tr>
          <td >
            Contract Name
          </td>
          <td>
            <textarea rows="2" cols="50" name="contract_name">{{contract_name}}
            </textarea> *
          </td>
          <td class="error">
            {{error['contract_name_error']}}
          </td>
        </tr>
         <tr>
           <td > Project </td>
           <td>
            <select name="project">
                 <option value=""> --- </option>
               %for p in projects:
                 <option value="{{p['project']}}">{{p['name']}} </option>
               % end
            </select>
          </td>
        </tr>
        <tr>
          <td> Contract Type </td>
          <td>
            <input type="text" name="contract_type" value="{{contract_type}}">
          </td>
        </tr>
        <tr>
          <td> Institution </td>
          <td>
            <input type="text" name="institution" value="{{institution}}">
          </td>
        </tr>

        <tr>
          <td >
            start date
          </td>
          <td>
            <input type="text" name="start_date" id="datepicker" value="{{start_date}}"> *
          </td>
            <td class="error">
            {{error['start_date_error']}}
          </td>
        </tr>
       <tr>
          <td>
            valid contract
          </td>
          <td>
           <input type="radio" name="is_active" value="Y">Y
           <input type="radio" name="is_active" value="N">N
          </td>

      </table>

      <input type="submit" name="submit">
    </form>


% include admin_menu.tpl
