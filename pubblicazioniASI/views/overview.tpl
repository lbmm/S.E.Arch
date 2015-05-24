%setdefault(username, False)
%setdefault(is_admin, False)


% include header_template.tpl css_array=[], js_array=['https://www.google.com/jsapi'], username=False

<script type="text/javascript">

      // histogramm visualization

      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart_histogram);


      function drawChart_histogram() {

        % legend = [str(type) for type in types]
        var legend = {{!legend}}
        var data = google.visualization.arrayToDataTable([
          % header_hist = ['Year']
          %for type in types:
          %   header_hist.append(str(type.title()))
          % end

           {{!header_hist}}
           % for f in histogram_year:
          ,['{{f['year']}}',
            % for type in types:
               {{f[type]}},
            %end
               ]
          %end
        ]);

        var options = {
          title: 'ASI Publications overview',
          titleTextStyle: {color: '#434C4C'},
          width: 900,
	      height: 500,
          chartArea: {left:50}, 
          hAxis: {title: 'Year', titleTextStyle: {color: 'red'}},
          bar: { groupWidth: '75%' },
          isStacked: true
        };

        var chart = new google.visualization.ColumnChart(document.getElementById('chart_div'));
        chart.draw(data, options);

        google.visualization.events.addListener(chart, 'select', function() {


    var selection = chart.getSelection();
    var year = 0;
    var type = '';
    var location = '';

    for (var i = 0; i < selection.length; i++) {
      var item = selection[i];
      if (item.row != null && item.column != null) {
        year = data.getFormattedValue(item.row,0);
        type = legend[item.column -1];
        location = "/query_details?year=" + year + "&type=" + type;
      }  else if (item.column != null) {
        type = legend[item.column -1];
         location = "/query_details?type="+ type;
      }
    }

        window.location = location;
        
     });


        }
        // end of histogram

</script>


<div id="Content">


       <div id="chart_div" align="left" ></div>

</div>

% include common_footer.tpl  username=username, is_admin=is_admin
