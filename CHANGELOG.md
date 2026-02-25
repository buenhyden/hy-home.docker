# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
## [Unreleased]

### Added

- Add new agent rules for CI/CD pipelines, Docker, monitoring, and DevSecOps.
- Add Traefik, Terrakube, SeaweedFS, and Observability infrastructure components with new docker-compose configurations and supporting files.
- Implement CI/CD pipeline with compose validation, service management scripts, linting, and development documentation.
- Add Prometheus and Tempo configuration files, update HAProxy settings, and restructure PostgreSQL cluster setup
- Update images for Kafka, Keycloak, and PostgreSQL components; enhance Grafana OAuth settings
- Add root docker-compose.yml for infrastructure services including Ollama, and update .gitignore paths.
- Add Docker Compose setup for a KRaft Kafka cluster, Schema Registry, and Kafka Connect.
- Add initial Docker infrastructure services with configurations and documentation for various components.
- Add docker-compose configurations for SeaweedFS, Valkey, Terrakube, Cassandra, Locust, and MongoDB, and update README.
- Add Docker Compose configuration for a 3-node Kafka cluster, Schema Registry, and Kafka Connect, and refine gitignore rules.
- Add Docker Compose configurations for a comprehensive infrastructure stack including observability, data stores, and CI/CD workflow.
- Add Docker Compose configuration for Redis, Redis Exporter, RedisInsight, PostgreSQL, and PostgreSQL Exporter services.
- Introduce agent workflows and rules for Docker, Dev Containers, and sandboxed execution.
- Redis -> valkey 수정중
- 인프라 서비스 구성 최적화 및 신규 스택 추가
- **infra:** Init React JS and TS Storybook design system templates
- **observability:** Enhance alert rules with bilingual documentation and comprehensive service coverage
- **prometheus:** Enhance alert rules with Awesome Prometheus Alerts best practices
- **grafana:** Refine dashboards with datasource variables and add missing dashboards
- **n8n:** Enable private nodes support
- **infra:** Enhance n8n capabilities and optimize sonarqube resources
- **infra:** Enhance n8n capabilities and optimize sonarqube resources
- **infra:** Integrate vault, cleanup unused services, and update docs
- **infra:** Add terraform setup and update vault configuration
- Add `.env.example` files to `infra` and `projects` directories and update `.gitignore` to exclude `projects/.env`.
- Add Dependabot configuration for automated dependency updates
- Add issue templates, AI agent personas documentation, and a database setting example while updating gitignore and simplifying the README.
- Add initial README files for the project and infra directories
- Introduce comprehensive project documentation, GitHub community standards, and CI/CD workflows.
- Add `.env.example` with extensive service configurations and update `.gitignore` to rename opencode skill directory.
- Add Kafka infrastructure with a new docker-compose file and a comprehensive `.env.example` for configuration.
- Add n8n Docker Compose setup including main, worker, task runner, Valkey, and Valkey exporter services.
- Set up initial Docker Compose infrastructure for local development, integrating various services, networks, and volumes.
- Add Docker Compose configurations for Valkey, PostgreSQL, OpenSearch, and observability services, and update .gitignore.
- Add Docker Compose configurations for various infrastructure services.
- Add initial Docker Compose configurations and documentation for various infrastructure services including Vault, CouchDB, Kafka, Minio, Ollama, OpenSearch, Mail, InfluxDB, and observability components.
- Add initial Docker Compose configurations for various infrastructure services, a setup script, and an environment example.
- Add Docker Compose configurations for various infrastructure services including CouchDB, Nginx, Kafka, and OpenSearch.
- Add initial Docker Compose configurations for various infrastructure services.
- Introduce comprehensive Docker Compose configurations for various infrastructure services.
- Add Docker Compose configurations for observability stack, OpenSearch, and n8n services.
- Add OpenSearch and OpenSearch Dashboards infrastructure with OIDC authentication and security configurations.
- Add initial observability stack (Prometheus, Loki, Tempo, Grafana) and OpenSearch cluster setup.
- Add OpenSearch internal users configuration and ignore OpenSearch and Dashboards local config files.
- Set up initial documentation for ops, standards, and infra, and update gitignore to reflect storybook project path changes.
- Introduce Redis cluster, OpenSearch, Kafka, PostgreSQL, N8N, and Open WebUI services with supporting documentation.
- Add OpenSearch, OpenSearch Dashboards, and KSQL infrastructure configurations, and restructure documentation.
- Add modular Docker Compose infrastructure with categorized services for data, AI, messaging, and more.
- Add 05-messaging infrastructure category with RabbitMQ service definition and documentation.
- Add initial Docker Compose configuration for Supabase services.
- Introduce RabbitMQ messaging service, update Supabase configuration, and add architectural decision records.
- Set up Storybook design system monorepo with React TS/JS templates and standardized development tooling.
- Add numerous infrastructure services via Docker Compose and introduce Storybook project templates for Next.js and React.
- Enhance project tooling by adding Hadolint, migrating Markdownlint to YAML, expanding pre-commit checks, updating ESLint ignores, and introducing GitHub stale bot and Zizmor configurations.
- Add Docker Compose configurations for various infrastructure services including observability, data stores, messaging, authentication, and gateways.
- Introduce comprehensive GitHub Actions for CI/CD and linting, update project configurations, and refine documentation.
- Add GitHub Actions workflow for pre-commit checks.
- Introduce `validate_compose.py` script for Docker Compose file validation, including environment loading and root file integration.
- Add Python script to validate Docker Compose files, handling environment variables and dummy defaults.
- Add initial configuration and setup files for various infrastructure services, including example configs and docker-compose setups.
- Add initial infrastructure setup including observability stack (Prometheus, Loki, Tempo, Grafana), Kafka, Valkey, and OAuth2 Proxy.
- Add initial setup for OAuth2 Proxy, Prometheus, OpenSearch, Kafka, and Traefik middleware.
- Introduce Docker Compose configurations for a wide range of infrastructure services including messaging, data stores, authentication, gateways, and workflow tools.
- Add Docker Compose configuration for observability stack including Prometheus, Loki, Tempo, and Grafana.
- Introduce WSL2 clock drift troubleshooting documentation and update Prometheus alert rules to prevent false restart alerts.
- Introduce documentation templates, generation scripts, and validation tools for ADRs, PRDs, ARDs, Plans, and Specs.
- Add OpenSearch Docker Compose setup with comprehensive security configurations, including roles, action groups, and internal users.
- Add example configurations for OpenSearch and Dashboards for Keycloak OIDC integration, including supporting middleware and a troubleshooting guide.
- Introduce core infrastructure services including Kafka, OpenSearch, OAuth2 Proxy, Prometheus, and Grafana with a Kafka overview dashboard.
- Add Docker Compose configuration for a 3-node Kafka cluster (KRaft) and Schema Registry.
- Add Docker Compose configurations for a wide array of infrastructure services, data stores, and tools, and update main Docker Compose files.
- Introduce a comprehensive set of agent workflows, updated templates, and new documentation while removing old scripts and redundant files.
- Add comprehensive agent rules and standards across various domains, and update ignore files.
- Add numerous Grafana dashboards, update various Docker images, and enable bind mounts for data volumes.
- Enhance infrastructure with comprehensive documentation, operational runbooks, example configurations, and PostgreSQL cluster improvements.
- Refine Dependabot Docker scanning for infrastructure services, enhance Docker Compose validation with dummy secrets, and add architectural analysis and optimization recommendations to documentation.
- Enhance container security with `no-new-privileges` and `cap_drop: ALL`, migrate sensitive environment variables to Docker secrets, and update Supabase configuration.
- Enhance security across various infrastructure services by adding capability drops, no-new-privileges, and migrating sensitive variables to Docker secrets.
- Migrate sensitive environment variables to Docker secrets for enhanced security across services.
- Migrate CouchDB and Alertmanager credentials to Docker secrets and add new environment variables for various services.
- Add linting and secret scanning workflows, expand Dependabot to new infra services, update bug report template with Docker version, and refine labeler and compose validation.
- Introduce structured runbooks and dedicated directories for operational procedures, incidents, and postmortems, and refine documentation structure.
- Introduce a new `docs/context` hub with comprehensive operational guides and context documents, updating `operations` and `runbooks` READMEs.
- Add Ollama and Airflow blueprints and enhance existing service documentation with technical specifications and provisioning verification.
- Enhance container security by adding `no-new-privileges` and `cap_drop: ALL` to most services, create a SeaweedFS security example, and
- Implement container security hardening with `no-new-privileges` and `cap_drop` across multiple services, introduce RabbitMQ secrets, and update documentation.
- Remove `validate-compose` and `zizmor` GitHub Actions workflows, integrate Docker Compose validation into pre-commit hooks, and update changelog generation.
- Introduce a dedicated script for Docker Compose validation, integrate it into pre-commit, and update `smtp_username` to use a Docker secret.
- Add GitHub Actions workflow for greeting first-time contributors and configure Zizmor security checks.
- Implement and document standard Docker security hardening for infrastructure services by adding `no-new-privileges` and `cap_drop: ALL` to compose files and updating related documentation.
- **specs:** Add new infrastructure and feature specifications and plans, and update the main README.
- Introduce local certificate generation, Docker Compose preflight checks, and infra bootstrap runbooks for improved development readiness.
- Migrate PostgreSQL Patroni credentials from .env files to Docker secrets via a new entrypoint script and standardize Slack webhook variable.
- Introduce Docker secrets for managing sensitive credentials across various services and update preflight checks and documentation.
- Set default values for environment variables across docker-compose files and add a dedicated OAuth2 Proxy configuration.

