
import json
import tools

class ShrimpBotAgent:
    def __init__(self, tool_registry_path="tool_registry.json"):
        # Load tool registry JSON
        with open(tool_registry_path) as f:
            self.tool_registry = json.load(f)

    def route_to_tools(self, query: str) -> list[str]:
        """
        Routes the query to the appropriate tools using keyword matching.

        Args:
            query (str): User's question.

        Returns:
            list[str]: List of relevant tool outputs.
        """
        query_lower = query.lower()
        tool_outputs = []

        # Keyword mapping
        routing_keywords = {
            "get_tank_disinfection_info": ["disinfect", "tank", "chlorine", "clean", "sanitize", "bleach"],
            "get_water_quality_info": ["ph", "ammonia", "parameter", "alkalinity", "water quality"],
            "get_feeding_guidelines_info": ["feed", "feeding", "ration", "survival", "rate", "shrimp"],
            "get_temperature_control_info": ["temperature", "heat", "climate", "cold", "cool"],
            "get_disease_control_info": ["vibrio", "white spot", "infection", "disease", "outbreak"]
        }

        # Tool invocation
        for tool_name, keywords in routing_keywords.items():
            if any(kw in query_lower for kw in keywords):
                func_path = self.tool_registry.get(tool_name)
                if func_path:
                    _, func_name = func_path.rsplit(".", 1)
                    try:
                        func = getattr(tools, func_name)
                        result = func(query)
                        if result:
                            tool_outputs.append(result)
                    except Exception as e:
                        print(f"⚠️ Error executing {tool_name}: {e}")

        return tool_outputs
