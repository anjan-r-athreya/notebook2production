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
    console.print("=" * 60, style="bold")
    console.print("NOTEBOOK ANALYSIS", style="bold", justify="center")
    console.print("=" * 60, style="bold")
    console.print()

    # Parse notebook
    console.print(f"[bold]Analyzing:[/bold] {notebook_path.name}")
    console.print()

    try:
        parser = NotebookParser(str(notebook_path))
        data = parser.parse()
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        return

    # Analyze code
    code_cells = parser.get_code_cells()
    stats = data['stats']

    if not code_cells:
        console.print("[yellow]No code cells found in notebook[/yellow]")
        return

    analyzer = CellAnalyzer(code_cells)
    results = analyzer.analyze_all()
    summary = analyzer.get_summary()

    # Display compact summary
    console.print(f"[dim]Code cells: {stats['code_cells']} | "
                  f"Functions: {summary['total_functions']} | "
                  f"Imports: {summary['total_imports']}[/dim]")
    console.print()

    # Show imports if detailed
    if detailed and summary['imports_list']:
        console.print("[bold]Dependencies:[/bold]")
        for imp in summary['imports_list']:
            console.print(f"  - {imp}")
        console.print()

    # Filter and display only actionable issues
    issues = summary['issues']
    actionable_issues = []

    for issue in issues:
        issue_type = issue['type']

        # Skip "no functions" for notebooks with mostly markdown (likely educational)
        if issue_type == 'no_functions':
            markdown_ratio = stats['markdown_cells'] / max(stats['total_cells'], 1)
            if markdown_ratio > 0.3:  # More than 30% markdown = likely educational
                continue

        actionable_issues.append(issue)

    if actionable_issues:
        console.print(f"[bold]Issues Requiring Attention:[/bold]")
        console.print()

        for issue in actionable_issues:
            issue_type = issue['type']

            if issue_type == 'execution_order':
                console.print(Panel(
                    f"[yellow]{issue['message']}[/yellow]\n\n"
                    f"[dim]Impact:[/dim] This cell depends on variables defined in a later cell. "
                    f"The notebook will fail if cells are run sequentially from top to bottom.\n\n"
                    f"[dim]Fix:[/dim] Reorder cells or ensure all dependencies are defined before use.",
                    title="Execution Order Problem",
                    border_style="yellow"
                ))

            elif issue_type == 'hardcoded_paths':
                cells_str = ', '.join(map(str, issue['cells'][:10]))
                if len(issue['cells']) > 10:
                    cells_str += f" ... and {len(issue['cells']) - 10} more"

                console.print(Panel(
                    f"[yellow]Found hardcoded file paths in cells: {cells_str}[/yellow]\n\n"
                    f"[dim]Impact:[/dim] Code won't be portable across different environments.\n\n"
                    f"[dim]Fix:[/dim] Move paths to a configuration file or use relative paths.",
                    title="Configuration Issue",
                    border_style="yellow"
                ))

            elif issue_type == 'no_functions':
                console.print(Panel(
                    f"[yellow]{issue['message']}[/yellow]\n\n"
                    f"[dim]Impact:[/dim] Code is harder to test, reuse, and maintain.\n\n"
                    f"[dim]Fix:[/dim] Extract logical blocks into functions with clear inputs/outputs.",
                    title="Code Organization",
                    border_style="yellow"
                ))

            console.print()
    else:
        console.print("[green]No critical issues detected.[/green]")
        console.print()

    # Calculate production readiness score based on actionable issues only
    score = 10
    for issue in actionable_issues:
        if issue['type'] == 'execution_order':
            score -= 4  # Critical issue
        elif issue['type'] == 'hardcoded_paths':
            score -= 2  # Moderate issue
        elif issue['type'] == 'no_functions':
            score -= 2  # Moderate issue

    score = max(0, min(10, score))

    # Determine assessment based on score
    if score >= 8:
        score_color = "green"
        assessment = "Ready for production use with minimal changes."
    elif score >= 6:
        score_color = "yellow"
        assessment = "Requires improvements before production deployment."
    else:
        score_color = "red"
        assessment = "Significant refactoring needed for production use."

    # Display score only if there are actionable issues
    if actionable_issues:
        score_panel = Panel(
            f"[bold {score_color}]{score}/10[/bold {score_color}]\n\n{assessment}",
            title="Production Readiness Assessment",
            border_style=score_color,
            box=box.ROUNDED
        )
        console.print(score_panel)
        console.print()

    # Show detailed cell-by-cell analysis if requested
    if detailed:
        console.print("[bold]Cell Dependencies:[/bold]")
        console.print()

        has_dependencies = False
        for analysis in results:
            if analysis['depends_on'] or analysis['external_dependencies']:
                has_dependencies = True
                cell_info = []

                if analysis['external_dependencies']:
                    deps_list = list(analysis['external_dependencies'])[:5]
                    cell_info.append(f"Uses: {', '.join(deps_list)}")

                if analysis['depends_on']:
                    deps = [str(d['cell_index']) for d in analysis['depends_on'][:3]]
                    cell_info.append(f"From cells: {', '.join(deps)}")

                if cell_info:
                    console.print(f"  Cell {analysis['index']}: {' | '.join(cell_info)}")

        if not has_dependencies:
            console.print("  [dim]No cross-cell dependencies detected.[/dim]")

        console.print()

    console.print("=" * 60, style="bold")
    console.print()


if __name__ == '__main__':
    cli()
