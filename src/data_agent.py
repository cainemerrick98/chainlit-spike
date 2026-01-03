from models.semantic import SemanticModel
from tools import ToolRegistration
from openai import Client
from prompts import DATA_AGENT_PROMPT



class DataAgent():
    def __init__(self, llm_client: Client):
        self.llm = llm_client
        self.semantic_model = None
        self.tools = []


    def register_semantics(self, semantic: SemanticModel):
        self.semantic_model = semantic
    
    def register_tools(self, tool: ToolRegistration | list[ToolRegistration]):
        if isinstance(tool, list):
            self.tools += tool
        else:
            self.tools.append(tool)
    
    def create_response(self, messages:list):
        return self.llm.responses.create(
            model="gpt-4.1",
            instructions=DATA_AGENT_PROMPT.format(semantic_model=self.semantic_model.model_dump_json()),
            input=messages,
            tools=self.tools,
            tool_choice="auto"
            
        )


