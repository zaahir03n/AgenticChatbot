from src.langgraphagenticai.state.state import State

class ChatBotWithToolNode:
    """
    ChatBot logic enhanced with tool integration
    """

    def __init__(self,model):
        self.llm = model

    #just simulating tool (we dont need this actually since we will be using next function)
    def process(self,state:State)->dict:
        """
        Process the input state and generate chat bot response
        """

        user_input = state["messages"][-1] if state["messages"] else ""
        llm_response = self.llm.invoke({"role":"user","content":user_input})
        
        tool_responsse = f"Tool integrtion for : '{user_input}'"

        return {"messages" : [llm_response, tool_responsse]}
    
    def create_chatbot(self, tools):
        """
        Returns a chatbot node function
        """
        llm_with_tools = self.llm.bind_tools(tools)

        def chatbot_nodes(state: State):
            """
            Chatbot logic processing the input state and returning a response
            """
            return {"messages" : [llm_with_tools.invoke(state["messages"])]}
        
        return chatbot_nodes
    