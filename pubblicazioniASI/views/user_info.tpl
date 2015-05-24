% include header_template.tpl css_array=["/static/table.css","/static/style.css"],js_array=["/js/jquery.dataTables.js","/js/jquery.jeditable.js","/js/jquery.blockUI.js","/js/user_info.js"], username=username

	<div class="container">

    <h3>You can update your email information  double clicking the cell.</h3>
	<br>
	<br>

		<table class="table" id="users">
			<thead>
				<tr>
					<th>username</th>
					<th>Name</th>
					<th>Lastname</th>
					<th>email</th>

				</tr>
			</thead>

			<tbody>
				<tr id="{{user['username']}}">
					<td class="hidden-phone">{{user['username']}}</td>
					<td class="hidden-phone">{{user['name']}}</td>
					<td class="hidden-phone">{{user['lastname']}}</td>
					<td id="mail-{{user['username']}}"class="editable_email">{{user['email']}}</td>
				</tr>
	          </tbody>
		</table>



	</div>

% include user_menu.tpl username=username


