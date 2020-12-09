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

    <p class="lead">
        ${_('Vanuatu Voices presents phonetically-transcribed primary recordings, from numerous villages throughout different islands, to both document and exhibit the extensive variation and unparalleled diversity of the Vanuatu languages.')}
    </p>

    <p>
        ${_('Cite the Vanuatu Voices dataset as')}
    </p>
    <blockquote>
        Aviva Shimelman, Mary Walworth, Lana Takau, Tom Ennever, Iveth Rodriguez, Tom Fitzpatrick, Marie-France Duhamel, Giovanni Abete, Daria Dërmaku, Laura Wägerle, Heidi Colleran, Paul Heggarty, Kaitip W. Kami, Hans-Jörg Bibiko and Russell Gray. (2020). Vanuatu Voices (Version v1.0) [Data set]. Zenodo. http://doi.org/10.5281/zenodo.4309141
        <a href="https://doi.org/10.5281/zenodo.4309141"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.4309141.svg" alt="DOI"></a>
    </blockquote>
</div>
