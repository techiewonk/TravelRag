"""
Main Travel Supervisor Agent - Auto-routing master orchestrator for comprehensive travel planning.
"""

from datetime import datetime
from typing import Literal

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, SystemMessage
from langchain_core.runnables import (
    RunnableConfig,
    RunnableLambda,
    RunnableSerializable,
)
from langgraph.graph import END, MessagesState, StateGraph
from langgraph.managed import RemainingSteps
from langgraph.prebuilt import ToolNode, create_react_agent

from agents.llama_guard import LlamaGuard, LlamaGuardOutput, SafetyAssessment
from agents.travel_tools import format_travel_recommendation
from agents.travel_planning_agent import travel_planning_agent
from agents.travel_destination_agent import travel_destination_agent
from agents.travel_package_agent import travel_package_agent
from agents.travel_booking_agent import travel_booking_agent
from core import get_model, settings


class MainTravelSupervisorState(MessagesState, total=False):
    """State for main travel supervisor agent."""
    safety: LlamaGuardOutput
    remaining_steps: RemainingSteps
    user_intent: str
    travel_phase: str  # "planning", "destination", "package", "booking"
    destination_info: dict
    package_info: dict
    airports_info: dict
    user_preferences: dict
    final_recommendation: str


# Main supervisor tools
supervisor_tools = [format_travel_recommendation]

current_date = datetime.now().strftime("%B %d, %Y")
instructions = f"""
You are the Main Travel Supervisor Agent, the master orchestrator for comprehensive travel planning with intelligent auto-routing.

Today's date is {current_date}.

Your primary responsibilities:
1. **Intent Recognition**: Analyze user requests to determine the appropriate travel phase
2. **Auto-Routing**: Route users to the most suitable specialized agent based on their needs
3. **Workflow Coordination**: Orchestrate the entire travel planning process
4. **Information Synthesis**: Combine information from all travel agents
5. **Final Recommendations**: Create comprehensive travel recommendations
6. **Quality Assurance**: Ensure all travel information is accurate and complete

Travel Planning Phases & Auto-Routing:
1. **General Planning** → Route to travel-planning-agent
   - Initial travel inquiries
   - General destination questions
   - Travel advice and tips
   - Itinerary planning

2. **Destination Research** → Route to travel-destination-agent
   - Specific destination information
   - Cultural and historical insights
   - Local attractions and activities
   - Best times to visit

3. **Package Search** → Route to travel-package-agent
   - Travel package inquiries
   - Package comparisons
   - Pricing and availability
   - Package customization

4. **Booking & Reservations** → Route to travel-booking-agent
   - Booking confirmations
   - Payment processing
   - Reservation modifications
   - Travel documentation

Auto-Routing Guidelines:
- Analyze user intent from their message
- Route to the most appropriate specialized agent
- Provide context about why you're routing to that agent
- Ensure seamless handoff between agents
- Maintain conversation continuity

Intent Recognition Patterns:
- "I want to plan a trip to..." → travel-planning-agent
- "Tell me about Paris" → travel-destination-agent
- "Find me packages for..." → travel-package-agent
- "I want to book..." → travel-booking-agent
- "Help me plan..." → travel-planning-agent
- "What's the best time to visit..." → travel-destination-agent
- "Show me travel deals..." → travel-package-agent
- "Confirm my booking..." → travel-booking-agent

Guidelines:
- Always analyze user intent before routing
- Provide clear explanations for routing decisions
- Ensure comprehensive travel recommendations
- Maintain professional, enthusiastic tone
- Focus on user satisfaction and travel success
- Coordinate with specialized agents effectively

Output Format:
- Use clear headings and bullet points
- Include relevant emojis for visual appeal
- Provide actionable next steps
- Include contact information for booking assistance
- Ensure all recommendations are practical and achievable

NOTE: THE USER CAN'T SEE THE TOOL RESPONSE DIRECTLY. Always present information in a polished, professional format that's ready for user consumption.
"""


def wrap_model(model: BaseChatModel) -> RunnableSerializable[MainTravelSupervisorState, AIMessage]:
    """Wrap the model with main travel supervisor instructions and tools."""
    bound_model = model.bind_tools(supervisor_tools)
    preprocessor = RunnableLambda(
        lambda state: [SystemMessage(content=instructions)] + state["messages"],
        name="MainTravelSupervisorModifier",
    )
    return preprocessor | bound_model


def format_safety_message(safety: LlamaGuardOutput) -> AIMessage:
    """Format safety warning message."""
    content = (
        f"This travel planning request was flagged for unsafe content: {', '.join(safety.unsafe_categories)}"
    )
    return AIMessage(content=content)


