<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "languages" %>
<%block name="title">${_('Language')} ${ctx.name}</%block>

<h2>${_('Language')} ${ctx.name}</h2>

${request.get_datatable('values', h.models.Value, language=ctx).render()}

<%def name="sidebar()">
    % if ctx.contribution.contributor_assocs:
        <h4>Contributors</h4>
            <ul class="unstyled">
                % for ca in ctx.contribution.contributor_assocs:
                <li><strong>${ca.contributor.name}</strong>: ${', '.join([r.replace('_', ' ') for r in ca.jsondata['roles']])}</li>
                % endfor
            </ul>
    % endif
    ${util.language_meta()}
</%def>
