<script>


$(document).ready(function(){
 $("#project_mission_bs").multiselect().multiselectfilter( {

       autoReset:true,
       optGroupCollapsible:true

   } );
     $("#projects_bs").multiselect().multiselectfilter( {

       autoReset:true,
       optGroupCollapsible:true

   } );

    $("#contract_bs").multiselect().multiselectfilter( {

       autoReset:true,
       optGroupCollapsible:true

   } );
});



</script>


    <form method="post" action="/add_publication">

     <input type="hidden" name="type" value="Book Section">
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
            <input type="text" name="journal"  value="{{publication['booktitle']}}">
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
            DOI
          </td>
          <td>
            <input type="text" name="doi"  value="{{publication['doi']}}" >
          </td>
        </tr>


        <tr>
          <td >
            ISSN
          </td>
          <td>
            <input type="text" name="issn"  value="{{publication['issn']}}">
          </td>
        </tr>

        <tr>
          <td >
            ISBN
          </td>
          <td>
            <input type="text"  name="isbn" value="{{publication['isbn']}}">
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
            <select id='project_mission_bs' name="project_mission" style="width:370px"  multiple="multiple">
               %for p_m in utilities_values['projects_missions']:
                 <option value="{{p_m['name']}}">{{p_m['name']}}</option>
               % end
            </select>
          </td>
        </tr>

        <tr>
           <td > Projects/Missions </td>
           <td>
             <select name="project" id="projects_bs" multiple="multiple" style="width:370px">

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
          <td> Contracts </td>
          <td>
            <select name="contracts"  id="contract_bs" multiple="multiple" style="width:370px">
               %for c in utilities_values['contracts']:
                 <option value="{{c['contract_id']}}" >{{c['contract_id']}}-{{c['contract_name']}} </option>
               % end
            </select>
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
         <button type="submit" name="add book section" >add book section</button>
        </td>
        </tr>

      </table>

       <i> (*) required fields </i>

    </form>
