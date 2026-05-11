from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from events import get_calendar_events

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://workshoppefitness.com", "https://www.workshoppefitness.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def root():
    return {'message': 'Welcome to Gym Scheduler'}

@app.get('/status')
async def status():
    return {'message': 'Gym Scheduler is running'}

@app.get('/abcfitness/calendar/events')
async def get_calendar_events_route(eventDateRange: str):
    return await get_calendar_events(eventDateRange = eventDateRange)