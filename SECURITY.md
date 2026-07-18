# Security Policy

## Scope

This is an educational prototype that can call third-party LLM APIs (Google Gemini, OpenAI) when API keys are configured.

## API keys & secrets

- **Never commit API keys.** Keys are read from environment variables / a local `.env` (see `.env.example`), which is gitignored.
- If a key is ever committed, **rotate it immediately** at the provider console — removing it from the latest commit does not remove it from git history.

## Data privacy

- Do not enter real personal health information. When keys are set, conversation text is sent to third-party APIs and may be logged by those providers.
- The dataset in this repo is synthetic/educational.

## Reporting a vulnerability

Report suspected security issues privately via email: gelbalmertcan@gmail.com. Please do not open a public issue for sensitive reports.
