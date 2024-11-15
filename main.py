from fastapi import FastAPI
import auth, area, category, item
import models
from database import engine
from fastapi.middleware.cors import CORSMiddleware

# start the FastAPI app
app = FastAPI()

# include routers 
# authentication router
app.include_router(auth.router)
# area router
app.include_router(area.router)
# category router
app.include_router(category.router)
# item router
app.include_router(item.router)

# create tables
models.Base.metadata.create_all(bind=engine)

# allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
