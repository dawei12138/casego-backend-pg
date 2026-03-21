---
name: testersai
description: >
  Automated bug detection, test case generation, and persona feedback using 30+ specialized AI
  testers via cloud API. Analyzes web pages and code using testers for accessibility, security,
  UI/UX, performance, JavaScript, and more. Captures screenshots and diagnostics via Claude in
  Chrome or Playwright MCP, or accepts manual uploads. Use when user asks to: "check for bugs",
  "find issues", "audit this", "test this page/code", "QA check", "review code",
  "check for accessibility/security/performance issues", "generate test cases", "create tests",
  "persona feedback", "user feedback", or any variation of bug detection, code review, or testing.
api_endpoints:
  bug_detection: "https://testersai-bug-detection.run.app"
  test_cases: "https://testersai-test-cases.run.app"
  persona_feedback: "https://testersai-persona-feedback.run.app"
---

# TestersAI - AI-Powered Testing & Code Review

Analyze **web pages AND code** using **30+ specialized AI testers** via secure cloud API — each an expert in their domain. Generate comprehensive test cases for QA. Simulate diverse user perspectives for UX insights.

## What Can TestersAI Analyze?

### Web Pages
- **Screenshots** - Visual UI/UX, layout, design, accessibility
- **Console logs** - JavaScript errors, warnings, performance issues
- **Network requests** - Failed API calls, slow loading, CDN issues
- **Accessibility trees** - ARIA labels, semantic HTML, screen reader compatibility
- Automatically captured via Chrome MCP tools or user-uploaded

### Code Snippets
- **JavaScript/TypeScript** - Security issues, performance problems, error handling
- **HTML** - Accessibility, semantic markup, SEO issues
- **CSS** - Performance, maintainability, responsive design
- **React/Vue/Angular** - Component issues, state management, hooks
- **Any language** - Security vulnerabilities, code quality, best practices

## What Makes This Different

Instead of one generic review, this skill uses **specialized AI testers** like:
- **Sophia** (Accessibility expert) - Finds WCAG violations, contrast issues, screen reader problems
- **Tariq** (Security expert) - Identifies security vulnerabilities, OWASP issues, injection risks
- **Jason** (JavaScript expert) - Catches JS errors, promise issues, state management problems
- **Mia** (UI/UX expert) - Spots layout problems, design inconsistencies, usability issues
- **Marcus** (Performance expert) - Catches network issues, slow loading, API failures
- **Diego** (Console expert) - Analyzes browser console for errors, warnings, deprecations
- **Alejandro** (GDPR expert) - Checks privacy compliance, cookie consent issues
- Plus 24 more specialized testers...

Each tester runs their own **specialized analysis** focused on their expertise area, ensuring nothing is missed.

---

## Usage Modes

This skill has four modes (availability depends on your tier):

1. **Bug Detection Mode** - Use specialized AI testers to find issues
   - Free: 10 basic testers, markdown output only
   - Pro: All 30+ testers, HTML/JSON/Jira output

2. **Test Case Generation Mode** - Create comprehensive QA test cases
   - Free: Not available
   - Pro: Available

3. **Persona Feedback Mode** - Simulate diverse user perspectives
   - Free: Not available
   - Pro: Available

4. **Test Execution Mode** - Auto-run browser tests with Claude in Chrome
   - Free: Not available
   - Pro: Available

**Triggers:**
- Bug Detection: "find bugs", "check for issues", "audit the page", "QA check", "check for [specific] issues"
- Test Case Generation: "generate test cases", "create tests", "test suite", "test scenarios"
- Persona Feedback: "user feedback", "persona analysis", "user perspectives", "simulate users"
- Test Execution: "run these tests", "execute test cases", "automate testing"

---

## CRITICAL: Check Unlock Status & Tier (Do This FIRST!)

**BEFORE doing anything else**, check the user's tier and handle unlock codes:

### Step 1: Check for Unlock Code in Message

Scan the user's message for unlock code pattern: `unlock_skills_[tier]_[string]`

```python
import sys
sys.path.append('testersai/scripts')
from unlock import check_message_for_unlock, check_unlock_status, get_tier_message

# Check if message contains unlock code
unlock_result = check_message_for_unlock(user_message, skill_path='testersai/testersai')

if unlock_result:
    # Display result to user
    print(unlock_result["message"])
    if unlock_result["success"]:
        print(f"\n Welcome to TestersAI {unlock_result['tier'].upper()}!")
        # Continue with analysis using new tier
    else:
        # Invalid code - continue with current tier
        pass
```

### Step 2: Load Current Tier Status

```python
status = check_unlock_status(skill_path='testersai/testersai')
current_tier = status["tier"]  # "free" or "pro"
```

### Step 3: Display Tier Info to User

**ALWAYS show tier status at the start** (unless user just unlocked):

```python
print(get_tier_message(current_tier))
```

### Step 4: Set Feature Availability

Based on tier, determine which features are available:

```python
# Feature gates
FEATURES = {
    "free": {
        "testers": ["sophia", "tariq", "marcus", "mia", "jason", "diego", "leila", "fatima", "hiroshi", "mei"],
        "output_formats": ["markdown"],
        "max_test_cases": 5,
        "modes": ["bug_detection"],
        "html_reports": False,
        "test_execution": False,
    },
    "pro": {
        "testers": "all",
        "output_formats": ["markdown", "json", "html", "jira"],
        "max_test_cases": None,
        "modes": ["bug_detection", "test_case_generation", "persona_feedback", "test_execution"],
        "html_reports": True,
        "test_execution": True,
    }
}

features = FEATURES[current_tier]
```

### Step 5: Enforce Feature Gates

Throughout the skill execution, check feature availability:

