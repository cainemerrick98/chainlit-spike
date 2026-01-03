import chainlit as cl
import pandas as pd
from semantic import SemanticModel
from tools import get_data, display_table



@cl.on_chat_start
async def chat_start():
   ...

@cl.on_message
async def message(message: cl.Message):
    if message.content == 'Table':
        async with cl.Step(name="Get Data", type="Tool Call") as step:
            step.input = "Some filters"
            data = get_data(filters=[('Age', 55, '<')], data=df)
            step.output = data
    
        async with cl.Step(name="Display Table", type="Tool Call") as step:
            step.input = data
            result = display_table(data)
        

        elements = [cl.Dataframe(data=df, display='inline', name='DataFrame')]

        await cl.Message(content="Here's your table", elements=elements).send()

    else:
        await cl.Message(content="What the helly")
    

