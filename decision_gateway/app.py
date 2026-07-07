"""
Zero Trust Policy Decision Gateway
"""

from fastapi import FastAPI, HTTPException

from models import DecisionRequest, DecisionResponse
from opa_service import evaluate_opa_policy


app = FastAPI(
    title="Zero Trust Decision Gateway",
    version="1.0.0"
)


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "decision-gateway"
    }


@app.post(
    "/decide",
    response_model=DecisionResponse
)
def decide(request: DecisionRequest):

    try:
        decision = evaluate_opa_policy(
            request.policy_path,
            request.input
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        ) from error

    except Exception as error:
        raise HTTPException(
            status_code=503,
            detail=f"OPA evaluation failed: {error}"
        ) from error

    return DecisionResponse(
        allowed=decision is True,
        policy_path=request.policy_path,
        decision=decision
    )