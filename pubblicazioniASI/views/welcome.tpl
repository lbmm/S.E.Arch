% include header_template.tpl css_array=[], js_array=[], username=username

%setdefault('msg','')
%setdefault('is_admin', False)

<div id="Content">
<h1>ASI Bibliography tool</h1>

{{!msg}}

% include common_footer.tpl  username=username, is_admin=is_admin