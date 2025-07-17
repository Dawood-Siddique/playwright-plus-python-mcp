from agents.mcp import MCPServerStdio
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel
from dotenv import load_dotenv
import os 
load_dotenv()
import asyncio


async def create_agent(server):
    """Create an agent."""
    client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # OpenAI key
    model = OpenAIChatCompletionsModel(model="gpt-4o", openai_client=client)
    return Agent(name="AI", instructions="You are helpful", model=model, mcp_servers=[server])


async def main():
    """Run the main program."""
    async with MCPServerStdio(name="playwright", params={"command": "playwright-server"}) as server:
        agent = await create_agent(server)
        query = "navigate to https://www.google.com and take a screenshot named 'google.png'"
        out = await Runner.run(agent, input=query)
        print(out.final_output)


if __name__ == "__main__":
    asyncio.run(main())

