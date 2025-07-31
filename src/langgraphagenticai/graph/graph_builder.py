from langgraph.graph import StateGraph
from  src.langgraphagenticai.state.state import State
from langgraph.graph import START, END
from src.langgraphagenticai.nodes.basic_chatbot_node import BasicChatBotNode
from src.langgraphagenticai.tools.tool_search import get_tools, create_tool_node
from src.langgraphagenticai.nodes.chatbot_with_tool_node import ChatBotWithToolNode
from langgraph.prebuilt import ToolNode,tools_condition
class GraphBuilder:
    def __init__(self, model):
        self.llm = model
        self.graph_builder = StateGraph(State)


    def basic_chatbot_built_graph(self):
        """
        Builds a basic chatbot graph using LangGraph.
        This method initializes a chatbot node using the `BasicChatbotNode` class 
        and integrates it into the graph. The chatbot node is set as both the 
        entry and exit point of the graph.
        """

        self.basic_chatbot_built_graph =BasicChatBotNode(self.llm)

        self.graph_builder.add_node("chatbot",self.basic_chatbot_built_graph.process)
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_edge("chatbot",END)


    def chatbot_with_tools_build_graph(self):
            """
            Builds an advanced chatbot graph with tool integration.
            This method creates a chatbot graph that includes both a chatbot node 
            and a tool node. It defines tools, initializes the chatbot with tool 
            capabilities, and sets up conditional and direct edges between nodes. 
            The chatbot node is set as the entry point.
            """

            # define tool and tool node(to call tool)
            tools = get_tools()
            tool_node = create_tool_node(tools)

            # def llm
            llm = self.llm
            print(22)
            obj_chatbot_with_node =ChatBotWithToolNode(llm)
            chatbot_node = obj_chatbot_with_node.create_chatbot(tools)

            # add nodes
            print(23)
            self.graph_builder.add_node("chatbot",chatbot_node)
            self.graph_builder.add_node("tools",tool_node)
            self.graph_builder.add_edge(START, "chatbot")
            self.graph_builder.add_conditional_edges("chatbot",tools_condition)
            self.graph_builder.add_edge("tools","chatbot")
            self.graph_builder.add_edge("chatbot",END)#its not even required, tools will handle to end this
            print(24)

    def setup_graph(self,usecase:str):
        """
        Sets up the graph for the selected use case
        """
        print(usecase)
        if usecase == "Basic Chatbot":
            self.basic_chatbot_built_graph()
        if usecase == "Chatbot with Web":
            self.chatbot_with_tools_build_graph()
        return self.graph_builder.compile()
