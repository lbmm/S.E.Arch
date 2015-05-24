% include header_template.tpl css_array=["/static/table.css","/static/style.css"],js_array=["/js/jquery.dataTables.js","/js/jquery.jeditable.js","/js/jquery.blockUI.js","/js/contracts_list.js"], username=username

	<div class="container">


		<table class="table" id="contracts">
			<thead>
				<tr>
				    <th>Contract Id</th>
				    <th>Contract Name</th>
					<th>Project</th>
					<th>Contract Type</th>
					<th>Institution</th>
					<th>Start date</th>
					<th>valid</th>
					<th>Remove</th>
				</tr>
			</thead>

			<tbody>

			% for c in contracts:
                % contract_id_html = c['contract_id'].replace("/","_")
				<tr id="{{contract_id_html}}">
					<td class="hidden-phone">{{c['contract_id']}}</td>
					<td class="hidden-phone">{{c['contract_name']}}</td>
					<td id="projects|'{{!c['contract_id']}}'" class="editable_projects">
					% p_name = ''.join([d['name'] for d in projects if str(d['project']) in (c['project'])])
					 {{p_name}}

					</td>
					<td class="hidden-phone">{{c['contrat_type']}}</td>
					<td class="hidden-phone">{{c['institution']}}</td>
					<td  class="hidden-phone">{{c['start_date']}}</td>
				    <td class="hidden-phone">{{c['is_active']}}</td>

					<td><a href="javascript:;" id="delete-{{contract_id_html}}" class="delete no-underline">x</a></td>
				</tr>
			% end
	          </tbody>
		</table>

	</div>

% include admin_menu.tpl


