#!/usr/bin/env python3
"""
Convert Swagger UI HTML documentation to hierarchical markdown files.

This script extracts the embedded OpenAPI specification from a Swagger UI HTML file
and generates AI-navigable markdown documentation with:
- A top-level README.md index file
- Individual category files for each API tag
- A schemas.md file containing all data models

Usage:
    python convert_swagger_to_markdown.py
"""

import json
import os
import re
from pathlib import Path
from typing import Any


def extract_openapi_spec(html_content: str) -> dict:
    """Extract the OpenAPI spec object from Swagger UI HTML."""
    lines = html_content.split('\n')
    
    # Find the SwaggerUIBundle call first, then find spec within it
    swagger_bundle_line = None
    for i, line in enumerate(lines):
        if 'SwaggerUIBundle' in line and 'window.ui' in line:
            swagger_bundle_line = i
            break
    
    if swagger_bundle_line is None:
        raise ValueError("Could not find SwaggerUIBundle")
    
    # Find the start of the spec (line containing "spec: {") after SwaggerUIBundle
    spec_start_line = None
    for i in range(swagger_bundle_line, min(swagger_bundle_line + 10, len(lines))):
        if re.search(r'spec:\s*\{', lines[i]):
            spec_start_line = i
            break
    
    if spec_start_line is None:
        raise ValueError("Could not find spec start")
    
    # Find where spec ends by counting braces
    # Start from the opening brace of spec
    brace_count = 0
    spec_started = False
    spec_end_line = None
    
    for i in range(spec_start_line, len(lines)):
        line = lines[i]
        
        for char in line:
            if char == '{':
                if not spec_started:
                    spec_started = True
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if spec_started and brace_count == 0:
                    spec_end_line = i
                    break
        
        if spec_end_line is not None:
            break
    
    if spec_end_line is None:
        raise ValueError("Could not find spec end")
    
    # Extract the spec text
    spec_lines = lines[spec_start_line:spec_end_line + 1]
    spec_text = '\n'.join(spec_lines)
    
    # Remove the "spec:" prefix to get just the object
    spec_text = re.sub(r'^\s*spec:\s*', '', spec_text, count=1)
    
    # Remove any trailing comma after the final closing brace
    spec_text = spec_text.rstrip()
    if spec_text.endswith(','):
        spec_text = spec_text[:-1]
    
    # Convert JavaScript object to valid JSON
    spec_json = js_object_to_json(spec_text)
    
    # Final cleanup: remove any remaining trailing commas that might cause issues
    spec_json = re.sub(r',\s*$', '', spec_json)
    
    try:
        return json.loads(spec_json)
    except json.JSONDecodeError as e:
        # Debug: write the problematic JSON to a file
        with open('/tmp/debug_spec.json', 'w') as f:
            f.write(spec_json)
        print(f"JSON parse error at position {e.pos}")
        print(f"Context around error: ...{spec_json[max(0,e.pos-50):e.pos+50]}...")
        raise


