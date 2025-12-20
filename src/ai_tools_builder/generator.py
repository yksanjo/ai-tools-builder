"""Tool generator for creating AI tool projects."""

import os
import shutil
from pathlib import Path
from typing import Dict, Any
import json


# Tool definitions with metadata
AVAILABLE_TOOLS: Dict[str, Dict[str, Any]] = {
    "prompt-testing-lab": {
        "name": "AI Prompt Testing Lab",
        "description": "Interactive tool where users paste prompts, test across different scenarios, compare outputs, and save/version their best prompts.",
        "monetization": "Freemium - limit saves/tests, charge for teams/export features",
    },
    "meeting-action-extractor": {
        "name": "Meeting Notes → Action Items Extractor",
        "description": "Paste meeting transcript or notes, AI extracts action items, assigns priority, suggests owners, and formats for Slack/email/project tools.",
        "monetization": "Pay-per-conversion or monthly subscription",
    },
    "resume-optimizer": {
        "name": "Resume ATS Optimizer",
        "description": "Upload resume and job description, AI scores ATS compatibility, suggests keyword improvements, reformats for optimal parsing, shows before/after comparison.",
        "monetization": "$9-29 per resume optimization, or monthly unlimited",
    },
    "social-media-multiplier": {
        "name": "Social Media Post Multiplier",
        "description": "Input one idea/post, AI generates versions for Twitter, LinkedIn, Instagram, Facebook with optimal formatting, hashtags, and hooks for each platform.",
        "monetization": "Credit-based system or monthly subscription",
    },
    "contract-analyzer": {
        "name": "Contract Red Flag Analyzer",
        "description": "Paste contract text, AI highlights risky clauses, unfavorable terms, missing protections, and explains implications in plain English.",
        "monetization": "$19-49 per contract analysis",
    },
    "email-response-generator": {
        "name": "Email Response Generator Pro",
        "description": "Input received email + context, AI generates 3-5 response options (professional, friendly, firm, brief). Learn user's writing style over time.",
        "monetization": "Monthly subscription with usage tiers",
    },
    "sales-outreach-personalizer": {
        "name": "Sales Outreach Personalizer",
        "description": "Input prospect LinkedIn/company info + your offer, AI generates personalized cold email with multiple variants and subject lines.",
        "monetization": "Per-email credits or unlimited monthly",
    },
    "product-description-generator": {
        "name": "Product Description Generator for E-commerce",
        "description": "Input basic product details/features, AI generates SEO-optimized descriptions, bullet points, meta descriptions in brand voice. Multiple style options.",
        "monetization": "Bulk credits or monthly subscription",
    },
    "interview-prep-coach": {
        "name": "Interview Question Prep Coach",
        "description": "Input job description, AI generates likely interview questions, provides sample answers, offers feedback on user's practice responses.",
        "monetization": "$29-99 per job prep package",
    },
    "seo-content-optimizer": {
        "name": "Blog Post → SEO Content Optimizer",
        "description": "Paste blog draft, AI suggests title variations, meta descriptions, heading structure, internal linking opportunities, keyword density improvements.",
        "monetization": "Per-post fee or monthly subscription",
    },
}


