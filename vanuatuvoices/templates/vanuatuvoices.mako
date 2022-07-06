<%inherit file="app.mako"/>

##
## define app-level blocks:
##
<%block name="header">
    ##<a href="${request.route_url('dataset')}">
    ##    <img src="${request.static_url('vanuatuvoices:static/header.gif')}"/>
    ##</a>
        <style>
        #html {
            min-height: 99%; /* or whatever your desired height is */
            height: 99%; /* or whatever your desired height is */
            min-width: 99%; /* or whatever your desired width is */
            width: 99%; /* or whatever your desired width is */
        }

        html::after {
            content: "";
            background-image: url('${req.static_url("vanuatuvoices:static/ico-Vanuatu.jpg")}');
            background-size: cover;
            opacity: 0.15;
            top: 0;
            left: 0;
            bottom: 0;
            right: 0;
            position: absolute;
            z-index: -2;
        }
    </style>
        <script src="${req.static_url('vanuatuvoices:static/L.Control.Resizer.js')}"></script>
        <link rel="stylesheet" href="${req.static_url('vanuatuvoices:static/L.Control.Resizer.css')}">
</%block>

<%block name="navextra">
  <div class="pull-right">
    <ul class="nav">
      <li>
        <a style="padding: 0px !important;" href="${h.localize_url(req, 'en')}">
          <img width="34" src="${req.static_url('vanuatuvoices:static/gb.svg')}"/>
        </a>
      </li>
      <li>
        <a style="margin-left: 10px; padding: 0px !important;" href="${h.localize_url(req, 'eo')}">
          <img width="30" src="${req.static_url('vanuatuvoices:static/vu.svg')}"/>
        </a>
       </li>
    </ul>
  </div>
</%block>

${next.body()}
