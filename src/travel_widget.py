"""
Travel Planning Widget for Streamlit App.
Provides a specialized interface for travel planning with the travel agents.
"""

import json
from datetime import datetime, timedelta
from typing import Any, Dict, List

import streamlit as st

from client.client import AgentClient


class TravelWidget:
    """Travel planning widget for Streamlit."""
    
    def __init__(self):
        self.client = AgentClient()
        self.planning_agent_id = "travel-planning-agent"
        self.booking_agent_id = "travel-booking-agent"
    
    def render_travel_planning_form(self) -> Dict[str, Any]:
        """Render the travel planning form."""
        st.markdown("## 🌍 Travel Planning Assistant")
        st.markdown("Plan your perfect trip with our AI-powered travel assistant!")
        
        # Create two columns for better layout
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Destination input
            destination = st.text_input(
                "🏛️ Destination",
                placeholder="e.g., Paris, Tokyo, Bali, New York",
                help="Enter the city, country, or region you want to visit"
            )
            
            # Travel dates
            col_date1, col_date2 = st.columns(2)
            with col_date1:
                start_date = st.date_input(
                    "📅 Start Date",
                    value=datetime.now() + timedelta(days=30),
                    min_value=datetime.now().date(),
                    help="When do you want to start your trip?"
                )
            
            with col_date2:
                duration = st.number_input(
                    "⏱️ Duration (days)",
                    min_value=1,
                    max_value=90,
                    value=7,
                    help="How many days will your trip be?"
                )
            
            # Travel party
            col_adults, col_children = st.columns(2)
            with col_adults:
                adults = st.number_input(
                    "👥 Adults",
                    min_value=1,
                    max_value=10,
                    value=2,
                    help="Number of adult travelers"
                )
            
            with col_children:
                children = st.number_input(
                    "👶 Children",
                    min_value=0,
                    max_value=10,
                    value=0,
                    help="Number of children"
                )
            
            # Child ages (if children > 0)
            child_ages = []
            if children > 0:
                st.markdown("**Child Ages:**")
                for i in range(children):
                    age = st.number_input(
                        f"Child {i+1} age",
                        min_value=0,
                        max_value=17,
                        value=5,
                        key=f"child_age_{i}"
                    )
                    child_ages.append(age)
        
        with col2:
            # Travel preferences
            st.markdown("### 🎯 Travel Preferences")
            
            # Budget range
            budget = st.selectbox(
                "💰 Budget Range",
                ["Budget", "Mid-range", "Luxury", "Any"],
                help="Select your preferred budget range"
            )
            
            # Travel type
            travel_type = st.multiselect(
                "🎨 Travel Type",
                ["Cultural", "Adventure", "Relaxation", "Business", "Family", "Romantic", "Solo"],
                default=["Cultural"],
                help="What type of travel experience are you looking for?"
            )
            
            # Hotel preferences
            hotel_star = st.selectbox(
                "⭐ Hotel Rating",
                [3, 4, 5],
                index=1,  # Default to 4 stars
                help="Preferred hotel star rating"
            )
            
            # Starting airport
            start_airport = st.text_input(
                "✈️ Starting Airport",
                value="BOM",
                placeholder="e.g., BOM, DEL, BLR",
                help="IATA code of your starting airport"
            )
        
        # Additional preferences
        with st.expander("🔧 Additional Preferences"):
            col_pref1, col_pref2 = st.columns(2)
            
            with col_pref1:
                # Season preference
                season = st.selectbox(
                    "🌤️ Preferred Season",
                    ["Any", "Spring", "Summer", "Autumn", "Winter"],
                    help="When do you prefer to travel?"
                )
                
                # Activity level
                activity_level = st.selectbox(
                    "🏃 Activity Level",
                    ["Relaxed", "Moderate", "Active", "Adventure"],
                    help="How active do you want your trip to be?"
                )
            
            with col_pref2:
                # Group size preference
                group_size = st.selectbox(
                    "👥 Group Size Preference",
                    ["Small (2-4)", "Medium (5-8)", "Large (9+)", "Any"],
                    help="Preferred group size for activities"
                )
                
                # Special requirements
                special_reqs = st.text_area(
                    "♿ Special Requirements",
                    placeholder="e.g., wheelchair accessible, dietary restrictions, etc.",
                    help="Any special requirements or preferences"
                )
        
        # Create the travel request
        travel_request = {
            "destination": destination,
            "start_date": start_date.strftime("%d/%m/%Y"),
            "duration_days": duration,
            "adults": adults,
            "children": children,
            "child_ages": child_ages,
            "budget_range": budget,
            "travel_type": travel_type,
            "hotel_star": hotel_star,
            "start_airport": start_airport,
            "season": season,
            "activity_level": activity_level,
            "group_size": group_size,
            "special_requirements": special_reqs
        }
        
        return travel_request
    
    def format_travel_request(self, travel_request: Dict[str, Any]) -> str:
        """Format the travel request into a natural language prompt."""
        prompt_parts = [
            f"I want to plan a trip to {travel_request['destination']}",
            f"starting on {travel_request['start_date']}",
            f"for {travel_request['duration_days']} days",
            f"with {travel_request['adults']} adults"
        ]
        
        if travel_request['children'] > 0:
            prompt_parts.append(f"and {travel_request['children']} children (ages: {travel_request['child_ages']})")
        
        prompt_parts.extend([
            f"Budget: {travel_request['budget_range']}",
            f"Travel type: {', '.join(travel_request['travel_type'])}",
            f"Hotel rating: {travel_request['hotel_star']} stars",
            f"Starting from: {travel_request['start_airport']} airport"
        ])
        
        if travel_request['season'] != "Any":
            prompt_parts.append(f"Preferred season: {travel_request['season']}")
        
        if travel_request['activity_level']:
            prompt_parts.append(f"Activity level: {travel_request['activity_level']}")
        
        if travel_request['special_requirements']:
            prompt_parts.append(f"Special requirements: {travel_request['special_requirements']}")
        
        return "Please help me plan this trip: " + ", ".join(prompt_parts) + ". Provide a comprehensive travel recommendation with destination information, available packages, airport details, and next steps for booking."
    
    def format_booking_request(self, travel_request: Dict[str, Any]) -> str:
        """Format the travel request into a booking prompt."""
        prompt_parts = [
            f"I want to book a travel package to {travel_request['destination']}",
            f"starting on {travel_request['start_date']}",
            f"for {travel_request['duration_days']} days",
            f"with {travel_request['adults']} adults"
        ]
        
        if travel_request['children'] > 0:
            prompt_parts.append(f"and {travel_request['children']} children (ages: {travel_request['child_ages']})")
        
        prompt_parts.extend([
            f"Hotel rating: {travel_request['hotel_star']} stars",
            f"Starting from: {travel_request['start_airport']} airport"
        ])
        
        return "Please help me book this travel package: " + ", ".join(prompt_parts) + ". Search for available packages and process the booking with confirmation details."
    
    def display_booking_response(self, response: str):
        """Display the booking response in a formatted way."""
        st.markdown("## 📋 Booking Response")
        
        # Display the response (which should be markdown formatted)
        st.markdown(response)
        
        # Add action buttons
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📞 Contact Booking Support", type="primary"):
                st.info("Contact our booking support at: booking@travelrag.com")
        
        with col2:
            if st.button("💾 Save Booking Details"):
                st.success("Booking details saved to your travel history!")
        
        with col3:
            if st.button("🔄 Make Another Booking"):
                st.rerun()
    
    def display_travel_recommendation(self, response: str):
        """Display the travel recommendation in a formatted way."""
        st.markdown("## ✨ Your Travel Recommendation")
        
        # Display the response (which should be markdown formatted)
        st.markdown(response)
        
        # Add action buttons
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📞 Contact Travel Expert", type="primary"):
                st.info("Contact our travel experts at: travel@investmentadvisory.com")
        
        with col2:
            if st.button("💾 Save Recommendation"):
                st.success("Recommendation saved to your travel history!")
        
        with col3:
            if st.button("🔄 Plan Another Trip"):
                st.rerun()
    
    def run_travel_planning(self):
        """Run the complete travel planning workflow."""
        # Render the form
        travel_request = self.render_travel_planning_form()
        
        # Submit buttons
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🚀 Plan My Trip", type="primary", use_container_width=True):
                if not travel_request['destination']:
                    st.error("Please enter a destination to continue.")
                    return
                
                # Format the request
                prompt = self.format_travel_request(travel_request)
                
                # Show progress
                with st.spinner("🤖 Planning your perfect trip..."):
                    try:
                        # Call the travel planning agent
                        response = self.client.invoke(
                            agent_id=self.planning_agent_id,
                            message=prompt
                        )
                        
                        # Display the recommendation
                        self.display_travel_recommendation(response)
                        
                    except Exception as e:
                        st.error(f"Error planning your trip: {str(e)}")
                        st.info("Please try again or contact our support team.")
        
        with col2:
            if st.button("📋 Book Package", type="secondary", use_container_width=True):
                if not travel_request['destination']:
                    st.error("Please enter a destination to continue.")
                    return
                
                # Format the booking request
                booking_prompt = self.format_booking_request(travel_request)
                
                # Show progress
                with st.spinner("📋 Processing your booking..."):
                    try:
                        # Call the travel booking agent
                        response = self.client.invoke(
                            agent_id=self.booking_agent_id,
                            message=booking_prompt
                        )
                        
                        # Display the booking response
                        self.display_booking_response(response)
                        
                    except Exception as e:
                        st.error(f"Error processing your booking: {str(e)}")
                        st.info("Please try again or contact our support team.")


def main():
    """Main function for the travel widget."""
    st.set_page_config(
        page_title="Travel Planning Assistant",
        page_icon="🌍",
        layout="wide"
    )
    
    # Initialize the travel widget
    travel_widget = TravelWidget()
    
    # Run the travel planning interface
    travel_widget.run_travel_planning()


if __name__ == "__main__":
    main()
