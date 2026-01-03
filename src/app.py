import chainlit as cl
import pandas as pd
import models
from models.semantic import SemanticModel, Table, SemanticColumn, DataTypes, KPI, Filter
from models.query import Measure, Aggregation, Comparison, Query, QueryColumn
from tools import ToolRegistration, make_get_data, register_tool, run_tool
from data_connection import DuckDBDataConnection
from data_agent import DataAgent
from dotenv import load_dotenv
from openai import Client
import os
from pydantic import BaseModel
import json

load_dotenv()

#Sematics
sales_columns = [
    SemanticColumn(
        name="ORDERNUMBER",
        data_type=DataTypes.NUMERIC,
        description="The unique identifier of the order"
    ),
    SemanticColumn(
        name="SALES",
        data_type=DataTypes.NUMERIC,
        description="The revenue associated with an individual order."
    ),
    SemanticColumn(
        name="STATUS",
        data_type=DataTypes.STRING,
        description="The current status of the order. Can be 'Shipped', 'Cancelled', 'Resolved', 'On Hold' or 'In Progress'"
    ),
    SemanticColumn(
        name="CITY",
        data_type=DataTypes.STRING,
        description="The city of the customer"
    )
]
sales_table = Table(
    name="Sales",
    description="The sales table. Each row represents an order",
    columns=sales_columns
)
total_sales_kpi = KPI(
    name="TotalSales",
    expression=Measure(
        kind="measure",
        column=QueryColumn(kind="column", name="SALES"),
        aggregation=Aggregation.SUM
    ),
    description="The sum of the sales column",
    return_type=DataTypes.NUMERIC


)
sales_semantic_model = SemanticModel(
    tables=[sales_table],
    kpis=[total_sales_kpi],
    filters=None,
)

#Data Connections
df = pd.read_csv('./datasets/sales_data.csv')
data_connection = DuckDBDataConnection(tables={'Sales':df})


# Tools
get_data = make_get_data(data_connection, sales_semantic_model)
class GetDataArgs(BaseModel):
    query: Query

tool_registry = [
    ToolRegistration(
        type="function",
        name="get_data",
        description="runs the query you pass against the connected data and returns the result",
        parameters=GetDataArgs.model_json_schema(),
        required=['query']
    )
]
register_tool('get_data')(get_data)

# Data Agent
api_key = os.getenv('OPENAI_KEY')
llm = Client(api_key=api_key)
sales_agent = DataAgent(llm)

sales_agent.register_semantics(sales_semantic_model)
sales_agent.register_tools(tool_registry)

@cl.on_chat_start
async def chat_start():
   response = data_connection.query('SELECT * FROM SALES')
   assert response['row_count'] > 1000

@cl.on_message
async def on_message(message: cl.Message):
    messages = cl.chat_context.to_openai()
    i = 0
    while True:
        messages = cl.chat_context.to_openai()
        response = sales_agent.create_response(messages)

        if response.output[0].type == 'function_call':
            for tool_choice in response.output:
                tool_name = tool_choice.name
                tool_args = tool_choice.arguments
                tool_output = run_tool(tool_name, tool_args)

                async with cl.Step(type="tool", name=tool_name) as step:
                    step.input = str(tool_args)
                    step.output = str(tool_output)
                
                cl.chat_context.add(
                    cl.Message(
                        content=str(tool_output),
                        author=tool_name
                    )
                )

        else:
            await cl.Message(content=response.output_text).send()
            break
