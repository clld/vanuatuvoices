from sqlalchemy.orm import joinedload
from sqlalchemy import or_
from clld.web import datatables
from clld.web.datatables.base import LinkCol, Col, LinkToMapCol
from clld.web.datatables.contributor import Contributors
from clld.web.datatables.value import Values
from clld.web.datatables.parameter import Parameters
from clld.web.util import concepticon
from clld.db.models import common
from clld.db.util import get_distinct_values, icontains
from clld_audio_plugin.datatables import AudioCol

from vanuatuvoices import models


_ = lambda s: s


class LongTableMixin:
    def get_options(self):
        return {'iDisplayLength': 200}


class Languages(LongTableMixin, datatables.Languages):
    def col_defs(self):
        return [
            LinkCol(self, 'name', sTitle=self.req._('Name')),
            Col(self,
                'Island',
                sTitle=self.req._('Island'),
                model_col=models.Variety.island,
                choices=get_distinct_values(models.Variety.island)),
            Col(self, 'count_concepts',
                sTitle=self.req._('# concepts'),
                sTooltip=self.req._('number of concepts per language'),
                model_col=models.Variety.count_concepts),
            Col(self, 'count_lexemes',
                sTitle=self.req._('# words'),
                sTooltip=self.req._('number of words per language'),
                model_col=models.Variety.count_lexemes),
            Col(self, 'count_soundfiles',
                sTitle=self.req._('# audio'),
                sTooltip=self.req._('number of sound files per language'),
                model_col=models.Variety.count_soundfiles),
            Col(self,
                'latitude',
                sDescription='<small>The geographic latitude</small>'),
            Col(self,
                'longitude',
                sDescription='<small>The geographic longitude</small>'),
            LinkToMapCol(self, 'm'),
        ]


class Words(LongTableMixin, Values):
    def base_query(self, query):
        if not any([self.language, self.parameter, self.contribution]):
            return query\
                .join(common.ValueSet)\
                .join(common.Parameter)\
                .join(common.Language)\
                .options(
                    joinedload(common.Value.valueset).joinedload(common.ValueSet.parameter),
                    joinedload(common.Value.valueset).joinedload(common.ValueSet.language)
                )
        else:
            return Values.base_query(self, query)

    def get_default_options(self):
        opts = super(Values, self).get_default_options()
        opts['aaSorting'] = [[1, 'asc']]
        return opts

    def col_defs(self):
        if self.language:
            return [
                LinkCol(self,
                        'name',
                        sTitle=self.req._('English'),
                        get_object=lambda v: v.valueset.parameter,
                        model_col=common.Parameter.name),
                Col(self,
                    'name',
                    sTitle=self.req._('Semantic Field'),
                    get_object=lambda v: v.valueset.parameter,
                    model_col=models.Concept.concepticon_semantic_field,
                    choices=get_distinct_values(models.Concept.concepticon_semantic_field)),
                Col(self,
                    'description',
                    sTitle=self.req._('Bislama'),
                    get_object=lambda v: v.valueset.parameter,
                    model_col=common.Parameter.description),
                LinkCol(self, 'name', sTitle=self.req._('Word')),
                Col(self, 'description', sTitle=self.req._('Segments')),
                AudioCol(self, '#', bSearchable=False, bSortable=False),
            ]
        elif self.parameter:
            return [
                LinkCol(self, 'name', sTitle=self.req._('Word')),
                Col(self, 'description', sTitle=self.req._('Segments')),
                LinkCol(self, 'language', sTitle=self.req._('Language'),
                        model_col=common.Language.name,
                        get_object=lambda v: v.valueset.language),
                LinkToMapCol(self, 'm', get_object=lambda i: i.valueset.language),
                AudioCol(self, '#', bSearchable=False, bSortable=False),
            ]
        return [
            LinkCol(self, 'name', sTitle=self.req._('Word')),
            LinkCol(self,
                    'name',
                    sTitle=self.req._('English'),
                    get_object=lambda v: v.valueset.parameter,
                    model_col=common.Parameter.name),
            Col(self,
                'name',
                sTitle=self.req._('Semantic Field'),
                get_object=lambda v: v.valueset.parameter,
                model_col=models.Concept.concepticon_semantic_field,
                choices=get_distinct_values(models.Concept.concepticon_semantic_field)),
            LinkCol(self, 'language', sTitle=self.req._('Language'),
                    model_col=common.Language.name,
                    get_object=lambda v: v.valueset.language),
            AudioCol(self, '#', bSearchable=False, bSortable=False),
        ]


class VVContributors(Contributors):
    def col_defs(self):
        return [
            Col(self, 'name', sTitle=self.req._('Name')),
            Col(self, 'description', sTitle=self.req._('Role')),
        ]


class ConcepticonCol(Col):
    def format(self, item):
        return concepticon.link(self.dt.req, item.concepticon_id, label=item.concepticon_gloss)

    def search(self, qs):
        return or_(icontains(models.Concept.concepticon_gloss, qs), models.Concept.concepticon_id.__eq__(qs))


class Concepts(LongTableMixin, Parameters):
    def col_defs(self):
        return [
            LinkCol(self, 'name', sTitle=self.req._('English')),
            Col(self, 'description', sTitle=self.req._('Bislama')),
            Col(self, 'count_lexemes',
                sTitle=self.req._('# words'),
                sTooltip=self.req._('number of words per concept'),
                model_col=models.Concept.count_lexemes),
            # ConcepticonCol(self, 'concepticon'),
            Col(self, 'concepticon_semantic_field',
                model_col=models.Concept.concepticon_semantic_field,
                choices=get_distinct_values(models.Concept.concepticon_semantic_field)),
        ]


def includeme(config):
    config.register_datatable('languages', Languages)
    config.register_datatable('parameters', Concepts)
    config.register_datatable('values', Words)
    config.register_datatable('contributors', VVContributors)
