import pathlib
import collections

from pycldf import Sources
from clldutils.misc import nfilter
from clldutils.misc import slug
from clldutils import licenses
from clld.cliutil import Data, bibtex2source
from clld.db.meta import DBSession
from clld.db.models import common
from clld.lib import bibtex
from nameparser import HumanName
from cldfbench import get_dataset
from clld_audio_plugin.models import Counterpart
from clld_audio_plugin import util as audioutil

import vanuatuvoices
from vanuatuvoices import models


def main(args):  # pragma: no cover
    license = licenses.find(args.cldf.properties['dc:license'])
    assert license and license.id.startswith('CC-')

    data = Data()
    ds = data.add(
        common.Dataset,
        vanuatuvoices.__name__,
        id=vanuatuvoices.__name__,
        name='Vanuatu Voices',
        domain='vanuatuvoices.clld.org',
        contact="vanuatuvoices@shh.mpg.de",
        publisher_name="Max Planck Institute for the Science of Human History",
        publisher_place="Jena",
        publisher_url="https://www.shh.mpg.de",
        license=license.url,
        jsondata={
            'license_icon': '{}.png'.format(
                '-'.join([p.lower() for p in license.id.split('-')[:-1]])),
            'license_name': license.name},

    )

    form2audio = audioutil.form2audio(args.cldf, 'audio/mpeg')

    r = get_dataset('vanuatuvoices', ep='lexibank.dataset')
    authors, _ = r.get_creators_and_contributors()
    for ord, author in enumerate(authors):
        cid = slug(HumanName(author['name']).last)
        img = pathlib.Path(vanuatuvoices.__file__).parent / 'static' / '{}.jpg'.format(cid)
        c = data.add(
            common.Contributor,
            cid,
            id=cid,
            name=author['name'],
            description=author.get('description'),
            jsondata=dict(img=img.name if img.exists() else None),
        )
    data.add(
        common.Contributor,
            'forkel',
            id='forkel',
            name='Robert Forkel',
            description='Data curation and website implementation',
            jsondata=dict(img=None),
    )
    for ord, cid in enumerate(['walworth', 'forkel', 'gray']):
        DBSession.add(common.Editor(
            ord=ord,
            dataset=ds,
            contributor=data['Contributor'][cid]))

    contribs = collections.defaultdict(lambda: collections.defaultdict(list))
    for c in args.cldf.iter_rows('contributions.csv'):
        for role in ['phonetic_transcriptions', 'recording', 'sound_editing']:
            for name in c[role].split(' and '):
                if name:
                    cid = slug(HumanName(name).last)
                    contribs[c['Language_ID']][cid].append(role)

    for lang in args.cldf.iter_rows('LanguageTable', 'id', 'glottocode', 'name', 'latitude', 'longitude'):
        contrib = data.add(
            common.Contribution,
            lang['id'],
            id=lang['id'],
            name='Wordlist for {}'.format(lang['name']),
        )
        if lang['id'] in contribs:
            for cid, roles in contribs[lang['id']].items():
                DBSession.add(common.ContributionContributor(
                    contribution=contrib,
                    contributor=data['Contributor'][cid],
                    jsondata=dict(roles=roles),
                ))
        data.add(
            models.Variety,
            lang['id'],
            id=lang['id'],
            name=lang['name'],
            latitude=lang['latitude'],
            longitude=lang['longitude'],
            glottocode=lang['glottocode'],
            description=lang['LongName'],
            contribution=contrib,
            island=lang['Island'],
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
                contribution=data['Contribution'][form['languageReference']],
            )
        for ref in form.get('source', []):
            sid, pages = Sources.parse(ref)
            refs[(vsid, sid)].append(pages)
        data.add(
            Counterpart,
            form['id'],
            id=form['id'],
            name=form['form'],
            valueset=vs,
            audio=form2audio.get(form['id'])
        )

    for (vsid, sid), pages in refs.items():
        DBSession.add(common.ValueSetReference(
            valueset=data['ValueSet'][vsid],
            source=data['Source'][sid],
            description='; '.join(nfilter(pages))
        ))


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """
