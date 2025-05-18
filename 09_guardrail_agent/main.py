from agents import Agent,Runner,RunConfig
from input_guard import polytics_guardrail
from output_guard import output_guardrail_poly
from setup_config import gemini_config
import chainlit as cl
from typing import cast

@cl.on_chat_start
async def start():
    cl.user_session.set('config',gemini_config)
    cl.user_session.set('chat_history',[])

    agent = Agent(
        name = 'customer support agent',
        instructions = 'You are a customer support agent.You help customers with their questions.',
        input_guardrails = [polytics_guardrail],
        output_guardrails = [output_guardrail_poly]
    )

    cl.user_session.set('agent',agent)

    await cl.Message(content = 'Welcome to Dani AI Assistant! How can i help u today?').send()

@cl.on_message
async def main(message:cl.Message):
    """process incoming messages and generate responses."""

    msg = cl.Message(content='Thinking...')
    await msg.send()

    agent:Agent = cast(Agent,cl.user_session.get('agent'))
    config:RunConfig = cast(RunConfig,cl.user_session.get('config'))

    history = cl.user_session.get('chat_history') or []

    history.append({'role':'user','content':message.content})

    try:
        print('\n[CALLING_AGENT_WITH_CONTEXT]\n',history,'\n')
        result = Runner.run_sync(
            starting_agent = agent,
            input = history,
            run_config = config
        )

        print(f'Raw Result:{result}')

        response_content = result.final_output

        msg.content = response_content
        await msg.update()

        cl.user_session.set('chat_history',result.to_input_list())
        print(f"User: {message.content}")
        print(f"Assistant: {response_content}")

    except Exception as e:
        msg.content = f"Error: {str(e)}"
        await msg.update()
        print(f"Error: {str(e)}")