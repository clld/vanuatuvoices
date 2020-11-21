<%inherit file="app.mako"/>

##
## define app-level blocks:
##
<%block name="header">
    ##<a href="${request.route_url('dataset')}">
    ##    <img src="${request.static_url('vanuatuvoices:static/header.gif')}"/>
    ##</a>
</%block>

<%block name="navextra">
  <div class="pull-right">
    <ul class="nav">
      <li>
        <a style="padding: 0px !important;" href="${req.purl.query_param('__locale__', 'en')}">
          <img width="34" src="${req.static_url('vanuatuvoices:static/gb.svg')}"/>
        </a>
      </li>
      <li>
        <a style="margin-left: 10px; padding: 0px !important;" href="${req.purl.query_param('__locale__', 'eo')}">
          <img width="30" src="${req.static_url('vanuatuvoices:static/vu.svg')}"/>
        </a>
       </li>
    </ul>
  </div>
</%block>

${next.body()}
