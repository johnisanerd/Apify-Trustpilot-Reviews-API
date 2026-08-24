# ⭐ Trustpilot Reviews API: Reputation Monitoring Data as Structured JSON

> The most efficient, reliable, and developer-friendly way to use the Trustpilot Reviews API.

**Actor page:** [apify.com/johnvc/trustpilot-reviews-api](https://apify.com/johnvc/trustpilot-reviews-api?fpr=9n7kx3)
**Input schema:** [apify.com/johnvc/trustpilot-reviews-api/input-schema](https://apify.com/johnvc/trustpilot-reviews-api/input-schema?fpr=9n7kx3)

Give it one or more company review-page URLs and it returns one clean JSON row per review: the star rating, the review title and full text, the posting date, the separate date of experience, the verified flag, the reviewer's country, and any reply the business posted. Every row also carries company context, so the same pull gives you the overall rating, the total review count, and the full 5-to-1 star breakdown with counts and percentages. It is built API-first and MCP-ready, so you can call it from Python or drive it as a tool from an AI agent.

## Video Walkthrough

[![Watch the walkthrough](https://img.youtube.com/vi/jREWahDGhJM/maxresdefault.jpg)](https://www.youtube.com/watch?v=jREWahDGhJM)

### Text walkthrough

Most people arrive here because dashboards priced for enterprise reputation monitoring do not expose the underlying rows, and the official developer API is gated. This one is the opposite shape: you pass `companyUrls`, you set `maxReviewsPerCompany`, and you get flat records back. Each record carries `reviewRating`, `reviewTitle`, `reviewContent`, `reviewDate`, and `dateOfExperience`, which are separate fields on purpose because the day someone posts is rarely the day the thing happened. `isVerifiedReview` and `reviewerTotalReviews` let you weight a one-time account differently from an established reviewer. `reviewReplies` is the field that makes real reputation monitoring possible: filter for a low `reviewRating` with an empty reply list and you have an unanswered-complaint queue rather than a spreadsheet. Company-level fields ride along on every row, so `companyOverallRating` and `starBreakdown` give you the distribution behind the headline score. Put several companies in one run and the same export covers your whole competitive set. Save the input as a task in the Apify Console, schedule it weekly, and the pipeline stays current with no manual runs.

## Quick Start

### Prerequisites
- Python 3.11 or higher
- An Apify account and API key ([get a free key here](https://apify.com?fpr=9n7kx3))

1. **Clone the repository**
   ```bash
   git clone https://github.com/johnisanerd/Apify-Trustpilot-Reviews-API.git
   cd Apify-Trustpilot-Reviews-API
   ```

2. **Install dependencies with UV**
   ```bash
   # Install UV if you do not have it:
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Install project dependencies:
   uv sync
   ```

3. **Configure your API key**
   ```bash
   cp .env.example .env
   # Edit .env and add your Apify API key
   # Get your free API key at: https://apify.com?fpr=9n7kx3
   ```

4. **Run the example**
   ```bash
   uv run python trustpilot-reviews-api-example.py
   ```

The example asks for three reviews from a single company, which is deliberately tiny so your first call costs almost nothing. Raise `maxReviewsPerCompany` and add URLs once you know your budget.

### Alternative: set the API key directly
```bash
export APIFY_API_TOKEN="your_api_key_here"
uv run python trustpilot-reviews-api-example.py
```

## Why Use This Trustpilot API?

**A URL in, structured data out.** You never touch collection infrastructure. Pass company review-page URLs, or even bare domains, and get flat, predictable fields you can load straight into a sheet, a database, or a BI tool.

**Built for reputation monitoring, not one-off exports.** The date of experience is a separate field from the posting date, replies come through as structured entries, and the star breakdown carries both counts and percentages, so you can watch a rating move rather than just read where it currently sits.

**Small runs are genuinely cheap.** Billing is per review returned. The per-run start charge is one thousandth of a cent, so a three-review spot check costs roughly what three reviews cost. Actors that charge a real per-run setup fee punish exactly this pattern, and daily monitoring is exactly this pattern.

**The cap is your cost control.** `maxReviewsPerCompany` is applied at the source, so nothing beyond your cap is collected or billed. You are never paying for rows that get discarded after the fact.

**Batch a whole competitive set.** Up to 200 companies per run. Every row carries its own company name and overall rating, so one export covers the full comparison.

**Failures stay contained.** A company URL that returns nothing produces a row with `result_type: "error"` and a plain-language `error_message`, so one bad link never sinks the batch or disappears silently.

**MCP-ready.** Call it as a tool from Claude, Cursor, and other AI agents (see the install sections below). Every review row includes a one-line `summary` field, so an agent can read a record without post-processing.

## Features

### Core Capabilities
- Collect reviews from one or many company review-page URLs, up to 200 companies per run
- Bare domains such as `example.com` work as shorthand for the full review-page URL
- Cap reviews per company with `maxReviewsPerCompany`, from 1 to 1000
- Narrow to a recent window with `datePosted` for incremental monitoring runs
- Company reply text and reply date returned as structured entries

### Data Quality
- One consistent JSON row per review, every time
- Posting date and date of experience kept as separate fields
- Verified-review flag plus the reviewer's total review count, for weighting
- Full 5-to-1 star breakdown with both absolute counts and percentage shares
- Clear error rows for URLs that cannot be collected, so a batch never fails as a whole

## Run It on a Schedule

Reputation monitoring is a recurring job, not a one-time pull. Save this input as a task in the [Apify Console](https://console.apify.com) and give it a daily or weekly schedule. Each run appends to its own dataset, so you build a history of the star breakdown over time and can see the distribution shifting before the headline average does. Pair a small `maxReviewsPerCompany` with a `datePosted` window to keep recurring runs cheap: you only need the reviews that arrived since the last run.

## Usage Examples

### One company, small and cheap
```json
{
  "companyUrls": ["https://www.trustpilot.com/review/www.dugood.org"],
  "maxReviewsPerCompany": 3
}
```

### A competitive set in one run
```json
{
  "companyUrls": [
    "https://www.trustpilot.com/review/www.dugood.org",
    "example.com",
    "https://www.trustpilot.com/review/another-company.com"
  ],
  "maxReviewsPerCompany": 100
}
```

### Recent reviews only, for an incremental monitoring run
```json
{
  "companyUrls": ["https://www.trustpilot.com/review/www.dugood.org"],
  "maxReviewsPerCompany": 50,
  "datePosted": "Last 30 days"
}
```

## Input Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `companyUrls` | `list[str]` | YES | - | One or more company review-page URLs, for example `https://www.trustpilot.com/review/example.com`. A bare domain such as `example.com` also works. Up to 200 companies per run. |
| `maxReviewsPerCompany` | `int` | No | `100` | Reviews returned per company, from 1 to 1000. This is your cost control, since billing is per review returned. The cap is applied at the source, so nothing beyond it is collected or billed. |
| `datePosted` | `str` | No | `""` | Optional filter that narrows results to a recent window. Values verified working on the current build are relative windows such as `Last 30 days` and `Last 6 months`. Leave it out to return all reviews. |

## Output Format

Each review is returned as one JSON row. This is the real field set from a live run, with the reviewer's name replaced by a placeholder:

```json
{
  "result_type": "review",
  "reviewId": "689a0c5ec74e753dfb8bb0f7",
  "companyName": "DuGood Credit Union",
  "companyUrl": "https://www.trustpilot.com/review/www.dugood.org",
  "companyWebsite": "https://www.dugood.org",
  "companyCategory": "credit_union",
  "companyActivities": ["Credit Union", "Bank", "Mortgage Lender"],
  "categoryPath": ["Money & Insurance", "Credit & Debt Services", "Credit Union"],
  "companyOverallRating": 4.7,
  "companyRatingLabel": "Excellent",
  "companyTotalReviews": 4388,
  "companyIsVerified": false,
  "companyEmail": "marketing@dugood.org",
  "companyPhone": "(409) 899-3430",
  "companyLocation": "7505 Eastex Frwy, 77708, Beaumont, United States",
  "companyCountry": "US",
  "companyAbout": "We're on a mission to DO GOOD for Southeast Texas.",
  "companyLogo": "https://s3-eu-west-1.amazonaws.com/tpd/logos/592855190000ff0005a33f85/0x0.png",
  "starBreakdown": {
    "star5": { "count": 4082, "percent": 93 },
    "star4": { "count": 169, "percent": 4 },
    "star3": { "count": 55, "percent": 1 },
    "star2": { "count": 24, "percent": 1 },
    "star1": { "count": 58, "percent": 1 }
  },
  "reviewTitle": "Great service and rate",
  "reviewContent": "Everyone involved was prompt and professional.",
  "reviewRating": 5,
  "reviewDate": "2025-08-11T17:29:34.000Z",
  "dateOfExperience": "2025-08-08T00:00:00.000Z",
  "isVerifiedReview": true,
  "reviewerName": "Jane D.",
  "reviewerLocation": "US",
  "reviewerTotalReviews": 2,
  "reviewUsefulCount": 31,
  "reviewReplies": [
    {
      "text": "Thank you for trusting us with your auto loan.",
      "date": "2025-08-14T17:03:05.000Z"
    }
  ],
  "reviewUrl": "https://www.trustpilot.com/reviews/689a0c5ec74e753dfb8bb0f7",
  "summary": "5-star verified review of DuGood Credit Union by Jane D.: \"Great service and rate\"",
  "fetched_at": "2026-08-07T17:51:18.702092+00:00"
}
```

A company URL that returns nothing produces an error row instead:

```json
{
  "result_type": "error",
  "companyUrl": "https://www.trustpilot.com/review/does-not-exist.com",
  "error_type": "CollectionError",
  "error_message": "This company page no longer exists on the source site.",
  "fetched_at": "2026-08-07T17:51:18.702092+00:00"
}
```

The Actor also ships two ready-made dataset views on the Output tab: **Reviews overview** for a flat table of company, stars, title, reviewer, experience date, and verified flag, and **Reputation snapshot** for the company-level rating, total reviews, star split, and reply activity.

## People also search for

### How do I monitor my online reputation?

Run this API on your own company URL on a schedule and keep each run's dataset. `companyOverallRating` gives you the headline, and `starBreakdown` gives you counts and percentages at every level, which is where a shift shows up first. A drift from 93 percent five-star to 89 percent is visible in the breakdown long before the rounded average moves.

### How do I monitor a competitor's online reputation?

Put every company you care about into one `companyUrls` array. Each row carries its own `companyName`, `companyOverallRating`, and `starBreakdown`, so a single export covers the whole comparison set with no joining afterwards. Re-running weekly turns it into a trend rather than a snapshot.

### How do I choose a reputation monitoring tool for crisis prevention?

The question to ask is whether the tool gives you rows or only charts. Crisis prevention depends on catching the first cluster of one-star reviews and the complaints nobody answered, which means you need per-review records with rating, timestamp, and reply status. This API returns exactly those fields, so your alerting logic can live in your own code rather than inside somebody's dashboard.

### How does media monitoring support reputation management?

Review feeds and media mentions answer different halves of the same question. Media monitoring tells you what is being said about you publicly; review data tells you what your actual customers experienced and whether you replied. Feeding both into the same warehouse is common, and this API is the review half, delivered as JSON that a pipeline can consume directly.

### How do I monitor brand reputation on AI search engines?

AI assistants summarize what they can read, and review scores carry weight in those summaries. Since this Actor is MCP-ready, you can point Claude, Cursor, or ChatGPT at it and ask directly what the current rating and recent complaints look like, using live data rather than whatever was in the model's training set. The install sections below cover all five clients.

### Is this a Trustpilot scraper?

It is packaged as an API. You send JSON in and get JSON back, with no browser automation, proxies, or parsing to maintain on your side. If you searched for a way to scrape Trustpilot reviews, this does that job; it just hands you a stable field contract instead of HTML.

### How do I get customer review data into Python?

Use the Apify Python client, as `trustpilot-reviews-api-example.py` in this repo does. Install with `uv sync`, put your token in `.env`, and run it. The whole call is one `client.actor(...).call(run_input=...)` followed by iterating the run's default dataset.

### Can I run it as an MCP tool instead of writing code?

Yes. The Actor is exposed through the hosted Apify MCP server, so Claude Cowork Desktop, Claude Code, Claude on the web, Cursor, and ChatGPT can all call it as a tool. Each install section below has the exact configuration.

---

## Install in Claude Cowork Desktop

![Install in Claude Cowork Desktop](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_desktop.png)

Cowork is the desktop app's automation mode. To give it the Trustpilot Reviews API as a tool, add the Apify MCP server as a connector.

1. Open the Claude desktop app and go to **Settings → Connectors** (or **Settings → Developer → Edit Config** to edit `claude_desktop_config.json` directly).
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
2. Add the Apify MCP server, preloaded with only this Actor:

```json
{
  "mcpServers": {
    "apify": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.apify.com/?tools=actors,docs,johnvc/trustpilot-reviews-api"
      ]
    }
  }
}
```

3. Restart the app. When Cowork first calls the tool, complete the OAuth prompt in your browser, or add your Apify API token in the connector settings to skip OAuth.
4. In a Cowork chat, confirm the tool is available and ask it to run the Trustpilot Reviews API.

Download the desktop app and start a free trial: https://claude.ai/referral/uIlpa7nPLg
More help: https://docs.apify.com/platform/integrations/claude-desktop

---

## Install in Claude Code

![Install in Claude Code](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_code.png)

Claude Code is the command-line tool. Add the Actor's MCP server with one command:

```bash
claude mcp add --transport http apify \
  "https://mcp.apify.com/?tools=actors,docs,johnvc/trustpilot-reviews-api"
```

To use a token instead of browser OAuth:

```bash
claude mcp add --transport http apify \
  "https://mcp.apify.com/?tools=actors,docs,johnvc/trustpilot-reviews-api" \
  --header "Authorization: Bearer YOUR_APIFY_TOKEN"
```

Then verify with `claude mcp list`, or run `/mcp` inside a session. Ask Claude Code to call the Trustpilot Reviews API, for example "pull the last 30 days of reviews for this company and list the one-star ones with no reply".

Try Claude Code free: https://claude.ai/referral/uIlpa7nPLg
Claude Code MCP docs: https://code.claude.com/docs/en/mcp

---

## Install in Claude (website)

![Install in Claude (website)](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_ai.png)

On claude.ai you add Apify as a connector, then enable just this Actor's tool.

1. Go to **Settings → Connectors → Browse connectors** and search for **Apify MCP server**. Install it (enable or update if prompted).
2. When connecting, authenticate with your Apify API token, and enable the tool `johnvc/trustpilot-reviews-api`.
3. In any chat, open **+ → Connectors** and turn on **Apify**.
4. Alternatively, choose **Add custom connector** and paste the full MCP URL `https://mcp.apify.com/?tools=actors,docs,johnvc/trustpilot-reviews-api`, using OAuth when prompted.
5. Ask Claude to run the Trustpilot Reviews API.

Open Claude on the web: https://claude.ai

---

## Install in Cursor

![Install in Cursor](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_cursor.png)

Cursor reads MCP servers from a project file at `.cursor/mcp.json`.

1. In your project, create `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "apify": {
      "url": "https://mcp.apify.com/?tools=actors,docs,johnvc/trustpilot-reviews-api"
    }
  }
}
```

2. If you prefer token auth over browser OAuth, add a header:

```json
{
  "mcpServers": {
    "apify": {
      "url": "https://mcp.apify.com/?tools=actors,docs,johnvc/trustpilot-reviews-api",
      "headers": { "Authorization": "Bearer YOUR_APIFY_TOKEN" }
    }
  }
}
```

3. Open **Cursor → Settings → MCP** and confirm the **apify** server is connected (green dot).
4. In Composer or Chat, ask Cursor to call the Trustpilot Reviews API.

New to Cursor? Get it here: https://cursor.com/referral?code=XQP4VBLI3NNX

---

## Install in ChatGPT

![Install in ChatGPT](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_ChatGPT.png)

ChatGPT connects to the Apify MCP server through Developer mode (available on ChatGPT Pro, Plus, Business, Enterprise, and Education plans).

1. Click your profile icon, then go to **Settings > Apps**. If you do not see a **Create app** button, open **Advanced settings** and enable **Developer mode**.
2. Click **Create app** and fill out the form:
   - **Name:** Apify
   - **MCP Server URL:** `https://mcp.apify.com/?tools=actors,docs,johnvc/trustpilot-reviews-api`
   - **Authentication:** OAuth
3. Click **Create** and authorize the connection with Apify.
4. To use the app in a conversation, click **+** in the chat, choose **Developer mode**, and select **Apify**.

More help: https://docs.apify.com/platform/integrations/mcp

---

## Related APIs

- [G2 Reviews API](https://apify.com/johnvc/g2-reviews-api?fpr=9n7kx3) for B2B software reviews
- [Glassdoor Reviews API](https://apify.com/johnvc/glassdoor-reviews-api?fpr=9n7kx3) for employer reviews
- [Yelp Reviews API](https://apify.com/johnvc/yelp-reviews-api?fpr=9n7kx3) for local business reviews
- [OpenTable Reviews API](https://apify.com/johnvc/opentable-reviews-api?fpr=9n7kx3) for restaurant reviews

---

## 🌐 About Alpha OSINT

This example repo is part of [Alpha OSINT](https://www.alphaosint.com), toolset of financial and operations data sources and APIs.
For support or requests for this actor, please start a ticket [directly on our support page](https://apify.com/johnvc/trustpilot-reviews-api/issues/open?fpr=9n7kx3).

---

[**Made with care**](https://apify.com/johnvc?fpr=9n7kx3)

*Use the Trustpilot Reviews API to power reputation monitoring, competitor tracking, and customer review data pipelines with reliable, structured results.*

Last Updated: 2026.08.24