class ToolGenerator:
    """Generates AI tool projects from templates."""
    
    def __init__(self):
        self.template_dir = Path(__file__).parent / "templates"
        self.base_template_dir = self.template_dir / "base"
    
    def generate_tool(self, tool_name: str, output_dir: Path):
        """Generate a complete AI tool project."""
        if tool_name not in AVAILABLE_TOOLS:
            raise ValueError(f"Unknown tool: {tool_name}")
        
        tool_info = AVAILABLE_TOOLS[tool_name]
        output_path = Path(output_dir) / tool_name
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Create base project structure
        self._create_base_structure(output_path, tool_name, tool_info)
        
        # Create tool-specific files
        self._create_tool_files(output_path, tool_name, tool_info)
        
        return output_path
    
    def _create_base_structure(self, output_path: Path, tool_name: str, tool_info: Dict):
        """Create base React + Vite + Tailwind structure."""
        
        # package.json
        package_json = {
            "name": tool_name.replace("-", "_"),
            "version": "1.0.0",
            "type": "module",
            "scripts": {
                "dev": "vite",
                "build": "vite build",
                "preview": "vite preview"
            },
            "dependencies": {
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "@anthropic-ai/sdk": "^0.20.0",
                "lucide-react": "^0.294.0"
            },
            "devDependencies": {
                "@types/react": "^18.2.43",
                "@types/react-dom": "^18.2.17",
                "@vitejs/plugin-react": "^4.2.1",
                "autoprefixer": "^10.4.16",
                "postcss": "^8.4.32",
                "tailwindcss": "^3.3.6",
                "vite": "^5.0.8"
            }
        }
        
        (output_path / "package.json").write_text(json.dumps(package_json, indent=2))
        
        # vite.config.js
        vite_config = """import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
});
"""
        (output_path / "vite.config.js").write_text(vite_config)
        
        # tailwind.config.js
        tailwind_config = """/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
"""
        (output_path / "tailwind.config.js").write_text(tailwind_config)
        
        # postcss.config.js
        postcss_config = """export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
"""
        (output_path / "postcss.config.js").write_text(postcss_config)
        
        # index.html
        index_html = f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{tool_info['name']}</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
"""
        (output_path / "index.html").write_text(index_html)
        
        # .env.example
        env_example = """# Anthropic Claude API Key
# Get your API key from https://console.anthropic.com/
VITE_ANTHROPIC_API_KEY=your-api-key-here
"""
        (output_path / ".env.example").write_text(env_example)
        
        # .gitignore
        gitignore = """# Logs
logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*
lerna-debug.log*

node_modules
dist
dist-ssr
*.local

