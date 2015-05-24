% include header_template.tpl js_array=["/js/library/jquery.multiselect.js","/js/library/jquery.multiselect.filter.js","/js/month_only_calendar.js"], css_array=["/static/library/jquery.multiselect.css", "/static/library/jquery.multiselect.filter.css", "/static/addon.css"], username=username

<style>
.ui-datepicker-calendar {
    display: none;
    }
</style>


<script type="text/javascript">

 $(function() {
      $( "button" ).button();

});
</script>



<div id="Content">
<h1>Modify {{publication['type']}} detail</h1>



% from bottle import template

% for type in ptypes:

   % type_js = type.replace(' ', '_')
   % if str(type) == publication['type']:
      <div id="{{type_js}}">
    %else:
       <div id="{{type_js}}" class='contentPublication'>
    %end

      % template_name = 'update_%s.tpl' %  (type.lower().replace(' ', '_'))
      % templ = template(template_name, dict(utilities_values=utilities_values, publication=publication)) 
      {{!templ}}
  </div>

%end



% include admin_menu.tpl username=username
