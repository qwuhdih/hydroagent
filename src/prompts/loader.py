"""Prompt loading and rendering utilities."""

from pathlib import Path
from typing import Dict, Any, Optional
import yaml
from jinja2 import Environment, FileSystemLoader, Template


# Get prompts directory
PROMPTS_DIR = Path(__file__).parent / "templates"
TEMPLATES_DIR = PROMPTS_DIR

# Initialize Jinja2 environment
jinja_env = Environment(
    loader=FileSystemLoader(str(TEMPLATES_DIR)),
    trim_blocks=True,
    lstrip_blocks=True,
)


def load_prompt(template_name: str, format: str = "auto") -> str:
    """Load a prompt template from file.
    
    Args:
        template_name: Name of the template file (without extension)
        format: File format ('yaml', 'txt', 'jinja2', or 'auto' to detect)
        
    Returns:
        Raw template content as string
    """
    # Try different extensions if auto
    if format == "auto":
        extensions = [".yaml", ".yml", ".txt", ".jinja2", ".j2"]
    else:
        extensions = [f".{format}"]

    for ext in extensions:
        template_path = PROMPTS_DIR / f"{template_name}{ext}"
        if template_path.exists():
            return template_path.read_text(encoding="utf-8")

    raise FileNotFoundError(f"Prompt template '{template_name}' not found in {PROMPTS_DIR}")


def render_prompt(template_name: str, context: Optional[Dict[str, Any]] = None, format: str = "auto") -> str:
    """Load and render a prompt template with context.
    
    Args:
        template_name: Name of the template file
        context: Variables to inject into the template
        format: File format ('yaml', 'txt', 'jinja2', or 'auto')
        
    Returns:
        Rendered prompt string
    """
    content = load_prompt(template_name, format=format)
    context = context or {}

    # If YAML, parse it first
    if template_name.endswith((".yaml", ".yml")):
        data = yaml.safe_load(content)
        # If it's a structured YAML with a 'prompt' key, extract it
        if isinstance(data, dict) and "prompt" in data:
            content = data["prompt"]
            # Merge YAML metadata into context
            context = {**data.get("variables", {}), **context}

    # Render with Jinja2
    template = Template(content)
    return template.render(**context)


def get_system_prompt(context: Optional[Dict[str, Any]] = None) -> str:
    """Get the system prompt.
    
    Args:
        context: Optional context variables
        
    Returns:
        Rendered system prompt
    """
    return render_prompt("system_prompt", context=context)


def get_planner_prompt(context: Optional[Dict[str, Any]] = None) -> str:
    """Get the planner prompt.
    
    Args:
        context: Optional context variables
        
    Returns:
        Rendered planner prompt
    """
    return render_prompt("planner_prompt", context=context)

