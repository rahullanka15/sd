# streamlit_app.py
import streamlit as st
from utils.ai_processor import AIProcessor
from utils.diagram_generator import DiagramGenerator
import streamlit.components.v1 as components
import json

def setup_page():
    st.set_page_config(
        page_title="System Design Analyzer",
        page_icon="🔄",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    if 'current_analysis' not in st.session_state:
        st.session_state.current_analysis = None

def display_analysis(analysis_data):
    try:
        # Display the system overview
        st.markdown("## System Flow Analysis")
        st.markdown(analysis_data['overview'])
        
                        # Display each component
        for component in analysis_data['components']:
            with st.expander(f"📍 {component['name']}", expanded=True):
                st.markdown(f"**Purpose**: {component['purpose']}")
                
                # Display Steps
                st.markdown("### Implementation Steps")
                for step in component['steps']:
                    st.markdown(f"**Step {step['step']}: {step['action']}**")
                    for detail in step['details']:
                        st.markdown(f"- {detail}")
                
                # Display Technologies
                st.markdown("### Technologies Used")
                for tech in component['technologies']:
                    st.markdown(f"**{tech['name']}**")
                    st.markdown(f"- Purpose: {tech['purpose']}")
                    st.markdown(f"- Configuration: {tech['configuration']}")
                
                # Display Data Flow
                st.markdown("### Data Flow")
                st.markdown(f"1. **Input**: {component['data_flow']['input']}")
                st.markdown(f"2. **Process**: {component['data_flow']['process']}")
                st.markdown(f"3. **Output**: {component['data_flow']['output']}")
        
        # # Display Flow Steps
        # st.markdown("## System Flow")
        # for step in analysis_data['flow_steps']:
        #     st.markdown(f"### Step {step['step']}: {step['title']}")
        #     st.markdown(step['description'])
        #     st.markdown("**Technical Details:**")
        #     for detail in step['technical_details']:
        #         st.markdown(f"- {detail}")
        
        # Display the system flow diagram
        st.markdown("## System Flow Diagram")
        render_mermaid(analysis_data['diagram'])
        
    except Exception as e:
        st.error(f"Error displaying analysis: {str(e)}")

def main():
    setup_page()
    
    st.title("🔄 System Design Analyzer")
    
    with st.container():
        st.markdown("""
        ### Design Your System
        Describe your system requirements in detail. Include:
        - User interaction flow
        - Data processing requirements
        - Storage needs
        - Performance requirements
        - Security considerations
        """)
        
        process_input = st.text_area(
            "Enter your system design requirements",
            height=200,
            placeholder="Example: Design a URL shortening service where a user enters a long URL in a React form. The URL should be processed through API Gateway, validated, and stored in DynamoDB with a unique short identifier generated using SHA-256...",
            help="Be specific about the technical flow and requirements"
        )
    
    # Additional configuration options
    with st.expander("Technical Configuration", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            frontend = st.selectbox(
                "Frontend Framework",
                ["React", "Angular", "Vue.js", "Next.js"],
                index=0
            )
            database = st.selectbox(
                "Database",
                ["DynamoDB", "PostgreSQL", "MongoDB", "Redis"],
                index=0
            )
        with col2:
            cloud_provider = st.selectbox(
                "Cloud Provider",
                ["AWS", "Google Cloud", "Azure"],
                index=0
            )
            cache_strategy = st.selectbox(
                "Caching Strategy",
                ["Redis", "Memcached", "CDN"],
                index=0
            )
    
    if st.button("Generate Design", type="primary"):
        if not process_input.strip():
            st.warning("Please enter system requirements")
            return
            
        try:
            with st.spinner("Analyzing system requirements..."):
                # Initialize processors
                ai_processor = AIProcessor()
                
                # Process the input with technical preferences
                requirements = {
                    "description": process_input,
                    "preferences": {
                        "frontend": frontend,
                        "database": database,
                        "cloud_provider": cloud_provider,
                        "cache_strategy": cache_strategy
                    }
                }
                
                # Get the analysis
                analysis_result = ai_processor.analyze_process(requirements)
                
                # Store in session state
                st.session_state.current_analysis = analysis_result
                
                # Display the analysis
                display_analysis(analysis_result)
                
        except Exception as e:
            st.error(f"Analysis failed: {str(e)}")

# streamlit_app.py (consolidated render_mermaid function)
def render_mermaid(mermaid_code):
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/roughjs@4.5.2/bundled/rough.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js"></script>
        <style>
            .mermaid {{
                padding: 20px;
                background: white;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
        </style>
    </head>
    <body>
        <div class="mermaid">
            {mermaid_code}
        </div>
        <script>
            mermaid.initialize({{
                startOnLoad: true,
                securityLevel: 'loose'
            }});
        </script>
    </body>
    </html>
    """
    return components.html(html, height=800)

if __name__ == "__main__":
    main()