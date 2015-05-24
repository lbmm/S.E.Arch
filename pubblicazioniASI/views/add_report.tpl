<script>


$(document).ready(function(){
 $("#projects_missions_rp").multiselect().multiselectfilter( );
     $("#projects_rp").multiselect().multiselectfilter( {

       autoReset:true,
       optGroupCollapsible:true

   } );
});



</script>




    <form method="post" action="/add_publication">

     <input type="hidden" name="type" value="Report">
      <table>

      <tr>
         <td colspan="2">
           <hr>
         </td>
       </tr>

      <tr>
        <td class="error" colspan="2">
	    {{utilities_values['errors']['general']}}
          </td>
        </tr>



         <tr>
          <td >
           Title
          </td>
          <td>

            <textarea rows="1" cols="50" name="title" autofocus required>{{publication['title']}}</textarea> *

           </td>
          <td class="error">
            {{utilities_values['errors']['title']}}
         </td>
        </tr>
        <tr>
          <td >
           Authors
          </td>
          <td>
            <textarea rows="1" cols="50" name="author" required>{{publication['author']}}</textarea> *
          </td>
         <td class="error">
            {{utilities_values['errors']['author']}}
         </td>
         </tr>

        <tr>
         <td colspan="2">
           <hr>
         </td>
       </tr>


        <tr>
          <td >
            Publication Date
          </td>
          <td>
            <input type="text" name="pub_date" class="date-picker"  id="datepicker" value="{{publication['pub_date']}}" required> *
          </td>
          <td class="error">
	    {{utilities_values['errors']['start_date_error']}}
          </td>
        </tr>


        <tr>
          <td >
            Book Title
          </td>
          <td>
            <input type="text" name="booktitle" size=80  value="{{publication['booktitle']}}">
          </td>
        </tr>





        <tr>
          <td >
            external URL
          </td>
          <td>
            <input type="url"  size="80" name="link" value="{{''.join(publication['link'])}}">
          </td>
          <td class="error">
	    {{utilities_values['errors']['link_error']}}
          </td>
        </tr>

        <tr>
         <td colspan="2">
           <hr>
         </td>
       </tr>




        <tr>
          <td >
            Report N.
          </td>
          <td>
            <input type="text" name="code"  value="{{publication['code']}}" >
          </td>
        </tr>



        <tr>
         <td colspan="2">
           <hr>
         </td>
       </tr>

        <tr>
          <td >
            Abstract
          </td>
          <td>
            <textarea rows="6" cols="50" name="abstract"> {{publication['abstract']}}
            </textarea>
          </td>
          </td>
        </tr>
        <tr>
          <td >
            keywords
          </td>
          <td>
            <textarea rows="2" cols="50" name="keyword"> {{publication['keyword']}}
            </textarea>
          </td>
          </td>
        </tr>

        <tr>
           <td > Area/Category </td>
           <td>
            <select id='projects_missions_rp' name="project_mission" style="width:370px"  multiple="multiple">
               %for p_m in utilities_values['projects_missions']:
                 <option value="{{p_m['name']}}">{{p_m['name']}}</option>
               % end
            </select>
          </td>
        </tr>

        <tr>
           <td > Projects/Missions </td>
           <td>
             <select name="project" id="projects_rp" multiple="multiple" style="width:370px">

               %for category in   utilities_values['projects'].keys():

                   <optgroup label="{{category}}">
                    %for prj in utilities_values['projects'][category]:
                        <option value="{{prj}}">{{prj}} </option>
                    %end

               % end
                </optgroup>
            </select>
          </td>
        </tr>

        <tr>
           <td > Contracts </td>

          <td class="click">
          select contracts:
          <div class="hidden">
            <select name="contracts"  multiple>
               %for c in utilities_values['contracts']:
                 <option value="{{c['contract_id']}}">{{c['contract_id']}}-{{c['contract_name']}} </option>
               % end
            </select>
            </div>
          </td>
        </tr>

         <tr>
         <td colspan="2">
           <hr>
         </td>
       </tr>

        <tr>
          <td >
           Notes 
          </td>
          <td>
            <textarea rows="6" cols="50" name="note"> {{publication['note']}}
            </textarea>
          </td>
          </td>
        </tr>


        <tr>
         <td colspan="2">
           <hr>
         </td>
       </tr>

        <tr>
        <td> &nbsp; </td>
        <td>
         <button type="submit" name="add report" >add report</button>
        </td>
        </tr>

      </table>

       <i> (*) required fields </i>

    </form>