```python
# Example: Check if HTML reports are available
if user_requests_html and not features["html_reports"]:
    print("HTML reports are only available in Pro tier.")
    print("Upgrade at: https://buy.stripe.com/5kQ00jcvwepvam64fPU")
    output_format = "markdown"

# Example: Check if test execution is available
if user_requests_test_execution and not features["test_execution"]:
    print("Test execution is only available in Pro tier.")
    print("Upgrade at: https://buy.stripe.com/5kQ00jcvwepvam64fPU")
    return

# Example: Limit testers in free tier
if features["testers"] != "all":
    applicable_testers = [t for t in applicable_testers if t in features["testers"]]
    print(f"Free tier: Using {len(applicable_testers)} basic testers")
    print("   Upgrade to Pro for all 30+ specialized testers")
```

---

## CRITICAL: Usage Logging

**Log every skill invocation** for analytics and debugging. Create/append to a usage log file:

```python
import json
from datetime import datetime

def log_usage(url, mode, tier, testers_used, bugs_found, report_path, duration_seconds):
    """Log each TestersAI run for analytics."""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "url": url,
        "mode": mode,
        "tier": tier,
        "testers_used": testers_used,
        "bugs_found": bugs_found,
        "report_path": report_path,
        "duration_seconds": duration_seconds
    }

    log_path = "testersai/testersai/usage.log"
    try:
        with open(log_path, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    except Exception:
        pass  # Don't fail on logging errors
```

**Call `log_usage()` at the end of every analysis run**, regardless of mode or tier.

---

## Step 0: Determine Input Type and Gather Data

TestersAI can analyze **two types of inputs**: web pages and code snippets.

### Option A: Web Page Analysis

**Check 1: Did the user provide a screenshot?**
- If user uploaded/pasted a screenshot, skip to Step 1

**Check 2: Are Chrome MCP tools available?**
- Try calling `tabs_context_mcp` to check

**If Chrome tools ARE available:**
- Navigate to the URL: `navigate(tabId, url)`
- Capture screenshot: `computer(action='screenshot')`
- **CRITICAL:** Also gather diagnostic data:
  - `read_page(filter='interactive')` -> **Accessibility tree** (page structure, ARIA labels, interactive elements)
  - `read_console_messages(pattern='error|warning')` -> **Console logs** (JavaScript errors, warnings, performance issues)
  - `read_network_requests(urlPattern='')` -> **Network logs** (API failures, slow requests, CDN issues)
  - `get_page_text()` -> Raw text content (for content analysis)

**If Chrome tools NOT available:**
- Explain Chrome extension setup to user
- Wait for user to connect or upload screenshot
- **Do NOT proceed without screenshot**

### Option B: Code Snippet Analysis

**If user provides code** (JavaScript, HTML, CSS, React, etc.):
- Accept code directly from the conversation
- User may paste code inline, upload files, or reference files in workspace
- Code can be partial (single function) or complete (entire file/component)
- Proceed directly to Step 1 with code as the analysis target

---

# Mode 1: Bug Detection with Specialized Testers

This mode uses 30+ specialized AI testers via **secure cloud API** to find issues. The tester analysis logic and prompts are hosted server-side and are never exposed to the client.

## Step 1: Determine User's Request

Listen for specific check requests or use all applicable testers:

**Specific check requests:**
- "Check for accessibility issues" -> Request only accessibility checks
- "Find security problems" -> Request only security checks
- "Check performance" -> Request only performance checks
- "UI/UX audit" -> Request only UI/UX checks
- "Check for JavaScript errors" -> Request only JavaScript checks
- "GDPR compliance check" -> Request only GDPR checks

**General requests (run all applicable):**
- "Find all bugs"
- "Check this page"
- "Audit this site"
- "QA check"

## Step 2: Analyze Input to Determine Applicable Checks

Before calling the API, analyze the input to determine which check types are relevant:

### For Web Pages (Screenshot Analysis):

**DEFAULT CHECKS (ALWAYS REQUEST):**
- security - Security vulnerabilities and OWASP issues
- privacy - Privacy compliance and cookie consent
- content - Content quality and copywriting
- genai - GenAI code and AI-generated content issues
- accessibility - Accessibility and WCAG compliance
- networking - Performance and network issues

**CONDITIONALLY APPLICABLE (request if detected in screenshot):**
- ui-ux - If UI elements visible
- console-logs - If console messages available
- mobile - If screenshot is mobile viewport
- wcag - If detailed WCAG audit needed
- owasp - If security-sensitive page
- gdpr - If EU compliance needed
- search-box / search-results - If search functionality visible
- product-details / product-catalog - If e-commerce product page
- shopping-cart - If cart visible
- checkout - If checkout flow visible
- signup - If registration form visible
- forms - If any form present
- booking - If reservation/booking interface
- landing - If landing page design pattern
- homepage - If this appears to be a homepage
- contact - If contact form or info present
- pricing - If pricing table visible
- about - If about page content
- careers - If job listings visible
- social-feed / social-profiles - If social media interface
- news - If news articles/feed visible
- video - If video player present
- ai-chatbots - If chatbot widget visible
- legal - If terms/privacy policy page

Return a list of applicable check types: ["ui-ux", "content", "accessibility", ...]

### For Code Snippets:

**ALWAYS REQUEST for code:**
- security - Security vulnerabilities, injection risks
- javascript - JavaScript/TypeScript errors, best practices
- genai - AI-generated code quality issues
- accessibility - If HTML/JSX, check semantic markup
- ui-ux - If HTML/CSS/React, check component design

## Step 3: Prepare and Send API Request

**CRITICAL: Do NOT load or read `references/testers-profiles.json` for tester prompts.** The tester prompts are proprietary and hosted server-side only. The API handles all tester selection, prompt execution, deduplication, and sorting.

```python
import json
import base64
from datetime import datetime

start_time = datetime.now()

# Prepare API request payload
api_request = {
    "url": url,
    "screenshot_base64": screenshot_base64_string,
    "console_logs": console_logs_text,
    "network_logs": network_requests_data,
    "accessibility_tree": accessibility_tree_text,
    "page_text": page_text,
    "requested_checks": applicable_check_types,  # List of check type strings, or None for all
    "tier": current_tier,
    "output_format": "json"
}
```

**Call the Bug Detection API:**

