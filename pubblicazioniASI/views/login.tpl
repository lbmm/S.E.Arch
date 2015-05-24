<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">

<head>
<meta http-equiv="content-type" content="text/html; charset=iso-8859-1" />
<title>ASI publications </title>
<link rel="stylesheet" href="/static/library/jquery-ui-1.10.4.custom.css">
<style href="/static/page_layout.css" type="text/css" media="all">@import "/static/page_layout.css";</style>

<script src="/js/jquery-ui-1.10.4.custom/js/jquery-1.10.2.js"></script>
<script src="/js/jquery-ui-1.10.4.custom/js/jquery-ui-1.10.4.custom.min.js"></script>

<script type="text/javascript">

$(function() {

$("button").button();
});

</script>

</head>
<body>



%setdefault('username', '')
%setdefault('login_error', '')


<div id="Header"><a href="/overview"><b>S.E.ARCH.</b></a></p> </div>
 <div id="Content">
    <h1>Login</h1>
    <form method="post" action="/login">
      <table>
        <tr>
          <td class="label">
            Username
          </td>
          <td colspan="2">
            <input type="text" name="username" value="{{username}}">
          </td>
          <td class="error">
          </td>
        </tr>

        <tr>
          <td class="label">
            Password
          </td>
          <td colspan=2>
            <input type="password" name="password" value="">
          </td>
          <td class="error">
	    {{login_error}}
            
          </td>
        </tr>


      <tr>
      <td>&nbsp; </td>
      <td>
      <button type="submit" name="login" >login</button>

      </td>
      </form>
      <form action="/forgot_password" method="post">
      <td>
      <button type="submit" name="reset password" >reset password</button>
      </td>
      </tr>
      </table>

  </body>
</div>

</html>
