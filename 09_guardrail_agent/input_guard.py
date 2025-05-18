from agents import Agent,RunContextWrapper,TResponseInputItem,Runner,GuardrailFunctionOutput,input_guardrail,RunConfig
from setup_config import gemini_config
from pydantic import BaseModel

class PolyticsQuestionOutput(BaseModel):
    is_polytics:bool
    reasoning:str
    answer:str

guardrail_agent = Agent(
    name = 'Guardrail_agent',
    instructions = 'check if the user is asking polytics related questions,any polytics related questions of world and specially pakistan.',
    output_type=PolyticsQuestionOutput,
)

@input_guardrail
async def polytics_guardrail(
    ctx:RunContextWrapper[None],agent:Agent,input:str|list[TResponseInputItem]

)->GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent,input,context=ctx.context,run_config=gemini_config)

    return GuardrailFunctionOutput(
        output_info = result.final_output,
        tripwire_triggered = result.final_output.is_polytics,
    )

