from clld.web.maps import Map, ParameterMap


class LanguagesMap(Map):
    def get_options(self):
        return {
            'max_zoom': 17,
            'base_layer': 'Esri.WorldTopoMap',
            'show_labels': False,
        }


class ConceptsMap(ParameterMap):
    def get_options(self):
        return {
            'max_zoom': 17,
            'base_layer': 'Esri.WorldTopoMap',
            'show_labels': False,
        }


def includeme(config):
    config.register_map('languages', LanguagesMap)
    config.register_map('parameter', ConceptsMap)
