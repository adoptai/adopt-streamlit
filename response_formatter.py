import json

def format_adopt_response(response):
    """
    Format Adopt API response into user-friendly markdown text
    
    Args:
        response: The response from Adopt API (dict, str, or other)
    
    Returns:
        Formatted string ready for display
    """
    
    # If it's already a string, return it
    if isinstance(response, str):
        return response
    
    # If it's not a dict, convert to JSON
    if not isinstance(response, dict):
        return f"```json\n{json.dumps(response, indent=2)}\n```"
    
    # Start building formatted response
    formatted = ""
    
    # Add header if present
    if 'header_message' in response and response['header_message']:
        formatted += f"**{response['header_message']}**\n\n"
    
    # Format the data section
    if 'data' in response:
        data = response['data']
        
        # If data is a list of items (actions/categories)
        if isinstance(data, list) and len(data) > 0:
            # Separate categories and actions
            categories = {}
            actions = []
            
            for item in data:
                if isinstance(item, dict):
                    if not item.get('isPrompt', False):
                        # This is a category/parent
                        categories[item.get('index')] = item.get('Name', 'Unknown')
                    else:
                        # This is an action
                        actions.append(item)
            
            # Display categories with their actions
            if categories:
                for cat_idx, cat_name in sorted(categories.items()):
                    formatted += f"### 📁 {cat_name}\n\n"
                    
                    # Find actions under this category
                    cat_actions = [
                        a for a in actions 
                        if a.get('parentIndex') == cat_idx
                    ]
                    
                    if cat_actions:
                        for action in cat_actions:
                            action_name = action.get('Name', 'Unknown Action')
                            formatted += f"- ✨ **{action_name}**\n"
                        formatted += "\n"
                
                # Show actions without a parent (orphans)
                orphan_actions = [
                    a for a in actions 
                    if a.get('parentIndex') is None
                ]
                if orphan_actions:
                    formatted += "### 📋 Other Actions\n\n"
                    for action in orphan_actions:
                        action_name = action.get('Name', 'Unknown Action')
                        formatted += f"- ✨ **{action_name}**\n"
                    formatted += "\n"
            
            # If no categories, just list all actions
            elif actions:
                formatted += "### Available Actions\n\n"
                for action in actions:
                    action_name = action.get('Name', 'Unknown Action')
                    formatted += f"- ✨ **{action_name}**\n"
                formatted += "\n"
        
        # If data is a string message
        elif isinstance(data, str) and data:
            formatted += f"📝 {data}\n\n"
        
        # If data is a dict with fields
        elif isinstance(data, dict):
            formatted += "### Response Details\n\n"
            for key, value in data.items():
                if value:  # Only show non-empty values
                    formatted += f"**{key}:** {value}\n"
            formatted += "\n"
    
    # Add footer if present
    if 'footer_message' in response and response['footer_message']:
        formatted += f"\n💡 _{response['footer_message']}_\n"
    
    # If we didn't format anything useful, show raw JSON
    if not formatted.strip():
        formatted = f"```json\n{json.dumps(response, indent=2)}\n```"
    
    return formatted


def count_actions(response):
    """
    Count total actions in response
    
    Args:
        response: The response dict
    
    Returns:
        Number of actions found
    """
    if not isinstance(response, dict):
        return 0
    
    data = response.get('data', [])
    if isinstance(data, list):
        return len([item for item in data if item.get('isPrompt', False)])
    
    return 0


def extract_actions(response):
    """
    Extract action items from response
    
    Args:
        response: The response dict
    
    Returns:
        List of action dicts
    """
    if not isinstance(response, dict):
        return []
    
    data = response.get('data', [])
    if isinstance(data, list):
        return [item for item in data if item.get('isPrompt', False)]
    
    return []