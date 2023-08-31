import uuid
import uvicorn
import sentry_sdk
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration
import jwt
from fastapi import Depends, FastAPI, HTTPException, Request
from mangum import Mangum

from routes import (
    users_route,
    theory_of_change,
    activity_route,
    monitoring,
    project_route,
    lookups_route,
    organisation_route,
    communication_route,
    data_service_route,
    open_ai_route,
    feedback_route,
    twilio_route,
)
from monitoring import logging_config
from middlewares.correlation_id_middleware import CorrelationIdMiddleware
from middlewares.logging_middleware import LoggingMiddleware
from handlers.exception_handler import exception_handler
from handlers.http_exception_handler import http_exception_handler
from fastapi.middleware.cors import CORSMiddleware
from helpers.jwt_verifier import CognitoAuthenticator
import models
from helpers.config import settings
from helpers import model_events

if settings.sentry_dsn is not None:
    sentry_sdk.init(
        dsn=settings.sentry_dsn,
        integrations=[
            AwsLambdaIntegration(timeout_warning=True),
        ],
        #     # Set traces_sample_rate to 1.0 to capture 100%
        #     # of transactions for performance monitoring.
        #     # We recommend adjusting this value in production,
        #     # traces_sample_rate=1.0,
    )


# from database import SessionLocal, engine

# models.Base.metadata.create_all(bind=engine)

# FIXME: add congnito JWT verify middleware

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:4173",
    "https://sbcimpact.amplio.org",
    "https://sbcimpact.amplio.org/",
    "https://*.amplio.org",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# cognito_auth = CognitoAuthenticator()


# @app.middleware("http")
# async def verify_jwt(request: Request, call_next):
#     # return await call_next(request)

#     # Get the access token from the request headers
#     if request.method == "OPTIONS":
#         return await call_next(request)

#     token = request.headers.get("Authorization")
#     if not token:
#         raise HTTPException(status_code=401, detail="No access token provided")

#     # cognito_auth.verify_token(token.replace("Bearer ", ""))

#     response = await call_next(request)

#     return response


if not settings.is_local:
    ###############################################################################
    #   Logging configuration                                                     #
    ###############################################################################
    logging_config.configure_logging(
        level="DEBUG", service="SBC", instance=str(uuid.uuid4())
    )

    ###############################################################################
    #   Error handlers configuration                                              #
    ###############################################################################
    app.add_exception_handler(Exception, exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)

    ###############################################################################
    #   Middlewares configuration                                                 #
    ###############################################################################

    # Tip : middleware order : CorrelationIdMiddleware > LoggingMiddleware -> reverse order
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(CorrelationIdMiddleware)


###############################################################################
#   Routers configuration                                                     #
###############################################################################

app.include_router(
    users_route.router,
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(models.get_db)],
)
app.include_router(
    theory_of_change.router,
    prefix="/theory-of-change",
    tags=["theory-of-change"],
    dependencies=[Depends(models.get_db)],
)
app.include_router(
    activity_route.router,
    prefix="/activity",
    tags=["activity"],
    dependencies=[Depends(models.get_db)],
)
app.include_router(
    monitoring.router,
    prefix="/monitoring",
    tags=["monitoring"],
    dependencies=[Depends(models.get_db)],
)
app.include_router(
    project_route.router,
    prefix="/project",
    tags=["project"],
    dependencies=[Depends(models.get_db)],
)
app.include_router(
    lookups_route.router,
    prefix="/lu",
    tags=["lu"],
    dependencies=[Depends(models.get_db)],
)
app.include_router(
    organisation_route.router,
    prefix="/organisation",
    tags=["organisation"],
    dependencies=[Depends(models.get_db)],
)
app.include_router(
    communication_route.router,
    prefix="/communications",
    tags=["communications"],
    dependencies=[Depends(models.get_db)],
)
app.include_router(
    data_service_route.router,
    prefix="/data-service",
    tags=["data-service"],
    dependencies=[Depends(models.get_db)],
)
app.include_router(
    open_ai_route.router,
    prefix="/open-ai",
    tags=["open-ai"],
    dependencies=[Depends(models.get_db)],
)
app.include_router(
    feedback_route.router,
    prefix="/feedback",
    tags=["feedback"],
    dependencies=[Depends(models.get_db)],
)
app.include_router(
    twilio_route.router,
    prefix="/twilio",
    tags=["twilio"],
    dependencies=[Depends(models.get_db)],
)


###############################################################################
#   Handler for AWS Lambda                                                    #
###############################################################################

handler = Mangum(app)

###############################################################################
#   Run the self contained application                                        #
###############################################################################

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
