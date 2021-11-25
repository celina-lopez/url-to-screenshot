from typing import Optional

import fastapi
from fastapi import Depends

from services import screenshot

router = fastapi.APIRouter()


@router.get('/api/{url}')
async def weather(url):
    report = await screenshot.get_image_async(url)

    return report
