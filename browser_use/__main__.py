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




    task = (
        "1. Login to the site: https://us.cwcloudpartner.com/das-develop-aqa/e/eng/bp_-b5BDTgOsAmkIzK-f2w/index.jsp#/documents. "
        "2. Use the credentials: `x_member_number` and `x_passphrase`. "
        "3. Click the three dots in the top left and unhide items. to View more actions Select unhide items"
        "4. Click on 'IC-1' and tell me about it. "
        "5. Go back and then click on 'abfd' and tell me about it."
    )

    


    allowed_domains = [
        ["https://us.cwcloudpartner.com/das-develop-aqa/e/eng/bp_-b5BDTgOsAmkIzK-f2w/*"]
    ]

    browser_session = BrowserSession(
        
    )
    email: str = os.getenv("DAS_EMAIL", "")
    password: str = os.getenv("DAS_PASSWORD", "")
    agent = Agent(
        task=task, 
        llm=ChatAzureOpenAI(
            model="gpt-4o", 
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_API_ENDPOINT"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            temperature=1.0
            ),
        browser_session=browser_session,
        sensitive_data={
            '*.cwcloudpartner.com': {
                'x_member_number': email,
                'x_passphrase': password,  # 'x_placeholder': '<actual secret value>',
            },
        },
    )
    await agent.run()


if __name__ == "__main__":
    asyncio.run(main())