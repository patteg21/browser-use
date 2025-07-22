import os
import asyncio

from dotenv import load_dotenv

load_dotenv()

from browser_use import Agent, BrowserSession
from browser_use.llm import ChatAzureOpenAI
from browser_use.dom.history_tree_processor.service import HistoryTreeProcessor


# PYTHONPATH=. python browser_use
async def main():
    click_sequence: list[dict] = []

    browser_session = BrowserSession()

    agent = Agent(
        task="Compare the price of gpt-4o and DeepSeek-V3. Click a few buttons before as well",
        llm=ChatAzureOpenAI(
            model="o4-mini", 
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_API_ENDPOINT"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            temperature=1.0
            ),
        browser_session=browser_session
    )
    await agent.run()


if __name__ == "__main__":
    asyncio.run(main())