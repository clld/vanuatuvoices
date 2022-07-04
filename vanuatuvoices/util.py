import urllib
from pyclts.ipachart import VowelTrapezoid, PulmonicConsonants


def language_detail_html(context=None, request=None, **kw):
    res = {}
    d = VowelTrapezoid()
    covered = d.fill_slots(context.inventory)
    res['vowels_html'], res['vowels_css'] = d.render()
    d = PulmonicConsonants()
    covered = covered.union(d.fill_slots(context.inventory))
    res['consonants_html'], res['consonants_css'] = d.render()
    res['uncovered'] = [p for i, p in enumerate(context.inventory) if i not in covered]
    return res


def localize_url(req, lang):
    assert lang
    k_str = '__locale__'
    p_url = urllib.parse.urlsplit(req.url)
    params = dict(req.params)
    if k_str in params and lang.lower() == 'en':
        del params[k_str]
    elif lang.lower() != 'en':
        params[k_str] = lang.lower()
    return urllib.parse.urlunsplit(
        urllib.parse.SplitResult(p_url.scheme, p_url.netloc, p_url.path,
                                 urllib.parse.urlencode(params, doseq=True),
                                 p_url.fragment))
