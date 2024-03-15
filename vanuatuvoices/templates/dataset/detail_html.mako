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


<div style="float:left;margin-top:10px">
    <img src="${req.static_url('vanuatuvoices:static/logo_vv.svg')}" width=100 alt="Logo SVG"/>
</div>

<div id="with-background">
    <h2>${_('Welcome to')} Vanuatu Voices</h2>

    <p class="lead">
        ${_('Vanuatu Voices presents phonetically-transcribed primary recordings, from numerous villages throughout different islands, to both document and exhibit the extensive variation and unparalleled diversity of the Vanuatu languages.')}
    </p>

    <p>
        ${_('Cite the Vanuatu Voices dataset as')}
    </p>
    <blockquote>
        Lana Takau, Mary Walworth, Aviva Shimelman, Sandrine Bessis, Tom Ennever, Iveth Rodriguez, Hans-Jörg Bibiko, Daria Dërmaku, Murray Garde, Marie-France Duhamel, Giovanni Abete, Laura Wägerle, Kaitip W. Kami, Russell Gray. (2024). Vanuatu Voices (Version v1.1) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.10821732
        <a href="https://doi.org/10.5281/zenodo.10821732"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.10821732.svg" alt="DOI"></a>
    </blockquote>
</div>
