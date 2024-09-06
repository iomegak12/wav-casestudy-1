import uvicorn
from art import tprint

if __name__ == "__main__":
    tprint("Stores and Items", font="random")

    uvicorn.run("store_service.api:app", port=8000, reload=True)
