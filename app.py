#!/usr/bin/env python3
"""Streamlit web interface for nb2prod."""

import streamlit as st
import tempfile
import shutil
from pathlib import Path
import os
import zipfile
from io import BytesIO

from nb2prod.parser import NotebookParser
from nb2prod.analyzer import CellAnalyzer
from nb2prod.grouper import CellGrouper
from nb2prod.extractor import FunctionExtractor
from nb2prod.generator import ProjectGenerator


def create_zip_from_directory(directory_path):
    """Create a ZIP file from a directory."""
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, directory_path)
                zip_file.write(file_path, arcname)
    zip_buffer.seek(0)
    return zip_buffer


def analyze_notebook(notebook_path):
    """Analyze a notebook and return results."""
    try:
        parser = NotebookParser(str(notebook_path))
        data = parser.parse()
        code_cells = parser.get_code_cells()
        stats = data["stats"]

        if not code_cells:
            return None, "No code cells found in notebook"

        analyzer = CellAnalyzer(code_cells)
        results = analyzer.analyze_all()
        summary = analyzer.get_summary()

        # Calculate production readiness score
        issues = summary["issues"]
        actionable_issues = []

        for issue in issues:
            issue_type = issue["type"]
            if issue_type == "no_functions":
                markdown_ratio = stats["markdown_cells"] / max(stats["total_cells"], 1)
                if markdown_ratio > 0.3:
                    continue
            actionable_issues.append(issue)

        score = 10
        for issue in actionable_issues:
            if issue["type"] == "execution_order":
                score -= 4
            elif issue["type"] == "hardcoded_paths":
                score -= 2
            elif issue["type"] == "no_functions":
                score -= 2

        score = max(0, min(10, score))

        return {
            "stats": stats,
            "summary": summary,
            "results": results,
            "actionable_issues": actionable_issues,
            "score": score,
            "code_cells": code_cells,
        }, None

    except Exception as e:
        return None, str(e)


def extract_functions_from_notebook(notebook_path):
    """Extract functions from a notebook."""
    try:
        parser = NotebookParser(str(notebook_path))
        data = parser.parse()
        code_cells = parser.get_code_cells()
        stats = data["stats"]

        if not code_cells:
            return None, "No code cells found in notebook"

        analyzer = CellAnalyzer(code_cells)
        results = analyzer.analyze_all()
        summary = analyzer.get_summary()

        # Check for critical issues
        has_critical_issues = (
            len([i for i in summary["issues"] if i["type"] == "execution_order"]) > 1
        )

        if has_critical_issues:
            return None, "Notebook has critical execution order issues. Fix these first."

        # Group cells
        grouper = CellGrouper(code_cells, results, notebook_stats=stats)

        if grouper.is_educational:
            return None, "This appears to be an educational/tutorial notebook, not suitable for extraction."

        groups = grouper.group_cells()

        if not groups:
            return None, "No extractable functions found in this notebook."

        # Extract functions
        extractor = FunctionExtractor(code_cells, groups)
        functions = extractor.extract_functions()

        return {
            "functions": functions,
            "summary": summary,
        }, None

    except Exception as e:
        return None, str(e)


def convert_notebook(notebook_path, output_dir, enhance=False):
    """Convert notebook to production project."""
    try:
        parser = NotebookParser(str(notebook_path))
        data = parser.parse()
        code_cells = parser.get_code_cells()
        stats = data["stats"]

        if not code_cells:
            return None, "No code cells found in notebook"

        analyzer = CellAnalyzer(code_cells)
        results = analyzer.analyze_all()
        summary = analyzer.get_summary()

        # Check for critical issues
        has_critical_issues = (
            len([i for i in summary["issues"] if i["type"] == "execution_order"]) > 1
        )

        if has_critical_issues:
            return None, "Notebook has critical execution order issues."

        # Group cells
        grouper = CellGrouper(code_cells, results, notebook_stats=stats)

        if grouper.is_educational:
            return None, "Educational notebook detected. Not suitable for conversion."

        groups = grouper.group_cells()

        if not groups:
            return None, "No functions to convert."

        # Extract functions
        extractor = FunctionExtractor(code_cells, groups)
        functions = extractor.extract_functions()

        # Enhance with LLM if requested
        if enhance:
            try:
                from nb2prod.llm_refactor import LLMRefactor
                refactor = LLMRefactor()
                functions = refactor.enhance_functions(functions)
            except Exception as e:
                return None, f"Enhancement failed: {str(e)}"

        # Generate project
        generator = ProjectGenerator(
            functions=functions,
            imports=summary["imports_list"],
            output_dir=output_dir,
            use_llm_main=enhance,
        )

        generator.generate_project()

        return output_dir, None

    except Exception as e:
        return None, str(e)


