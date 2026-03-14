# README Template

> Use this template when creating README.md for new projects or major features.

---

# {Project Name}

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Version](https://img.shields.io/badge/version-1.0.0-green.svg)

> One-line project description that clearly states what this project does.

## Overview

Brief paragraph explaining:

- What problem does this project solve?
- Who is the target audience?
- What are the key features?

## Tech Stack

| Category   | Technology                        |
| ---------- | --------------------------------- |
| Language   | {TypeScript / Python / Go / etc.} |
| Framework  | {Next.js / FastAPI / etc.}        |
| Database   | {PostgreSQL / MongoDB / etc.}     |
| Deployment | {Docker / Kubernetes / etc.}      |

## Prerequisites

List all required tools and versions:

- Node.js >= 18.x
- npm >= 9.x or pnpm >= 8.x
- Docker >= 24.x (optional)

## Quick Start

### 1. Clone and Install

```bash
git clone https://github.com/org/{project-name}.git
cd {project-name}
npm install
```

### 2. Environment Setup

```bash
cp .env.example .env
# Edit .env with your values
```

### 3. Run Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure

This project follows an AI-Agent-managed, Spec-Driven Development structure:

```text
{project-name}/
├── .agent/             # AI Agent rules, workflows, and prompts
├── .github/            # CI/CD workflows and repository templates
├── app/                # Native application source
├── server/             # Backend services and API source
├── web/                # Web frontend application source
├── docs/               # Project documentation (PRD, ADR, ARD, Guides, Manuals)
├── operations/         # Operation definitions and infrastructure
├── runbooks/           # Operational, incident, and deployment runbooks
├── scripts/            # Utility and automation scripts
├── specs/              # Implementation Plans, Specs, and API Contracts
├── templates/          # Markdown templates for engineering and product
├── tests/              # Unit and Integration test suites
├── AGENTS.md           # Multi-Agent governance and persona guide
├── ARCHITECTURE.md     # High-level system blueprints and principles
├── OPERATION.md       # Target environment and deployment baseline
├── llms.txt            # System context for prompt construction
├── .env.example        # Environment template
└── README.md           # This file
```

## Available Scripts

| Command          | Description              |
| ---------------- | ------------------------ |
| `npm run dev`    | Start development server |
| `npm run build`  | Build for production     |
| `npm run test`   | Run test suite           |
| `npm run lint`   | Run linter               |
| `npm run format` | Format code              |

## Configuration

### Environment Variables

| Variable       | Required | Description                          |
| -------------- | -------- | ------------------------------------ |
| `DATABASE_URL` | Yes      | Database connection string           |
| `API_KEY`      | Yes      | External API authentication key      |
| `NODE_ENV`     | No       | Environment (development/production) |

## Extensibility & Documentation

Ensure you read the governance files before contributing or generating code via AI Agents:

- [🤖 Multi-Agent Governance](./AGENTS.md)
- [🏛️ System Architecture](./ARCHITECTURE.md)
- [⚙️ Operations Baseline](./OPERATION.md)
- [📝 Specifications & API Contracts](./specs/)
- [📚 Product & Arch Docs](./docs/)
- [🤝 Contributor Guide](./CONTRIBUTING.md)

## Testing

```bash
# Run all tests
npm run test

# Run with coverage
npm run test:coverage

# Run specific test file
npm run test -- path/to/test.spec.ts
```

## Deployment

### Docker

```bash
# Build image
docker build -t {project-name}:latest .

# Run container
docker run -p 3000:3000 --env-file .env {project-name}:latest
```

### Production Checklist

- [ ] All environment variables are set
- [ ] Database migrations are applied
- [ ] SSL/TLS is enabled
- [ ] Logging is configured
- [ ] Health check endpoint is accessible

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [COLLABORATING.md](./COLLABORATING.md) and [CONTRIBUTING.md](./CONTRIBUTING.md) for detailed guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