# Editor directories and files
.vscode/*
!.vscode/extensions.json
.idea
.DS_Store
*.suo
*.ntvs*
*.njsproj
*.sln
*.sw?

# Environment variables
.env
.env.local
.env.production
"""
        (output_path / ".gitignore").write_text(gitignore)
        
        # vercel.json
        vercel_config = {
            "rewrites": [
                {
                    "source": "/(.*)",
                    "destination": "/index.html"
                }
            ]
        }
        (output_path / "vercel.json").write_text(json.dumps(vercel_config, indent=2))
        
        # netlify.toml
        netlify_config = """[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
"""
        (output_path / "netlify.toml").write_text(netlify_config)
        
        # Create src directory
        src_dir = output_path / "src"
        src_dir.mkdir(exist_ok=True)
        
        # Create components directory
        components_dir = src_dir / "components"
        components_dir.mkdir(exist_ok=True)
    
    def _create_tool_files(self, output_path: Path, tool_name: str, tool_info: Dict):
        """Create tool-specific React components and logic."""
        
        src_dir = output_path / "src"
        
        # main.jsx
        main_jsx = """import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './App.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
"""
        (src_dir / "main.jsx").write_text(main_jsx)
        
        # App.css
        app_css = """@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
"""
        (src_dir / "App.css").write_text(app_css)
        
        # App.jsx - Generate based on tool type
        app_jsx = self._generate_app_jsx(tool_name, tool_info)
        (src_dir / "App.jsx").write_text(app_jsx)
        
        # README.md
        readme = f"""# {tool_info['name']}

{tool_info['description']}

## Setup

1. Copy `.env.example` to `.env`
2. Add your `VITE_ANTHROPIC_API_KEY` to `.env`
3. Install dependencies: `npm install`
4. Run dev server: `npm run dev`
5. Build for production: `npm run build`

## Deployment

### Vercel
\`\`\`bash
vercel
\`\`\`

### Netlify
\`\`\`bash
netlify deploy
\`\`\`

## Monetization

{tool_info['monetization']}

## License

MIT
"""
        (output_path / "README.md").write_text(readme)
    
    def _generate_app_jsx(self, tool_name: str, tool_info: Dict) -> str:
        """Generate App.jsx content based on tool type."""
        
        # Tool-specific configurations
        tool_configs = {
            "prompt-testing-lab": {
                "input_label": "Your Prompt",
                "input_placeholder": "Enter your prompt here...",
                "input_rows": 6,
                "prompt": """return `You are an expert at analyzing and improving prompts. The user wants to test this prompt:

${userInput}

Please:
1. Analyze the prompt for clarity, specificity, and effectiveness
2. Suggest 3 improved versions with different approaches
3. Explain what makes each version better
4. Provide example outputs for each version

Format your response clearly with sections for each version.`"""
            },
            "meeting-action-extractor": {
                "input_label": "Meeting Notes or Transcript",
                "input_placeholder": "Paste your meeting notes or transcript here...",
                "input_rows": 10,
                "prompt": """return `Extract action items from the following meeting notes. For each action item, identify:
1. The action item description
2. Priority (High/Medium/Low)
3. Suggested owner (if mentioned)
4. Due date (if mentioned)
5. Context/notes

Format as a structured list that can be easily copied to Slack, email, or project management tools.

Meeting notes:
${userInput}`"""
            },
            "resume-optimizer": {
                "input_label": "Resume and Job Description",
                "input_placeholder": "Paste your resume and the job description here, separated by '---JOB DESCRIPTION---'...",
                "input_rows": 15,
                "prompt": """return `Analyze the resume and job description below. Provide:
1. ATS compatibility score (0-100)
2. Missing keywords from the job description
3. Suggested improvements for ATS parsing
4. A reformatted version optimized for ATS
5. Before/after comparison

Resume and Job Description:
${userInput}`"""
            },
            "social-media-multiplier": {
                "input_label": "Your Post Idea",
                "input_placeholder": "Enter your post idea or content here...",
                "input_rows": 6,
                "prompt": """return `Generate platform-specific versions of this post for:
1. Twitter (280 chars, with hashtags)
2. LinkedIn (professional tone, longer form)
3. Instagram (engaging, with relevant hashtags)
4. Facebook (conversational, engaging)

For each platform, optimize:
- Formatting and structure
- Hashtags and mentions
- Tone and style
- Hook/opening line

Original post idea:
${userInput}`"""
            },
            "contract-analyzer": {
                "input_label": "Contract Text",
                "input_placeholder": "Paste the contract text you want analyzed...",
                "input_rows": 15,
                "prompt": """return `Analyze this contract for:
1. Red flags and risky clauses
2. Unfavorable terms
3. Missing protections
4. Unusual or concerning language

For each issue found, explain:
- What the clause means in plain English
- Why it might be problematic
- What you should consider before signing

Contract text:
${userInput}`"""
            },
            "email-response-generator": {
                "input_label": "Received Email and Context",
                "input_placeholder": "Paste the email you received and any relevant context...",
                "input_rows": 8,
                "prompt": """return `Generate 5 different response options for this email:
1. Professional and formal
2. Friendly and warm
3. Firm and direct
4. Brief and concise
5. Collaborative and open

For each option, provide:
- The full email text
- Subject line suggestion
- Tone explanation

Received email:
${userInput}`"""
            },
            "sales-outreach-personalizer": {
                "input_label": "Prospect Info and Your Offer",
                "input_placeholder": "Enter prospect LinkedIn/company info and your offer...",
                "input_rows": 8,
                "prompt": """return `Create a personalized cold email based on this prospect information. Generate:
1. A personalized opening that shows you researched them
2. The value proposition tailored to their situation
3. A clear call-to-action
4. 3 subject line variations
5. A follow-up email template

Prospect info and offer:
${userInput}`"""
            },
            "product-description-generator": {
                "input_label": "Product Details",
                "input_placeholder": "Enter product name, features, and any brand voice guidelines...",
                "input_rows": 8,
                "prompt": """return `Generate SEO-optimized product descriptions:
1. Main product description (engaging, SEO-friendly)
2. Bullet points of key features
3. Meta description (150-160 characters)
4. Product title variations
5. Suggested keywords

Product details:
${userInput}`"""
            },
            "interview-prep-coach": {
                "input_label": "Job Description",
                "input_placeholder": "Paste the job description here...",
                "input_rows": 10,
                "prompt": """return `Based on this job description, provide:
1. 10-15 likely interview questions (technical, behavioral, situational)
2. Sample answers for each question
3. Key points to emphasize based on the role
4. Questions to ask the interviewer
5. Red flags to watch for in the interview

Job description:
${userInput}`"""
            },
            "seo-content-optimizer": {
                "input_label": "Blog Post Draft",
                "input_placeholder": "Paste your blog post draft here...",
                "input_rows": 15,
                "prompt": """return `Optimize this blog post for SEO. Provide:
1. 5 title variations (SEO-optimized)
2. Meta description (150-160 characters)
3. Suggested heading structure (H2, H3)
4. Internal linking opportunities
5. Keyword density analysis and suggestions
6. Content improvements for SEO

Blog post:
${userInput}`"""
            },
        }
        
        config = tool_configs.get(tool_name, tool_configs["prompt-testing-lab"])
        
        # Generate the App.jsx file
        app_jsx = f"""import {{ useState }} from 'react'
import {{ Sparkles, Loader2 }} from 'lucide-react'

function App() {{
  const [input, setInput] = useState('')
  const [output, setOutput] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const apiKey = import.meta.env.VITE_ANTHROPIC_API_KEY

  const handleSubmit = async (e) => {{
    e.preventDefault()
    if (!input.trim()) return
    if (!apiKey) {{
      setError('Please set VITE_ANTHROPIC_API_KEY in your .env file')
      return
    }}

    setLoading(true)
    setError('')
    setOutput('')

    try {{
      const response = await fetch('https://api.anthropic.com/v1/messages', {{
        method: 'POST',
        headers: {{
          'Content-Type': 'application/json',
          'x-api-key': apiKey,
          'anthropic-version': '2023-06-01'
        }},
        body: JSON.stringify({{
          model: 'claude-3-5-sonnet-20241022',
          max_tokens: 4096,
          messages: [{{
            role: 'user',
            content: generatePrompt(input)
          }}]
        }})
      }})

      if (!response.ok) {{
        throw new Error(`API error: ${{response.statusText}}`)
      }}

      const data = await response.json()
      const content = data.content[0].text
      setOutput(content)
    }} catch (err) {{
      setError(err.message || 'An error occurred')
    }} finally {{
      setLoading(false)
    }}
  }}

  function generatePrompt(userInput) {{
    {config['prompt']}
  }}

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-2 mb-4">
            <Sparkles className="w-8 h-8 text-indigo-600" />
            <h1 className="text-4xl font-bold text-gray-900">{tool_info['name']}</h1>
          </div>
          <p className="text-gray-600">{tool_info['description']}</p>
        </div>

        <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
          <form onSubmit={{handleSubmit}} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                {config['input_label']}
              </label>
              <textarea
                value={{input}}
                onChange={{e => setInput(e.target.value)}}
                placeholder="{config['input_placeholder']}"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none"
                rows={config['input_rows']}
                disabled={{loading}}
              />
            </div>

            <button
              type="submit"
              disabled={{loading || !input.trim()}}
              className="w-full bg-indigo-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              {{loading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Processing...
                </>
              ) : (
                <>
                  <Sparkles className="w-5 h-5" />
                  Generate
                </>
              )}}
            </button>
          </form>

          {{error && (
            <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
              {{error}}
            </div>
          )}}
        </div>

        {{output && (
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Result</h2>
            <div className="prose max-w-none">
              <pre className="whitespace-pre-wrap text-gray-700 bg-gray-50 p-4 rounded-lg border">
                {{output}}
              </pre>
            </div>
            <div className="mt-4 flex gap-2">
              <button
                onClick={{() => navigator.clipboard.writeText(output)}}
                className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200"
              >
                Copy
              </button>
            </div>
          </div>
        )}}
      </div>
    </div>
  )
}}

export default App
"""
        
        return app_jsx

