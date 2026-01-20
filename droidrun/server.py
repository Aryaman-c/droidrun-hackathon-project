from fastapi import FastAPI, BackgroundTasks, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import uvicorn
import asyncio
from reddit_agent import RedditAutomation

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Initialize automation agent lazily
reddit_bot = None

def get_reddit_bot():
    global reddit_bot
    if reddit_bot is None:
        try: 
            reddit_bot = RedditAutomation()
        except Exception as e:
            print(f"Failed to initialize RedditAutomation: {e}")
            return None
    return reddit_bot

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/post")
async def post_message(request: Request):
    bot = get_reddit_bot()
    if not bot:
        return JSONResponse({"status": "error", "message": "Backend not initialized. Check GOOGLE_API_KEY."}, status_code=500)

    data = await request.json()
    title = data.get("title")
    body = data.get("body", "") # Optional
    subreddit = data.get("subreddit", "u/me") # Default to profile if not specified, or force user to specify
    
    if not title:
        return JSONResponse({"status": "error", "message": "Title is required"}, status_code=400)
    if not subreddit:
         return JSONResponse({"status": "error", "message": "Subreddit is required"}, status_code=400)

    # Run in background to not block response? 
    # Actually, for this simpler version, the user might want to know when it's done. 
    # But DroidRun takes time. Let's send a "Started" response and let them check logs.
    # We'll use a wrapper to run it properly.
    
    asyncio.create_task(bot.post_message(title, body, subreddit))
    return {"status": "success", "message": f"Posting task started for {subreddit}"}

@app.post("/start_monitor")
async def start_monitor():
    bot = get_reddit_bot()
    if not bot:
         return JSONResponse({"status": "error", "message": "Backend not initialized."}, status_code=500)

    if bot.is_monitoring:
        return {"status": "info", "message": "Already monitoring"}
    
    asyncio.create_task(bot.start_monitoring_loop())
    return {"status": "success", "message": "Monitoring started"}

@app.post("/stop_monitor")
async def stop_monitor():
    bot = get_reddit_bot()
    if bot:
        bot.stop_monitoring()
    return {"status": "success", "message": "Monitoring stopping..."}

@app.get("/logs")
async def get_logs():
    bot = get_reddit_bot()
    if not bot:
        return {"logs": ["System: Waiting for initialization... Check API Key."], "is_monitoring": False}
    return {"logs": bot.logs, "is_monitoring": bot.is_monitoring}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
