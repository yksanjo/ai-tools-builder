# Quick Start Guide

## Installation

```bash
cd ai-tools-builder
pip install -e .
```

## Create Your First Tool

```bash
# List all available tools
ai-tools-builder list

# Create a single tool
ai-tools-builder create resume-optimizer --output ./my-tools

# Create all 10 tools at once
ai-tools-builder create-all --output ./ai-tools
```

## Setup Generated Tool

```bash
cd my-tools/resume-optimizer

# 1. Set up environment
cp .env.example .env
# Edit .env and add: VITE_ANTHROPIC_API_KEY=your-key-here

# 2. Install dependencies
npm install

# 3. Run development server
npm run dev

# 4. Build for production
npm run build
```

## Deploy

### Vercel
```bash
vercel
```

### Netlify
```bash
netlify deploy
```

## Get Your API Key

1. Go to https://console.anthropic.com/
2. Create an account or sign in
3. Navigate to API Keys
4. Create a new API key
5. Add it to your `.env` file

## Next Steps

1. Customize the UI (colors, branding) in `tailwind.config.js`
2. Adjust the AI prompts in `src/App.jsx`
3. Add Stripe integration for payments
4. Deploy and start getting users!

## Tool Names Reference

- `prompt-testing-lab` - AI Prompt Testing Lab
- `meeting-action-extractor` - Meeting Notes → Action Items Extractor
- `resume-optimizer` - Resume ATS Optimizer
- `social-media-multiplier` - Social Media Post Multiplier
- `contract-analyzer` - Contract Red Flag Analyzer
- `email-response-generator` - Email Response Generator Pro
- `sales-outreach-personalizer` - Sales Outreach Personalizer
- `product-description-generator` - Product Description Generator
- `interview-prep-coach` - Interview Question Prep Coach
- `seo-content-optimizer` - Blog Post SEO Optimizer



