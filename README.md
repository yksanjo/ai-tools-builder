# AI Tools Builder

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

Scaffold and build 10 revenue-ready AI-powered frontend tools in minutes. Each tool is a standalone React + Vite + Tailwind application that can be deployed immediately.

## Features

- 🚀 **Instant Scaffolding** - Generate fully functional AI tools in seconds
- 💰 **Revenue-Ready** - Built-in Stripe integration templates
- 🎨 **Modern Stack** - React + Vite + Tailwind CSS
- 🔌 **API Integration** - Pre-configured Claude API integration
- 📦 **Zero Backend** - Pure frontend, runs entirely in browser
- 🚢 **Deploy Ready** - Includes Vercel/Netlify configs

## The 10 AI Tools

1. **AI Prompt Testing Lab** - Test prompts across scenarios, compare outputs, save versions
2. **Meeting Notes → Action Items Extractor** - Extract action items from transcripts
3. **Resume ATS Optimizer** - Optimize resumes for ATS compatibility
4. **Social Media Post Multiplier** - Generate platform-specific posts from one idea
5. **Contract Red Flag Analyzer** - Analyze contracts for risky clauses
6. **Email Response Generator Pro** - Generate multiple email response options
7. **Sales Outreach Personalizer** - Create personalized cold emails
8. **Product Description Generator** - Generate SEO-optimized e-commerce descriptions
9. **Interview Question Prep Coach** - Prepare for interviews with AI coaching
10. **Blog Post SEO Optimizer** - Optimize blog content for SEO

## Installation

```bash
pip install -e .
```

Or install globally:
```bash
pip install .
```

## Quick Start

### List Available Tools

```bash
ai-tools-builder list
```

### Scaffold a Tool

```bash
ai-tools-builder create <tool-name> --output ./my-tool
```

Example:
```bash
ai-tools-builder create resume-optimizer --output ./resume-optimizer
```

### Scaffold All Tools

```bash
ai-tools-builder create-all --output ./ai-tools
```

## Tool Names

Use these exact names when creating tools:

- `prompt-testing-lab`
- `meeting-action-extractor`
- `resume-optimizer`
- `social-media-multiplier`
- `contract-analyzer`
- `email-response-generator`
- `sales-outreach-personalizer`
- `product-description-generator`
- `interview-prep-coach`
- `seo-content-optimizer`

## Generated Project Structure

Each generated tool includes:

```
your-tool/
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
├── postcss.config.js
├── .env.example
├── vercel.json
├── netlify.toml
├── README.md
└── src/
    ├── main.jsx
    ├── App.jsx
    ├── App.css
    └── components/
        └── ...
```

## Environment Setup

Each tool requires a Claude API key. After scaffolding:

1. Copy `.env.example` to `.env`
2. Add your `VITE_ANTHROPIC_API_KEY`
3. Install dependencies: `npm install`
4. Run dev server: `npm run dev`
5. Build for production: `npm run build`

## Monetization Integration

Each tool includes:
- Stripe checkout button templates
- Usage tracking hooks
- Credit system templates
- Subscription tier templates

## Deployment

### Vercel

```bash
cd your-tool
vercel
```

### Netlify

```bash
cd your-tool
netlify deploy
```

Both configs are included in each generated project.

## Customization

After scaffolding, customize:
- Brand colors in `tailwind.config.js`
- Pricing in component files
- API prompts in `src/App.jsx`
- Landing page copy

## Examples

### Create Resume Optimizer

```bash
ai-tools-builder create resume-optimizer --output ./resume-optimizer
cd resume-optimizer
cp .env.example .env
# Add VITE_ANTHROPIC_API_KEY to .env
npm install
npm run dev
```

### Create All Tools at Once

```bash
ai-tools-builder create-all --output ./ai-tools
```

This creates 10 folders, one for each tool.

## Why These Tools Work

✅ **No Backend** - Pure frontend, runs in browser  
✅ **No Database** - Results generated on-demand  
✅ **No Auth Required** - Can add Stripe checkout for paid tiers  
✅ **Clear Value Prop** - Users understand benefit immediately  
✅ **Single Session** - No need for saved state/history  
✅ **Fast Build** - Fully functional in 30-60 minutes each  

## Fastest Path to Revenue

1. Pick a tool based on your distribution channel
2. Scaffold with `ai-tools-builder create`
3. Deploy on Vercel/Netlify (free tier)
4. Add Stripe payment (30 min integration)
5. Drive traffic to your distribution channel
6. Iterate based on feedback

## Best First Choices

- **B2C**: `resume-optimizer` or `interview-prep-coach` - high intent, clear ROI
- **B2B**: `sales-outreach-personalizer` or `seo-content-optimizer` - businesses pay more
- **Creators**: `social-media-multiplier` - viral potential

## Creating GitHub Repositories

After generating tools, you can create high-quality GitHub repositories with automated quality checks:

### Quick Start

```bash
# Set up GitHub token
export GITHUB_TOKEN=ghp_your_token_here
export GITHUB_USERNAME=your-username

# Create all repos with quality checks
python3 create_repos.py
```

This will:
- ✅ Generate all 10 tools
- ✅ Validate quality (files, structure, code)
- ✅ Initialize git repositories
- ✅ Create/configure GitHub repositories
- ✅ Add descriptions, topics, and badges

### Quality Validation

Each tool is automatically validated for:
- Required files and structure
- Valid package.json
- API integration
- Error handling
- Documentation quality
- Deployment configurations

### Manual Quality Check

```bash
python3 quality_checker.py ./my-tools/resume-optimizer
```

See [REPO_CREATION_GUIDE.md](REPO_CREATION_GUIDE.md) for complete documentation.

## License

MIT License - see LICENSE file for details

## Contributing

Contributions welcome! Please open an issue or submit a pull request.