def main():
    st.set_page_config(
        page_title="nb2prod - Notebook to Production",
        page_icon="📓",
        layout="wide"
    )

    st.title("📓 nb2prod - Notebook to Production")
    st.markdown("Convert messy Jupyter notebooks to production-ready Python code using AI-powered analysis")

    # Sidebar for configuration
    st.sidebar.header("⚙️ Settings")

    # API Key input for enhancement
    use_enhancement = st.sidebar.checkbox("Enable AI Enhancement", help="Use Claude AI to improve functions (requires API key)")
    api_key = None
    if use_enhancement:
        api_key = st.sidebar.text_input("Anthropic API Key", type="password", help="Required for AI enhancement")
        if api_key:
            os.environ["ANTHROPIC_API_KEY"] = api_key

    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.markdown("""
    nb2prod analyzes Jupyter notebooks and converts them into production-ready Python projects.

    **Features:**
    - Production readiness analysis
    - Function extraction
    - AI-powered enhancement
    - Complete project generation
    """)

    # File uploader
    uploaded_file = st.file_uploader(
        "Upload a Jupyter Notebook (.ipynb)",
        type=["ipynb"],
        help="Select a .ipynb file to analyze and convert"
    )

    if uploaded_file is not None:
        # Save uploaded file to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".ipynb") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_path = tmp_file.name

        # Create tabs for different operations
        tab1, tab2, tab3 = st.tabs(["📊 Analysis", "🔍 Extract Functions", "🚀 Convert to Project"])

        # Tab 1: Analysis
        with tab1:
            st.header("Notebook Analysis")

            with st.spinner("Analyzing notebook..."):
                analysis_result, error = analyze_notebook(tmp_path)

            if error:
                st.error(f"Error: {error}")
            elif analysis_result:
                stats = analysis_result["stats"]
                summary = analysis_result["summary"]
                score = analysis_result["score"]
                issues = analysis_result["actionable_issues"]

                # Display statistics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Cells", stats["total_cells"])
                with col2:
                    st.metric("Code Cells", stats["code_cells"])
                with col3:
                    st.metric("Functions", summary["total_functions"])
                with col4:
                    st.metric("Imports", summary["total_imports"])

                st.markdown("---")

                # Production readiness score
                st.subheader("Production Readiness Score")

                score_color = "green" if score >= 8 else ("orange" if score >= 6 else "red")
                st.markdown(f"### :{score_color}[{score}/10]")

                if score >= 8:
                    st.success("Ready for production use with minimal changes.")
                elif score >= 6:
                    st.warning("Requires improvements before production deployment.")
                else:
                    st.error("Significant refactoring needed for production use.")

                # Display issues
                if issues:
                    st.markdown("---")
                    st.subheader("Issues Requiring Attention")

                    for issue in issues:
                        issue_type = issue["type"]

                        if issue_type == "execution_order":
                            st.warning(f"⚠️ **Execution Order Problem**: {issue['message']}")
                            st.caption("Fix: Reorder cells or ensure all dependencies are defined before use.")

                        elif issue_type == "hardcoded_paths":
                            cells_str = ", ".join(map(str, issue["cells"][:10]))
                            if len(issue["cells"]) > 10:
                                cells_str += f" ... and {len(issue['cells']) - 10} more"
                            st.warning(f"⚠️ **Hardcoded Paths**: Found in cells: {cells_str}")
                            st.caption("Fix: Move paths to a configuration file or use relative paths.")

                        elif issue_type == "no_functions":
                            st.warning(f"⚠️ **Code Organization**: {issue['message']}")
                            st.caption("Fix: Extract logical blocks into functions with clear inputs/outputs.")
                else:
                    st.success("✅ No critical issues detected!")

                # Display imports
                if summary["imports_list"]:
                    st.markdown("---")
                    st.subheader("Dependencies")
                    st.code(", ".join(summary["imports_list"]))

        # Tab 2: Extract Functions
        with tab2:
            st.header("Function Extraction")

            with st.spinner("Extracting functions..."):
                extract_result, error = extract_functions_from_notebook(tmp_path)

            if error:
                st.error(f"Error: {error}")
            elif extract_result:
                functions = extract_result["functions"]

                st.success(f"Found {len(functions)} function candidate(s)")

                show_code = st.checkbox("Show generated code", value=True)

                for i, func in enumerate(functions, 1):
                    with st.expander(f"Function {i}: {func['name']}", expanded=(i == 1)):
                        st.code(func['signature'], language="python")

                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"**Category:** {func['category']}")
                            st.markdown(f"**Source cells:** {', '.join(map(str, func['cells']))}")
                        with col2:
                            if func['parameters']:
                                st.markdown(f"**Parameters:** {', '.join(func['parameters'])}")
                            if func['returns']:
                                st.markdown(f"**Returns:** {', '.join(func['returns'])}")

                        if show_code:
                            st.markdown("**Generated Code:**")
                            st.code(func['full_code'], language="python")

        # Tab 3: Convert to Project
        with tab3:
            st.header("Convert to Production Project")

            if use_enhancement and not api_key:
                st.warning("Please enter your Anthropic API Key in the sidebar to enable AI enhancement.")

            if st.button("🚀 Generate Project", type="primary"):
                with tempfile.TemporaryDirectory() as tmp_output:
                    with st.spinner("Converting notebook to production project..."):
                        if use_enhancement:
                            st.info("Using AI enhancement... This may take a moment.")

                        output_dir, error = convert_notebook(
                            tmp_path,
                            tmp_output,
                            enhance=use_enhancement and api_key is not None
                        )

                    if error:
                        st.error(f"Error: {error}")
                    elif output_dir:
                        st.success("Project generated successfully!")

                        # Create ZIP file
                        zip_buffer = create_zip_from_directory(output_dir)

                        # Offer download
                        st.download_button(
                            label="📥 Download Project (ZIP)",
                            data=zip_buffer,
                            file_name=f"{Path(uploaded_file.name).stem}_project.zip",
                            mime="application/zip"
                        )

                        st.markdown("---")
                        st.subheader("Next Steps")
                        st.markdown("""
                        1. Download and extract the ZIP file
                        2. Navigate to the project directory
                        3. Install dependencies: `pip install -r requirements.txt`
                        4. Run the project: `python main.py`
                        """)

                        # Show project structure
                        st.markdown("---")
                        st.subheader("Project Structure")

                        structure = []
                        for root, dirs, files in os.walk(output_dir):
                            level = root.replace(output_dir, '').count(os.sep)
                            indent = ' ' * 2 * level
                            structure.append(f"{indent}{os.path.basename(root)}/")
                            subindent = ' ' * 2 * (level + 1)
                            for file in files:
                                structure.append(f"{subindent}{file}")

                        st.text('\n'.join(structure))

        # Clean up temp file
        try:
            os.unlink(tmp_path)
        except:
            pass


if __name__ == "__main__":
    main()
