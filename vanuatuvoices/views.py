from clld.db.meta import DBSession
from clld.db.models import common


def credits(context, request):
    return {'contributors': DBSession.query(common.Contributor)
        .order_by(common.Contributor.id)
        .all()}