def js_object_to_json(js_text: str) -> str:
    """Convert JavaScript object notation to valid JSON."""
    result = []
    i = 0
    in_string = False
    string_char = None
    
    while i < len(js_text):
        char = js_text[i]
        
        # Handle string boundaries
        if char in '"\'':
            if not in_string:
                in_string = True
                string_char = char
                result.append('"')  # Always use double quotes
                i += 1
                continue
            elif char == string_char:
                # Check if escaped
                num_backslashes = 0
                j = i - 1
                while j >= 0 and js_text[j] == '\\':
                    num_backslashes += 1
                    j -= 1
                
                if num_backslashes % 2 == 0:  # Not escaped
                    in_string = False
                    string_char = None
                    result.append('"')
                    i += 1
                    continue
        
        if in_string:
            # Handle escape sequences and special characters in strings
            if char == '\n':
                result.append('\\n')
            elif char == '\r':
                result.append('\\r')
            elif char == '\t':
                result.append('\\t')
            elif char == '"' and string_char == "'":
                # Double quote inside single-quoted string
                result.append('\\"')
            elif char == '\\' and i + 1 < len(js_text):
                next_char = js_text[i + 1]
                if next_char == "'":
                    # Escaped single quote - just output the quote
                    result.append("'")
                    i += 2
                    continue
                else:
                    result.append(char)
            else:
                result.append(char)
            i += 1
            continue
        
        # Handle unquoted keys (word followed by colon)
        if char.isalpha() or char == '_' or char == '$':
            # Collect the identifier
            identifier = ''
            j = i
            while j < len(js_text) and (js_text[j].isalnum() or js_text[j] == '_' or js_text[j] == '$'):
                identifier += js_text[j]
                j += 1
            
            # Skip whitespace
            while j < len(js_text) and js_text[j] in ' \t\n\r':
                j += 1
            
            # Check if followed by colon (it's a key)
            if j < len(js_text) and js_text[j] == ':':
                # It's an unquoted key - quote it
                result.append(f'"{identifier}"')
                i = j
                continue
            else:
                # It's a value (like true, false, null)
                result.append(identifier)
                i = j
                continue
        
        # Handle numeric keys (like 200, 400, etc.)
        if char.isdigit():
            # Collect the number
            number = ''
            j = i
            while j < len(js_text) and (js_text[j].isdigit() or js_text[j] == '.'):
                number += js_text[j]
                j += 1
            
            # Skip whitespace
            k = j
            while k < len(js_text) and js_text[k] in ' \t\n\r':
                k += 1
            
            # Check if followed by colon (it's a key)
            if k < len(js_text) and js_text[k] == ':':
                # It's a numeric key - quote it
                result.append(f'"{number}"')
                i = j
                continue
            else:
                # It's a numeric value
                result.append(number)
                i = j
                continue
        
        # Remove trailing commas before } or ]
        if char == ',':
            # Look ahead for } or ]
            j = i + 1
            while j < len(js_text) and js_text[j] in ' \t\n\r':
                j += 1
            if j < len(js_text) and js_text[j] in '}]':
                # Skip this trailing comma
                i += 1
                continue
        
        result.append(char)
        i += 1
    
    return ''.join(result)


def slugify(text: str) -> str:
    """Convert text to a URL-friendly slug."""
    return text.lower().replace(' ', '-').replace('_', '-')


def get_method_badge(method: str) -> str:
    """Return a formatted method badge."""
    method = method.upper()
    return f"**{method}**"


def format_schema_ref(ref: str) -> str:
    """Convert a $ref to a markdown link."""
    if not ref:
        return ""
    schema_name = ref.split('/')[-1]
    return f"[{schema_name}](schemas.md#{slugify(schema_name)})"


def render_schema_property(name: str, prop: dict, required: list = None, indent: int = 0) -> str:
    """Render a single schema property as markdown."""
    lines = []
    prefix = "  " * indent
    required_marker = " *(required)*" if required and name in required else ""
    
    prop_type = prop.get('type', '')
    if '$ref' in prop:
        prop_type = format_schema_ref(prop['$ref'])
    elif prop_type == 'array' and 'items' in prop:
        if '$ref' in prop['items']:
            prop_type = f"array of {format_schema_ref(prop['items']['$ref'])}"
        else:
            prop_type = f"array of {prop['items'].get('type', 'any')}"
    
    description = prop.get('description', '')
    
    lines.append(f"{prefix}- **{name}** (`{prop_type}`){required_marker}")
    if description:
        lines.append(f"{prefix}  - {description}")
    
    # Handle enum values
    if 'enum' in prop:
        enum_values = ', '.join([f"`{v}`" for v in prop['enum']])
        lines.append(f"{prefix}  - Possible values: {enum_values}")
    
    # Handle format
    if 'format' in prop:
        lines.append(f"{prefix}  - Format: `{prop['format']}`")
    
    return '\n'.join(lines)


