# from agents.mcp import MCPServerSse
# from openai import AsyncOpenAI
# from agents import Agent, Runner, OpenAIChatCompletionsModel
from dotenv import load_dotenv
import os 
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

load_dotenv()


# async def main():
#     async with MCPServerSse(name="playwright", params={
#         "url": "http://localhost:8931/sse",
#         "transport": "sse",
#         "timeout": 300
#     }) as server:
#         client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # OpenAI key
#         model = OpenAIChatCompletionsModel(model="gpt-4o", openai_client=client)
#         agent = Agent(name="AI", instructions="You can browse with Playwright", model=model, mcp_servers=[server])
#         # print((await Runner.run(agent, input="Go to https://www.google.com, find the search field, click on the search field and add text 'hello' and press enter and print the first link and heading")).final_output)
#         print((await Runner.run(agent, input="Go to https://www.einfach-sparsam.de/gewinnspiele, find the competitions, print the Heading and Competition links")).final_output)


llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o")

async def main():
    client = MultiServerMCPClient({
        "browser": {
            "url": "http://localhost:8931/sse",
            "transport": "sse",
        }
    })
    tools = await client.get_tools()
    agent = create_react_agent(model=llm, tools=tools)
    resp = await agent.ainvoke({"messages":[{"role":"user","content":"Click first link on python.org"}]})
    print(resp)

if __name__ == "__main__":
    asyncio.run(main())


