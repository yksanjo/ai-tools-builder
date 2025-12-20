# Repository Creation Guide for AI Tools

This guide explains the complete process for creating high-quality GitHub repositories for the 10 AI tools.

## Overview

The repository creation process includes:
1. ✅ **Generation** - Create all 10 AI tool projects
2. ✅ **Quality Validation** - Check each project meets quality standards
3. ✅ **Git Initialization** - Set up git repositories
4. ✅ **GitHub Setup** - Create and configure GitHub repositories
5. ✅ **Automation** - Add descriptions, topics, and badges

## Prerequisites

### 1. GitHub Personal Access Token

1. Go to https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a name: "AI Tools Repo Creator"
4. Select scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `public_repo` (Access public repositories)
5. Click "Generate token"
6. Copy the token (you won't see it again!)

Set it as an environment variable:
```bash
export GITHUB_TOKEN=ghp_your_token_here
```

### 2. GitHub Username

Set your GitHub username:
```bash
export GITHUB_USERNAME=your-username
```

Or it will be auto-detected from your token.

### 3. Install Dependencies

```bash
cd ai-tools-builder
pip install -e .
```

## Quick Start

### Option 1: Full Automated Process (Recommended)

This will generate, validate, initialize git, and configure GitHub repos:

```bash
python3 create_repos.py
```

### Option 2: Step-by-Step Process

#### Step 1: Generate All Tools

```bash
ai-tools-builder create-all --output ./ai-tools-generated
```

#### Step 2: Validate Quality

```bash
# Validate a single tool
python3 quality_checker.py ./ai-tools-generated/resume-optimizer

# Or validate all tools
for tool in ./ai-tools-generated/*/; do
    echo "Checking $tool"
    python3 quality_checker.py "$tool"
done
```

#### Step 3: Create GitHub Repositories

```bash
python3 create_repos.py
```

## Quality Checklist

Each tool is validated against these criteria:

### ✅ Required Files
- [ ] `package.json` - Valid JSON with all required fields
- [ ] `vite.config.js` - Vite configuration
- [ ] `tailwind.config.js` - Tailwind configuration
- [ ] `postcss.config.js` - PostCSS configuration
- [ ] `index.html` - Entry HTML file
- [ ] `.env.example` - Environment variable template
- [ ] `.gitignore` - Git ignore rules
- [ ] `README.md` - Documentation
- [ ] `vercel.json` - Vercel deployment config
- [ ] `netlify.toml` - Netlify deployment config
- [ ] `src/main.jsx` - React entry point
- [ ] `src/App.jsx` - Main React component
- [ ] `src/App.css` - Styles

### ✅ Package.json Requirements
- [ ] Has `name`, `version`, `type`, `scripts`, `dependencies`, `devDependencies`
- [ ] Scripts: `dev`, `build`, `preview`
- [ ] Dependencies: `react`, `react-dom`, `@anthropic-ai/sdk`, `lucide-react`
- [ ] DevDependencies: `@vitejs/plugin-react`, `vite`, `tailwindcss`, `autoprefixer`, `postcss`

### ✅ Code Quality
- [ ] API integration present (Anthropic/Claude)
- [ ] Error handling implemented
- [ ] Loading states implemented
- [ ] React hooks used correctly

### ✅ Documentation
- [ ] README has title
- [ ] README has setup instructions
- [ ] README has description
- [ ] `.env.example` has `VITE_ANTHROPIC_API_KEY`

### ✅ Deployment
- [ ] Vercel config has rewrites
- [ ] Netlify config has redirects

## What Gets Created on GitHub

For each tool, the script will:

1. **Create Repository** (if it doesn't exist)
   - You'll need to create it manually first, or the script will guide you

2. **Set Description**
   - Professional, descriptive text explaining what the tool does

3. **Add Topics/Tags**
   - Relevant tags for discoverability:
     - `ai`, `claude`, `anthropic`
     - Tool-specific tags (e.g., `resume`, `ats`, `job-search`)
     - Tech stack tags (`react`, `vite`, `frontend`)
     - `ai-tools` (common tag for all)

4. **Add Badges to README**
   - License badge
   - Language/tech badges
   - GitHub stats (stars, forks, issues)
   - Last commit badge

## Manual Repository Creation

If you prefer to create repos manually:

### 1. Create Repository on GitHub

For each tool:
1. Go to https://github.com/new
2. Repository name: `tool-name` (e.g., `resume-optimizer`)
3. Description: (use from TOOL_METADATA in create_repos.py)
4. Choose **Public**
5. **DO NOT** initialize with README, .gitignore, or license
6. Click "Create repository"

### 2. Push Code

```bash
cd ai-tools-generated/resume-optimizer

# Initialize git (if not done)
git init
git branch -M main

# Add remote
git remote add origin https://github.com/YOUR_USERNAME/resume-optimizer.git

# Push
git add .
git commit -m "Initial commit: Resume ATS Optimizer"
git push -u origin main
```

### 3. Configure Repository

```bash
python3 create_repos.py
```

This will update the description, topics, and badges even if the repo already exists.

## Tool Names and Repositories

| Tool Name | Repository Name | Description |
|-----------|----------------|-------------|
| `prompt-testing-lab` | `prompt-testing-lab` | AI Prompt Testing Lab |
| `meeting-action-extractor` | `meeting-action-extractor` | Meeting Notes → Action Items Extractor |
| `resume-optimizer` | `resume-optimizer` | Resume ATS Optimizer |
| `social-media-multiplier` | `social-media-multiplier` | Social Media Post Multiplier |
| `contract-analyzer` | `contract-analyzer` | Contract Red Flag Analyzer |
| `email-response-generator` | `email-response-generator` | Email Response Generator Pro |
| `sales-outreach-personalizer` | `sales-outreach-personalizer` | Sales Outreach Personalizer |
| `product-description-generator` | `product-description-generator` | Product Description Generator |
| `interview-prep-coach` | `interview-prep-coach` | Interview Question Prep Coach |
| `seo-content-optimizer` | `seo-content-optimizer` | Blog Post SEO Optimizer |

## Troubleshooting

### Quality Check Fails

If a tool fails quality checks:

1. Review the errors:
   ```bash
   python3 quality_checker.py ./ai-tools-generated/tool-name
   ```

2. Fix the issues manually or regenerate:
   ```bash
   rm -rf ./ai-tools-generated/tool-name
   ai-tools-builder create tool-name --output ./ai-tools-generated
   ```

3. Re-validate:
   ```bash
   python3 quality_checker.py ./ai-tools-generated/tool-name
   ```

### GitHub API Errors

**401 Unauthorized:**
- Check your GitHub token is valid
- Ensure token has `repo` scope

**403 Forbidden:**
- Check rate limits (5000 requests/hour for authenticated users)
- Wait and retry

**404 Not Found:**
- Repository doesn't exist - create it manually first
- Check username is correct

### Git Errors

**"Not a git repository":**
- Run `git init` in the tool directory

**"Remote already exists":**
- Remove and re-add: `git remote remove origin && git remote add origin ...`

## Best Practices

1. **Always validate before creating repos**
   - Don't use `--skip-validation` unless you're sure

2. **Review generated code**
   - Check `src/App.jsx` for tool-specific logic
   - Verify API integration is correct

3. **Test locally first**
   ```bash
   cd ai-tools-generated/resume-optimizer
   cp .env.example .env
   # Add your API key to .env
   npm install
   npm run dev
   ```

4. **Customize before pushing**
   - Update README with your branding
   - Adjust colors in `tailwind.config.js`
   - Add your logo/favicon

5. **Set up CI/CD** (optional)
   - Add GitHub Actions for automated testing
   - Set up Vercel/Netlify for auto-deployment

## Next Steps After Creating Repos

1. **Deploy to Vercel/Netlify**
   - Connect your GitHub repo
   - Add environment variable: `VITE_ANTHROPIC_API_KEY`
   - Deploy!

2. **Add Stripe Integration**
   - Follow Stripe docs for React integration
   - Add payment buttons to your tool

3. **Drive Traffic**
   - Share on Product Hunt
   - Post on Twitter/LinkedIn
   - Submit to AI tool directories

4. **Iterate**
   - Gather user feedback
   - Add requested features
   - Improve prompts based on usage

## Support

If you encounter issues:
1. Check the quality checker output
2. Review GitHub API error messages
3. Verify your token has correct permissions
4. Check rate limits

For questions or issues, open an issue on the ai-tools-builder repository.



