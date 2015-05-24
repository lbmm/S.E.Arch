% include header_template.tpl css_array=["/static/table.css","/static/style.css"], js_array=["/js/jquery.dataTables.js","/js/jquery.jeditable.js","/js/jquery.blockUI.js","/js/projects_list.js"], username=username

	<div class="container">
    <h2>Projects/Missions List</h2>

		<table class="table" id="projects">
			<thead>
				<tr>
				    <th>Area/Category</th>
					<th>Project/Mission</th>
					<th>Remove</th>
				</tr>
			</thead>

			<tbody>

			% for m in projects:
				<tr id="{{m['project']}}">
				    % p_m_name = ''.join([d['name'] for d in projects_missions if str(d['id']) in (m['project_mission'])])
				    <td class="hidden-phone">{{p_m_name}}</td>
					<td class="hidden-phone"><a href="{{m['URL']}}"> <b>{{m['name']}}</b> </a></td>
					% info = '%s_%s' % (m['project'],  m['name'])
					<td><a href="javascript:;" id="delete-{{info}}" class="delete no-underline">x</a></td>

				</tr>
			% end
	          </tbody>
		</table>




	</div>

% include admin_menu.tpl