def render_request_body(request_body: dict) -> str:
    """Render request body documentation."""
    lines = []
    
    description = request_body.get('description', '')
    if description:
        lines.append(f"\n{description}\n")
    
    content = request_body.get('content', {})
    for content_type, content_spec in content.items():
        lines.append(f"\n**Content-Type:** `{content_type}`\n")
        
        schema = content_spec.get('schema', {})
        if '$ref' in schema:
            lines.append(f"\nSchema: {format_schema_ref(schema['$ref'])}\n")
        elif 'properties' in schema:
            lines.append("\n**Properties:**\n")
            required = schema.get('required', [])
            for prop_name, prop_spec in schema['properties'].items():
                lines.append(render_schema_property(prop_name, prop_spec, required))
    
    return '\n'.join(lines)


def render_responses(responses: dict) -> str:
    """Render response documentation."""
    lines = ["\n**Responses:**\n"]
    
    for status_code, response_spec in responses.items():
        description = response_spec.get('description', '')
        lines.append(f"- **{status_code}**: {description}")
        
        content = response_spec.get('content', {})
        for content_type, content_spec in content.items():
            schema = content_spec.get('schema', {})
            if '$ref' in schema:
                lines.append(f"  - Schema: {format_schema_ref(schema['$ref'])}")
            elif 'properties' in schema:
                for prop_name, prop_spec in schema.get('properties', {}).items():
                    if '$ref' in prop_spec:
                        lines.append(f"  - `{prop_name}`: {format_schema_ref(prop_spec['$ref'])}")
                    elif prop_spec.get('type') == 'array' and 'items' in prop_spec:
                        if '$ref' in prop_spec['items']:
                            lines.append(f"  - `{prop_name}`: array of {format_schema_ref(prop_spec['items']['$ref'])}")
    
    return '\n'.join(lines)


def render_parameters(parameters: list) -> str:
    """Render parameter documentation."""
    if not parameters:
        return ""
    
    lines = ["\n**Parameters:**\n"]
    
    for param in parameters:
        name = param.get('name', '')
        location = param.get('in', '')
        required = param.get('required', False)
        description = param.get('description', '')
        schema = param.get('schema', {})
        param_type = schema.get('type', 'string')
        
        required_marker = " *(required)*" if required else ""
        lines.append(f"- **{name}** (`{param_type}`, in {location}){required_marker}")
        if description:
            lines.append(f"  - {description}")
    
    return '\n'.join(lines)


def render_endpoint(path: str, method: str, operation: dict) -> str:
    """Render a single endpoint as markdown."""
    lines = []
    
    summary = operation.get('summary', '')
    description = operation.get('description', '')
    deprecated = operation.get('deprecated', False)
    
    # Endpoint header
    lines.append(f"### {get_method_badge(method)} `{path}`\n")
    
    if deprecated:
        lines.append("> **⚠️ DEPRECATED**\n")
    
    if summary:
        lines.append(f"{summary}\n")
    
    if description and description != summary:
        lines.append(f"{description}\n")
    
    # Parameters
    parameters = operation.get('parameters', [])
    if parameters:
        lines.append(render_parameters(parameters))
    
    # Request Body
    request_body = operation.get('requestBody')
    if request_body:
        lines.append("\n**Request Body:**")
        lines.append(render_request_body(request_body))
    
    # Responses
    responses = operation.get('responses', {})
    if responses:
        lines.append(render_responses(responses))
    
    lines.append("\n---\n")
    
    return '\n'.join(lines)


def render_schema(name: str, schema: dict) -> str:
    """Render a single schema as markdown."""
    lines = []
    
    lines.append(f"### {name}\n")
    
    description = schema.get('description', '')
    deprecated = schema.get('deprecated', False)
    
    if deprecated:
        lines.append("> **⚠️ DEPRECATED**\n")
    
    if description:
        lines.append(f"{description}\n")
    
    schema_type = schema.get('type', 'object')
    lines.append(f"**Type:** `{schema_type}`\n")
    
    # Handle oneOf
    if 'oneOf' in schema:
        lines.append("\n**One of:**\n")
        for option in schema['oneOf']:
            if '$ref' in option:
                lines.append(f"- {format_schema_ref(option['$ref'])}")
    
    # Handle properties
    properties = schema.get('properties', {})
    required = schema.get('required', [])
    
    if properties:
        lines.append("\n**Properties:**\n")
        for prop_name, prop_spec in properties.items():
            lines.append(render_schema_property(prop_name, prop_spec, required))
    
    # Handle additionalProperties
    if 'additionalProperties' in schema:
        add_props = schema['additionalProperties']
        if isinstance(add_props, dict):
            add_type = add_props.get('type', 'any')
            lines.append(f"\n**Additional Properties:** `{add_type}`")
    
    lines.append("\n---\n")
    
    return '\n'.join(lines)


