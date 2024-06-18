from fastapi import FastAPI
import uvicorn

app = FastAPI()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)

@app.get("/")
async def root():
    return {"message": "всё работает"}
