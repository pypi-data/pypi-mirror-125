import json

import pytest

from acondbs.db.sa import sa
from acondbs.models import WebConfig


##__________________________________________________________________||
@pytest.fixture
def app(app_empty):

    y = app_empty

    config_json = json.dumps(
        {
            "headTitle": "Head Title",
            "toolbarTitle": "Toolbar Title",
            "devtoolLoadingstate": True,
            "productCreationDialog": False,
            "productUpdateDialog": True,
            "productDeletionDialog": True,
        },
        indent=2,
    )

    c = WebConfig(
        id_=1,
        json=config_json,
    )

    with y.app_context():
        sa.session.add(c)
        sa.session.commit()
    yield y


##__________________________________________________________________||
