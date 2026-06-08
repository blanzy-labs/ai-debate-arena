from fastapi import APIRouter, HTTPException

from app.config import settings
from app.debate.schemas import DebateRequest, DebateResponse
from app.debate.service import run_debate
from app.llm.errors import MissingProviderKeyError, ProviderCallError, UnsupportedProviderError


router = APIRouter(prefix="/debate", tags=["debate"])


@router.post("/run", response_model=DebateResponse)
async def run_debate_route(request: DebateRequest) -> DebateResponse:
    try:
        return await run_debate(request, settings)
    except MissingProviderKeyError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except UnsupportedProviderError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except ProviderCallError as error:
        raise HTTPException(status_code=502, detail=str(error)) from error
