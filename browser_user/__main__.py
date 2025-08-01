import os
import asyncio

from dotenv import load_dotenv

load_dotenv()

from browser_user import Agent, BrowserSession, BrowserProfile
from browser_user.llm.azure.chat import ChatAzureOpenAI


# PYTHONPATH=. python browser_user
async def main():
    # Verify environment variables are loaded
    email = os.getenv("DAS_EMAIL", "")
    password = os.getenv("DAS_PASSWORD", "")
    api_key = os.getenv("AZURE_OPENAI_API_KEY", "")
    endpoint = os.getenv("AZURE_OPENAI_API_ENDPOINT", "")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "")
    
    # Check if required environment variables are set
    if not all([email, password, api_key, endpoint, api_version]):
        missing = []
        if not email: missing.append("DAS_EMAIL")
        if not password: missing.append("DAS_PASSWORD") 
        if not api_key: missing.append("AZURE_OPENAI_API_KEY")
        if not endpoint: missing.append("AZURE_OPENAI_API_ENDPOINT")
        if not api_version: missing.append("AZURE_OPENAI_API_VERSION")
        print(f"❌ Missing required environment variables: {', '.join(missing)}")
        print("Please check your .env file")
        return
    
    print(f"✅ Environment variables loaded:")
    print(f"   - Email: {email[:5]}***@{email.split('@')[1] if '@' in email else 'missing'}")
    print(f"   - Password: {'*' * len(password) if password else 'missing'}")
    print(f"   - Azure endpoint: {endpoint}")

    task = (
        "1. Login to the site: https://us.cwcloudpartner.com/das-develop-aqa/e/eng/bp_-b5BDTgOsAmkIzK-f2w/index.jsp#/documents. "
        "2. Wait for the page to fully load and locate the login form. "
        "3. Use the credentials provided in sensitive_data to fill in the login form fields. "
        "4. Submit the login form and wait for successful authentication. "
        "5. Once logged in, click the three dots menu in the top left corner. "
        "6. Look for and click 'unhide items' or 'View more actions' then 'unhide items'. "
        "7. After unhiding items, locate and click on 'IC-1'. "
        "8. Extract and summarize information about 'IC-1'. "
        "9. Navigate back to the main view. "
        "10. Locate and click on 'abfd'. "
        "11. Extract and summarize information about 'abfd'. "
        "12. Provide a summary of both items found."
    )

    allowed_domains = [
        "*.cwcloudpartner.com"
    ]

    # Create browser profile with allowed domains and slower navigation
    browser_profile = BrowserProfile(
        allowed_domains=allowed_domains
    )
    
    browser_session = BrowserSession(
        browser_profile=browser_profile
    )
    
    agent = Agent(
        task=task, 
        llm=ChatAzureOpenAI(
            model="gpt-4o", 
            api_key=api_key,
            azure_endpoint=endpoint,
            api_version=api_version,
            temperature=0.3  # Lower temperature for more focused behavior
            ),
        browser_session=browser_session,
        sensitive_data={
            '*.cwcloudpartner.com': {
                'x_member_number': email,
                'x_passphrase': password,
                'email': email,  # Also provide as 'email' in case form uses this field name
                'password': password,  # Also provide as 'password' in case form uses this field name
            },
        },
    )
    await agent.run()


if __name__ == "__main__":
    asyncio.run(main())