### Changed

- Consolidate AI agent documentation, add new infrastructure configurations for Vault, Valkey, and Terrakube, and update project documentation and license.
- Standardize restart policies and enhance security for select services in docker-compose configurations.
- Migrate and restructure documentation from READMEs to dedicated guides and introduce helper scripts.
- Enhance secret management by introducing service-specific external secrets and add a Korean user dictionary for OpenSearch.
- Remove numerous example environment variables, including secret placeholders and specific service configurations, from .env.example.
- Migrate InfluxDB sensitive credentials from environment variables to Docker secrets.
- Standardize Docker Compose secret names for MinIO, Alertmanager, and Terrakube services, and add sensitive environment variable documentation.
- Adjust secret management by removing MinIO username files from CI and ignoring `SENSITIVE_ENV_VARS.md`.
- Migrate setup guides into detailed context blueprints and guides, and update related documentation.
- Improve documentation structure, enhance integration guidance, and update example patterns across guides and runbooks.
- Improve compose environment variable specificity and coverage, including Supabase PostgreSQL connection updates and expanded `.env.example` definitions, with new optimization documentation.

### Docs

- README 구조화 및 Docker 서비스(n8n, Ollama, DB) 설정 업데이트
- Docker Infra 서비스별 README 문서화 완료
- Observability(Tempo/Loki) 구성 변경 및 문서 업데이트

