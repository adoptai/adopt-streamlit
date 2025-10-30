import streamlit as st
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to Python path for imports
current_dir = Path(__file__).parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

# Set page configuration
st.set_page_config(
    page_title="Adopt Chat Interface",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

if 'pending_action' not in st.session_state:
    st.session_state['pending_action'] = None

# Demo mode flag (set to True when you don't have credentials)
DEMO_MODE = False  # Change to True to test UI without real credentials

# === AUTHENTICATION SCREEN ===
if not st.session_state['authenticated']:
    st.title("Adopt Chat Interface")
    st.markdown("### Connect to your Adopt instance")
    
    # Demo mode banner
    if DEMO_MODE:
        st.warning("⚠️ **DEMO MODE** - Enter any credentials to see the UI (no real connection)")
    
    st.info("""
    **How to get your credentials:**
    1. Go to Adopt Platform → [adopt.ai](https://www.adopt.ai)
    2. Navigate to `Settings → Profile → Personal Tokens`
    3. Click "Generate Token"
    4. Copy the `clientId` and `secret` values
    """)
    
    # Two column layout for inputs
    col1, col2 = st.columns(2)
    
    with col1:
        client_id = st.text_input(
            "Client ID",
            placeholder="Enter your Adopt Client ID",
            help="Your Adopt API Client ID from the platform"
        )
    
    with col2:
        client_secret = st.text_input(
            "Client Secret",
            type="password",
            placeholder="Enter your Adopt Client Secret",
            help="Your Adopt API Client Secret (kept secure)"
        )
    
    # Info about profile
    st.info("Profile will be loaded from: `examples/adopt_profile.json`")
    
    # Connect button
    if st.button("Connect", type="primary", use_container_width=True):
        if not client_id or not client_secret:
            st.error("Please provide both Client ID and Client Secret")
        else:
            if DEMO_MODE:
                # Demo mode - just show success
                st.session_state['authenticated'] = True
                st.session_state['client_id'] = client_id
                st.session_state['demo_mode'] = True
                st.success("✅ Connected successfully! (Demo Mode)")
                st.balloons()
                st.rerun()
            else:
                # Real mode - connect to actual Adopt API
                os.environ['ADOPT_CLIENT_ID'] = client_id
                os.environ['ADOPT_CLIENT_SECRET'] = client_secret
                
                try:
                    from examples.action_api_samples.api_sample import (
                        load_adopt_profile,
                        list_actions
                    )
                    
                    with st.spinner("Connecting to Adopt..."):
                        # Load profile (automatically finds examples/adopt_profile.json)
                        profile = load_adopt_profile()
                        
                        # Test connection by listing actions
                        actions = list_actions()
                        
                        st.session_state['authenticated'] = True
                        st.session_state['client_id'] = client_id
                        st.session_state['profile'] = profile
                        st.session_state['actions_count'] = len(actions.capabilities)
                        st.session_state['demo_mode'] = False
                        
                        st.success(f"✅ Connected! Found {len(actions.capabilities)} actions.")
                        st.balloons()
                        st.rerun()
                        
                except ImportError as e:
                    st.error(f"""
                    ⚠️ Required module not found.
                    
                    Please ensure you have the Adopt SDK installed and run from AdoptXchange directory:
                    
                    **Option 1 (Recommended):**
                    ```bash
                    cd /path/to/AdoptXchange
                    poetry run streamlit run /path/to/adopt-streamlit/app.py
                    ```
                    
                    **Option 2:**
                    Set PYTHONPATH:
                    ```bash
                    $env:PYTHONPATH="C:\\path\\to\\AdoptXchange"
                    streamlit run app.py
                    ```
                    
                    Error details: {str(e)}
                    """)
                    st.stop()
                except FileNotFoundError:
                    st.error("Profile file not found")
                    st.info("Make sure examples/adopt_profile.json exists.")
                except ValueError as e:
                    st.error(f"Invalid profile file: {str(e)}")
                except Exception as e:
                    st.error(f"Connection failed: {str(e)}")
                    with st.expander("Show error details"):
                        st.code(str(e))

else:  # Show chat when authenticated
    # === CHAT INTERFACE ===
    st.title("Adopt Chat Interface")
    
    # Connection status bar
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        if st.session_state.get('demo_mode', True):
            st.warning(f"Demo Mode - User: {st.session_state['client_id'][:15]}...")
        else:
            st.success(f"✅ Connected - User: {st.session_state['client_id'][:15]}...")
    
    with col2:
        if 'actions_count' in st.session_state:
            st.info(f"{st.session_state['actions_count']} actions available")
        else:
            st.info("Demo actions available")
    
    with col3:
        if st.button("Disconnect"):
            st.session_state['authenticated'] = False
            st.session_state['messages'] = []
            st.session_state['pending_action'] = None
            st.rerun()
    
    st.markdown("---")
    
    # Sidebar for settings
    with st.sidebar:
        st.header("Settings")
        
        st.subheader("System Prompt")
        system_prompt = st.text_area(
            "Customize AI behavior",
            value="You are a helpful assistant that helps users interact with the Adopt platform. Be concise and clear.",
            height=100,
            help="This guides how Adopt responds to your requests"
        )
        
        st.markdown("---")
        
        st.subheader("Response Options")
        use_enhancement = st.checkbox(
            "Enhance responses with LLM",
            value=False,
            help="Use Groq to make responses more readable (requires GROQ_API_KEY)"
        )
        
        if use_enhancement:
            st.info("Responses will be formatted using LLM")
        
        st.markdown("---")
        
        # Clear chat button
        if st.button("Clear Chat", use_container_width=True):
            st.session_state['messages'] = []
            st.session_state['pending_action'] = None
            st.rerun()
        
        # Export chat button
        if st.session_state['messages']:
            if st.button("Export Chat", use_container_width=True):
                chat_text = ""
                for msg in st.session_state['messages']:
                    chat_text += f"{msg['role'].upper()}: {msg['content']}\n\n"
                
                st.download_button(
                    "Download Chat",
                    chat_text,
                    file_name="adopt_chat_export.txt",
                    mime="text/plain",
                    use_container_width=True
                )
    
    # Display chat messages
    for idx, message in enumerate(st.session_state['messages']):
        with st.chat_message(message['role']):
            st.markdown(message['content'])
    
    # === INITIAL PROMPT BUTTONS (shown when chat is empty) ===
    if len(st.session_state['messages']) == 0:
        st.markdown("### Welcome! Get started by exploring available actions:")
        st.markdown("")  # Add spacing
        
        # Main action button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("Show all available actions", key="initial_prompt", use_container_width=True, type="primary"):
                prompt = "Show me all the available actions"
                st.session_state['messages'].append({
                    "role": "user",
                    "content": prompt
                })
                st.session_state['pending_action'] = prompt
                st.rerun()
        
        st.markdown("")  # Add spacing
        st.markdown("#### Or try these quick actions:")
        
        # Quick action buttons
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            if st.button("Help", key="help_prompt", use_container_width=True):
                prompt = "What can you help me with?"
                st.session_state['messages'].append({
                    "role": "user",
                    "content": prompt
                })
                st.session_state['pending_action'] = prompt
                st.rerun()
        
        with col_b:
            if st.button("Get Pickup Locations", key="pickup_prompt", use_container_width=True):
                prompt = "Get All Pickup Locations"
                st.session_state['messages'].append({
                    "role": "user",
                    "content": prompt
                })
                st.session_state['pending_action'] = prompt
                st.rerun()
        
        with col_c:
            if st.button("Show Capabilities", key="capabilities_prompt", use_container_width=True):
                prompt = "List all your capabilities"
                st.session_state['messages'].append({
                    "role": "user",
                    "content": prompt
                })
                st.session_state['pending_action'] = prompt
                st.rerun()
        
        st.markdown("---")
    
    # === HANDLE PENDING ACTION (for button clicks) ===
    if st.session_state.get('pending_action'):
        prompt = st.session_state['pending_action']
        st.session_state['pending_action'] = None  # Clear it
        
        # Generate response
        with st.chat_message("assistant"):
            if st.session_state.get('demo_mode', True):
                # Demo mode response
                with st.spinner("Processing (Demo Mode)..."):
                    import time
                    time.sleep(1)
                    
                    if "segment" in prompt.lower():
                        response = "**Demo Response**: I would create a segment for you.\n\nIn real mode, this would connect to Adopt and create an actual segment on your platform."
                    elif "list" in prompt.lower() or "show" in prompt.lower() or "available actions" in prompt.lower():
                        response = "**Demo Response**: Here are the available actions:\n\n1. Create Segment\n2. Manage Campaigns\n3. View Analytics\n4. Export Data\n\nIn real mode, this would show actual data from your Adopt instance."
                    elif "help" in prompt.lower() or "capabilities" in prompt.lower():
                        response = "**Demo Response**: I can help you with:\n\n• Creating and managing segments\n• Running campaigns\n• Viewing analytics\n• Exporting data\n\nIn real mode, I would show capabilities from your actual Adopt configuration."
                    elif "pickup" in prompt.lower():
                        response = "**Demo Response**: Here are your pickup locations:\n\n1. Main Warehouse - Delhi\n2. Secondary Hub - Mumbai\n3. Distribution Center - Bangalore\n\nIn real mode, this would fetch actual pickup locations from Shiprocket."
                    else:
                        response = f"**Demo Response**: I received your request: '{prompt}'\n\nIn real mode, I would process this through the Adopt API and execute the appropriate action."
                    
                    st.markdown(response)
            else:
                # Real mode API call
                with st.spinner("Processing with Adopt..."):
                    try:
                        from examples.action_api_samples.api_sample import run_simple_action
                        
                        result = run_simple_action(prompt, st.session_state['profile'])
                        
                        # Format response
                        try:
                            import json
                            import ast
                            from response_formatter import format_adopt_response
                            
                            if isinstance(result, str):
                                try:
                                    result = ast.literal_eval(result)
                                except (ValueError, SyntaxError):
                                    pass
                            
                            response = format_adopt_response(result)
                            
                        except ImportError as e:
                            import json
                            if isinstance(result, dict):
                                response = f"```json\n{json.dumps(result, indent=2)}\n```"
                            else:
                                response = str(result)
                        except Exception as e:
                            import json
                            if isinstance(result, dict):
                                response = f"```json\n{json.dumps(result, indent=2)}\n```"
                            else:
                                response = str(result)
                        
                        if use_enhancement:
                            try:
                                from llm_enhancer import enhance_response
                                response = enhance_response(response, system_prompt)
                            except Exception as e:
                                st.warning(f"Enhancement failed: {e}")
                        
                        st.markdown(response)
                        
                    except Exception as e:
                        response = f"**Error**: {str(e)}"
                        st.error(response)
            
            # Save response
            st.session_state['messages'].append({
                "role": "assistant",
                "content": response
            })
        
        st.rerun()  # Refresh to show the new message
    
    # === CHAT INPUT ===
    if prompt := st.chat_input("Ask Adopt to do something..."):
        # Add user message
        st.session_state['messages'].append({
            "role": "user",
            "content": prompt
        })
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            if st.session_state.get('demo_mode', True):
                # Demo mode - simulated response
                with st.spinner("Processing (Demo Mode)..."):
                    import time
                    time.sleep(1)  # Simulate API delay
                    
                    # Generate demo response based on keywords
                    if "segment" in prompt.lower():
                        response = "**Demo Response**: I would create a segment for you.\n\nIn real mode, this would connect to Adopt and create an actual segment on your platform."
                    elif "list" in prompt.lower() or "show" in prompt.lower():
                        response = "**Demo Response**: Here are the available actions:\n\n1. Create Segment\n2. Manage Campaigns\n3. View Analytics\n4. Export Data\n\nIn real mode, this would show actual data from your Adopt instance."
                    elif "help" in prompt.lower():
                        response = "**Demo Response**: I can help you with:\n\n• Creating and managing segments\n• Running campaigns\n• Viewing analytics\n• Exporting data\n\nIn real mode, I would show capabilities from your actual Adopt configuration."
                    else:
                        response = f"**Demo Response**: I received your request: '{prompt}'\n\nIn real mode, I would process this through the Adopt API and execute the appropriate action."
                    
                    st.markdown(response)
            else:
                # Real mode - actual API call
                with st.spinner("Processing with Adopt..."):
                    try:
                        from examples.action_api_samples.api_sample import run_simple_action
                        
                        result = run_simple_action(
                            prompt,
                            st.session_state['profile']
                        )

                        # Format response using our formatter
                        try:
                            import json
                            import ast
                            from response_formatter import format_adopt_response
                            
                            # If result is a string, try to parse it as a Python dict
                            if isinstance(result, str):
                                try:
                                    result = ast.literal_eval(result)
                                except (ValueError, SyntaxError):
                                    pass  # Keep it as string
                            
                            response = format_adopt_response(result)
                            
                        except ImportError as e:
                            # Fallback if formatter not available
                            st.warning(f"Formatter not available: {e}")
                            import json
                            if isinstance(result, dict):
                                response = f"```json\n{json.dumps(result, indent=2)}\n```"
                            else:
                                response = str(result)
                        except Exception as e:
                            # If formatting fails, show raw data
                            st.error(f"Formatting failed: {str(e)}")
                            import json
                            if isinstance(result, dict):
                                response = f"```json\n{json.dumps(result, indent=2)}\n```"
                            else:
                                response = str(result)
                        
                        # Optional: Enhance with LLM
                        if use_enhancement:
                            try:
                                from llm_enhancer import enhance_response
                                response = enhance_response(response, system_prompt)
                            except Exception as e:
                                st.warning(f"Enhancement failed: {e}")
                        
                        st.markdown(response)
                        
                    except Exception as e:
                        response = f"**Error**: {str(e)}"
                        st.error(response)
            
            # Save response
            st.session_state['messages'].append({
                "role": "assistant",
                "content": response
            })