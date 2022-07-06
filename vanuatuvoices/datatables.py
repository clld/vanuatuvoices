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
        if self.parameter:
            opts['aaSorting'] = [[1, 'asc']]
        return opts

    def col_defs(self):
        res = []
        if self.language:
            res = [
                LinkCol(self,
                        'name',
                        sTitle=self.req._('English'),
                        get_object=lambda v: v.valueset.parameter,
                        model_col=common.Parameter.name),
                Col(self,
                    'description',
                    sTitle=self.req._('Bislama'),
                    get_object=lambda v: v.valueset.parameter,
                    model_col=common.Parameter.description),
                Col(self, 'name', sTitle=self.req._('Word')),
                AudioCol(self, '#', bSearchable=False, bSortable=False),
            ]
        elif self.parameter:
            res = [
                Col(self, 'name', sTitle=self.req._('Word')),
                LinkCol(self, 'language', sTitle=self.req._('Language'),
                        model_col=common.Language.name,
                        get_object=lambda v: v.valueset.language),
                LinkToMapCol(self, 'm', get_object=lambda i: i.valueset.language),
                AudioCol(self, '#', bSearchable=False, bSortable=False),
            ]
        return res


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
            ConcepticonCol(self, 'concepticon'),
        ]


def includeme(config):
    config.register_datatable('languages', Languages)
    config.register_datatable('parameters', Concepts)
    config.register_datatable('values', Words)
    config.register_datatable('contributors', VVContributors)
