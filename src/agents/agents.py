from dataclasses import dataclass

from langgraph.graph.state import CompiledStateGraph
from langgraph.pregel import Pregel

from agents.chatbot import chatbot
from agents.knowledge_base_agent import kb_agent
from agents.rag_assistant import rag_assistant
from agents.travel_booking_agent import travel_booking_agent
from agents.travel_destination_agent import travel_destination_agent
from agents.travel_package_agent import travel_package_agent
from agents.travel_planning_agent import travel_planning_agent
from agents.travel_supervisor_agent import travel_supervisor_agent
from schema import AgentInfo

DEFAULT_AGENT = "travel-planning-agent"

# Type alias to handle LangGraph's different agent patterns
# - @entrypoint functions return Pregel
# - StateGraph().compile() returns CompiledStateGraph
AgentGraph = CompiledStateGraph | Pregel  # What get_agent() returns (always loaded)
AgentGraphLike = CompiledStateGraph | Pregel  # What can be stored in registry


@dataclass
class Agent:
    description: str
    graph_like: AgentGraphLike


agents: dict[str, Agent] = {
    "chatbot": Agent(description="A simple chatbot.", graph_like=chatbot),
    "rag-assistant": Agent(
        description="A RAG assistant with access to information in a database.",
        graph_like=rag_assistant,
    ),
    "knowledge-base-agent": Agent(
        description="A retrieval-augmented generation agent using Amazon Bedrock Knowledge Base",
        graph_like=kb_agent,
    ),
    "travel-destination-agent": Agent(
        description="A specialized agent for destination research and travel insights.",
        graph_like=travel_destination_agent,
    ),
    "travel-package-agent": Agent(
        description="A specialized agent for travel package search and booking assistance.",
        graph_like=travel_package_agent,
    ),
    "travel-supervisor-agent": Agent(
        description="A travel supervisor agent that coordinates travel planning workflow.",
        graph_like=travel_supervisor_agent,
    ),
    "travel-planning-agent": Agent(
        description="A comprehensive travel planning agent with end-to-end travel coordination.",
        graph_like=travel_planning_agent,
    ),
    "travel-booking-agent": Agent(
        description="A specialized agent for travel package booking and reservation management.",
        graph_like=travel_booking_agent,
    ),
}


async def load_agent(agent_id: str) -> None:
    """Load agents if needed."""
    # All agents are now loaded directly, no lazy loading needed
    pass


def get_agent(agent_id: str) -> AgentGraph:
    """Get an agent graph."""
    return agents[agent_id].graph_like


def get_all_agent_info() -> list[AgentInfo]:
    return [
        AgentInfo(key=agent_id, description=agent.description) for agent_id, agent in agents.items()
    ]
