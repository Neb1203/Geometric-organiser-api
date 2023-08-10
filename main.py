import os

import uvicorn
from controllers.Authenticate import Authenticate
from controllers.PlayerDetails import PlayerDetails

from fastapi import FastAPI

app = FastAPI()
player_details = PlayerDetails()
authenticate = Authenticate()

@app.post("/authenticate/")
async def post_authenticate(email: str, password: str):
    return authenticate.index(email, password)
@app.get("/validate/")
async def validation(sessionToken: str):
    return authenticate.validate(sessionToken)

@app.get("/player_details/")
async def get_player_details(email: str, password: str):
    return player_details.cloudLogin(email, password)
@app.post("/player_details/")
async def post_player_details(user_name: str, email: str, password: str):
    return player_details.write(user_name, email, password)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.2", port=5000, log_level="info")
