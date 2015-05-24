<script>


$(document).ready(function(){
 $("#projects_missions_th").multiselect().multiselectfilter( {

       autoReset:true,
       optGroupCollapsible:true

   } );
     $("#projects_th").multiselect().multiselectfilter( {

       autoReset:true,
       optGroupCollapsible:true

   } );

    $("#contract_th").multiselect().multiselectfilter( {

       autoReset:true,
       optGroupCollapsible:true

   } );

   $("#authors_asi_th").multiselect().multiselectfilter( {

       autoReset:true,
       optGroupCollapsible:true

   } );

});



</script>




    <form method="post" action="/update_publication">

     <input type="hidden" name="type" value="Thesis">
     <input type="hidden" name="_id" value="{{publication['_id']}}">
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

            <textarea rows="1" cols="50" name="title" autofocus required>{{publication.get('title', '')}}</textarea> *

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
            <textarea rows="1" cols="50" name="author" required>{{publication.get('author', '')}}</textarea> *
          </td>
         <td class="error">
            {{utilities_values['errors']['author']}}
         </td>
         </tr>


         <tr>
          <td >
           ASI Authors
          </td>
          <td>

          <select id='authors_asi_th' name="asi_authors" style="width:370px" multiple="multiple" >
               %for author_asi in utilities_values['asi_authors']:
                 %if author_asi['value'] in publication.get('ASI_authors', ''):
                 <option value="{{author_asi['value']}}" selected>{{author_asi['name']}}</option>
                 %else:
                  <option value="{{author_asi['value']}}" >{{author_asi['name']}}</option>
                  %end
               % end
            </select>

          </td>

         </tr>


         <tr>
          <td >
           Authors to show
          </td>
          <td>

            <textarea rows="2" cols="50" name="authors_to_show"  >{{publication.get('authors_to_show', '')}}</textarea> *

           </td>
          <td class="error">
            {{utilities_values['errors']['title']}}
         </td>
        </tr>


        <tr>
         <td colspan="2">
           <hr>
         </td>
       </tr>

        <tr>
          <td >
           University
          </td>
          <td>
            <input type="text"  name="university" size="60" value="{{publication.get('university','')}}"/>
          </td>

         </tr>

            <tr>
          <td >
           Academic Year
          </td>
          <td>
            <input type="text"  name="academic_year" size="60"  value="{{publication.get('academic_year','')}}"/>
          </td>
          </td>

         </tr>


        <tr>
          <td >
            Publication Date
          </td>
          <td>
            <input type="text" name="pub_date" class="date-picker"  id="datepicker" value="{{publication.get('pub_date', '').strftime("%B %Y")}}" required> *
          </td>
          <td class="error">
	    {{utilities_values['errors']['start_date_error']}}
          </td>
        </tr>


        <tr>
          <td >
            external URL
          </td>
          <td>
            <input type="url"  size="80" name="link" value="{{' '.join(publication.get('link', ''))}}">
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
            Abstract
          </td>
          <td>
            <textarea rows="6" cols="50" name="abstract"> {{publication.get('abstract', '')}}
            </textarea>
          </td>
          </td>
        </tr>
        <tr>
          <td >
            keywords
          </td>
          <td>
            <textarea rows="2" cols="50" name="keyword"> {{publication.get('keyword', '')}}
            </textarea>
          </td>
          </td>
        </tr>

        <tr>
           <td > Area/Category </td>
           <td>
            <select id='projects_missions_th' name="project_mission" style="width:370px"  multiple="multiple">
               %for p_m in utilities_values['projects_missions']:
                 %if p_m['name'] in publication.get('project_mission', ''):
                 <option value="{{p_m['name']}}" selected>{{p_m['name']}}</option>
                 %else:
                  <option value="{{p_m['name']}}" >{{p_m['name']}}</option>
                  %end
               % end
            </select>
          </td>
        </tr>

        <tr>
           <td > Projects/Missions </td>
           <td>
             <select id='projects_th' name="project"   style="width:370px" multiple="multiple">

               %for category in   utilities_values['projects'].keys():

                   <optgroup label="{{category}}">
                    %for prj in utilities_values['projects'][category]:
                        %if prj in publication.get('project', ''):
                        <option value="{{prj}}" selected>{{prj}} </option>
                        %else:
                        <option value="{{prj}}" >{{prj}} </option>
                        %end
                    %end

               % end
                </optgroup>
            </select>
          </td>
        </tr>

        <tr>
           <td > Contracts </td>

          <td >
            <select name="contracts"  id="contract_th" multiple="multiple" style="width:370px">
               %for c in utilities_values['contracts']:
                 %if c['contract_id'] in publication.get('contracts', ''):
                 <option value="{{c['contract_id']}}" selected>{{c['contract_id']}}-{{c['contract_name']}} </option>
                 %else:
                 <option value="{{c['contract_id']}}" >{{c['contract_id']}}-{{c['contract_name']}} </option>
                 %end
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
          <td >
           Notes 
          </td>
          <td>
            <textarea rows="6" cols="50" name="note"> {{publication.get('note', '')}}
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
         <button type="submit" name="update thesis" >update thesis</button>
        </td>
        </tr>

      </table>

       <i> (*) required fields </i>

    </form>
