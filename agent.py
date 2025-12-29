
from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions, ChatContext
from livekit.plugins import (
    noise_cancellation,
)
from livekit.plugins import google
from prompts import instructions_prompt, Reply_prompts
from tools import get_weather, search_web #set_brightness
#from orb_controller import start_orb, stop_orb
from mem0 import AsyncMemoryClient
import json
import logging
import os


load_dotenv()


class Assistant(Agent):
    def __init__(self, chat_ctx=None) -> None:
        super().__init__(
            instructions=instructions_prompt,
            llm=google.beta.realtime.RealtimeModel(
                model="gemini-2.5-flash-native-audio-preview-09-2025",
                voice="Leda",
                temperature=0.8,
            ),
            tools=[
                get_weather,
                search_web,
                #set_brightness,
            ],
            chat_ctx=chat_ctx
        )


async def entrypoint(ctx: agents.JobContext):

    async def shutdown_hook(chat_ctx: ChatContext, mem0: AsyncMemoryClient, memory_str: str):
        logging.info("shutting down, saving chat context to memory...")

        messages_formatted = []

        logging.info(f"Chat context messages: {chat_ctx.items}")

        for item in chat_ctx.items:
            content_str = ''.join(item.content) if isinstance(item.content, list) else str(item.content)

            if memory_str and memory_str in content_str:
                continue

            if item.role in ['user', 'assistant']:
                messages_formatted.append({
                    "role": item.role,
                    "content": content_str.strip()
                })

        logging.info(f"Formatted messages to add to memory: {messages_formatted}")
        await mem0.add(messages_formatted, user_id="Ausaaf")
        logging.info("chat context saved to memory.")

    session = AgentSession()

    mem0 = AsyncMemoryClient()
    user_name = 'Ausaaf'

    results = await mem0.get_all(user_id=user_name)
    initial_ctx = ChatContext()
    memory_str = ''

    if results:
        memories = [
            {
                "memory": result["memory"],
                "updated_at": result["updated_at"]
            }
            for result in results
        ]
        memory_str = json.dumps(memories)
        logging.info(f"Memories: {memory_str}")
        initial_ctx.add_message(
            role="assistant",
            content=f"the user's name is {user_name}, and this is relevant context about him: {memory_str}."
        )

    # 🔵 START ORB WHEN SESSION STARTS
    #start_orb()

    await session.start(
        room=ctx.room,
        agent=Assistant(chat_ctx=initial_ctx),
        room_input_options=RoomInputOptions(
            video_enabled=True,
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    await ctx.connect()

    await session.generate_reply(
        instructions=Reply_prompts
    )

    # 🔴 STOP ORB WHEN SESSION ENDS
    ctx.add_shutdown_callback(
        lambda: (
            #stop_orb(),
            shutdown_hook(session._agent.chat_ctx, mem0, memory_str)
        )
    )


if __name__ == "__main__":
    agents.cli.run_app(
        agents.WorkerOptions(entrypoint_fnc=entrypoint)
    )
