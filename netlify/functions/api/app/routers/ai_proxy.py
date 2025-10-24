from fastapi import APIRouter, Body

router = APIRouter()

@router.post('/tts')
async def tts_proxy(text: str = Body(..., embed=True)):
    return {"message": "tts not implemented", "text": text}

@router.post('/stt')
async def stt_proxy():
    return {"message": "stt not implemented"}
