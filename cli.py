#!/usr/bin/env python3
"""CLI interface for nb2prod."""

import click
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

from parser import NotebookParser
from simple_analyze import CellAnalyzer

console = Console()


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Convert messy Jupyter notebooks to production-ready Python code."""
    pass


@cli.command()
@click.argument('notebook', type=click.Path(exists=True))
@click.option('--detailed', is_flag=True, help='Show detailed analysis')
def analyze(notebook, detailed):
    """Analyze a notebook for production readiness.

    Args:
        notebook: Path to the .ipynb file to analyze
        detailed: Show detailed analysis output
    """
    notebook_path = Path(notebook)

    # Header
    console.print()
    console.print("=" * 60, style="bold blue")
    console.print("nb2prod - Notebook Analysis", style="bold blue", justify="center")
    console.print("=" * 60, style="bold blue")
    console.print()

    # Parse notebook
    console.print(f"[bold cyan]🔍 Analyzing notebook:[/bold cyan] {notebook_path.name}")
    console.print()

    try:
        parser = NotebookParser(str(notebook_path))
        data = parser.parse()
    except Exception as e:
        console.print(f"[bold red]✗ Error parsing notebook:[/bold red] {e}")
        return

    # Display structure
    stats = data['stats']
    table = Table(title="📊 Notebook Structure", box=box.ROUNDED)
    table.add_column("Metric", style="cyan")
    table.add_column("Count", style="green", justify="right")

    table.add_row("Code cells", str(stats['code_cells']))
    table.add_row("Markdown cells", str(stats['markdown_cells']))
    table.add_row("Empty cells", str(stats['empty_cells']))
    table.add_row("Total cells", str(stats['total_cells']))

    console.print(table)
    console.print()

    # Analyze code
    code_cells = parser.get_code_cells()

    if not code_cells:
        console.print("[yellow]⚠️  No code cells found in notebook[/yellow]")
        return

    analyzer = CellAnalyzer(code_cells)
    results = analyzer.analyze_all()
    summary = analyzer.get_summary()

    # Display analysis summary
    analysis_table = Table(title="📦 Code Analysis", box=box.ROUNDED)
    analysis_table.add_column("Metric", style="cyan")
    analysis_table.add_column("Count", style="green", justify="right")

    analysis_table.add_row("Imports detected", str(summary['total_imports']))
    analysis_table.add_row("Variables defined", str(summary['total_variables']))
    analysis_table.add_row("Functions defined", str(summary['total_functions']))
    analysis_table.add_row("Hardcoded values", str(summary['hardcoded_values_count']))

    console.print(analysis_table)
    console.print()

    # Show imports if detailed
    if detailed and summary['imports_list']:
        console.print("[bold cyan]📚 Imports:[/bold cyan]")
        for imp in summary['imports_list']:
            console.print(f"  • {imp}")
        console.print()

    # Display issues
    issues = summary['issues']
    if issues:
        console.print(f"[bold yellow]⚠️  Issues Found ({len(issues)}):[/bold yellow]")
        console.print()

        for issue in issues:
            issue_type = issue['type']

            if issue_type == 'execution_order':
                console.print(Panel(
                    f"[yellow]{issue['message']}[/yellow]",
                    title="Execution Order Issue",
                    border_style="yellow"
                ))

            elif issue_type == 'hardcoded_paths':
                cells_str = ', '.join(map(str, issue['cells'][:10]))
                if len(issue['cells']) > 10:
                    cells_str += f" ... and {len(issue['cells']) - 10} more"

                console.print(Panel(
                    f"[yellow]{issue['message']}[/yellow]\n"
                    f"Cells: {cells_str}",
                    title="Hardcoded Paths Detected",
                    border_style="yellow"
                ))

            elif issue_type == 'no_functions':
                console.print(Panel(
                    f"[yellow]{issue['message']}[/yellow]\n"
                    "Consider organizing code into reusable functions.",
                    title="Code Organization",
                    border_style="yellow"
                ))

            console.print()
    else:
        console.print("[bold green]✓ No major issues found![/bold green]")
        console.print()

    # Calculate production readiness score
    score = 10
    for issue in issues:
        if issue['type'] == 'execution_order':
            score -= 2
        elif issue['type'] == 'hardcoded_paths':
            score -= 2
        elif issue['type'] == 'no_functions':
            score -= 3

    score = max(0, min(10, score))

    # Determine color and emoji based on score
    if score >= 8:
        score_color = "green"
        emoji = "🎉"
        message = "Excellent! This notebook is production-ready."
    elif score >= 5:
        score_color = "yellow"
        emoji = "⚠️"
        message = "Moderate. Some improvements needed."
    else:
        score_color = "red"
        emoji = "❌"
        message = "Needs work. Multiple issues to address."

    # Display score
    score_panel = Panel(
        f"[bold {score_color}]{score}/10[/bold {score_color}]\n{message}",
        title=f"{emoji} Production Readiness Score",
        border_style=score_color,
        box=box.DOUBLE
    )
    console.print(score_panel)
    console.print()

    # Show detailed cell-by-cell analysis if requested
    if detailed:
        console.print("[bold cyan]📋 Detailed Cell Analysis:[/bold cyan]")
        console.print()

        for analysis in results:
            if analysis['variables_defined'] or analysis['imports'] or analysis['functions_defined']:
                cell_info = []

                if analysis['imports']:
                    cell_info.append(f"Imports: {', '.join(analysis['imports'][:3])}")
                if analysis['variables_defined']:
                    vars_list = list(analysis['variables_defined'])[:3]
                    cell_info.append(f"Defines: {', '.join(vars_list)}")
                if analysis['functions_defined']:
                    cell_info.append(f"Functions: {', '.join(analysis['functions_defined'])}")
                if analysis['depends_on']:
                    deps = [str(d['cell_index']) for d in analysis['depends_on'][:3]]
                    cell_info.append(f"Depends on cells: {', '.join(deps)}")

                console.print(f"  [cyan]Cell {analysis['index']}:[/cyan] {' | '.join(cell_info)}")

        console.print()

    console.print("=" * 60, style="bold blue")
    console.print()


if __name__ == '__main__':
    cli()
