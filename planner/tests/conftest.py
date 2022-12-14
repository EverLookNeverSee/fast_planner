"""
    This file will be responsible for creating an instance of our application required by the test files.
    Author: Milad Sadeghi DM - EverLookNeverSee@GitHub
"""

import httpx
import pytest
import asyncio
from planner.main import app
from planner.models.users import User
from planner.models.events import Event
from planner.database.connection import Settings


@pytest.fixture(scope="session")
def event_loop():
    """Event loop session fixture"""
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


async def init_db():
    """Initialize new database instance"""
    test_settings = Settings()
    test_settings.DATABASE_URL = "mongodb://localhost:27017/testdb"
    test_settings.SECRET_KEY = "HI5HL3V3L$3CR3T"
    await test_settings.initialize_database()


@pytest.fixture(scope="session")
async def default_client():
    await init_db()
    async with httpx.AsyncClient(app=app, base_url="http://app") as client:
        yield client
        # clean up resources
        await Event.find_all().delete()
        await User.find_all().delete()
