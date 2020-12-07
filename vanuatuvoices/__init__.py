from pyramid.config import Configurator


# we must make sure custom models are known at database initialization!
from vanuatuvoices import models

_ = lambda s: s
_('Languages')
_('Parameters')
_('Language')
_('Parameter')
_('Contributors')
_('Download')
_('Contact')
_('Credits')
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



def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('clld.web.app')

    config.include('clldmpg')

    return config.make_wsgi_app()
