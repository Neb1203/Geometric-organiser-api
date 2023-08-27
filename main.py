import os

import uvicorn
from controllers.Authenticate import Authenticate
from controllers.login import Login
from controllers.PlayerDetails import PlayerDetails

from fastapi import *

app = FastAPI()
player_details = PlayerDetails()
authenticate = Authenticate()
login = Login()

@app.post("/authenticate/")
async def post_authenticate(email: str, password: str):
    return authenticate.index(email, password)
@app.get("/validate/")
async def validation(sessionToken: str, response: Response):
    validateToken = authenticate.validate(sessionToken)
    if not validateToken:
        response.status_code = 422
        return "Not logged in"
    return "Logged in"


@app.get("/fetchUsername/")
async def username():
    return login.username()

@app.get("/player_details/")
async def get_player_details(email: str, password: str):
    return player_details.cloudLogin(email, password)
@app.post("/player_details/")
async def post_player_details(user_name: str, email: str, password: str):
    return player_details.write(user_name, email, password)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")
