"""
Prompt Management System for SwiggyBot
Handles loading, caching, and validation of prompt templates
"""

import os
import json
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class PromptManager:
    """Manages prompt templates for different query types"""
    
    def __init__(self, prompts_dir: str = "prompts"):
        self.prompts_dir = prompts_dir
        self.prompt_cache: Dict[str, str] = {}
        self.load_all_prompts()
    
    def load_all_prompts(self) -> None:
        """Load all prompt templates from files into cache"""
        try:
            if not os.path.exists(self.prompts_dir):
                logger.warning(f"Prompts directory '{self.prompts_dir}' not found")
                return
            
            prompt_files = {
                'inventory': 'inventory.txt',
                'sales': 'sales.txt', 
                'low_stock': 'low_stock.txt',
                'top_selling': 'top_selling.txt',
                'overview': 'overview.txt',
                'default': 'default.txt'
            }
            
            for query_type, filename in prompt_files.items():
                file_path = os.path.join(self.prompts_dir, filename)
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        self.prompt_cache[query_type] = f.read().strip()
                    logger.info(f"Loaded prompt template: {query_type}")
                else:
                    logger.warning(f"Prompt file not found: {file_path}")
            
            logger.info(f"Loaded {len(self.prompt_cache)} prompt templates")
            
        except Exception as e:
            logger.error(f"Error loading prompt templates: {e}")
    
    def get_prompt(self, query_type: str) -> str:
        """Get prompt template for specified query type"""
        # Try to get specific prompt
        if query_type in self.prompt_cache:
            return self.prompt_cache[query_type]
        
        # Fall back to default prompt
        if 'default' in self.prompt_cache:
            logger.info(f"Using default prompt for query type: {query_type}")
            return self.prompt_cache['default']
        
        # Ultimate fallback - hardcoded basic prompt
        logger.warning(f"No prompt found for '{query_type}', using basic fallback")
        return self._get_basic_fallback_prompt()
    
    def _get_basic_fallback_prompt(self) -> str:
        """Basic fallback prompt if no files are available"""
        return """You are a helpful restaurant management assistant.

USER QUERY: {query}

DATA CONTEXT:
{context}

Please provide a helpful, accurate response based on the data provided. Be professional and focus on restaurant operations."""

    def format_prompt(self, query_type: str, query: str, context: Dict) -> str:
        """Format prompt template with actual query and context data"""
        try:
            prompt_template = self.get_prompt(query_type)
            
            # Format the context as JSON for better structure
            context_json = json.dumps(context, indent=2, ensure_ascii=False)
            
            # Replace placeholders in template
            formatted_prompt = prompt_template.format(
                query=query,
                context=context_json
            )
            
            return formatted_prompt
            
        except Exception as e:
            logger.error(f"Error formatting prompt for {query_type}: {e}")
            # Return basic formatted prompt as fallback
            basic_prompt = self._get_basic_fallback_prompt()
            context_json = json.dumps(context, indent=2, ensure_ascii=False)
            return basic_prompt.format(query=query, context=context_json)
    
    def reload_prompts(self) -> None:
        """Reload all prompt templates from disk"""
        logger.info("Reloading prompt templates...")
        self.prompt_cache.clear()
        self.load_all_prompts()
    
    def get_available_prompts(self) -> Dict[str, str]:
        """Get list of available prompt types and their first few lines"""
        result = {}
        for query_type, prompt in self.prompt_cache.items():
            # Get first line as preview
            first_line = prompt.split('\n')[0][:100]
            result[query_type] = first_line
        return result
    
    def validate_prompts(self) -> Dict[str, bool]:
        """Validate that all prompt templates have required placeholders"""
        validation_results = {}
        required_placeholders = ['{query}', '{context}']
        
        for query_type, prompt in self.prompt_cache.items():
            has_all_placeholders = all(
                placeholder in prompt for placeholder in required_placeholders
            )
            validation_results[query_type] = has_all_placeholders
            
            if not has_all_placeholders:
                missing = [p for p in required_placeholders if p not in prompt]
                logger.warning(f"Prompt '{query_type}' missing placeholders: {missing}")
        
        return validation_results

# Global prompt manager instance
prompt_manager = PromptManager()

def get_formatted_prompt(query_type: str, query: str, context: Dict) -> str:
    """Convenience function to get formatted prompt"""
    return prompt_manager.format_prompt(query_type, query, context)

def reload_prompts() -> None:
    """Convenience function to reload prompts"""
    prompt_manager.reload_prompts()

def get_prompt_info() -> Dict:
    """Get information about loaded prompts"""
    return {
        'available_prompts': list(prompt_manager.prompt_cache.keys()),
        'prompt_previews': prompt_manager.get_available_prompts(),
        'validation_status': prompt_manager.validate_prompts()
    }
