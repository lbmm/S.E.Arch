% include header_template.tpl css_array=["/static/table.css","/static/style.css"], js_array=["/js/jquery.dataTables.js","/js/jquery.jeditable.js","/js/jquery.blockUI.js","/js/projects_missions_list.js"], username=username

	<div class="container">
	<h2>Areas/Categories List</h2>



		<table class="table" id="projects_missions">
			<thead>
				<tr>
					<th>Area/Category</th>
					<th>Remove</th>
				</tr>
			</thead>

			<tbody>

			% for p_m in projects_missions:
				<tr id="{{p_m['id']}}">
					<td class="hidden-phone"><a href="{{p_m['URL']}}"> <b>{{p_m['name']}}</b></a></td>
					% info = '%s_%s' % (p_m['id'],  p_m['name'])
					<td><a href="javascript:;" id="delete-{{info}}" class="delete no-underline">x</a></td>
				</tr>
			% end
	          </tbody>
		</table>




	</div>

% include admin_menu.tpl


