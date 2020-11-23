import itertools
import collections

from pycldf import Sources
from clldutils.misc import nfilter
from clldutils.color import qualitative_colors
from clldutils.misc import slug
from clldutils import licenses
from clld.cliutil import Data, bibtex2source
from clld.db.meta import DBSession
from clld.db.models import common
from clld.lib import bibtex
from nameparser import HumanName

from clld_glottologfamily_plugin.util import load_families
from cldfbench import get_dataset

import vanuatuvoices
from vanuatuvoices import models

"""
([{'description': 'author, data entry, audio recordings', 'name': 'Aviva Shimelman', 'github user': ''}, {'description': 'author', 'name': 'Paul Heggarty', 'github user': ''}, {'description': 'author, data entry, audio recordings', 'name': 'Tom Enneve', 'github user': ''}, {'description': 'author, data entry, audio recordings, audio post-processing, mark-up', 'name': 'Iveth Rodriguez', 'github user': ''}, {'description': 'author, data entry, audio recordings, audio post-processing, mark-up', 'name': 'Tom Fitzpatrick', 'github user': ''}, {'description': 'author, data entry, audio recordings', 'name': 'Marie-France Duhamel', 'github user': ''}, {'description': 'author, data entry, audio recordings', 'name': 'Lana Takau', 'github user': ''}, {'description': 'data entry', 'name': 'Mary Walworth', 'github user': ''}, {'description': 'data entry', 'name': 'Giovanni Abete', 'github user': ''}, {'description': 'data entry', 'name': 'Benjamin Touati', 'github user': ''}, {'description': 'audio post-processing, mark-up', 'name': 'Darja Dërmaku-Appelganz', 'github user': ''}, {'description': 'audio post-processing, mark-up', 'name': 'Laura Wägerle', 'github user': ''}, {'description': 'admin', 'name': 'Kaitip W. Kami', 'github user': ''}, {'description': 'admin', 'name': 'Heidi Colleran', 'github user': ''}, {'description': 'admin', 'name': 'Russell Gray', 'github user': ''}, {'description': 'audio post-processing, mark-up', 'name': 'Darja Dërmaku-Appelganz', 'github user': ''}, {'description': 'audio post-processing, mark-up', 'name': 'Laura Wägerle', 'github user': ''}], [{'description': 'patron, maintainer', 'name': 'Hans-Jörg Bibiko', 'type': 'Other', 'github user': '@Bibiko'}])
"""


def main(args):

    assert args.glottolog, 'The --glottolog option is required!'

    license = licenses.find(args.cldf.properties['dc:license'])
    assert license and license.id.startswith('CC-')

    data = Data()
    ds = data.add(
        common.Dataset,
        vanuatuvoices.__name__,
        id=vanuatuvoices.__name__,
        name='Vanuatu Voices',
        domain='vanuatuvoices.clld.org',
        publisher_name="Max Planck Institute for the Science of Human History",
        publisher_place="Jena",
        publisher_url="https://www.shh.mpg.de",
        license=license.url,
        jsondata={
            'license_icon': '{}.png'.format(
                '-'.join([p.lower() for p in license.id.split('-')[:-1]])),
            'license_name': license.name},

    )

    contrib = data.add(
        common.Contribution,
        None,
        id='cldf',
        name=args.cldf.properties.get('dc:title'),
        description=args.cldf.properties.get('dc:bibliographicCitation'),
    )
    r = get_dataset('vanuatuvoices', ep='lexibank.dataset')
    authors, _ = r.get_creators_and_contributors()
    for ord, author in enumerate(authors):
        c = data.add(
            common.Contributor,
            slug(HumanName(author['name']).last),
            id=slug(HumanName(author['name']).last),
            name=author['name'],
            description=author.get('description'))
        DBSession.add(common.ContributionContributor(contribution=contrib, contributor=c))
    DBSession.add(common.Editor(dataset=ds, contributor=data['Contributor']['walworth']))

    form2audio = {}
    for r in args.cldf.iter_rows('media.csv', 'id', 'formReference'):
        if r['mimetype'] == 'audio/mpeg':
            form2audio[r['formReference']] = r

    for lang in args.cldf.iter_rows('LanguageTable', 'id', 'glottocode', 'name', 'latitude', 'longitude'):
        data.add(
            models.Variety,
            lang['id'],
            id=lang['id'],
            name=lang['name'],
            latitude=lang['latitude'],
            longitude=lang['longitude'],
            glottocode=lang['glottocode'],
            description=lang['LongName'],
        )

    for rec in bibtex.Database.from_file(args.cldf.bibpath, lowercase=True):
        data.add(common.Source, rec.id, _obj=bibtex2source(rec))

    refs = collections.defaultdict(list)

    for param in args.cldf.iter_rows('ParameterTable', 'id', 'concepticonReference', 'name'):
        data.add(
            models.Concept,
            param['id'],
            id=param['id'],
            name='{} [{}]'.format(param['name'], param['id'].split('_')[0]),
            description=param['Bislama_Gloss'],
            concepticon_id=param['concepticonReference'],
            concepticon_gloss=param['Concepticon_Gloss'],
        )
    for form in args.cldf.iter_rows('FormTable', 'id', 'form', 'languageReference', 'parameterReference', 'source'):
        vsid = (form['languageReference'], form['parameterReference'])
        vs = data['ValueSet'].get(vsid)
        if not vs:
            vs = data.add(
                common.ValueSet,
                vsid,
                id='-'.join(vsid),
                language=data['Variety'][form['languageReference']],
                parameter=data['Concept'][form['parameterReference']],
                contribution=contrib,
            )
        for ref in form.get('source', []):
            sid, pages = Sources.parse(ref)
            refs[(vsid, sid)].append(pages)
        data.add(
            common.Value,
            form['id'],
            id=form['id'],
            name=form['form'],
            valueset=vs,
            jsondata=dict(audio=args.cldf.get_row_url('media.csv', form2audio[form['id']])
            if form['id'] in form2audio else None),
        )

    for (vsid, sid), pages in refs.items():
        DBSession.add(common.ValueSetReference(
            valueset=data['ValueSet'][vsid],
            source=data['Source'][sid],
            description='; '.join(nfilter(pages))
        ))
    load_families(
        Data(),
        [(l.glottocode, l) for l in data['Variety'].values()],
        glottolog_repos=args.glottolog,
        isolates_icon='tcccccc',
        strict=False,
    )


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """
