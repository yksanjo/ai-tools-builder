"""CLI interface for AI Tools Builder."""

import click
from pathlib import Path
from .generator import ToolGenerator, AVAILABLE_TOOLS


@click.group()
def cli():
    """AI Tools Builder - Scaffold revenue-ready AI-powered frontend tools."""
    pass


@cli.command()
def list():
    """List all available AI tools."""
    click.echo("\n📦 Available AI Tools:\n")
    for tool_id, tool_info in AVAILABLE_TOOLS.items():
        click.echo(f"  {tool_id:30} - {tool_info['name']}")
    click.echo()


@cli.command()
@click.argument('tool_name')
@click.option('--output', '-o', default='.', help='Output directory for the generated tool')
def create(tool_name, output):
    """Create a new AI tool project.
    
    TOOL_NAME: Name of the tool to create (e.g., resume-optimizer)
    """
    if tool_name not in AVAILABLE_TOOLS:
        click.echo(f"❌ Error: Unknown tool '{tool_name}'", err=True)
        click.echo(f"\nAvailable tools:", err=True)
        for tool_id in AVAILABLE_TOOLS.keys():
            click.echo(f"  - {tool_id}", err=True)
        return
    
    output_path = Path(output)
    generator = ToolGenerator()
    
    try:
        generator.generate_tool(tool_name, output_path)
        click.echo(f"\n✅ Successfully created '{AVAILABLE_TOOLS[tool_name]['name']}' in {output_path}")
        click.echo(f"\n📝 Next steps:")
        click.echo(f"  1. cd {output_path / tool_name}")
        click.echo(f"  2. cp .env.example .env")
        click.echo(f"  3. Add your VITE_ANTHROPIC_API_KEY to .env")
        click.echo(f"  4. npm install")
        click.echo(f"  5. npm run dev")
        click.echo()
    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        raise click.Abort()


@cli.command()
@click.option('--output', '-o', default='./ai-tools', help='Output directory for all tools')
def create_all(output):
    """Create all 10 AI tool projects."""
    output_path = Path(output)
    generator = ToolGenerator()
    
    click.echo(f"\n🚀 Creating all 10 AI tools in {output_path}...\n")
    
    for tool_name in AVAILABLE_TOOLS.keys():
        try:
            click.echo(f"  Creating {tool_name}...", nl=False)
            generator.generate_tool(tool_name, output_path)
            click.echo(" ✅")
        except Exception as e:
            click.echo(f" ❌ Error: {e}")
    
    click.echo(f"\n✅ All tools created in {output_path}")
    click.echo(f"\n📝 Next steps:")
    click.echo(f"  1. cd into any tool directory")
    click.echo(f"  2. cp .env.example .env")
    click.echo(f"  3. Add your VITE_ANTHROPIC_API_KEY to .env")
    click.echo(f"  4. npm install")
    click.echo(f"  5. npm run dev")
    click.echo()


def main():
    """Entry point for the CLI."""
    cli()


if __name__ == '__main__':
    main()



