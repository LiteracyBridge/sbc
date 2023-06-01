import uuid
import uvicorn

from fastapi import Depends, FastAPI, HTTPException
from mangum import Mangum

from routes import users, indicators, theory_of_change, activity
from monitoring import logging_config
from middlewares.correlation_id_middleware import CorrelationIdMiddleware
from middlewares.logging_middleware import LoggingMiddleware
from handlers.exception_handler import exception_handler
from handlers.http_exception_handler import http_exception_handler
from fastapi.middleware.cors import CORSMiddleware

import models
from config import settings

# from database import SessionLocal, engine

# models.Base.metadata.create_all(bind=engine)


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
    indicators.router,
    prefix="/indicators",
    tags=["indicators"],
    dependencies=[Depends(models.get_db)],
)
app.include_router(
    theory_of_change.router,
    prefix="/theory-of-change",
    tags=["theory-of-change"],
    dependencies=[Depends(models.get_db)],
)
app.include_router(
    activity.router,
    prefix="/activity",
    tags=["activity"],
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
