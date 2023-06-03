import uvicorn
from controllers.PlayerDetails import PlayerDetails
from fastapi import FastAPI

app = FastAPI()
player_details = PlayerDetails()


@app.post("/player_details/")
async def post_player_details(user_name: str, email: str, password: str):
    return player_details.write(user_name, email, password)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.2", port=5000, log_level="info")
