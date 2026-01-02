import chainlit as cl
import pandas as pd
from semantic import SemanticModel
from tools import get_data, display_table


data = {
        "Name": [
            "Alice",
            "David",
            "Charlie",
            "Bob",
            "Eva",
            "Grace",
            "Hannah",
            "Jack",
            "Frank",
            "Kara",
            "Liam",
            "Ivy",
            "Mia",
            "Noah",
            "Olivia",
        ],
        "Age": [25, 40, 35, 30, 45, 55, 60, 70, 50, 75, 80, 65, 85, 90, 95],
        "City": [
            "New York",
            "Houston",
            "Chicago",
            "Los Angeles",
            "Phoenix",
            "San Antonio",
            "San Diego",
            "San Jose",
            "Philadelphia",
            "Austin",
            "Fort Worth",
            "Dallas",
            "Jacksonville",
            "Columbus",
            "Charlotte",
        ],
        "Salary": [
            70000,
            100000,
            90000,
            80000,
            110000,
            130000,
            140000,
            160000,
            120000,
            170000,
            180000,
            150000,
            190000,
            200000,
            210000,
        ],
    }

df = pd.DataFrame(data=data)

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
    

