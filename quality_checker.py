#!/usr/bin/env python3
"""
Quality checker for AI tool projects before creating GitHub repositories.
Validates structure, files, and code quality.
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import re


class QualityChecker:
    """Check quality of generated AI tool projects."""
    
    REQUIRED_FILES = [
        "package.json",
        "vite.config.js",
        "tailwind.config.js",
        "postcss.config.js",
        "index.html",
        ".env.example",
        ".gitignore",
        "README.md",
        "vercel.json",
        "netlify.toml",
        "src/main.jsx",
        "src/App.jsx",
        "src/App.css",
    ]
    
    REQUIRED_PACKAGE_JSON_FIELDS = [
        "name",
        "version",
        "type",
        "scripts",
        "dependencies",
        "devDependencies",
    ]
    
    REQUIRED_SCRIPTS = ["dev", "build", "preview"]
    
    REQUIRED_DEPENDENCIES = [
        "react",
        "react-dom",
        "@anthropic-ai/sdk",
        "lucide-react",
    ]
    
    REQUIRED_DEV_DEPENDENCIES = [
        "@vitejs/plugin-react",
        "vite",
        "tailwindcss",
        "autoprefixer",
        "postcss",
    ]
    
    def __init__(self, project_path: Path):
        """Initialize with project path."""
        self.project_path = Path(project_path)
        self.errors = []
        self.warnings = []
        self.info = []
    
    def check_all(self) -> Tuple[bool, List[str], List[str], List[str]]:
        """Run all quality checks."""
        self.errors = []
        self.warnings = []
        self.info = []
        
        # Check project exists
        if not self.project_path.exists():
            self.errors.append(f"Project path does not exist: {self.project_path}")
            return False, self.errors, self.warnings, self.info
        
        # Run all checks
        self.check_required_files()
        self.check_package_json()
        self.check_readme()
        self.check_env_example()
        self.check_gitignore()
        self.check_source_files()
        self.check_deployment_configs()
        self.check_code_quality()
        
        is_valid = len(self.errors) == 0
        return is_valid, self.errors, self.warnings, self.info
    
    def check_required_files(self):
        """Check all required files exist."""
        for file_path in self.REQUIRED_FILES:
            full_path = self.project_path / file_path
            if not full_path.exists():
                self.errors.append(f"Missing required file: {file_path}")
            else:
                self.info.append(f"✓ Found: {file_path}")
    
    def check_package_json(self):
        """Validate package.json structure and content."""
        package_json_path = self.project_path / "package.json"
        if not package_json_path.exists():
            return
        
        try:
            with open(package_json_path, 'r') as f:
                package_json = json.load(f)
            
            # Check required fields
            for field in self.REQUIRED_PACKAGE_JSON_FIELDS:
                if field not in package_json:
                    self.errors.append(f"package.json missing field: {field}")
            
            # Check scripts
            scripts = package_json.get("scripts", {})
            for script in self.REQUIRED_SCRIPTS:
                if script not in scripts:
                    self.errors.append(f"package.json missing script: {script}")
            
            # Check dependencies
            dependencies = package_json.get("dependencies", {})
            for dep in self.REQUIRED_DEPENDENCIES:
                if dep not in dependencies:
                    self.warnings.append(f"package.json missing dependency: {dep}")
            
            # Check devDependencies
            dev_dependencies = package_json.get("devDependencies", {})
            for dep in self.REQUIRED_DEV_DEPENDENCIES:
                if dep not in dev_dependencies:
                    self.warnings.append(f"package.json missing devDependency: {dep}")
            
            # Check name format
            name = package_json.get("name", "")
            if not name or name == "your-project-name":
                self.warnings.append("package.json has placeholder name")
            
            self.info.append("✓ package.json structure is valid")
            
        except json.JSONDecodeError as e:
            self.errors.append(f"package.json is not valid JSON: {e}")
        except Exception as e:
            self.errors.append(f"Error reading package.json: {e}")
    
    def check_readme(self):
        """Check README quality."""
        readme_path = self.project_path / "README.md"
        if not readme_path.exists():
            self.errors.append("README.md is missing")
            return
        
        try:
            content = readme_path.read_text()
            
            # Check for title
            if not re.search(r'^#\s+.+', content, re.MULTILINE):
                self.warnings.append("README.md missing main title (# heading)")
            
            # Check for setup instructions
            if "setup" not in content.lower() and "install" not in content.lower():
                self.warnings.append("README.md missing setup/installation instructions")
            
            # Check for description
            if len(content.strip()) < 100:
                self.warnings.append("README.md seems too short")
            
            self.info.append("✓ README.md exists and has content")
            
        except Exception as e:
            self.errors.append(f"Error reading README.md: {e}")
    
    def check_env_example(self):
        """Check .env.example file."""
        env_example_path = self.project_path / ".env.example"
        if not env_example_path.exists():
            self.errors.append(".env.example is missing")
            return
        
        try:
            content = env_example_path.read_text()
            
            # Check for API key
            if "VITE_ANTHROPIC_API_KEY" not in content:
                self.errors.append(".env.example missing VITE_ANTHROPIC_API_KEY")
            
            # Check for placeholder
            if "your-api-key-here" not in content.lower():
                self.warnings.append(".env.example might be missing placeholder value")
            
            self.info.append("✓ .env.example is properly configured")
            
        except Exception as e:
            self.errors.append(f"Error reading .env.example: {e}")
    
    def check_gitignore(self):
        """Check .gitignore file."""
        gitignore_path = self.project_path / ".gitignore"
        if not gitignore_path.exists():
            self.errors.append(".gitignore is missing")
            return
        
        try:
            content = gitignore_path.read_text()
            
            # Check for common ignores
            required_ignores = ["node_modules", ".env"]
            for ignore in required_ignores:
                if ignore not in content:
                    self.warnings.append(f".gitignore missing: {ignore}")
            
            self.info.append("✓ .gitignore exists")
            
        except Exception as e:
            self.errors.append(f"Error reading .gitignore: {e}")
    
    def check_source_files(self):
        """Check source files quality."""
        app_jsx_path = self.project_path / "src" / "App.jsx"
        if not app_jsx_path.exists():
            return
        
        try:
            content = app_jsx_path.read_text()
            
            # Check for API integration
            if "anthropic" not in content.lower() and "claude" not in content.lower():
                self.warnings.append("App.jsx might be missing API integration")
            
            # Check for error handling
            if "catch" not in content or "error" not in content.lower():
                self.warnings.append("App.jsx might be missing error handling")
            
            # Check for loading state
            if "loading" not in content.lower():
                self.warnings.append("App.jsx might be missing loading state")
            
            # Check for React hooks
            if "useState" not in content:
                self.warnings.append("App.jsx might be missing React hooks")
            
            self.info.append("✓ App.jsx has basic structure")
            
        except Exception as e:
            self.errors.append(f"Error reading App.jsx: {e}")
    
    def check_deployment_configs(self):
        """Check deployment configuration files."""
        # Check Vercel config
        vercel_path = self.project_path / "vercel.json"
        if vercel_path.exists():
            try:
                with open(vercel_path, 'r') as f:
                    vercel_config = json.load(f)
                if "rewrites" not in vercel_config:
                    self.warnings.append("vercel.json missing rewrites configuration")
                else:
                    self.info.append("✓ vercel.json is configured")
            except Exception as e:
                self.warnings.append(f"vercel.json might be invalid: {e}")
        
        # Check Netlify config
        netlify_path = self.project_path / "netlify.toml"
        if netlify_path.exists():
            content = netlify_path.read_text()
            if "redirects" not in content:
                self.warnings.append("netlify.toml missing redirects configuration")
            else:
                self.info.append("✓ netlify.toml is configured")
    
    def check_code_quality(self):
        """Check code quality indicators."""
        # Check for TypeScript (optional but good)
        tsconfig_path = self.project_path / "tsconfig.json"
        if not tsconfig_path.exists():
            self.info.append("ℹ️  No TypeScript config (optional)")
        
        # Check for linting config (optional)
        eslint_path = self.project_path / ".eslintrc"
        if not eslint_path.exists():
            self.info.append("ℹ️  No ESLint config (optional)")
    
    def get_report(self) -> str:
        """Generate a quality report."""
        is_valid, errors, warnings, info = self.check_all()
        
        report = []
        report.append("=" * 60)
        report.append("Quality Check Report")
        report.append("=" * 60)
        report.append(f"Project: {self.project_path.name}")
        report.append(f"Status: {'✅ PASSED' if is_valid else '❌ FAILED'}")
        report.append("")
        
        if errors:
            report.append(f"❌ Errors ({len(errors)}):")
            for error in errors:
                report.append(f"   • {error}")
            report.append("")
        
        if warnings:
            report.append(f"⚠️  Warnings ({len(warnings)}):")
            for warning in warnings:
                report.append(f"   • {warning}")
            report.append("")
        
        if info:
            report.append(f"ℹ️  Info ({len(info)}):")
            for item in info:
                report.append(f"   • {item}")
            report.append("")
        
        report.append("=" * 60)
        
        return "\n".join(report)


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Check quality of AI tool project")
    parser.add_argument("project_path", help="Path to the project to check")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    checker = QualityChecker(args.project_path)
    is_valid, errors, warnings, info = checker.check_all()
    
    if args.json:
        output = {
            "valid": is_valid,
            "errors": errors,
            "warnings": warnings,
            "info": info,
        }
        print(json.dumps(output, indent=2))
    else:
        print(checker.get_report())
        if not is_valid:
            exit(1)


if __name__ == "__main__":
    main()



