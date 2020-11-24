<%inherit file="home_comp.mako"/>

<h2>${_('Acknowlegements')}</h2>

<p>
    ${_("This site drew inspiration from Paul Heggarty's")}
    ${h.external_link('https://soundcomparisons.com/', label='Sound Comparisons')}.
    See
</p>

<blockquote>
    Heggarty, Paul et al. 2019. Sound Comparisons: A new online database and resource for research in phonetic diversity. Proceedings of ICPhS 19, Melbourne, pp. 280-284, see paper for full list of authors.
</blockquote>
<p>
    ${_('The following people contributed to the Vanuatu Voices dataset')}:
</p>

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

<p>
    Lana Takau ${_('also provided the Bislama translations for this website')}.
</p>
