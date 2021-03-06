%setdefault('username', False)

% include header_template.tpl css_array=["/static/style.css"], js_array=[], username=username

<script>
  $(function() {
    $( "#tabs" ).tabs();
    $( "button" ).button();
  });
  </script>

<div class="container">


<div id="tabs" style="background: white">
  <ul>
    <li><a href="#tabs-1">Publication</a></li>
  </ul>
  <div id="tabs-1">
    <p>

    % link='#'
    % if publication['link'] :
    %    link = publication['link'][0]
    % end
    <a href="{{link}}" target="_blank">{{!publication['title']}} </a>
     <br>
    {{!publication['authors_to_show']}}

    <br>

    % pub_date = publication["pub_date"]
    <i>{{pub_date}}</i>

    % doi = publication.get('doi','')
    % if doi:
    <br>

    DOI: <b>{{doi}}</b>
    %end
    <br>
    % issn = publication.get('issn', '')
    % isbn = publication.get('isbn', '')
    %if issn:
    ISSN : <b>{{issn}}</b> ;
    %end
    %if isbn:
    ISBN :<b> {{isbn}}</b>
    <br>
    %end

    % if publication['type'] =='Article Journal':
       <br>
       % journal = publication.get('journal', '')
        journal : <strong>{{journal}} </strong>
        <br>

        % volume = publication.get("volume", "")
        % issue = publication.get("number", "")

        %if volume or issue:
    <br>
    %if volume:
    <b>Volume</b> : {{volume}} ;
    %end
    %if issue:
    <b> Issue</b> : {{issue}}
    <br>
    %end

   %end
    % elif publication['type'] == 'Conference Proceedings':
        <br>
        Event Title : {{publication.get('eventname', '')}}
        <br>
        Published in: <b>{{publication.get('booktitle', '')}}</b>
        <br>
        Publisher: {{publication.get('publisher', '')}}
        <br>
    % elif  publication['type'] == 'Article Journal':
        <br>
        Publisher: {{publication.get('publisher', '')}}
        <br>

    % elif  publication['type'] == 'Thesis':
        <br>
        University - Institution: {{publication.get('university', '')}}
        <br>
        Accademic Year: {{publication.get('academic_year', '')}}
        <br>
    %end



    % if publication['type'] in ['Book', 'Book Section', 'Report']:
       Book Title : <strong>{{publication.get('booktitle', '')}} </strong>
       <br>
       <i>
       %if publication.get('number',''):
       Issue : {{publication.get('number','')}} ;
       %end
       % if publication.get('pages', ''):
       pages: {{publication.get('pages', '')}};
       % end
       % if publication.get('volume', ''):
       Volume: {{publication.get('volume', '')}};
       %end
       %if publication.get('series', ''):
       series: <b>{{publication.get('series', '')}}</b>
       %end
       </i>
       <br>

    %end

    %if publication['type'] in ['Report', 'Patent'] and publication.get('code', ''):
       <br>
       {{publication['type']}} N. : <b>  {{publication.get('code', '')}} </b>
       </br>
    %end

    type: <i>{{publication['type']}}</i>
    <br>
    <br>
    % if len(publication['link']) > 1:
    publication available also here:
    <br>
       % for pub_link in publication['link'][1:]:
          <a href="{{!pub_link}}" target="_blank">{{!pub_link}} </a>
          <br>

       %end
    %end
    <p>
   <strong>Abstract</strong>
   <br>
   {{!publication.get('abstract', '')}}
    </p>

    <p>
    <strong>keywords</strong> : {{!publication.get('keyword','')}}

    </p>

    <p>
    % notes = publication.get('note', '')
    %if notes:
    <strong>Notes</strong> : {{!publication.get('note', '')}}
    %end

    </p>

    <p align="center">
     <form method="post" action="/confirm_update">
     <input type="hidden" name="publication" value="{{publication}}">
     <button type="submit" name="confirm update">confirm update</button>
     </form>
    </p>

  </div>

</div>

</div>


% include common_footer.tpl  username=username, is_admin=is_admin
