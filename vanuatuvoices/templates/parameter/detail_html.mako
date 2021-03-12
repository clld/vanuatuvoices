<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "parameters" %>

<%block name="head">
    <link rel="stylesheet" href="${req.static_url('clld_audio_plugin:static/clld_audio_plugin.css')}">
</%block>

<%block name="title">${_('Parameter')} ${ctx.name}</%block>

<h2>${_('Parameter')} "${ctx.description if req._LOCALE_ == 'eo' else ctx.name}"</h2>

<div style="clear: both"/>
% if map_ or request.map:
${(map_ or request.map).render()}
% endif

${request.get_datatable('values', h.models.Value, parameter=ctx).render()}
