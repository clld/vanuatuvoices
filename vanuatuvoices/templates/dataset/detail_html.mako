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


    <h4>${_('Acknowlegements')}</h4>

    <p>
        ${_("This site drew inspiration from Paul Heggarty's")}
        ${h.external_link('https://soundcomparisons.com/', label='Sound Comparisons')}.
        See
    </p>

    <blockquote>
        Heggarty, Paul et al. 2019. Sound Comparisons: A new online database and resource for research in phonetic diversity. Proceedings of ICPhS 19, Melbourne, pp. 280-284, see paper for full list of authors.
    </blockquote>

    The following people contributed to Vanuatu Voices:

    <table class="table table-condensed">
        <thead>
            <tr>
                <th>${_('Name')}</th>
                <th>${_('Role')}</th>
            </tr>
        </thead>
        <tbody>
        % for contrib in contributors:
            <tr>
                <td>${contrib.name}</td>
                <td>${contrib.description}</td>
            </tr>
        % endfor
        </tbody>
    </table>
</div>
