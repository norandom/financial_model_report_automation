#!/usr/bin/env python3
"""
Apply font configuration to LaTeX preamble and notebook YAML.
Reads font_config.env and generates preamble.tex from preamble.tex.template.
"""
import sys
import os

def load_font_config(config_path='buildfiles/font_config.env'):
    """Load font configuration from .env file."""
    config = {}

    if not os.path.exists(config_path):
        print(f"Warning: {config_path} not found, using defaults")
        return {
            'MAIN_FONT': 'Latin Modern Roman',
            'MONO_FONT': 'Latin Modern Mono',
            'MATH_FONT': 'Euler-Math.otf',
            'TABLE_FONT': 'Latin Modern Mono',
            'TABLE_FONT_SCALE': '1.0'
        }

    with open(config_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            if '=' in line:
                key, value = line.split('=', 1)
                # Remove quotes if present
                value = value.strip().strip('"').strip("'")
                config[key] = value

    return config

def apply_to_preamble(config, template_path='buildfiles/preamble.tex.template',
                      output_path='buildfiles/preamble.tex'):
    """Generate preamble.tex from template with font substitutions."""
    with open(template_path, 'r') as f:
        content = f.read()

    # Substitute all {{VARIABLE}} patterns
    for key, value in config.items():
        placeholder = '{{' + key + '}}'
        content = content.replace(placeholder, value)

    with open(output_path, 'w') as f:
        f.write(content)

    print(f"✓ Generated {output_path}")
    print(f"  Math font: {config.get('MATH_FONT', 'not set')}")
    print(f"  Table font: {config.get('TABLE_FONT', 'not set')} (scale {config.get('TABLE_FONT_SCALE', '1.0')})")

def get_notebook_fonts(config):
    """Return fonts for notebook YAML metadata."""
    return {
        'mainfont': config.get('MAIN_FONT', 'Latin Modern Roman'),
        'monofont': config.get('MONO_FONT', 'Latin Modern Mono')
    }

def show_notebook_instructions(config):
    """Show instructions for updating notebook YAML."""
    fonts = get_notebook_fonts(config)
    print("\n📝 Notebook YAML fonts (mainfont/monofont):")
    print(f"   mainfont: \"{fonts['mainfont']}\"")
    print(f"   monofont: \"{fonts['monofont']}\"")

if __name__ == '__main__':
    # Get config file from argument or use default
    config_file = sys.argv[1] if len(sys.argv) > 1 else 'buildfiles/font_config.env'

    print(f"Loading font configuration from: {config_file}")
    config = load_font_config(config_file)

    print("\nApplying fonts to preamble.tex...")
    apply_to_preamble(config)

    show_notebook_instructions(config)
