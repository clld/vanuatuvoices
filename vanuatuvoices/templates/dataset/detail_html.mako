<%inherit file="../home_comp.mako"/>

<%block name="head">
    <style>
        .dt-before-table {visibility: hidden; height: 0;}
        .dataTables_info {visibility: hidden; height: 0;}
        .dataTables_paginate {visibility: hidden; height: 0;}
    </style>
</%block>

<%def name="sidebar()">
    <div class="well">
        <img src="${req.static_url('vanuatuvoices:static/ico-Vanuatu.jpg')}" class="img-rounded">
    </div>
</%def>

<div id="with-background">
    <h2>${_('Welcome to')} Vanuatu Voices</h2>


</div>
