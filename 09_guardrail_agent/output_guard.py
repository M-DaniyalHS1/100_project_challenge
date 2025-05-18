from agents import Runner,Agent,GuardrailFunctionOutput,output_guardrail,RunContextWrapper
from pydantic import BaseModel
from setup_config import gemini_config

class MessageOutput(BaseModel):
    response:str

class PolyticsOutput(BaseModel):
    is_polytics_response:bool
    reasoning:str

guardrail_agent2 = Agent(
    name = 'Guardrail check',
    instructions = 'check if the output includes any polytics infor or response.',
    output_type = PolyticsOutput,
)

@output_guardrail
async def output_guardrail_poly(
    ctx:RunContextWrapper,agent:Agent,output:MessageOutput
)->GuardrailFunctionOutput:
    print(f'output: Guardrail trigerred',output)
    result = await Runner.run(guardrail_agent2,output,context=ctx.context,run_config = gemini_config)

    return GuardrailFunctionOutput(
        output_info = result.final_output,
        tripwire_triggered = result.final_output.is_polytics_response,
    )