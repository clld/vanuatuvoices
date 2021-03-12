from sqlalchemy.orm import joinedload
from clld.web import datatables
from clld.web.datatables.base import LinkCol, Col, LinkToMapCol
from clld.web.datatables.contributor import Contributors
from clld.web.datatables.value import Values
from clld.web.datatables.parameter import Parameters
from clld.web.util.htmllib import HTML
from clld.web.util import concepticon
from clld.db.models import common
from clld.db.util import get_distinct_values

from vanuatuvoices import models


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


class AudioCol(Col):
    def format(self, item):
        if item.jsondatadict['audio']:
            return HTML.audio(
                HTML.source(src=item.jsondata['audio'], type="audio/mpeg"),
                controls="controls"
            )
        return ''


class Words(LongTableMixin, Values):
    def base_query(self, query):
        if not any([self.language, self.parameter, self.contribution]):
            return query\
                .join(common.ValueSet)\
                .join(common.Parameter)\
                .join(common.Language)\
                .options(
                joinedload(common.Value.valueset).joinedload(common.ValueSet.parameter),
                joinedload(common.Value.valueset).joinedload(common.ValueSet.language))
        else:
            return Values.base_query(self, query)

    def col_defs(self):
        res = []
        if self.language:
            res.extend([
                LinkCol(self, 'gloss_en', sTitle=self.req._('English'), get_object=lambda v: v.valueset.parameter),
                Col(self,
                    'gloss_bi',
                    sTitle=self.req._('Bislama'),
                    get_object=lambda v: v.valueset.parameter,
                    model_col=common.Parameter.description,
                ),
            ])
        elif self.parameter:
            res.extend([
                LinkCol(self, 'language', sTitle=self.req._('Language'), get_object=lambda v: v.valueset.language),
                Col(self,
                    'desc',
                    sTitle=self.req._('Location'),
                    get_object=lambda v: v.valueset.language,
                    model_col=common.Language.description,
                ),
            ])
            # FIXME: link to map!
        res.extend([
            Col(self, 'name', sTitle=self.req._('Word')),
            LinkCol(self, 'language', sTitle=self.req._('Language'),
                    model_col=common.Language.name,
                    get_object=lambda v: v.valueset.language),
            LinkCol(self, 'gloss_en', sTitle=self.req._('English'),
                    model_col=common.Parameter.name,
                    get_object=lambda v: v.valueset.parameter),
            Col(self,
                'gloss_bi',
                sTitle=self.req._('Bislama'),
                get_object=lambda v: v.valueset.parameter,
                model_col=common.Parameter.description,
            ),
            AudioCol(self, '#', bSearchable=False, bSortable=False)
        ])
        return res


_ = lambda s: s

class VVContributors(Contributors):
    def col_defs(self):
        return [
            Col(self, 'name', sTitle=self.req._('Name')),
            Col(self, 'description', sTitle=self.req._('Role')),
        ]


class ConcepticonCol(Col):
    def format(self, item):
        return concepticon.link(self.dt.req, item.concepticon_id, label=item.concepticon_gloss)


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
