from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.controllers import account, auth, transaction
from src.database import database
from src.exceptions import AccountNotFoundError, BusinessError

# ======================================
# Lifespan
# ======================================
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


# ======================================
# Metadata e Tags
# ======================================
tags_metadata = [
    {"name": "auth", "description": "Operations for authentication."},
    {"name": "account", "description": "Operations to maintain accounts."},
    {"name": "transaction", "description": "Operations to maintain transactions."},
]


# ======================================
# Fast app
# ======================================
app = FastAPI(
    title="Transactions API",
    version="1.0.0",
    summary="Microservice to maintain withdrawal and deposit operations from current accounts.",
    description="""
Transactions API is the microservice for recording current account transactions.

## Account
- Create accounts
- List accounts
- List account transactions by ID

## Transaction
- Create transactions
""",
    openapi_tags=tags_metadata,
    redoc_url=None,
    lifespan=lifespan,
)


# ======================================
# Middleware
# ======================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajuste produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ======================================
# Routers
# ======================================
routers = [auth.router, account.router, transaction.router]
tags = ["auth", "account", "transaction"]

for r, t in zip(routers, tags):
    app.include_router(r, tags=[t])


# ======================================
# Exception 
# ======================================
@app.exception_handler(AccountNotFoundError)
async def account_not_found_error_handler(request: Request, exc: AccountNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "detail": "Account not found.",
            "path": request.url.path,
        },
    )


@app.exception_handler(BusinessError)
async def business_error_handler(request: Request, exc: BusinessError):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "detail": str(exc),
            "path": request.url.path,
        },
    )
