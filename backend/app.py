import uuid
import uvicorn
import sentry_sdk
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration

from fastapi import Depends, FastAPI, HTTPException
from mangum import Mangum

from routes import (
    users,
    theory_of_change,
    activity_route,
    monitoring,
    project,
    lookups,
    organisation_route,
    communication_route,
    data_service_route,
    open_ai_route,
    feedback_route
)
from monitoring import logging_config
from middlewares.correlation_id_middleware import CorrelationIdMiddleware
from middlewares.logging_middleware import LoggingMiddleware
from handlers.exception_handler import exception_handler
from handlers.http_exception_handler import http_exception_handler
from fastapi.middleware.cors import CORSMiddleware

import models
from config import settings
import model_events

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

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# # Dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

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
    users.router, prefix="/users", tags=["users"], dependencies=[Depends(models.get_db)]
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
    project.router,
    prefix="/project",
    tags=["project"],
    dependencies=[Depends(models.get_db)],
)
app.include_router(
    lookups.router,
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


###############################################################################
#   Handler for AWS Lambda                                                    #
###############################################################################

handler = Mangum(app)

###############################################################################
#   Run the self contained application                                        #
###############################################################################

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
