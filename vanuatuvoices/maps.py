from clld.web.util.helpers import JSNamespace
from clld.web.maps import ParameterMap, Map


class LanguagesMap(Map):
    def get_options(self):
        return {
            'on_init': JSNamespace('VANUATUVOICES').addResizer,
            'max_zoom': 13,
            'base_layer': 'Esri.DeLorme',
            'show_labels': True,
        }


class ParamMap(ParameterMap):
    def get_options(self):
        return {
            'on_init': JSNamespace('VANUATUVOICES').addResizerAndAudioplayer,
            'max_zoom': 13,
            'base_layer': 'Esri.DeLorme',
            'show_labels': True,
        }


def includeme(config):
    config.register_map('languages', LanguagesMap)
    config.register_map('parameter', ParamMap)
