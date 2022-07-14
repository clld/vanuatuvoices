<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "parameters" %>

<%block name="head">
    <link rel="stylesheet" href="${req.static_url('clld_audio_plugin:static/clld_audio_plugin.css')}">
</%block>

<%block name="title">${_('Parameter')} ${ctx.name}</%block>

%if req._LOCALE_ == 'eo':
    %if ctx.description:
        <h2>${_('Parameter')} "${ctx.description} – ${ctx.name}"</h2>
    %else:
        <h2>${_('Parameter')} "${ctx.name}"</h2>
    %endif
%else:
    %if ctx.description:
        <h2>${_('Parameter')} "${ctx.name} – ${ctx.description}"</h2>
    %else:
        <h2>${_('Parameter')} "${ctx.name}"</h2>
    %endif
%endif

<div style="clear: both"/>
${(map_ or request.map).render()}

${request.get_datatable('values', h.models.Value, parameter=ctx).render()}