def generate_readme(spec: dict, tags: list, output_dir: Path) -> None:
    """Generate the top-level README.md index file."""
    info = spec.get('info', {})
    title = info.get('title', 'API Documentation')
    description = info.get('description', '')
    version = info.get('version', '')
    
    servers = spec.get('servers', [])
    base_url = servers[0].get('url', '') if servers else ''
    
    lines = [
        f"# {title}\n",
        f"**Version:** {version}\n",
    ]
    
    if base_url:
        lines.append(f"**Base URL:** `{base_url}`\n")
    
    if description:
        lines.append(f"\n{description}\n")
    
    lines.append("\n## How to Use This Documentation\n")
    lines.append("This documentation is organized into separate files by API category. ")
    lines.append("Each category file contains all endpoints related to that functionality.\n")
    lines.append("\n**For AI Agents:** Start here to understand the API structure, then navigate to the ")
    lines.append("specific category file for detailed endpoint information. Schema definitions are in `schemas.md`.\n")
    
    lines.append("\n## API Categories\n")
    lines.append("| Category | Description | File |")
    lines.append("|----------|-------------|------|")
    
    # Count endpoints per tag
    paths = spec.get('paths', {})
    tag_endpoints = {}
    tag_descriptions = {}
    
    for path, methods in paths.items():
        for method, operation in methods.items():
            if method in ['get', 'post', 'put', 'delete', 'patch']:
                for tag in operation.get('tags', ['Other']):
                    if tag not in tag_endpoints:
                        tag_endpoints[tag] = 0
                    tag_endpoints[tag] += 1
    
    for tag in tags:
        slug = slugify(tag)
        count = tag_endpoints.get(tag, 0)
        lines.append(f"| [{tag}]({slug}.md) | {count} endpoints | `{slug}.md` |")
    
    lines.append(f"\n| [Schemas](schemas.md) | Data model definitions | `schemas.md` |")
    
    lines.append("\n## Authentication\n")
    lines.append("Most endpoints require authentication. Obtain an API token from the Orbit instance ")
    lines.append("and add it to the request header:\n")
    lines.append("```")
    lines.append('{"Authorization": "Bearer <API_TOKEN>"}')
    lines.append("```\n")
    
    lines.append("\n## Quick Reference\n")
    lines.append("| Method | Endpoint | Category | Summary |")
    lines.append("|--------|----------|----------|---------|")
    
    for path, methods in paths.items():
        for method, operation in methods.items():
            if method in ['get', 'post', 'put', 'delete', 'patch']:
                tags_list = operation.get('tags', ['Other'])
                tag = tags_list[0] if tags_list else 'Other'
                summary = operation.get('summary', '')[:50]
                if len(operation.get('summary', '')) > 50:
                    summary += '...'
                deprecated = '~~' if operation.get('deprecated') else ''
                lines.append(f"| {method.upper()} | {deprecated}`{path}`{deprecated} | [{tag}]({slugify(tag)}.md) | {summary} |")
    
    content = '\n'.join(lines)
    (output_dir / 'README.md').write_text(content)
    print(f"  Created README.md")


