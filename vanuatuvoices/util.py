from clld.db.meta import DBSession
from clld.db.models import common


def dataset_detail_html(context=None, request=None, **kw):
    return {'contributors': DBSession.query(common.Contributor)
        .join(common.ContributionContributor)
        .order_by(common.ContributionContributor.ord)
        .all()}
