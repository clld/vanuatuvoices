from clld.web.util.helpers import JSNamespace
from clld.web.maps import ParameterMap, Map


class LanguagesMap(Map):
    def get_options(self):
        return {
            'max_zoom': 13,
            'base_layer': 'Esri.DeLorme',
            'show_labels': True,
            'resize_direction': 'e',
        }


class ParamMap(ParameterMap):
    def get_options(self):
        return {
            'with_audioplayer': True,
            'max_zoom': 13,
            'base_layer': 'Esri.DeLorme',
            'show_labels': True,
            'resize_direction': 'e',
        }


def includeme(config):
    config.register_map('languages', LanguagesMap)
    config.register_map('parameter', ParamMap)
