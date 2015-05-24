<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
<meta http-equiv="content-type" content="text/html; charset=iso-8859-1" />
<title>ASI bibliography Tool - ADMIN functions </title>

<!-- different css for the pages-->

% for css in css_array:
<link href="{{css}}" media="screen" rel="stylesheet" type="text/css" />
% end 

<link rel="stylesheet" href="/static/library/jquery-ui-1.10.4.custom.css">
<style href="/static/page_layout.css" type="text/css" media="all">@import "/static/page_layout.css";</style>

<script src="/js/jquery-ui-1.10.4.custom/js/jquery-1.10.2.js"></script>
<script src="/js/jquery-ui-1.10.4.custom/js/jquery-ui-1.10.4.custom.min.js"></script>

% for js in js_array:
<script type="text/javascript" src="{{js}}"></script>
%end 

<script>
$(function() {
    $( "#menu" ).menu();
  });
  </script>

<style>
.ui-menu { width: 150px; }
</style>


</head>
<body>


</head>

<body>

<div id="Header">
      <a>Welcome {{username}}</a>
      <br />
</div>


