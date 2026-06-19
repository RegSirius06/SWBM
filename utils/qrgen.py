import base64
import os
import tempfile
import uuid
from pathlib import Path
from typing import Any

from django.core import signing
from django.urls import reverse
from MyQR import myqr

from SWBM import settings
from bank.models import account


def make_signed_token(account_id: uuid.UUID) -> str:
    data = {
        'acc': str(account_id)
    }
    return signing.dumps(data, salt='qr-token')

def unsign_token(token: str) -> Any:
    return signing.loads(token, salt='qr-token')

def generate_qr_for_user(user: account) -> str:
    token = make_signed_token(user.id)
    qr_url = f"{settings.SITE_URL}{reverse('qr-login')}?token={token}"

    filename = f"{uuid.uuid4().hex}.png"
    qr_dir = Path(settings.MEDIA_ROOT) / "qr"
    qr_dir.mkdir(parents=True, exist_ok=True)
    out_path = qr_dir / filename

    myqr.run(
        words=qr_url,
        picture=str(Path(settings.STATIC_ROOT) / 'favicon.png'),
        colorized=True,
        contrast=1.0,
        brightness=1.0,
        save_name=str(out_path),
        version=1,
        level='H',
    )

    return f"qr/{filename}"

def make_qr_base64(url: str, version: int = 1, level: str = "H") -> str:
    tmp_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    tmp_path = tmp_file.name
    tmp_file.close()

    myqr.run(
        url,
        save_name=tmp_path,
        picture=str(Path(settings.STATIC_ROOT) / 'favicon.png'),
        colorized=True,
        contrast=1.0,
        brightness=1.0,
        version=version,
        level=level,
    )

    with open(tmp_path, "rb") as f:
        img_bytes = f.read()
    b64 = base64.b64encode(img_bytes).decode("ascii")
    os.remove(tmp_path)

    return b64