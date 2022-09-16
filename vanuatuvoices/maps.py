from clld.web.maps import Map, ParameterMap


class LanguagesMap(Map):
    def get_options(self):
        return {
            'max_zoom': 17,
            'base_layer': 'Esri.WorldTopoMap',
            'show_labels': False,
        }


class ConceptMap(ParameterMap):
    def get_options(self):
        return {
            'with_audioplayer': True,
            'max_zoom': 17,
            'base_layer': 'Esri.WorldTopoMap',
            'show_labels': False,
        }


def includeme(config):
    config.register_map('languages', LanguagesMap)
    config.register_map('parameter', ConceptMap)
