from typing import Any

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from litellm import completion
from pydantic import BaseModel, Field

from app.routing.router import select_model

load_dotenv()

app = FastAPI(title="LLM Model Router", version="0.1.0")


class GenerateRequest(BaseModel):
    task: str = Field(min_length=1)
    temperature: float = Field(default=0.2, ge=0, le=2)


class GenerateResponse(BaseModel):
    model: str
    route: str
    answer: str
    usage: dict[str, Any] | None = None


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/generate", response_model=GenerateResponse)
def generate(request: GenerateRequest) -> GenerateResponse:
    model, route = select_model(request.task)

    try:
        response = completion(
            model=model,
            messages=[{"role": "user", "content": request.task}],
            temperature=request.temperature,
        )

        usage = response.usage.model_dump() if response.usage else None

        return GenerateResponse(
            model=model,
            route=route,
            answer=response.choices[0].message.content or "",
            usage=usage,
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc