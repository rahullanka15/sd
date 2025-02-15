# # utils/ai_processor.py
# import groq
# import streamlit as st
# import json
# import re

# class AIProcessor:
#     def __init__(self):
#         self.client = groq.Client(api_key=st.secrets["GROQ_API_KEY"])
    
#     def analyze_process(self, requirements):
#         prompt = self._generate_prompt(requirements)
        
#         try:
#             completion = self.client.chat.completions.create(
#                 messages=[{"role": "user", "content": prompt}],
#                 model="mixtral-8x7b-32768",
#                 temperature=0.1,
#                 max_tokens=4000,
#             )
            
#             response_text = completion.choices[0].message.content
#             return self._parse_response(response_text)
            
#         except Exception as e:
#             raise Exception(f"Analysis error: {str(e)}")
    
#     def _generate_prompt(self, requirements):
#         return f"""Analyze this system design requirement and provide a detailed technical implementation flow. Format the response as a structured JSON document.

# System Requirements:
# {requirements['description']}

# Technical Preferences:
# - Frontend: {requirements['preferences']['frontend']}
# - Database: {requirements['preferences']['database']}
# - Cloud Provider: {requirements['preferences']['cloud_provider']}
# - Cache Strategy: {requirements['preferences']['cache_strategy']}

# Return the response in this exact JSON structure:

# {{
#     "overview": "Brief overview of the entire system",
#     "components": [
#         {{
#             "name": "Component name",
#             "purpose": "Specific purpose",
#             "steps": [
#                 {{
#                     "step": "1",
#                     "action": "What happens in this step",
#                     "details": [
#                         "Detailed point 1",
#                         "Detailed point 2"
#                     ]
#                 }}
#             ],
#             "technologies": [
#                 {{
#                     "name": "Technology name",
#                     "purpose": "Why this technology is used",
#                     "configuration": "Specific configuration details"
#                 }}
#             ],
#             "data_flow": {{
#                 "input": "What comes in",
#                 "process": "What happens to it",
#                 "output": "What goes out"
#             }}
#         }}
#     ],
#     "flow_steps": [
#         {{
#             "step": "1",
#             "title": "Step title",
#             "description": "What happens in this step",
#             "technical_details": [
#                 "Technical detail 1",
#                 "Technical detail 2"
#             ]
#         }}
#     ],
#     "diagram": "mermaid flowchart code"
# }}

# Make sure to:
# 1. Show exact step-by-step flow of data
# 2. Include specific technology choices
# 3. Show how components interact
# 4. Include validation and error handling steps
# 5. Show data storage and caching details
# 6. Include security measures

# The mermaid diagram should show the complete system flow with all components."""

#     def _parse_response(self, response_text):
#         # Extract JSON from the response
#         json_match = re.search(r'\{[\s\S]*\}', response_text)
#         if not json_match:
#             raise ValueError("Could not extract JSON from response")
            
#         try:
#             return json.loads(json_match.group())
#         except json.JSONDecodeError as e:
#             raise ValueError(f"Invalid JSON format: {str(e)}")



# utils/ai_processor.py
import groq
import streamlit as st
import json
import re

class AIProcessor:
    def __init__(self):
        self.client = groq.Client(api_key=st.secrets["GROQ_API_KEY"])
    
    def analyze_process(self, requirements):
        prompt = self._generate_prompt(requirements)
        
        try:
            completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama-3.3-70b-versatile",
                temperature=0.1,
                max_tokens=4000,
            )
            
            response_text = completion.choices[0].message.content
            return self._parse_response(response_text)
            
        except Exception as e:
            raise Exception(f"Analysis error: {str(e)}")
    
    def _generate_prompt(self, requirements):
        return f"""Analyze this system design requirement and provide a detailed technical implementation flow. Format the response as a structured JSON document.

System Requirements:
{requirements['description']}

Return the response in this exact JSON structure:

{{
    "overview": "Brief overview of the entire system",
    "components": [
        {{
            "name": "Component name (Always Start from user and if applicable/possible End at the user like user entering something [frontend] then continue the process of what happens next [continuing frontend] like that map back to user at the end if possible/applicable, LINK EACH COMPONENT TWO WAYS - connect one to PREVIOUS COMPONENT and another to the NEXT COMPONENT.])",
            "purpose": "Specific purpose",
            "steps": [
                {{
                    "step": "1",
                    "action": "What happens in this step",
                    "details": [
                        "Detailed point 1 (Along with that provide latest real life example/algorithm name/syntax like how its done whenever possible)",
                        "Detailed point 2 (Along with that provide latest real life example/algorithm name/syntax like how its done whenever possible)"
                    ]
                }}
            ],
            "technologies": [
                {{
                    "name": "Technology name",
                    "purpose": "Why this technology is used",
                    "configuration": "Specific configuration details"
                }}
            ],
            "data_flow": {{
                "input": "What comes in",
                "process": "What happens to it",
                "output": "What goes out"
            }}
        }}
    ],
    "flow_steps": [
        {{
            "step": "1",
            "title": "Step title",
            "description": "What happens in this step",
            "technical_details": [
                "Technical detail 1",
                "Technical detail 2"
            ]
        }}
    ],
    "diagram": "mermaid flowchart code that shows the DETAILED IMPLEMENTATION STEPS"
}}

Make sure to:
1. Show exact step-by-step flow of data
2. Include specific technology choices
3. Show how components interact
4. Include validation and error handling steps
5. Show data storage and caching details
6. Include security measures

For the diagram field, create a detailed mermaid flowchart that shows EVERY step in the implementation process. The diagram should:
1. Start with the initial user action
2. Show EVERY step in the implementation process with with real-life examples/softwares/tools in minute detail to understand how a single process is done once covering all the success and fails, including:
   - Input validation steps
   - Data transformation steps
   - Processing logic
   - Error handling paths
   - Decision points and branches
   - Database operations
   - Cache operations
   - Response handling
3. Use proper mermaid syntax with conditions and branches like this:

graph TD
    Start[User Submits Form] --> Validate[Validate Input]
    Validate -->|Valid| Process[Process Data]
    Validate -->|Invalid| Error[Show Error]
    Process --> Transform[Transform Data]
    Transform --> Cache[Check Cache]
    Cache -->|Cache Hit| SendCached[Send Cached Response]
    Cache -->|Cache Miss| DB[Query Database]
    DB --> UpdateCache[Update Cache]
    UpdateCache --> Response[Send Response]

The above is just the REFERENCE for syntax generate the mermaid.js code correctly to show the COMPLETE system flow with ALL Implementation Steps."""

    def _parse_response(self, response_text):
        """
        Parse the AI response and extract valid JSON.
        Includes error handling and JSON cleanup.
        """
        try:
            # Try to find JSON content
            json_pattern = r'\{[\s\S]*\}'
            matches = re.finditer(json_pattern, response_text)
            
            # Try each JSON match until we find a valid one
            for match in matches:
                try:
                    json_str = match.group()
                    
                    # Clean up common JSON issues
                    json_str = re.sub(r'```json\s*', '', json_str)
                    json_str = re.sub(r'```\s*', '', json_str)
                    json_str = re.sub(r'---\s*config:[\s\S]*?---', '', json_str)
                    
                    # Fix formatting issues
                    json_str = json_str.replace('\n', ' ')
                    json_str = re.sub(r',\s*}', '}', json_str)
                    json_str = re.sub(r',\s*]', ']', json_str)
                    
                    # Parse the cleaned JSON
                    data = json.loads(json_str)
                    
                    # Validate required fields
                    if 'overview' in data and 'components' in data:
                        # Clean up the diagram field if it exists
                        if 'diagram' in data:
                            data['diagram'] = data['diagram'].strip()
                                                        # Add Mermaid config if not present
                            if not data['diagram'].startswith('%%{init:'):
                                data['diagram'] = '''%%{init: {
                                    'theme':'default',
                                    'flowchart': {
                                        'htmlLabels': true,
                                        'curve': 'basis',
                                        'useMaxWidth': true,
                                        'useMaxHeight': true,
                                        'scrollY': true
                                    }
                                }}%%\n''' + data['diagram']
                            if not data['diagram'].startswith('graph TD'):
                                data['diagram'] = 'graph TD\n' + data['diagram']
                        return data
                    
                except json.JSONDecodeError:
                    continue
            
            raise ValueError("No valid JSON found in response")
            
        except Exception as e:
            raise ValueError(f"Invalid JSON format: {str(e)}")
        