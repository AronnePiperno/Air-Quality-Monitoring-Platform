import uvicorn
from API import *
import streamlit
if __name__ == "__main__":
    uvicorn.run("main:app")