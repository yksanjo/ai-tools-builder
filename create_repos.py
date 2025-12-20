#!/usr/bin/env python3
"""
Create GitHub repositories for all 10 AI tools with quality checks.
This script:
1. Generates all 10 AI tools
2. Validates each tool's quality
3. Creates GitHub repositories
4. Sets up descriptions, topics, and badges
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import argparse

# Add parent directory to path to import quality_checker
sys.path.insert(0, str(Path(__file__).parent))
from quality_checker import QualityChecker

# Import generator - try package import first, then direct import
try:
    from ai_tools_builder.generator import ToolGenerator, AVAILABLE_TOOLS
except ImportError:
    # Fallback to direct import if package not installed
    generator_path = Path(__file__).parent / "src" / "ai_tools_builder" / "generator.py"
    if generator_path.exists():
        import importlib.util
        spec = importlib.util.spec_from_file_location("generator", generator_path)
        generator_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(generator_module)
        ToolGenerator = generator_module.ToolGenerator
        AVAILABLE_TOOLS = generator_module.AVAILABLE_TOOLS
    else:
        raise ImportError("Could not find generator module")

# Import GitHub automation (from parent directory)
parent_dir = Path(__file__).parent.parent
automation_path = parent_dir / "github-repo-automation" / "github-repo-automation.py"
if automation_path.exists():
    sys.path.insert(0, str(automation_path.parent))
    import importlib.util
    spec = importlib.util.spec_from_file_location("github_repo_automation", automation_path)
    github_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(github_module)
    GitHubRepoAutomation = github_module.GitHubRepoAutomation
    BadgeGenerator = github_module.BadgeGenerator
    ReadmeUpdater = github_module.ReadmeUpdater
else:
    print("⚠️  Warning: github-repo-automation not found. GitHub repo creation will be limited.")
    GitHubRepoAutomation = None


# Tool metadata for GitHub repos
TOOL_METADATA = {
    "prompt-testing-lab": {
        "description": "🧪 AI Prompt Testing Lab - Interactive tool to test prompts across scenarios, compare outputs, and save/version your best prompts. Built-in templates for common use cases.",
        "topics": ["ai", "prompt-engineering", "claude", "anthropic", "testing", "react", "vite", "frontend", "ai-tools"],
    },
    "meeting-action-extractor": {
        "description": "📝 Meeting Notes → Action Items Extractor - Paste meeting transcripts, AI extracts action items, assigns priority, suggests owners, and formats for Slack/email/project tools.",
        "topics": ["ai", "meetings", "productivity", "action-items", "claude", "anthropic", "react", "vite", "ai-tools"],
    },
    "resume-optimizer": {
        "description": "📄 Resume ATS Optimizer - Upload resume and job description, AI scores ATS compatibility, suggests keyword improvements, and shows before/after comparison.",
        "topics": ["ai", "resume", "ats", "job-search", "career", "claude", "anthropic", "react", "vite", "ai-tools"],
    },
    "social-media-multiplier": {
        "description": "📱 Social Media Post Multiplier - Input one idea/post, AI generates versions for Twitter, LinkedIn, Instagram, Facebook with optimal formatting and hashtags.",
        "topics": ["ai", "social-media", "content-creation", "marketing", "claude", "anthropic", "react", "vite", "ai-tools"],
    },
    "contract-analyzer": {
        "description": "⚖️ Contract Red Flag Analyzer - Paste contract text, AI highlights risky clauses, unfavorable terms, missing protections, and explains implications in plain English.",
        "topics": ["ai", "legal", "contracts", "analysis", "claude", "anthropic", "react", "vite", "ai-tools"],
    },
    "email-response-generator": {
        "description": "✉️ Email Response Generator Pro - Input received email + context, AI generates 3-5 response options (professional, friendly, firm, brief). Learns your writing style.",
        "topics": ["ai", "email", "productivity", "writing", "claude", "anthropic", "react", "vite", "ai-tools"],
    },
    "sales-outreach-personalizer": {
        "description": "💼 Sales Outreach Personalizer - Input prospect LinkedIn/company info + your offer, AI generates personalized cold email with multiple variants and subject lines.",
        "topics": ["ai", "sales", "outreach", "email", "claude", "anthropic", "react", "vite", "ai-tools"],
    },
    "product-description-generator": {
        "description": "🛍️ Product Description Generator for E-commerce - Input product details, AI generates SEO-optimized descriptions, bullet points, meta descriptions in brand voice.",
        "topics": ["ai", "ecommerce", "seo", "product-descriptions", "claude", "anthropic", "react", "vite", "ai-tools"],
    },
    "interview-prep-coach": {
        "description": "🎯 Interview Question Prep Coach - Input job description, AI generates likely interview questions, provides sample answers, offers feedback on practice responses.",
        "topics": ["ai", "interviews", "career", "job-prep", "claude", "anthropic", "react", "vite", "ai-tools"],
    },
    "seo-content-optimizer": {
        "description": "🔍 Blog Post → SEO Content Optimizer - Paste blog draft, AI suggests title variations, meta descriptions, heading structure, internal linking opportunities, keyword improvements.",
        "topics": ["ai", "seo", "content-marketing", "blogging", "claude", "anthropic", "react", "vite", "ai-tools"],
    },
}


class RepoCreator:
    """Create GitHub repositories for AI tools with quality checks."""
    
    def __init__(self, github_token: Optional[str] = None, github_username: Optional[str] = None, output_dir: Path = None):
        """Initialize repo creator."""
        self.github_token = github_token or os.getenv("GITHUB_TOKEN")
        self.github_username = github_username or os.getenv("GITHUB_USERNAME")
        self.output_dir = Path(output_dir) if output_dir else Path.cwd() / "ai-tools-generated"
        self.output_dir.mkdir(exist_ok=True)
        
        self.generator = ToolGenerator()
        
        if GitHubRepoAutomation and self.github_token:
            self.github = GitHubRepoAutomation(token=self.github_token)
        else:
            self.github = None
            if not self.github_token:
                print("⚠️  Warning: No GITHUB_TOKEN found. GitHub repo creation will be skipped.")
    
    def generate_tool(self, tool_name: str) -> Tuple[bool, Path]:
        """Generate a single tool and return success status and path."""
        print(f"\n{'='*60}")
        print(f"🔨 Generating: {tool_name}")
        print(f"{'='*60}")
        
        try:
            tool_path = self.generator.generate_tool(tool_name, self.output_dir)
            print(f"✅ Generated: {tool_path}")
            return True, tool_path
        except Exception as e:
            print(f"❌ Failed to generate {tool_name}: {e}")
            return False, None
    
    def validate_tool(self, tool_path: Path) -> Tuple[bool, List[str], List[str]]:
        """Validate tool quality."""
        print(f"\n🔍 Validating: {tool_path.name}")
        
        checker = QualityChecker(tool_path)
        is_valid, errors, warnings, info = checker.check_all()
        
        if is_valid:
            print(f"✅ Quality check PASSED")
        else:
            print(f"❌ Quality check FAILED")
            print(f"   Errors: {len(errors)}")
            for error in errors:
                print(f"     • {error}")
        
        if warnings:
            print(f"⚠️  Warnings: {len(warnings)}")
            for warning in warnings[:3]:  # Show first 3
                print(f"     • {warning}")
        
        return is_valid, errors, warnings
    
    def create_github_repo(self, tool_name: str, tool_path: Path, description: str, topics: List[str]) -> bool:
        """Create GitHub repository and configure it."""
        if not self.github:
            print("⚠️  Skipping GitHub repo creation (no token)")
            return False
        
        repo_name = tool_name.replace("-", "-")
        repo_full_name = f"{self.github_username}/{repo_name}"
        
        print(f"\n📦 Creating GitHub repo: {repo_full_name}")
        
        try:
            # Check if repo already exists
            try:
                existing_repo = self.github.get_repo_info(self.github_username, repo_name)
                print(f"⚠️  Repository already exists: {repo_full_name}")
                print(f"   Updating description and topics...")
                
                # Update description
                self.github.update_description(self.github_username, repo_name, description)
                
                # Update topics
                current_topics = set(existing_repo.get("topics", []))
                merged_topics = list(current_topics | set(topics))
                self.github.update_topics(self.github_username, repo_name, merged_topics)
                
                # Update badges
                repo_info = self.github.get_repo_info(self.github_username, repo_name)
                badge_gen = BadgeGenerator(self.github_username, repo_name, repo_info)
                badges = badge_gen.generate_badges()
                readme_content = self.github.get_readme(self.github_username, repo_name)
                if readme_content:
                    updated_readme = ReadmeUpdater.add_badges_to_readme(readme_content, badges)
                    if updated_readme != readme_content:
                        self.github.update_readme(self.github_username, repo_name, updated_readme)
                
                return True
                
            except Exception as e:
                if "404" in str(e) or "not found" in str(e).lower():
                    # Repo doesn't exist, need to create it
                    print(f"   Repository doesn't exist. You'll need to create it manually on GitHub.")
                    print(f"   Then run this script again to configure it.")
                    print(f"\n   To create manually:")
                    print(f"   1. Go to https://github.com/new")
                    print(f"   2. Repository name: {repo_name}")
                    print(f"   3. Description: {description}")
                    print(f"   4. Choose Public")
                    print(f"   5. DO NOT initialize with README (we have one)")
                    print(f"   6. Click 'Create repository'")
                    return False
                else:
                    raise
            
        except Exception as e:
            print(f"❌ Failed to create/update GitHub repo: {e}")
            return False
    
    def initialize_git_repo(self, tool_path: Path) -> bool:
        """Initialize git repository and prepare for push."""
        print(f"\n🔧 Initializing git repository...")
        
        try:
            # Check if already a git repo
            if (tool_path / ".git").exists():
                print(f"   Git repository already exists")
                return True
            
            # Initialize git
            subprocess.run(["git", "init"], cwd=tool_path, check=True, capture_output=True)
            subprocess.run(["git", "branch", "-M", "main"], cwd=tool_path, check=True, capture_output=True)
            
            # Add all files
            subprocess.run(["git", "add", "."], cwd=tool_path, check=True, capture_output=True)
            
            # Create initial commit
            commit_message = f"Initial commit: {tool_path.name}\n\n- Generated with ai-tools-builder\n- React + Vite + Tailwind setup\n- Claude API integration"
            subprocess.run(
                ["git", "commit", "-m", commit_message],
                cwd=tool_path,
                check=True,
                capture_output=True
            )
            
            print(f"✅ Git repository initialized")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to initialize git: {e}")
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def process_all_tools(self, skip_validation: bool = False, skip_github: bool = False, skip_git: bool = False):
        """Process all 10 tools."""
        results = {
            "generated": [],
            "validated": [],
            "failed_validation": [],
            "github_configured": [],
            "git_initialized": [],
        }
        
        print("🚀 AI Tools Repository Creator")
        print("=" * 60)
        print(f"Output directory: {self.output_dir}")
        print(f"Tools to process: {len(AVAILABLE_TOOLS)}")
        print("=" * 60)
        
        for tool_name in AVAILABLE_TOOLS.keys():
            # Generate
            success, tool_path = self.generate_tool(tool_name)
            if not success:
                continue
            results["generated"].append(tool_name)
            
            # Validate
            if not skip_validation:
                is_valid, errors, warnings = self.validate_tool(tool_path)
                if is_valid:
                    results["validated"].append(tool_name)
                else:
                    results["failed_validation"].append(tool_name)
                    print(f"⚠️  Skipping GitHub setup for {tool_name} due to validation failures")
                    continue
            else:
                results["validated"].append(tool_name)
            
            # Initialize git
            if not skip_git:
                if self.initialize_git_repo(tool_path):
                    results["git_initialized"].append(tool_name)
            
            # Create GitHub repo
            if not skip_github and tool_name in TOOL_METADATA:
                metadata = TOOL_METADATA[tool_name]
                if self.create_github_repo(tool_name, tool_path, metadata["description"], metadata["topics"]):
                    results["github_configured"].append(tool_name)
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 Summary")
        print("=" * 60)
        print(f"✅ Generated: {len(results['generated'])}/{len(AVAILABLE_TOOLS)}")
        print(f"✅ Validated: {len(results['validated'])}/{len(results['generated'])}")
        if results["failed_validation"]:
            print(f"❌ Failed validation: {len(results['failed_validation'])}")
            for tool in results["failed_validation"]:
                print(f"   • {tool}")
        print(f"✅ Git initialized: {len(results['git_initialized'])}/{len(results['validated'])}")
        print(f"✅ GitHub configured: {len(results['github_configured'])}/{len(results['validated'])}")
        print("=" * 60)
        
        return results


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Create GitHub repositories for all 10 AI tools with quality checks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate, validate, and prepare all tools
  python3 create_repos.py
  
  # Skip validation (faster, but not recommended)
  python3 create_repos.py --skip-validation
  
  # Skip GitHub repo creation (just generate and validate)
  python3 create_repos.py --skip-github
  
  # Custom output directory
  python3 create_repos.py --output ./my-tools
        """
    )
    
    parser.add_argument("--output", "-o", help="Output directory for generated tools", default=None)
    parser.add_argument("--token", help="GitHub token (or set GITHUB_TOKEN env var)")
    parser.add_argument("--username", help="GitHub username (or set GITHUB_USERNAME env var)")
    parser.add_argument("--skip-validation", action="store_true", help="Skip quality validation")
    parser.add_argument("--skip-github", action="store_true", help="Skip GitHub repo creation")
    parser.add_argument("--skip-git", action="store_true", help="Skip git initialization")
    
    args = parser.parse_args()
    
    # Check for GitHub token
    if not args.skip_github:
        token = args.token or os.getenv("GITHUB_TOKEN")
        if not token:
            print("⚠️  Warning: No GitHub token provided.")
            print("   Set GITHUB_TOKEN environment variable or use --token flag")
            print("   GitHub repo creation will be skipped")
            print("   Get token at: https://github.com/settings/tokens\n")
            args.skip_github = True
    
    creator = RepoCreator(
        github_token=args.token,
        github_username=args.username,
        output_dir=args.output
    )
    
    creator.process_all_tools(
        skip_validation=args.skip_validation,
        skip_github=args.skip_github,
        skip_git=args.skip_git
    )


if __name__ == "__main__":
    main()

