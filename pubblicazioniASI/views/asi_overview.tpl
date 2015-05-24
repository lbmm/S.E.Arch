% include header_template.tpl css_array=[], js_array=["https://www.google.com/jsapi?autoload={'modules':[{'name':'visualization','version':'1.1','packages':['motionchart']}]}"], username=username


<script type="text/javascript">


google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Publication Type');
        data.addColumn('number', 'Year');
        data.addColumn('number', 'Count');
        data.addRows([

        % for year_data in overview:

          % for key, value in overview[year_data].iteritems():

          ['{{key}}',  {{year_data}}, {{value}}],

           %end
        %end
        ]);

        var chart = new google.visualization.MotionChart(document.getElementById('chart_div'));

        var options = {}; 

        options['state'] = '{"playDuration":16144.444444444445,"colorOption":"_UNIQUE_COLOR","orderedByY":false,"sizeOption":"_UNISIZE","yZoomedDataMax":2000,"orderedByX":true,"iconKeySettings":[{"key":{"dim0":"Article Journal"}},{"key":{"dim0":"Book"}},{"key":{"dim0":"Conference Proceedings"}},{"key":{"dim0":"Report"}},{"key":{"dim0":"Patent"}},{"key":{"dim0":"Thesis"}},{"key":{"dim0":"Book Section"}}],"yAxisOption":"2","xLambda":1,"yZoomedIn":false,"xZoomedDataMax":7,"xZoomedIn":false,"xAxisOption":"2","yZoomedDataMin":0,"nonSelectedAlpha":0.4,"iconType":"VBAR","showTrails":false,"uniColorForNonSelected":false,"xZoomedDataMin":0,"time":"2015","dimensions":{"iconDimensions":["dim0"]},"yLambda":1,"duration":{"multiplier":1,"timeUnit":"Y"}}'
 
	options['width'] = 900; 
	options['height'] = 500;
        


        chart.draw(data, options);
      }

    </script>


<div id="Content">
<h1> ASI Publications overview </h1>

 <div id="chart_div" style="width: 900px; height: 500px;"></div>
</div>

% include common_footer.tpl  username=username, is_admin=is_admin
