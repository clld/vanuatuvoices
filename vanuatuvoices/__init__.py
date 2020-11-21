import collections

from pyramid.config import Configurator

from clld_glottologfamily_plugin import util

from clld.web import app
from clld.interfaces import IMapMarker, IValueSet, IValue, IDomainElement
from clldutils.svg import pie, icon, data_url

# we must make sure custom models are known at database initialization!
from vanuatuvoices import models

_ = lambda s: s
_('Languages')
_('Parameters')
_('Language')
_('Parameter')
_('Download')
_('Contact')
_('Legal')
_('Home')
_('You can contact us via email at')

# Maps
_('Icon size')
_('Show/hide Labels')

# DataTables
_("Next")
_("Previous")
_("First")
_("Last")
_("No data available in table")
_("Showing _START_ to _END_ of _TOTAL_ entries")
_("Showing 0 to 0 of 0 entries")
_("(filtered from _MAX_ total entries)")
_("Show _MENU_ entries")
_("Loading...")
_("Processing...")
_("Search:")
_("No matching records found")


class LanguageByFamilyMapMarker(util.LanguageByFamilyMapMarker):
    def __call__(self, ctx, req):
    
        if IValueSet.providedBy(ctx):
            if ctx.language.family:
                return data_url(icon(ctx.language.family.jsondata['icon']))
            return data_url(icon(req.registry.settings.get('clld.isolates_icon', util.ISOLATES_ICON)))
    
        return super(LanguageByFamilyMapMarker, self).__call__(ctx, req)



def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('clld.web.app')

    config.include('clldmpg')


    config.registry.registerUtility(LanguageByFamilyMapMarker(), IMapMarker)

    return config.make_wsgi_app()