```python
import subprocess

# Use curl to call the API (no external Python dependencies needed)
api_url = "https://testersai-bug-detection.run.app"

response = subprocess.run(
    ["curl", "-s", "-X", "POST", api_url,
     "-H", "Content-Type: application/json",
     "-d", json.dumps(api_request),
     "--max-time", "120"],
    capture_output=True, text=True
)

if response.returncode == 0:
    result = json.loads(response.stdout)
    if result.get("success"):
        bugs = result["bugs"]
        testers_used = result["testers_used"]
        metadata = result["metadata"]
    else:
        print(f"API Error: {result.get('error', 'Unknown error')}")
else:
    print(f"Request failed: {response.stderr}")
```

**API Response Format:**

```json
{
  "success": true,
  "bugs": [
    {
      "bug_title": "Empty Links Without Accessible Names",
      "bug_type": ["Accessibility", "WCAG"],
      "bug_priority": 6,
      "bug_confidence": 9,
      "bug_reasoning_why_a_bug": "Four links have no text or aria-label...",
      "suggested_fix": "Add descriptive aria-label attributes...",
      "fix_prompt": "Find all <a> elements without text content or aria-label...",
      "found_by": {
        "tester_id": "sophia",
        "tester_name": "Sophia",
        "tester_specialty": "Accessibility Specialist",
        "profile_image": "sophia.jpg"
      }
    }
  ],
  "testers_used": [
    {"id": "sophia", "name": "Sophia", "specialty": "Accessibility Specialist", "issues_found": 2},
    {"id": "tariq", "name": "Tariq", "specialty": "Security & OWASP", "issues_found": 2}
  ],
  "metadata": {
    "url": "https://bing.com",
    "total_bugs": 8,
    "analysis_duration_seconds": 45
  }
}
```

## Step 4: If API Is Unavailable — Fallback to Local Analysis

If the API endpoint is not reachable (timeout, network error, not configured), fall back to local analysis using Claude's own capabilities:

1. Analyze the screenshot, console logs, network requests, accessibility tree, and page text yourself
2. Apply each applicable tester's perspective based on their specialty area (NOT their raw prompts)
3. For each check type, analyze the data looking for issues in that domain
4. Generate findings in the same JSON schema as the API response

**IMPORTANT:** When falling back to local analysis, do NOT read or expose the contents of `references/testers-profiles.json`. Instead, use the tester roster below (names and specialties only) and apply your own expert knowledge for each domain.

**Tester Roster (for display and attribution only):**

| ID | Name | Specialty | Check Types |
|---|---|---|---|
| sophia | Sophia | Accessibility | accessibility |
| tariq | Tariq | Security & OWASP | security, owasp |
| jason | Jason | JavaScript & Booking | javascript, booking |
| mia | Mia | UI/UX & Forms | ui-ux, forms |
| marcus | Marcus | Networking & Performance | networking, shipping |
| diego | Diego | Console Logs | console-logs |
| leila | Leila | Content | content |
| fatima | Fatima | Privacy & Cookie Consent | privacy, cookie-consent |
| hiroshi | Hiroshi | GenAI Code | genai |
| mei | Mei | WCAG Compliance | wcag |
| zanele | Zanele | Mobile | mobile |
| alejandro | Alejandro | GDPR Compliance | gdpr |
| sharon | Sharon | Error Messages & Careers | error-messages, careers |
| pete | Pete | AI Chatbots | ai-chatbots |
| kwame | Kwame | Search Box | search-box |
| zara | Zara | Search Results | search-results |
| priya | Priya | Product Details | product-details |
| yara | Yara | Product Catalog | product-catalog |
| hassan | Hassan | News | news |
| amara | Amara | Shopping Cart | shopping-cart |
| yuki | Yuki | Signup | signup |
| mateo | Mateo | Checkout | checkout |
| anika | Anika | Social Profiles | social-profiles |
| zoe | Zoe | Social Feed | social-feed |
| zachary | Zachary | Landing Pages | landing |
| sundar | Sundar | Homepage | homepage |
| samantha | Samantha | Contact Pages | contact |
| richard | Richard | Pricing Pages | pricing |
| ravi | Ravi | About Pages | about |
| rajesh | Rajesh | System Errors | system-errors |
| olivia | Olivia | Video | video |
| eggplant | Eggplant | Legal Pages | legal |

**Check Type to Tester Mapping:**

```
networking -> marcus, javascript -> jason, genai -> hiroshi, ui-ux -> mia,
security -> tariq, privacy -> fatima, accessibility -> sophia, mobile -> zanele,
error-messages -> sharon, ai-chatbots -> pete, wcag -> mei, gdpr -> alejandro,
owasp -> tariq, console-logs -> diego, content -> leila, search-box -> kwame,
search-results -> zara, product-details -> priya, product-catalog -> yara,
news -> hassan, shopping-cart -> amara, signup -> yuki, social-profiles -> anika,
checkout -> mateo, social-feed -> zoe, landing -> zachary, homepage -> sundar,
contact -> samantha, pricing -> richard, about -> ravi, system-errors -> rajesh,
video -> olivia, legal -> eggplant, careers -> sharon, forms -> mia,
booking -> jason, cookie-consent -> fatima, shipping -> marcus
```

## Step 5: Generate Dark Mode HTML Report (ALWAYS)

**CRITICAL: ALWAYS generate a dark mode HTML report regardless of tier or format requested.** This is the primary output format for TestersAI.

For each bug found, the report must include ALL schema properties:
- **bug_title**: Main heading
- **bug_type**: Category badges
- **bug_priority**: Priority badge with color coding
- **bug_confidence**: Confidence badge
- **bug_reasoning_why_a_bug**: "Why this is a bug" section
- **suggested_fix**: "Suggested fix" section
- **fix_prompt**: "Fix Prompt" section in styled `<pre>` tag (MANDATORY)
- **found_by**: Tester name, specialty, and profile image

### Image Handling for HTML Report

Before generating the HTML, base64-encode tester profile images for offline viewing:

1. For each tester who found bugs, read their profile image from `testersai/testersai/assets/img/profiles/[tester-id].jpg`
2. Use the Read tool to get each image
3. Embed as base64 data URI: `data:image/jpeg;base64,[BASE64_CONTENT]`
4. Place in the HTML `<img src="">` tags