def generate_category_file(tag: str, endpoints: list, output_dir: Path) -> None:
    """Generate a category markdown file."""
    slug = slugify(tag)
    
    lines = [
        f"# {tag}\n",
        f"[← Back to Index](README.md) | [Schemas](schemas.md)\n",
        f"\nThis document describes the {tag} endpoints.\n",
        "\n## Endpoints\n",
    ]
    
    # Table of contents
    lines.append("| Method | Endpoint | Summary |")
    lines.append("|--------|----------|---------|")
    
    for path, method, operation in endpoints:
        summary = operation.get('summary', '')[:60]
        if len(operation.get('summary', '')) > 60:
            summary += '...'
        deprecated = '~~' if operation.get('deprecated') else ''
        lines.append(f"| {method.upper()} | {deprecated}`{path}`{deprecated} | {summary} |")
    
    lines.append("\n---\n")
    
    # Detailed endpoint documentation
    for path, method, operation in endpoints:
        lines.append(render_endpoint(path, method, operation))
    
    content = '\n'.join(lines)
    (output_dir / f'{slug}.md').write_text(content)
    print(f"  Created {slug}.md ({len(endpoints)} endpoints)")


def generate_schemas_file(schemas: dict, output_dir: Path) -> None:
    """Generate the schemas.md file."""
    lines = [
        "# Schemas\n",
        "[← Back to Index](README.md)\n",
        "\nThis document contains all data model definitions used by the API.\n",
        "\n## Table of Contents\n",
    ]
    
    # Table of contents
    for name in sorted(schemas.keys()):
        lines.append(f"- [{name}](#{slugify(name)})")
    
    lines.append("\n---\n")
    
    # Schema definitions
    for name in sorted(schemas.keys()):
        schema = schemas[name]
        lines.append(render_schema(name, schema))
    
    content = '\n'.join(lines)
    (output_dir / 'schemas.md').write_text(content)
    print(f"  Created schemas.md ({len(schemas)} schemas)")


def main():
    """Main entry point."""
    # Configuration
    script_dir = Path(__file__).parent
    html_file = script_dir / 'docs.html'
    output_dir = script_dir / 'api'
    
    print(f"Converting Swagger UI to Markdown")
    print(f"  Input:  {html_file}")
    print(f"  Output: {output_dir}/")
    print()
    
    # Read the HTML file
    if not html_file.exists():
        print(f"Error: {html_file} not found")
        return 1
    
    print("Reading HTML file...")
    html_content = html_file.read_text()
    
    # Extract the OpenAPI spec
    print("Extracting OpenAPI specification...")
    try:
        spec = extract_openapi_spec(html_content)
    except Exception as e:
        print(f"Error extracting spec: {e}")
        return 1
    
    print(f"  Found OpenAPI {spec.get('openapi', 'unknown')} specification")
    print(f"  Title: {spec.get('info', {}).get('title', 'Unknown')}")
    print(f"  Version: {spec.get('info', {}).get('version', 'Unknown')}")
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Organize endpoints by tag
    paths = spec.get('paths', {})
    endpoints_by_tag = {}
    all_tags = set()
    
    for path, methods in paths.items():
        for method, operation in methods.items():
            if method not in ['get', 'post', 'put', 'delete', 'patch']:
                continue
            
            tags = operation.get('tags', ['Other'])
            for tag in tags:
                all_tags.add(tag)
                if tag not in endpoints_by_tag:
                    endpoints_by_tag[tag] = []
                endpoints_by_tag[tag].append((path, method, operation))
    
    # Sort tags for consistent output
    sorted_tags = sorted(all_tags)
    
    print(f"\nFound {len(paths)} paths with {sum(len(v) for v in endpoints_by_tag.values())} endpoints")
    print(f"Found {len(sorted_tags)} categories: {', '.join(sorted_tags)}")
    
    # Get schemas
    schemas = spec.get('components', {}).get('schemas', {})
    print(f"Found {len(schemas)} schemas")
    
    # Generate files
    print("\nGenerating markdown files...")
    
    # Generate README
    generate_readme(spec, sorted_tags, output_dir)
    
    # Generate category files
    for tag in sorted_tags:
        endpoints = endpoints_by_tag.get(tag, [])
        generate_category_file(tag, endpoints, output_dir)
    
    # Generate schemas file
    generate_schemas_file(schemas, output_dir)
    
    print(f"\nDone! Generated {len(sorted_tags) + 2} files in {output_dir}/")
    return 0


if __name__ == '__main__':
    exit(main())