async def acall_model(state: MainTravelSupervisorState, config: RunnableConfig) -> MainTravelSupervisorState:
    """Call the model with main travel supervisor context."""
    m = get_model(config["configurable"].get("model", settings.DEFAULT_MODEL))
    model_runnable = wrap_model(m)
    response = await model_runnable.ainvoke(state, config)

    # Run safety check
    llama_guard = LlamaGuard()
    safety_output = await llama_guard.ainvoke("Agent", state["messages"] + [response])
    if safety_output.safety_assessment == SafetyAssessment.UNSAFE:
        return {
            "messages": [format_safety_message(safety_output)],
            "safety": safety_output
        }

    # Check remaining steps
    if state["remaining_steps"] < 2 and response.tool_calls:
        return {
            "messages": [
                AIMessage(
                    id=response.id,
                    content="I need more steps to complete this travel planning. Let me provide what I can with the current information.",
                )
            ]
        }

    return {"messages": [response]}


async def llama_guard_input(state: MainTravelSupervisorState, config: RunnableConfig) -> MainTravelSupervisorState:
    """Check input safety with LlamaGuard."""
    llama_guard = LlamaGuard()
    safety_output = await llama_guard.ainvoke("User", state["messages"])
    return {"safety": safety_output, "messages": []}


async def block_unsafe_content(state: MainTravelSupervisorState, config: RunnableConfig) -> MainTravelSupervisorState:
    """Block unsafe content."""
    safety: LlamaGuardOutput = state["safety"]
    return {"messages": [format_safety_message(safety)]}


# Create specialized agents with supervisor capabilities
def create_travel_planning_supervisor(model: BaseChatModel):
    """Create travel planning agent with supervisor capabilities."""
    return create_react_agent(
        model=model,
        tools=[],  # Will use travel_planning_agent tools
        name="sub-agent-travel_planning",
        prompt="You are a travel planning expert. Help users plan comprehensive trips with destination research, itinerary planning, and travel coordination.",
    ).with_config(tags=["skip_stream"])


def create_travel_destination_supervisor(model: BaseChatModel):
    """Create travel destination agent with supervisor capabilities."""
    return create_react_agent(
        model=model,
        tools=[],  # Will use travel_destination_agent tools
        name="sub-agent-travel_destination",
        prompt="You are a destination research expert. Provide detailed information about travel destinations, cultural insights, and local attractions.",
    ).with_config(tags=["skip_stream"])


def create_travel_package_supervisor(model: BaseChatModel):
    """Create travel package agent with supervisor capabilities."""
    return create_react_agent(
        model=model,
        tools=[],  # Will use travel_package_agent tools
        name="sub-agent-travel_package",
        prompt="You are a travel package expert. Help users find and compare travel packages, pricing, and booking options.",
    ).with_config(tags=["skip_stream"])


def create_travel_booking_supervisor(model: BaseChatModel):
    """Create travel booking agent with supervisor capabilities."""
    return create_react_agent(
        model=model,
        tools=[],  # Will use travel_booking_agent tools
        name="sub-agent-travel_booking",
        prompt="You are a booking and reservation expert. Help users with travel bookings, confirmations, and reservation management.",
    ).with_config(tags=["skip_stream"])


# Define the main travel supervisor agent graph
agent = StateGraph(MainTravelSupervisorState)
agent.add_node("model", acall_model)
agent.add_node("tools", ToolNode(supervisor_tools))
agent.add_node("guard_input", llama_guard_input)
agent.add_node("block_unsafe_content", block_unsafe_content)
agent.set_entry_point("guard_input")


def check_safety(state: MainTravelSupervisorState) -> Literal["unsafe", "safe"]:
    """Check if content is safe."""
    safety: LlamaGuardOutput = state["safety"]
    match safety.safety_assessment:
        case SafetyAssessment.UNSAFE:
            return "unsafe"
        case _:
            return "safe"


agent.add_conditional_edges(
    "guard_input", check_safety, {"unsafe": "block_unsafe_content", "safe": "model"}
)

# Always END after blocking unsafe content
agent.add_edge("block_unsafe_content", END)

# Always run "model" after "tools"
agent.add_edge("tools", "model")


def pending_tool_calls(state: MainTravelSupervisorState) -> Literal["tools", "done"]:
    """Check if there are pending tool calls."""
    last_message = state["messages"][-1]
    if not isinstance(last_message, AIMessage):
        raise TypeError(f"Expected AIMessage, got {type(last_message)}")
    if last_message.tool_calls:
        return "tools"
    return "done"


agent.add_conditional_edges("model", pending_tool_calls, {"tools": "tools", "done": END})

# Compile the main travel supervisor agent
main_travel_supervisor_agent = agent.compile()