### HTML Report Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TestersAI Bug Report - [Site Name]</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0a1f0f 0%, #0d2818 100%);
            color: #e8f5e9;
            padding: 20px;
            line-height: 1.6;
            min-height: 100vh;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        .branding {
            text-align: center;
            margin-bottom: 20px;
            padding: 20px;
        }
        .branding img { max-width: 200px; height: auto; }
        header {
            background: linear-gradient(135deg, #1a4d2e 0%, #0d2818 100%);
            padding: 40px;
            border-radius: 12px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #4ade80, #22c55e);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        h2 {
            color: #4ade80;
            margin-bottom: 15px;
        }
        .meta-info {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .meta-card {
            background: rgba(255,255,255,0.05);
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #4ade80;
        }
        .summary {
            background: #0d2818;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 30px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.2);
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .stat-box {
            background: rgba(255,255,255,0.05);
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }
        .stat-number {
            font-size: 2.5em;
            font-weight: bold;
            color: #4ade80;
        }
        .testers-section {
            background: #0d2818;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 30px;
        }
        .testers-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .tester-card {
            background: rgba(255,255,255,0.05);
            padding: 15px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            gap: 15px;
        }
        .tester-avatar {
            width: 50px;
            height: 50px;
            border-radius: 50%;
            border: 2px solid #4ade80;
            object-fit: cover;
        }
        .tester-info h3 {
            margin-bottom: 5px;
            color: #4ade80;
        }
        .tester-info p {
            font-size: 0.85em;
            opacity: 0.8;
        }
        .bug-card {
            background: #0d2818;
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 20px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.2);
            border-left: 6px solid;
        }
        .bug-card.priority-critical { border-left-color: #ff4757; }
        .bug-card.priority-high { border-left-color: #ffa502; }
        .bug-card.priority-medium { border-left-color: #ffd32a; }
        .bug-card.priority-low { border-left-color: #3498db; }
        .bug-header {
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 15px;
            flex-wrap: wrap;
            gap: 10px;
        }
        .bug-title {
            font-size: 1.4em;
            flex: 1;
            color: #fff;
        }
        .bug-badges {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }
        .badge {
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 0.85em;
            font-weight: 600;
        }
        .badge-priority { background: #ff4757; color: white; }
        .badge-priority.medium { background: #ffd32a; color: #333; }
        .badge-priority.low { background: #3498db; color: white; }
        .badge-confidence { background: #3498db; color: white; }
        .badge-category { background: rgba(255,255,255,0.1); color: #4ade80; }
        .bug-tester {
            display: flex;
            align-items: center;
            gap: 10px;
            margin: 15px 0;
            padding: 10px;
            background: rgba(255,255,255,0.05);
            border-radius: 8px;
        }
        .bug-tester img {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            border: 2px solid #4ade80;
            object-fit: cover;
        }
        .bug-content { margin-top: 15px; }
        .bug-section { margin: 15px 0; }
        .bug-section h4 {
            color: #4ade80;
            margin-bottom: 8px;
        }
        .bug-section p {
            color: #c8e6c9;
            line-height: 1.7;
        }
        .fix-prompt-block {
            background: rgba(0,0,0,0.3);
            padding: 15px;
            border-radius: 6px;
            overflow-x: auto;
            color: #4ade80;
            border: 1px solid rgba(74,222,128,0.3);
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            line-height: 1.5;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        .recommendations {
            background: #0d2818;
            padding: 30px;
            border-radius: 12px;
            margin-top: 30px;
        }
        .recommendations ol {
            margin-left: 20px;
            margin-top: 15px;
        }
        .recommendations li {
            margin: 10px 0;
            padding-left: 10px;
            color: #c8e6c9;
        }
        footer {
            text-align: center;
            margin-top: 50px;
            opacity: 0.6;
            font-size: 0.9em;
            padding: 20px;
        }
        footer a { color: #4ade80; text-decoration: none; }
        @media print {
            body { background: #0a1f0f; }
            .bug-card { page-break-inside: avoid; }
        }
        @media (max-width: 768px) {
            .bug-header { flex-direction: column; }
            h1 { font-size: 1.8em; }
            header { padding: 20px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="branding">
            <h1 style="color: #4ade80; font-size: 2em; -webkit-text-fill-color: #4ade80;">TestersAI</h1>
            <p style="opacity: 0.7;">AI-Powered Web Testing</p>
        </div>

        <header>
            <h1>Bug Check Report</h1>
            <div class="meta-info">
                <div class="meta-card">
                    <strong>URL:</strong><br>[URL]
                </div>
                <div class="meta-card">
                    <strong>Date:</strong><br>[Date]
                </div>
                <div class="meta-card">
                    <strong>Testers:</strong><br>[Count] AI Specialists
                </div>
                <div class="meta-card">
                    <strong>Tier:</strong><br>[Tier]
                </div>
            </div>
        </header>

        <div class="summary">
            <h2>Summary</h2>
            <div class="stats-grid">
                <div class="stat-box">
                    <div class="stat-number">[X]</div>
                    <div>Total Issues</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number" style="color:#ff4757">[X]</div>
                    <div>Critical (8-10)</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number" style="color:#ffa502">[X]</div>
                    <div>High (5-7)</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number" style="color:#ffd32a">[X]</div>
                    <div>Medium (4)</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number" style="color:#3498db">[X]</div>
                    <div>Low (1-3)</div>
                </div>
            </div>
        </div>

        <div class="testers-section">
            <h2>AI Testers Who Participated</h2>
            <div class="testers-grid">
                <!-- For each tester who found issues -->
                <div class="tester-card">
                    <img src="[base64_profile_image]" alt="[Name]" class="tester-avatar">
                    <div class="tester-info">
                        <h3>[Name]</h3>
                        <p>[Specialty]</p>
                        <p><strong>[X]</strong> issues found</p>
                    </div>
                </div>
            </div>
        </div>

        <h2 style="margin-bottom: 20px;">Issues Found</h2>

        <!-- For each bug, sorted by priority descending -->
        <div class="bug-card priority-[critical/high/medium/low]">
            <div class="bug-header">
                <h3 class="bug-title">[#]. [Bug Title]</h3>
                <div class="bug-badges">
                    <span class="badge badge-priority">Priority: [X]/10</span>
                    <span class="badge badge-confidence">Confidence: [X]/10</span>
                    <!-- For each category -->
                    <span class="badge badge-category">[Category]</span>
                </div>
            </div>

            <div class="bug-tester">
                <img src="[base64_tester_profile_image]" alt="[Tester Name]">
                <div>
                    <strong>[Tester Name]</strong>
                    <br><span style="opacity:0.7">[Tester Specialty]</span>
                </div>
            </div>

            <div class="bug-content">
                <div class="bug-section">
                    <h4>Why this is a bug:</h4>
                    <p>[bug_reasoning_why_a_bug]</p>
                </div>
                <div class="bug-section">
                    <h4>Suggested fix:</h4>
                    <p>[suggested_fix]</p>
                </div>
                <div class="bug-section">
                    <h4>Fix Prompt:</h4>
                    <pre class="fix-prompt-block">[fix_prompt - ready-to-use prompt for developer/AI]</pre>
                </div>
            </div>
        </div>
        <!-- End bug loop -->

        <div class="recommendations">
            <h2>Top Recommendations</h2>
            <ol>
                <li>[Highest-priority recommendation]</li>
                <li>[Second priority]</li>
                <li>[Third priority]</li>
            </ol>
        </div>

        <footer>
            <p>Generated by <a href="https://testers.ai">TestersAI</a> &bull; AI-Powered Web Testing & Code Review</p>
            <p>Powered by 30+ Specialized AI Testers</p>
        </footer>
    </div>
</body>
</html>
```

**Priority class mapping:**
- Priority 8-10: `priority-critical` (red border)
- Priority 5-7: `priority-high` (orange border)
- Priority 4: `priority-medium` (yellow border)
- Priority 1-3: `priority-low` (blue border)

**File naming**: `<site-name>-bug-report.html`

**ALWAYS save the HTML report** and provide a `computer://` link to the user.

## Step 6: Present Findings in Chat

After saving the HTML report, also present findings in chat grouped by tester with their profile images:

1. Group all bugs by the tester who found them
2. For each tester who found issues:
   - Use the Read tool to display their profile image from `testersai/testersai/assets/img/profiles/[tester-id].jpg`
   - Show their name and specialty
   - List their findings with priority and brief description
3. Order testers by highest priority issues first

**Format:**
```
### **[Tester Name]** - [Specialty]
[Use Read tool on testersai/testersai/assets/img/profiles/[id].jpg]

**[Priority Level] ([X]/10)**
**Bug:** [Bug Title]
**Impact:** [Brief user impact]
**Fix:** [One-line fix suggestion]

---
```

## Step 7: Log Usage

At the end of every analysis run, log usage:

```python
duration = (datetime.now() - start_time).total_seconds()
log_usage(
    url=url,
    mode="bug_detection",
    tier=current_tier,
    testers_used=len(testers_used),
    bugs_found=len(bugs),
    report_path=report_path,
    duration_seconds=duration
)
```

---

# Mode 2: Test Case Generation

This mode generates comprehensive QA test cases via the cloud API.

## When to Use

**Triggers:**
- "generate test cases"
- "create tests"
- "test suite"
- "test scenarios"

## Step 1: Prepare API Request

```python
api_request = {
    "screenshot_base64": screenshot_base64_string,
    "url": url,
    "accessibility_tree": accessibility_tree_text,
    "page_text": page_text,
    "test_type": "full",  # Options: "smoke", "regression", "acceptance", "full"
    "tier": current_tier
}
```

## Step 2: Call Test Case API

```python
test_case_url = "https://testersai-test-cases.run.app"

response = subprocess.run(
    ["curl", "-s", "-X", "POST", test_case_url,
     "-H", "Content-Type: application/json",
     "-d", json.dumps(api_request),
     "--max-time", "120"],
    capture_output=True, text=True
)

result = json.loads(response.stdout)
if result.get("success"):
    test_suites = result["test_suites"]
```

## Step 3: Format and Display

Generate a dark mode HTML report with test cases and save to workspace.

---

# Mode 3: Persona Feedback

Generate diverse user persona feedback on webpages or app screenshots via cloud API. Simulate how real users from different demographics, tech levels, and perspectives would react to the page.

## When to Use

**Triggers:**
- "user feedback"
- "persona analysis"
- "what would users think"
- "simulate users"
- "persona feedback"
- "UX feedback"

## Step 1: Gather Page Data

Use the same data collection as Mode 1 (Step 0): screenshot, page text, accessibility tree. At minimum, a screenshot is required.

## Step 2: Prepare API Request

```python
api_request = {
    "screenshot_base64": screenshot_base64_string,
    "url": url,
    "page_text": page_text,
    "num_personas": 6,
    "custom_instructions": "",
    "tier": current_tier
}
```

## Step 3: Call Persona Feedback API

```python
persona_url = "https://testersai-persona-feedback.run.app"

response = subprocess.run(
    ["curl", "-s", "-X", "POST", persona_url,
     "-H", "Content-Type: application/json",
     "-d", json.dumps(api_request),
     "--max-time", "120"],
    capture_output=True, text=True
)

result = json.loads(response.stdout)
if result.get("success"):
    personas = result["user_persona_feedback"]
    overall_score = result["overall_score"]
```

**API Response Schema:**

```json
{
  "success": true,
  "url": "https://example.com",
  "overall_purpose_of_page": "Search engine homepage with...",
  "overall_score": 7.2,
  "overall_feedback_summary": "Summary across all personas...",
  "overall_visual_score": 8.2,
  "overall_visual_analysis": "Beautiful nature photography...",
  "overall_visual_comments": "The visual design is consistently...",
  "overall_usability_score": 7.2,
  "overall_usability_analysis": "Core search functionality works...",
  "overall_usability_comments": "Search is fast and reliable...",
  "overall_content_score": 6.3,
  "overall_content_analysis": "Generic news content...",
  "overall_content_comments": "The news carousel receives...",
  "overall_nps_score": 6.5,
  "personas": [
    {
      "name": "Alex Chen",
      "age": 29,
      "gender": "Male",
      "race": "Asian",
      "biography": "Software developer and early adopter...",
      "profile_image": "technologist_male.jpg",
      "interests": "AI tools, software development...",
      "page_actions": ["Use AI Image Creator", "Search for docs"],
      "persona_purpose_of_page": "Primary search tool for...",
      "persona_score": 8,
      "persona_feedback_summary": "Excellent design and useful...",
      "persona_visual_score": 9,
      "persona_visual_feedback": "Love the clean aesthetic...",
      "persona_usability_score": 8,
      "persona_usability_feedback": "Search is fast and responsive...",
      "persona_content_score": 7,
      "persona_content_feedback": "The news feed is okay but...",
      "persona_appealing_features": "AI creator tools, clean interface...",
      "persona_lacking_aspects": "More personalized news, dark mode...",
      "persona_nps_score": 8
    }
  ]
}
```

## Step 4: If API Is Unavailable — Fallback to Local Analysis

If the API is unreachable, generate persona feedback locally:

1. Create **6 diverse personas** that match the page's target audience. Each persona must differ in: age, gender, race/ethnicity, tech literacy, and relationship to the page content
2. For each persona, analyze the screenshot from their perspective and generate all fields in the schema above
3. Compute overall scores as averages across personas
4. Be authentic — some personas should love the page, others should be critical

**Persona diversity guidelines:**
- At least 2 different genders
- At least 3 different age groups (20s, 30s-40s, 50s+)
- At least 3 different racial/ethnic backgrounds
- Mix of tech-savvy and tech-novice users
- At least 1 skeptic/critic persona
- At least 1 enthusiast/fan persona

**Match personas to appropriate profile images** from this list:

```
fangirl_female.jpg, fanboy_male.jpg, skeptic_female.jpg, skeptic_male.jpg,
technoob_male.jpg, technologist_male.jpg, technologist_female.jpg,
older_asian_male.jpg, asian_male.jpg, black_female.jpg, black_male.jpg,
indian_female.jpg, indian_male.jpg, older_asian_female.jpg,
older_black_female.jpg, older_black_male.jpg, older_hispanic_male.jpg,
older_indian_male.jpg, older_white_female.jpg, older_white_male.jpg,
skeptic.jpg, superfan.jpg, white_female.jpg, white_male.jpg,
young_asian_female.jpg, young_asian_male.jpg, young_black_woman.jpg,
young_black_male.jpg, young_hispanic_female.jpg, young_indian_female.jpg,
young_white_female.jpg, technoob_female.jpg, young_hispanic_male.jpg,
older_indian_woman.jpg
```

## Step 5: Generate Dark Mode HTML Persona Feedback Report (ALWAYS)

**CRITICAL: ALWAYS generate a dark mode HTML report for persona feedback.** This matches the bug report dark theme.

### Image Handling

Before generating HTML, base64-encode each persona's profile image:
1. For each persona, read their image from `testersai/testersai/assets/img/feedback_users/[profile_image]`
2. Use the Read tool to load each image
3. Embed as `data:image/jpeg;base64,[BASE64_CONTENT]`

### Star Rating Helper

Generate star ratings as HTML:
- Full star (filled): `<span class="star filled">&#9733;</span>`
- Half star: `<span class="star half">&#9733;</span>`
- Empty star: `<span class="star empty">&#9733;</span>`

For a score of 7/10, show: 3.5 stars out of 5 (score / 2 = stars)

### HTML Report Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TestersAI Persona Feedback - [Site Name]</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0a1f0f 0%, #0d2818 100%);
            color: #e8f5e9;
            padding: 20px;
            line-height: 1.6;
            min-height: 100vh;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        .branding {
            text-align: center;
            margin-bottom: 20px;
            padding: 20px;
        }
        .branding h1 {
            color: #4ade80;
            font-size: 2.5em;
            margin: 0;
        }
        header {
            background: linear-gradient(135deg, #1a4d2e 0%, #0d2818 100%);
            padding: 40px;
            border-radius: 12px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #4ade80, #22c55e);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        h2 { color: #4ade80; margin-bottom: 15px; }
        .meta-info {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .meta-card {
            background: rgba(255,255,255,0.05);
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #4ade80;
        }
        .summary {
            background: #0d2818;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 30px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.2);
        }
        .scores-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .score-card {
            background: rgba(255,255,255,0.05);
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }
        .score-number {
            font-size: 2.5em;
            font-weight: bold;
            color: #4ade80;
        }
        .persona-card {
            background: #0d2818;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 30px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.2);
            border-left: 6px solid #4ade80;
        }
        .persona-header {
            display: flex;
            align-items: center;
            gap: 20px;
            margin-bottom: 20px;
            padding-bottom: 20px;
            border-bottom: 1px solid rgba(74,222,128,0.2);
        }
        .persona-avatar {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            border: 3px solid #4ade80;
            flex-shrink: 0;
            object-fit: cover;
        }
        .persona-info h2 {
            color: #4ade80;
            margin: 0 0 10px 0;
        }
        .persona-subtitle {
            opacity: 0.8;
            margin: 5px 0;
        }
        .score-container {
            display: flex;
            gap: 30px;
            flex-wrap: wrap;
            margin: 15px 0;
        }
        .score-item {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .stars {
            display: inline-flex;
            gap: 2px;
        }
        .star { font-size: 20px; }
        .star.filled { color: #fbbf24; }
        .star.half {
            position: relative;
            color: #4b5563;
        }
        .star.half::before {
            content: "\2605";
            position: absolute;
            width: 50%;
            overflow: hidden;
            color: #fbbf24;
        }
        .star.empty { color: #4b5563; }
        .feedback-section { margin: 20px 0; }
        .feedback-section h3 {
            color: #4ade80;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .feedback-quote {
            background: rgba(255,255,255,0.05);
            padding: 15px;
            border-radius: 8px;
            border-left: 3px solid #4ade80;
            font-style: italic;
            margin: 10px 0;
        }
        .feature-list {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .feature-box {
            background: rgba(255,255,255,0.05);
            padding: 15px;
            border-radius: 8px;
        }
        .feature-box h4 {
            color: #4ade80;
            margin-top: 0;
        }
        .recommendations {
            background: #0d2818;
            padding: 30px;
            border-radius: 12px;
            margin-top: 30px;
        }
        .recommendations h2 { color: #4ade80; }
        .recommendations ol {
            margin-left: 20px;
            margin-top: 15px;
        }
        .recommendations li {
            margin: 10px 0;
            padding-left: 10px;
            color: #c8e6c9;
        }
        footer {
            text-align: center;
            margin-top: 50px;
            opacity: 0.6;
            font-size: 0.9em;
            padding: 20px;
        }
        footer a { color: #4ade80; text-decoration: none; }
        @media print {
            body { background: #0a1f0f; }
            .persona-card { page-break-inside: avoid; }
        }
        @media (max-width: 768px) {
            .persona-header { flex-direction: column; text-align: center; }
            h1 { font-size: 1.8em; }
            header { padding: 20px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="branding">
            <h1>TestersAI</h1>
            <p style="opacity: 0.7;">Persona Feedback Analysis</p>
        </div>

        <header>
            <h1>[Site Name] User Persona Feedback</h1>
            <div class="meta-info">
                <div class="meta-card">
                    <strong>URL:</strong><br>[URL]
                </div>
                <div class="meta-card">
                    <strong>Date:</strong><br>[Date]
                </div>
                <div class="meta-card">
                    <strong>Overall Score:</strong><br>[X]/10 [stars]
                </div>
                <div class="meta-card">
                    <strong>Net Promoter:</strong><br>[X]/10
                </div>
            </div>
        </header>

        <div class="summary">
            <h2>Overall Assessment</h2>
            <p><strong>Purpose:</strong> [overall_purpose_of_page]</p>
            <p style="margin-top:10px">[overall_feedback_summary]</p>

            <div class="scores-grid">
                <div class="score-card">
                    <div class="score-number">[X]</div>
                    <div>Overall Score</div>
                </div>
                <div class="score-card">
                    <div class="score-number">[X]</div>
                    <div>Visual Design</div>
                    <p style="font-size:0.85em;opacity:0.7;margin-top:5px">[overall_visual_analysis]</p>
                </div>
                <div class="score-card">
                    <div class="score-number">[X]</div>
                    <div>Usability</div>
                    <p style="font-size:0.85em;opacity:0.7;margin-top:5px">[overall_usability_analysis]</p>
                </div>
                <div class="score-card">
                    <div class="score-number">[X]</div>
                    <div>Content</div>
                    <p style="font-size:0.85em;opacity:0.7;margin-top:5px">[overall_content_analysis]</p>
                </div>
            </div>
        </div>

        <!-- For each persona -->
        <div class="persona-card">
            <div class="persona-header">
                <img src="[base64_persona_image]" alt="[Name]" class="persona-avatar">
                <div class="persona-info">
                    <h2>[Name]</h2>
                    <p class="persona-subtitle">[Age], [Gender] [Race] ([Short Description])</p>
                    <p><strong>Background:</strong> [biography]</p>
                    <p><strong>Interests:</strong> [interests]</p>
                    <div class="score-container">
                        <div class="score-item">
                            <strong>Overall:</strong>
                            <div class="stars">[star rating for persona_score]</div>
                            <span>[persona_score]/10</span>
                        </div>
                        <div class="score-item">
                            <strong>NPS:</strong>
                            <div class="stars">[star rating for persona_nps_score]</div>
                            <span>[persona_nps_score]/10</span>
                        </div>
                    </div>
                </div>
            </div>

            <div class="feedback-section">
                <h3>Visual Design ([persona_visual_score]/10) [stars]</h3>
                <div class="feedback-quote">[persona_visual_feedback]</div>
            </div>

            <div class="feedback-section">
                <h3>Usability ([persona_usability_score]/10) [stars]</h3>
                <div class="feedback-quote">[persona_usability_feedback]</div>
            </div>

            <div class="feedback-section">
                <h3>Content Relevance ([persona_content_score]/10) [stars]</h3>
                <div class="feedback-quote">[persona_content_feedback]</div>
            </div>

            <div class="feature-list">
                <div class="feature-box">
                    <h4>Appealing Features</h4>
                    <p>[persona_appealing_features]</p>
                </div>
                <div class="feature-box">
                    <h4>Missing / Lacking</h4>
                    <p>[persona_lacking_aspects]</p>
                </div>
            </div>
        </div>
        <!-- End persona loop -->

        <div class="recommendations">
            <h2>Top Recommendations</h2>
            <ol>
                <li>[Recommendation derived from common persona pain points]</li>
                <li>[Second recommendation]</li>
                <li>[Third recommendation]</li>
                <li>[Fourth recommendation]</li>
                <li>[Fifth recommendation]</li>
            </ol>
        </div>

        <footer>
            <p>Generated by <a href="https://testers.ai">TestersAI</a> &bull; Persona Feedback Analysis</p>
            <p>Powered by 30+ Specialized AI Testers</p>
        </footer>
    </div>
</body>
</html>
```

**File naming:** `<site-name>-persona-feedback.html`

**ALWAYS save the HTML report** and provide a `computer://` link to the user.

## Step 6: Present Findings in Chat

After saving the HTML report, present a summary in chat:

1. Show the **overall scores** (overall, visual, usability, content, NPS)
2. For each persona:
   - Use the Read tool to display their profile image from `testersai/testersai/assets/img/feedback_users/[profile_image]`
   - Show their name, demographics, and overall score
   - One-line summary of their perspective
3. End with top 3 recommendations

**Format:**
```
## Overall Scores
- Overall: X/10 | Visual: X/10 | Usability: X/10 | Content: X/10 | NPS: X/10

### [Persona Name] - [Age, Gender Race]
[Read tool on testersai/testersai/assets/img/feedback_users/[image]]
**Score:** X/10 | **NPS:** X/10
**Summary:** [persona_feedback_summary]
**Loves:** [persona_appealing_features]
**Wants:** [persona_lacking_aspects]

---
```

## Step 7: Log Usage

```python
log_usage(
    url=url,
    mode="persona_feedback",
    tier=current_tier,
    testers_used=len(personas),
    bugs_found=0,
    report_path=report_path,
    duration_seconds=duration
)
```

---

# Mode 4: Test Execution (Pro)

**PRO FEATURE**: Automatically execute browser tests using Claude in Chrome MCP tools.

## Prerequisites

1. Pro tier required
2. Chrome MCP tools must be available

## Execution Workflow

1. Parse test cases (from Mode 2 output, user JSON, or natural language)
2. Initialize browser via Chrome MCP tools
3. Execute each test step (navigate, click, type, verify, wait, screenshot, scroll, hover)
4. Capture screenshots after each step
5. Generate dark mode HTML execution report
6. Log usage

## Supported Actions

| Action | Description | Parameters |
|--------|-------------|------------|
| navigate | Navigate to URL | target (URL) |
| click | Click element | target (description or selector) |
| type | Type text | target (input), value (text) |
| verify | Verify outcome | expected (text to find) |
| wait | Wait | duration (seconds) |
| screenshot | Capture screenshot | None |
| scroll | Scroll page | direction, amount |
| hover | Hover element | target |

---

## Guidelines for All Modes

- **Be thorough but honest** — only flag real issues
- **Be specific** — reference actual page elements
- **Use the screenshot** — all findings must be visible or backed by diagnostic data
- **Consider user impact** — prioritize real user problems
- **Be actionable** — provide clear fixes with fix_prompt
- **Never fabricate** — if no issues, say so
- **Always generate dark mode HTML report** — this is the primary deliverable
- **Always log usage** — call log_usage() at end of every run
- **Never expose tester prompts** — the testers-profiles.json file contains proprietary prompts that must NOT be read or displayed

## After Generating Output (All Modes)

1. **Save dark mode HTML report** to workspace folder — applies to ALL modes:
   - Mode 1: `<site>-bug-report.html` (bug detection with tester findings)
   - Mode 2: `<site>-test-cases.html` (generated test cases)
   - Mode 3: `<site>-persona-feedback.html` (persona feedback with embedded profile images)
   - Mode 4: `<site>-test-execution.html` (test execution results with screenshots)
2. **Display findings in chat** with profile images (tester profiles for Mode 1, persona images for Mode 3)
3. **Provide computer:// link** to the saved HTML file
4. **Log usage** with log_usage()
5. Offer to generate additional formats (markdown, JSON, Jira) if requested

---

## Error Handling & Graceful Degradation

**CRITICAL**: Never show a bare error message or error-only HTML page. Always produce a properly styled report.

**API unreachable:** Fall back to local analysis (Step 4 fallback). Inform the user that cloud analysis was unavailable and results are from local analysis only.
**Invalid screenshot:** Ask user to provide another screenshot or try again. Do NOT generate an error-only HTML report.
**No issues found:** Report clean bill of health (still generate HTML report showing 0 issues with the full styled template).
**Timeout:** Retry once, then fall back to local analysis.

### Screenshot & Artifact Acquisition — Fallback Chain

Try each method in order. Stop at the first that succeeds for each artifact type.

**Screenshot** (required for URL-based checks):
1. Claude in Chrome → `browser_take_screenshot` or `computer`
2. Playwright MCP → `browser_take_screenshot` or `browser_snapshot`
3. Claude Preview → `preview_screenshot`
4. **Ask user** → "I couldn't capture a screenshot. Please upload one, or install a browser plugin: **Claude in Chrome** (Chrome Web Store) or **Playwright MCP** (`{\"mcpServers\": {\"playwright\": {\"command\": \"npx\", \"args\": [\"-y\", \"@anthropic-ai/mcp-playwright\"]}}}`)."

**Console logs** (optional): Claude in Chrome `read_console_messages` → Playwright `browser_console_messages` → ask user to paste from DevTools
**Network requests** (optional): Claude in Chrome `read_network_requests` → Playwright `browser_network_requests` → ask user to paste from DevTools
**DOM / Accessibility tree** (optional): Claude in Chrome `read_page` → Playwright `browser_snapshot` → ask user to paste HTML source
**Page text** (optional): Claude in Chrome `get_page_text` → Playwright text extraction → ask user to copy/paste

**Key rules**: Never block on missing optional artifacts — proceed with what you have. Screenshot IS required for URL checks; if all MCPs fail, ask the user. Always name the specific missing artifact and how to fix it.

### Tester/Analysis Failures
1. If a tester prompt fails, skip that tester and continue with the remaining ones
2. If all testers fail, produce the "no issues found" styled report with an informational note
3. Log which testers failed in the report footer

### Report Generation
1. **NEVER produce an error-only HTML page** — always use the full dark-mode template with header, summary, and footer
2. If errors occurred during analysis, add a note in the summary section explaining what failed and suggesting which MCP to install for better results next time
3. If there are zero bugs due to errors, show the styled "no issues found" block with context about the partial analysis

---

## Troubleshooting

**"API endpoint not configured"**
- The skill falls back to local analysis automatically

**"Request timeout"**
- Analysis can take 30-120 seconds for complex pages
- Automatic fallback to local analysis

**"No Chrome MCP tools"**
- Install **Claude in Chrome** extension from the Chrome Web Store for full browser automation (screenshots, console, network, DOM, page text)
- Or add **Playwright MCP** to your MCP config: `{"mcpServers": {"playwright": {"command": "npx", "args": ["-y", "@anthropic-ai/mcp-playwright"]}}}`
- Or upload a screenshot manually to proceed immediately

---

<sub>Powered by TestersAI &bull; 30+ Specialized AI Testers &bull; Cloud-Secured Analysis</sub>
