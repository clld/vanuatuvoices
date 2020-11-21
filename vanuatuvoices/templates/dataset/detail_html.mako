<%inherit file="../home_comp.mako"/>

<%def name="sidebar()">
    <div class="well">
        <h3>Sidebar</h3>
        <p>
            Content
        </p>
    </div>
</%def>

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
