from agents.mcp import MCPServerSse
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel
from dotenv import load_dotenv
import os 
import asyncio

load_dotenv()


async def main():
    async with MCPServerSse(name="playwright", params={
        "url": "http://localhost:8931/sse",
        "transport": "sse"
    }) as server:
        client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # OpenAI key
        model = OpenAIChatCompletionsModel(model="gpt-4o", openai_client=client)
        agent = Agent(name="AI", instructions="You can browse with Playwright", model=model, mcp_servers=[server])
        print((await Runner.run(agent, input="Go to https://www.google.com, find the search field, click on the search field and add text 'hello' and press enter and print the first link and heading")).final_output)

if __name__ == "__main__":
    asyncio.run(main())

