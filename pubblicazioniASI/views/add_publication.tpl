% include header_template.tpl js_array=["/js/library/jquery.multiselect.js","/js/library/jquery.multiselect.filter.js","/js/month_only_calendar.js", "/js/add_publications.js"], css_array=["/static/library/jquery.multiselect.css", "/static/library/jquery.multiselect.filter.css", "/static/addon.css"], username=username

<style>
.ui-datepicker-calendar {
    display: none;
    }
</style>



<div id="Content">
<h1>Add publication</h1>

  <p>
        Publication type
            % disabled=''
            %if publication['type']:
            % disabled = "disabled"
            %end
            <select name="type"  id="row1_layout_options" name="row1_layout_options" {{disabled}} >
               <option value="Select Layout Type">Select Layout Type</option>
               %for type in ptypes:
                 % if str(type) == publication['type']:
                  <option value="{{type.replace(" ", "_")}}" selected>{{type}} </option>
                 %else:
                  <option value="{{type.replace(" ", "_")}}">{{type}} </option>
                  %end
               % end
            </select> *
      </p>


% from bottle import template

% for type in ptypes:

   % if str(type) == publication['type']:
      <div id="{{type.replace(' ', '_')}}">
    %else:
       <div id="{{type.replace(' ', '_')}}" class='contentPublication'>
    %end

      % template_name = 'add_%s.tpl' %  (type.lower().replace(' ', '_'))
      % templ = template(template_name, dict(utilities_values=utilities_values, publication=publication)) 
      {{!templ}}
  </div>

%end



% include admin_menu.tpl username=username
