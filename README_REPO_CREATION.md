# Creating GitHub Repositories for AI Tools

## Quick Start

### 1. Set Up GitHub Token

```bash
export GITHUB_TOKEN=ghp_your_token_here
export GITHUB_USERNAME=your-username
```

Get token at: https://github.com/settings/tokens (needs `repo` scope)

### 2. Run the Creation Script

```bash
cd ai-tools-builder
python3 create_repos.py
```

This will:
- ✅ Generate all 10 AI tools
- ✅ Validate quality of each tool
- ✅ Initialize git repositories
- ✅ Create/configure GitHub repositories
- ✅ Add descriptions, topics, and badges

## What Gets Created

For each of the 10 tools:

1. **Local Project** - Full React + Vite + Tailwind project
2. **Git Repository** - Initialized with initial commit
3. **GitHub Repository** - Created and configured with:
   - Professional description
   - Relevant topics/tags
   - README badges
   - Proper structure

## Quality Checks

Each tool is validated for:
- ✅ All required files present
- ✅ Valid package.json structure
- ✅ Proper API integration
- ✅ Error handling
- ✅ Documentation quality
- ✅ Deployment configs

## Manual Process

If you prefer step-by-step:

1. **Generate tools:**
   ```bash
   ai-tools-builder create-all --output ./ai-tools
   ```

2. **Validate quality:**
   ```bash
   python3 quality_checker.py ./ai-tools/resume-optimizer
   ```

3. **Create GitHub repos manually:**
   - Go to https://github.com/new
   - Create each repo (don't initialize with README)
   - Push code

4. **Configure repos:**
   ```bash
   python3 create_repos.py
   ```

## Full Documentation

See [REPO_CREATION_GUIDE.md](REPO_CREATION_GUIDE.md) for complete documentation.



