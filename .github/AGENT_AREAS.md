# Agent Area Assignments
# Defines which agent is responsible for each area

## 🏗️ Agent Areas and Responsibilities

### Code Quality Area
| Agent | Responsibilities | Triggers |
|-------|-----------------|----------|
| `copilot-lint-agent` | Linting, formatting, style | Push, PR |
| `copilot-refactor-agent` | Refactoring, dead code | Schedule, Manual |

### Testing Area
| Agent | Responsibilities | Triggers |
|-------|-----------------|----------|
| `copilot-test-agent` | Test generation, execution | Push, PR |
| `copilot-coverage-agent` | Coverage analysis | Push, PR |

### Security Area
| Agent | Responsibilities | Triggers |
|-------|-----------------|----------|
| `copilot-security-agent` | Vulnerability scan, secrets | Push, PR, Schedule |

### Documentation Area
| Agent | Responsibilities | Triggers |
|-------|-----------------|----------|
| `copilot-docs-agent` | READMEs, docstrings, API docs | Push, Manual |

### Performance Area
| Agent | Responsibilities | Triggers |
|-------|-----------------|----------|
| `copilot-perf-agent` | Profiling, optimization | Schedule, Manual |

### Development Area
| Agent | Responsibilities | Triggers |
|-------|-----------------|----------|
| `copilot-api-agent` | API development | Manual |
| `copilot-db-agent` | Database operations | Manual |
| `copilot-debug-agent` | Debugging, error analysis | Manual |

### Operations Area
| Agent | Responsibilities | Triggers |
|-------|-----------------|----------|
| `copilot-build-agent` | Building, packaging | Push, Tags |
| `copilot-release-agent` | Releases, versioning | Tags |
| `copilot-chatops-agent` | Comment commands | Comments |

---

## 🤖 Automation Bots

### Continuous (Every Push/PR)
- `lint.yml` → Lint Agent
- `python-ci-cd.yml` → Test Agent, Build Agent
- `security-scan.yml` → Security Agent
- `auto-review.yml` → All Agents

### On Events
- `auto-assign.yml` → Issue/PR opened
- `auto-label.yml` → Issue/PR opened
- `auto-merge.yml` → PR approved
- `auto-notify.yml` → Various events

### Scheduled
- `auto-backup.yml` → Daily
- `auto-sync.yml` → Every 6 hours
- `dependency-check.yml` → Weekly
- `auto-close-stale.yml` → Daily

### Manual
- `auto-deploy.yml` → Dispatch
- `agent-automation.yml` → Dispatch

---

## 🎯 Quick Commands

Use these ChatOps commands in any issue/PR:

| Command | Agent | Action |
|---------|-------|--------|
| `/lint` | Lint Agent | Run linting |
| `/test` | Test Agent | Run tests |
| `/coverage` | Coverage Agent | Show coverage |
| `/security` | Security Agent | Security scan |
| `/docs` | Docs Agent | Generate docs |
| `/perf` | Perf Agent | Performance analysis |
| `/help` | ChatOps Agent | Show all commands |
