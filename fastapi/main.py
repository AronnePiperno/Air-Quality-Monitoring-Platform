import uvicorn
from API import *

# Run the FastAPI app using uvicorn
if __name__ == "__main__":
    uvicorn.run("main:app")
