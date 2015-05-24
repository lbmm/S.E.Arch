% include header_template.tpl css_array=["/static/table.css","/static/style.css"], js_array=["/js/jquery.dataTables.js","/js/jquery.jeditable.js","/js/jquery.blockUI.js","/js/publications_to_modify.js"], username=username



	<div class="container">


        <h1>Modify publications</h1>

        <p> <i>Retrieved {{len(publications)}} publications: </i></p>

		<table class="table" id="publications">
			<thead>
				<tr>
					<th>Title </th>
					<th>Pub date</th>
					<th>ASI Authors</th>
					<th>Publication type</th>
					<th>Area/Category</th>
					<th>Projects/Missions</th>
					<th>Modify</th>
				    <th>Remove</th>
				</tr>
			</thead>

			<tbody>

			% for p in publications:

				<tr id="{{p['id']}}">
					<td class="hidden-phone" style="width:150px"><a href="/pub_detail/{{p['id']}}" target="_blank">{{!p['title']}}</a></td>
					<td class="hidden-phone"><i>{{p['pub_date']}}</i></td>

					<td class="hidden-phone">
					%for auth in  p['ASI_authors']:
					{{auth.title()}}
					<br>
					%end
					%if not p['ASI_authors']:
					   ASI - sponsor
					%end
					</td>
					<td class="hidden-phone">{{p['type']}}</td>
					<td id="category-{{p['id']}}" class="editable_category">
					% for c in p['project_mission']:
					    {{c}} <br>
					% end
					</td>
					<td id="projects-{{p['id']}}" class="editable_projects">
					% for pr in p['project']:
					    {{pr}} <br>
					% end
					</td>
					<td><a href="/modify_publication_detail/{{p['id']}}"><img src='/static/images/detail.png' height="20" width="20"></a></td>
				   <td><a href="javascript:;" id="delete-{{p['id']}}" class="delete no-underline">x</a></td>

				</tr>
			% end
	          </tbody>
		</table>


	</div>

% include admin_menu.tpl
