import os
import uvicorn
from art import tprint
from dotenv import load_dotenv

if __name__ == "__main__":
    try:
        tprint("WAV Warehouse")
        load_dotenv()

        host = os.environ["UVICORN_HOST"]
        port = int(os.environ["UVICORN_PORT"])

        app = "warehouse.api:app"

        uvicorn.run(app, host=host, port=port, reload=True)
    except Exception as error:
        print(f"Error Occurred, Details : {error}")

        raise
