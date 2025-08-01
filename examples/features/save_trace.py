import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dotenv import load_dotenv

load_dotenv()

from browser_user.agent.service import Agent
from browser_user.browser import BrowserProfile, BrowserSession
from browser_user.llm import ChatOpenAI

llm = ChatOpenAI(model='gpt-4.1', temperature=0.0)


async def main():
	browser_session = BrowserSession(
		browser_profile=BrowserProfile(
			traces_dir='./tmp/traces/',
			user_data_dir='~/.config/browseruse/profiles/default',
		)
	)

	async with browser_session:
		agent = Agent(
			task='Go to hackernews, then go to apple.com and return all titles of open tabs',
			llm=llm,
			browser_session=browser_session,
		)
		await agent.run()


asyncio.run(main())
