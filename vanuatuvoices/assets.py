from pathlib import Path

from clld.web.assets import environment

import vanuatuvoices


environment.append_path(
    Path(vanuatuvoices.__file__).parent.joinpath('static').as_posix(),
    url='/vanuatuvoices:static/')
environment.load_path = list(reversed(environment.load_path))
