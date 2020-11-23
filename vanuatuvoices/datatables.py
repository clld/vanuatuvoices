from sqlalchemy.orm import joinedload
from clld.web import datatables
from clld.web.datatables.base import LinkCol, Col, LinkToMapCol
from clld.web.datatables.contributor import Contributors
from clld.web.datatables.value import Values
from clld.web.datatables.parameter import Parameters
from clld.web.util.htmllib import HTML
from clld.web.util import concepticon
from clld.db.models import common

from clld_glottologfamily_plugin.models import Family
from clld_glottologfamily_plugin.datatables import FamilyCol

from vanuatuvoices import models


class LongTableMixin:
    def get_options(self):
        return {'iDisplayLength': 200}


class Languages(LongTableMixin, datatables.Languages):
    def base_query(self, query):
        return query.join(Family).options(joinedload(models.Variety.family)).distinct()

    def col_defs(self):
        return [
            LinkCol(self, 'name'),
            FamilyCol(self, 'Family', models.Variety),
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
            AudioCol(self, '#')
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
