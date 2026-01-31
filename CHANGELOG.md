# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-01-31

### Added

- **Messaging**: Implemented RabbitMQ service (`4.2.3-management-alpine`) with management UI, healthchecks, and standard logging.
- **Messaging**: Integrated RabbitMQ into the root `docker-compose.yml` via the `rabbitmq` profile.
- **Environment**: Added RabbitMQ configuration variables to `.env`.
- **Documentation**: Added ADR for RabbitMQ adoption and Supabase standalone positioning.

### Changed

- **Supabase**: Updated standalone stack definition and aligned usage expectations for the self-hosted Supabase suite.
- **Documentation**: Updated messaging documentation and added RabbitMQ service guide.

## [0.1.0] - 2026-01-27

### Added

- **Documentation**: Comprehensive restructuring of `docs/` folder, including Index, Project Overview, Architecture Stack, and Dev Guide.
- **Root Files**: Added `LICENSE`, `CHANGELOG.md`, `CONTRIBUTING.md`, and updated `README.md` to serve as a portal.
- **GitHub Standards**: Added `.github` community health file (`CODE_OF_CONDUCT`, `SECURITY`) and automation workflows (`pr-labeler`, `validate-compose`).

### Changed

- Refined `ARCHITECTURE.md` to align with the new documentation structure.
- Updated `README.md` to better reflect the current state of the project.