### Documentation

- Update README.md with improved Docker usage guide
- Add initial README files for various infrastructure services.
- Add README files for various infrastructure services.
- **infra:** Update READMEs for all services with configuration details
- **infrastructure:** Comprehensive documentation restructure
- **infra:** Synchronize documentation with active infrastructure
- **auth:** Correct OAuth2 Proxy protected services
- **infra:** Synchronize infrastructure documentation with active services
- **infra:** Document environment variables and custom builds
- **infra:** Update custom build infrastructure documentation
- **infra:** Standardize service documentation
- **observability:** Comprehensive README rewrite with architecture diagram
- **infra:** Comprehensive README rewrite with architecture and service catalog
- **n8n:** Comprehensive README with architecture, config, and troubleshooting
- **opensearch:** Comprehensive README rewrite with architecture and cluster config
- **ollama:** Comprehensive README rewrite with model management guide
- **airflow:** Comprehensive README rewrite with architecture and CLI guide
- **kafka:** Comprehensive README rewrite with KRaft architecture and usage
- **keycloak:** Comprehensive README rewrite with architecture and IdP guide
- **minio:** Comprehensive README rewrite with architecture and init guide
- **mng-db:** Comprehensive README rewrite with architecture and init guide
- **oauth2-proxy:** Comprehensive README rewrite with architecture and middleware guide
- **ollama:** Refine README with RAG workflow and hardware specs
- **postgresql-cluster:** Comprehensive README rewrite with architecture and HA guide
- **qdrant:** Comprehensive README rewrite with architecture and API guide
- **redis-cluster:** Comprehensive README rewrite with architecture and mesh diagram
- **sonarqube:** Comprehensive README rewrite with architecture and kernel guide
- **storybook:** Comprehensive README rewrite with design system workflow
- **terrakube:** Comprehensive README rewrite with architecture diagram
- **traefik:** Comprehensive README rewrite with architecture and config guide
- **valkey-cluster:** Comprehensive README rewrite with architecture and mesh diagram
- **nginx:** Comprehensive README rewrite with architecture and SSO guide
- **couchdb:** Comprehensive README rewrite with cluster architecture and init guide
- **influxdb:** Comprehensive README rewrite with architecture and auto-init guide
- **harbor:** Comprehensive README rewrite with multi-service architecture
- **n8n:** Comprehensive README rewrite with multi-stage build guide
- **observability:** Refined README rewrite with Push/Pull architecture and Maintenance guide
- Finalize infrastructure and project root documentation with comprehensive guides
- Finalize infrastructure and project root documentation with comprehensive guides
- **root:** Update READMEs to reflect workspace structure
- **root:** Comprehensive README update with directory table and scripts
- **network:** Refine network topology and documentation index
- **github:** Rename .github/README.md to .github/GITHUB_GUIDE.md
- **rules,readme,docs:** Update AI agent rules and synchronize workspace documentation
- Add contributing guidelines and architecture documentation, and update agent rule paths in AGENTS.md.
- Add README files for various infrastructure services and components including Grafana, Prometheus, Keycloak, Alertmanager, Tempo, Loki, Vault, Terraform, and SeaweedFS.
- Add comprehensive documentation for various infrastructure services, architectural decisions, and project setup.
- Introduce example ADR, PRD, and runbook documents, and enhance project documentation structure and guidelines.
- Add comprehensive setup guides, operational procedures, and runbooks for various infrastructure components, and introduce utility scripts.
- Add new operational runbooks, infrastructure specifications, and an ADR for dynamic IP addressing.
- Add new runbooks, architecture documents, and specific operations guides, while refactoring existing consolidated documentation.
- Enhance infra component READMEs with detailed service information and remove global documentation migration notes.
- Replace global documentation redirects in READMEs with detailed local service information including services, dependencies, and file maps.
- Update READMEs with detailed service, networking, and persistence information across various infrastructure components.
- Update architecture technology stack, revise operations runbook catalog, and clarify the purpose of the operations directory.
- Revamp documentation structure with role-based navigation and extensive internal linking to guides and context.
- Clarify documentation hierarchy, update architecture with security hardening, and refresh observability and AI/workflow tech stack details.

