from getToken import *
from signup import *
from fastapi import FastAPI
import unicorn

app = FastAPI()

@app.get('/create/{botname}')
async def create(botname: str):
    print('I am here')
    phone = creating()
    bottoken, providertoken = create_bot(botname)
    print(bottoken, providertoken)
    return {"success": bottoken}, 200

if __name__ == "__main__":
    unicorn.run(app, host = '0.0.0.0', port = 8000)
    
