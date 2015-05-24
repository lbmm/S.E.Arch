%setdefault('username', False)
%setdefault('is_admin', False)

% include header_template.tpl css_array=[], js_array=['https://www.google.com/jsapi',], username=username


<script type="text/javascript">


      //piece for the pie chart visualization
      google.load("visualization", "1", {packages:["corechart"]});
      google.load("visualization", "1", {packages:["timeline"]});
      google.setOnLoadCallback(drawChart_all_year);
      % if ptype:
      google.setOnLoadCallback(drawChart_all_year_type);
      %end
      % if histogram_year:
      google.setOnLoadCallback(drawChart_histogram);
      %end



      function drawChart_all_year() {

         var data = google.visualization.arrayToDataTable([
          ['year', 'how many articles published']
          % for f in aggregation_year:
          ,["{{!f['author'].title()}}", {{f['count']}}]
          %end

        ]);

        %title = 'ASI all publications'

        var options = {
          title: '{{title}}',
          width: 500,
          height: 300,
          pieSliceText: 'value',
          is3D: true,
           }

        var chart = new google.visualization.PieChart(document.getElementById('piechart_all'));
        chart.draw(data, options);

      

        google.visualization.events.addListener(chart, 'select', function() {
        var selection = chart.getSelection();
        row = selection[0].row
        var selected =  data.getFormattedValue(row, 0)
        var year_selected = document.getElementById('year_selected').value
        var location = '/query_details?author=' + selected.toLowerCase();
        if ( year_selected !== 'None' ){
           location  = location+ "&year=" +year_selected; 
        }
        window.location = location;
         });


}
       % if ptype:

       function drawChart_all_year_type() {

         var data = google.visualization.arrayToDataTable([
          ['Publications', 'how many articles published']
          % for f in aggregation_year_type:
          ,["{{!f['author'].title()}}", {{f['count']}}]
          %end

        ]);

        var options = {
          title: 'ASI {{ptype}} Publications',
          width: 500,
          height: 300,
          pieSliceText: 'value',
          is3D: true,

        };

        var chart = new google.visualization.PieChart(document.getElementById('piechart_year_type'));
        chart.draw(data, options);
      
         google.visualization.events.addListener(chart, 'select', function() {
        var selection = chart.getSelection();
        row = selection[0].row
        var selected =  data.getFormattedValue(row, 0)
        var year_selected = document.getElementById('year_selected').value
        var type_selected = document.getElementById('type_selected').value
        var location = '/query_details?author=' + selected.toLowerCase();
        if ( year_selected !== 'None' ){
           location  = location+ "&year=" +year_selected; 
        }
        if ( type_selected !== 'None' ){
           location  = location+ "&type=" +type_selected; 
        }
        window.location = location;
         });
      }
      %end
      // end of pie part visualization

      // histogramm visualization


      % if histogram_year:

      function drawChart_histogram() {
         % legend = [str(type) for type in types]
        var legend = {{!legend}}
        var data = google.visualization.arrayToDataTable([
          ['Year'
 
          % for t in types:
            ,'{{t}}'
          % end 
          ]
           % for f in histogram_year:
          ,[
           % if author:
           '{{f['year']}}'
           %else:
           {{f['year']}}
           %end 
           % for t in types:
            ,{{f.get(t,0)}}
           % end 
           ]
           %end
        ]);

         var options = {
          title: 'Publications',
          width: 850,
	  height: 350,
          chartArea: {left:50}, 
          bar: { groupWidth: '75%' },
          isStacked: true,
          hAxis: {title: 'Year', titleTextStyle: {color: 'red'}, format:'#'}
        };

        var chart = new google.visualization.ColumnChart(document.getElementById('chart_div'));
        chart.draw(data, options);
        
         google.visualization.events.addListener(chart, 'select', function() {
          
         var selection = chart.getSelection();
         var year = 0;
         var type = '';
         var location = '/query_details?';

         var author_selected = document.getElementById('author_selected').value
           

         for (var i = 0; i < selection.length; i++) {
         var item = selection[i];
   
         if (item.row != null && item.column != null) {
             year = data.getFormattedValue(item.row,0);
             type = legend[item.column -1];
             if ( author_selected !== 'None' ){
                      location  = location +"author=" + author_selected + "&year=" + year + "&type=" + type;
               }else{
                location = location +"year=" + year + "&type=" + type;
               }
          }
            else if (item.column != null) {
                 type = legend[item.column -1];
                 if ( author_selected !== 'None' ){
                    location  = location +"author=" + author_selected + "&type=" + type;
                }else {
               location = location + "type="+ type;
               }
         }
        } 
        window.location = location;
        
       
        
         });
        }
        // end of histogram

      //multi tab visualization
      $(function() {
         $( "#tabs" ).tabs();


         % if author:
           $( "#tabs" ).tabs({ active: 1});
         %end
      });
      // end of the multi tab visualization

  </script>

<div id="Content">
<h1>ASI authors statistics</h1>


<div id="tabs" style="background: white">
  <ul>
    <li><a href="#tabs-2">Year details</a></li>
    <li><a href="#tabs-3">Authors details</a></li>
  </ul>




<div id="tabs-2">


<input id='year_selected'  value='{{year}}' type="hidden" year='{{year}}' />
<input id='type_selected'  value='{{ptype}}' type="hidden" year='{{ptype}}' />

<table  style="width: 900px; height: 300px;">
  <tr>
   <td align="left" >
   <select onChange='window.location="metrics_authors?year=" + this.value;'>
    <option value="">--</option>
    % for y in years:
      % if str(y) == str(year):
        <option value="{{y}}" selected>{{y}}</option>
      %else:
        <option value="{{y}}">{{y}}</option>
      %end
    % end
</select>
    </td>
     <td  align="left">
       <script>
       </script>
       <select onChange='window.location="metrics_authors?ptype=" + this.value + (document.getElementById("year_selected").value !== "None" ?"&year=" + document.getElementById("year_selected").value:  "");'>
         <option value="">--</option>
         % for t in types:
          % if str(t) == str(ptype):
           <option value="{{t}}" selected>{{t}}</option>
         %else:
         <option value="{{t}}">{{t}}</option>
       %end
     % end
</select>
     </td>
    </tr>
    <tr>
    <td >
       <div id="piechart_all"  align='left' style="width: 450px; height: 300px;"></div>
    </td>
    <td >
       <div id="piechart_year_type"  align='right' style="width: 450px; height: 300px;"></div>
    </td>
 </tr>
</table>
</div>

<div id="tabs-3">

<select onChange='window.location="metrics_authors?author=" + this.value;'>
    <option value="">--</option>
    % for a in authors:
      % if str(a) == str(author):
        <option value="{{a}}" selected>{{a}}</option>
      %else:
        <option value="{{a}}">{{a}}</option>
      %end
    % end
</select>

<input id='author_selected'  value='{{author}}' type="hidden" />

<table>
   % if not histogram_year:

   <tr>
     <td>
       No data to display
     </td>
   </tr>

   % else:
   <tr>
     <td>
       <div id="chart_div"></div> 
     </td>
   </tr>
   %end

</table>

</div>


</div>

% include common_footer.tpl  username=username, is_admin=is_admin