### Fixed

- **docs:** N8n README mng-db 의존성 정정
- **n8n:** Repair Dockerfile build by extending official image

### Infra

- N8n/Qdrant Observability 강화 및 n8n Redis 추가

### Miscellaneous

- Update infrastructure configurations and documentation
- **deps:** Replace dependency eslint-plugin-node with eslint-plugin-n ^14.0.0
- **deps:** Update alpine docker tag to v3.23.2
- Update Renovate configuration
- **deps:** Update apache/airflow docker tag to v3.1.5
- **deps:** Update dependency @storybook/addon-webpack5-compiler-swc to v1.0.6
- **deps:** Update kong docker tag to v2.8.5 (([#7](https://github.com/buenhyden/hy-home.docker/issues/7)))
- **deps:** Update mongo docker tag to v8.2.3
- **deps:** Update percona/mongodb_exporter docker tag to v0.47
- **deps:** Update postgrest/postgrest docker tag to v13.0.8
- **deps:** Update azbuilder/api-server docker tag to v2.29.0
- **deps:** Update azbuilder/executor docker tag to v2.29.0
- **deps:** Update azbuilder/terrakube-ui docker tag to v2.29.0
- **deps:** Update timberio/vector docker tag to v0.52.0
- **deps:** Update qdrant/qdrant docker tag to v1.16.3
- **deps:** Update opensearchproject/opensearch-dashboards docker tag to v3.4.0
- **deps:** Update postgres docker tag to v18
- **deps:** Update storybook monorepo to v10
- **deps:** Update redis/redisinsight docker tag to v3
- **deps:** Update influxdb docker tag to v2.8
- **deps:** Update supabase/postgres docker tag to v15.14.1.068
- **deps:** Update actions/checkout action to v6
- **deps:** Update syncthing/syncthing docker tag to v2.0.13
- **deps:** Update traefik docker tag to v3.6.6
- **deps:** Update chrislusf/seaweedfs docker tag to v4.05
- **deps:** Update couchdb docker tag to v3.5.1
- **deps:** Update darthsim/imgproxy docker tag to v3.30.1
- **deps:** Update kong docker tag to v3
- **deps:** Update github artifact actions
- **deps:** Update confluentinc/cp-kafka-rest docker tag to v8
- **deps:** Update confluentinc/cp-schema-registry docker tag to v8
- **deps:** Update confluentinc/cp-kafka docker tag to v8
- **deps:** Update percona/mongodb_exporter docker tag to v2
- **deps:** Update dependency lit to v3.3.2
- **deps:** Update gcr.io/cadvisor/cadvisor docker tag to v0.55.1
- **deps:** Update grafana/loki docker tag to v3.6.3
- **deps:** Update n8nio/n8n docker tag to v2.3.0
- **deps:** Update opensearchproject/opensearch docker tag to v3.4.0
- **deps:** Update prom/prometheus docker tag to v3.9.0
- **deps:** Update redis docker tag to v8.4
- **deps:** Update prometheuscommunity/elasticsearch-exporter docker tag to v1.10.0
- **deps:** Update quay.io/keycloak/keycloak docker tag to v26.5.0
- **deps:** Update storybook monorepo to v8.6.14
- **deps:** Update confluentinc/cp-kafka-connect docker tag to v8
- **deps:** Update actions/setup-python action to v6
- **deps:** Update actions/github-script action to v8
- **agent:** Consolidate and reorganize AI agent rules
- **deps:** Bump the npm_and_yarn group across 4 directories with 3 updates
- **gitignore:** Add examples/Setting_Database.txt
- **root:** Standardize configuration and documentation files
- **deps:** Bump hadolint/hadolint-action from 3.1.0 to 3.3.0
- **deps:** Bump actions/stale from 9 to 10
- **deps:** Bump actions/checkout from 4 to 6
- **deps:** Bump actions/labeler from 5 to 6
- **deps:** Bump davidanson/markdownlint-cli2-action from 16 to 22
- Remove stale pre-commit log files.
- **deps:** Bump the actions group with 2 updates
- Comment out n8n workflow service from docker-compose includes.
- Remove empty .mcp.json file
- Delete VERSION file and clear CHANGELOG.md content.
- Refresh Grafana dashboards by adding new, removing old, and modifying an existing one, and update docker-compose configuration.
- **docs:** Auto-format markdown docs and finalize MD001 syntax correction
- Automate changelog generation using git-cliff via a new GitHub Actions workflow.
- **release:** Update CHANGELOG.md [skip ci]
- **release:** Update CHANGELOG.md [skip ci]
- Version changelog as 0.0.1.
- Add yamllint and gitleaks pre-commit hooks and standardize YAML string quotes across configurations.
- **release:** Update CHANGELOG.md [skip ci]
- Externalize yamllint configuration to a dedicated file and remove redundant Docker Compose security options.
- **release:** Update CHANGELOG.md [skip ci]
- **release:** Update CHANGELOG.md [skip ci]
- **release:** Update CHANGELOG.md [skip ci]
- **release:** Update CHANGELOG.md [skip ci]
- **release:** Update CHANGELOG.md [skip ci]
- Update pre-commit hook versions for yamllint, markdownlint-cli2, actionlint, check-dependabot, and gitleaks.
- **release:** Update CHANGELOG.md [skip ci]
- **release:** Update CHANGELOG.md [skip ci]
- **release:** Update CHANGELOG.md [skip ci]
- **release:** Update CHANGELOG.md [skip ci]
- **release:** Update CHANGELOG.md [skip ci]
- **release:** Update CHANGELOG.md [skip ci]
- **deps:** Bump astral-sh/setup-uv

### Refactor

- Reorganize runbooks into a new categorized directory structure, consolidating and standardizing operational guides.
- Remove Docker Compose security options, add GitHub Actions read permissions, and format pre-commit hook arguments.

### Build

- Add default values for environment variables across various docker-compose configurations.

### Ci

- Docker-compose.test.yml 수정
- Introduce a unified CI quality workflow and add Docker Compose validation to pre-commit.

### Config

- Disable breaking change protection and commit filtering in `cliff.toml`.


