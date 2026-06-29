# Google Workspace CLI (`gws`) — Skills Study Guide

A complete study guide to **every skill** shipped in
[github.com/googleworkspace/cli](https://github.com/googleworkspace/cli).

The repo ships ~90 "Agent Skills" (Markdown `SKILL.md` modules under `/skills`)
that teach an AI agent how to drive Google Workspace through the `gws`
command-line tool. This guide summarizes what `gws` is, the conventions every
skill assumes, and what each individual skill does.

> Source: `googleworkspace/cli` @ `main`, skills version **0.22.5**.
> All commands below are from the project's own documentation.

---

## 1. What `gws` is

`gws` is a CLI for Google Workspace APIs built for **both humans and AI agents**.
It generates its command surface dynamically by reading Google's **Discovery
Service** at runtime, so it automatically picks up new API endpoints as Google
adds them — "zero boilerplate."

- **Services covered:** Drive, Gmail, Calendar, Sheets, Docs, Slides, Chat,
  Meet, Tasks, Keep, Forms, Classroom, People, Admin Reports, Apps Script,
  Events (push notifications), and Model Armor.
- **Output:** structured **JSON** by default (also `table`, `yaml`, `csv`).
- **Streaming:** NDJSON via `--page-all` for pagination.

### Install

```bash
npm install -g @googleworkspace/cli      # Node 18+
# or: prebuilt binary from GitHub Releases, Homebrew, Cargo, or Nix flake
```

### Authenticate

| Method | How |
|---|---|
| Interactive setup | `gws auth setup` (uses gcloud to create a project + enable APIs) |
| Browser OAuth | `gws auth login` |
| Manual OAuth | drop credentials in `~/.config/gws/client_secret.json` |
| Env token | `GOOGLE_WORKSPACE_CLI_TOKEN` |
| Credentials file | `GOOGLE_WORKSPACE_CLI_CREDENTIALS_FILE` |
| Service account | `GOOGLE_APPLICATION_CREDENTIALS` → key file |

Local credentials are encrypted at rest with **AES-256-GCM**.

---

## 2. Conventions every skill assumes (`gws-shared`)

`gws-shared` is the foundation skill. All other skills reference
`../gws-shared/SKILL.md`. Key rules:

- **Command shape:** `gws <service> <resource> [sub-resource] <method> [flags]`
- **Discovery workflow:**
  1. `gws <service> --help` — browse resources/methods
  2. `gws schema <service>.<resource>.<method>` — inspect required params/types
  3. call with `--params '{...}'` or `--json '{...}'`
- **Output:** `--format json|table|yaml|csv` (JSON is default)
- **Safety-first defaults:**
  - Never output secrets.
  - **Always confirm with the user before any write/delete command.**
  - Use `--dry-run` to preview a request without sending it.
  - `--page-all` / `--page-limit <N>` to control pagination.
- **Shell gotchas:** quote JSON with single quotes; beware zsh history
  expansion on `!` inside Sheets ranges.

### Core examples

```bash
gws drive files list --params '{"pageSize": 5}'
gws sheets spreadsheets create --json '{"properties": {"title": "Q1 Budget"}}'
gws schema drive.files.list
```

---

## 3. How the skills are installed / used

```bash
# Install all skills (or pick specific ones) into an agent project
npx skills add https://github.com/googleworkspace/cli
```

Skills work with **OpenClaw** and the **Gemini CLI Extension**; the extension
inherits the CLI's credentials automatically. Each skill is a small `SKILL.md`
with YAML frontmatter (`name`, `description`) plus example commands — it teaches
the agent *when* and *how* to call `gws` for a given task.

The skills fall into **four categories**:

1. **`gws-*`** — one skill per service (+ helper `+` command skills)
2. **`gws-workflow-*`** — multi-step cross-service workflows
3. **`persona-*`** — role bundles that combine several skills with guidance
4. **`recipe-*`** — ~50 concrete, copy-paste task templates

---

## 4. Service skills (`gws-*`)

Each service skill explains the resources/methods of that API and ships
hand-crafted **`+` helper commands** for common tasks. Helper-command skills
(e.g. `gws-gmail-send`) are split out so an agent can load just the one it needs.

### Gmail — `gws-gmail`
Email management via the Gmail API. Resources under `users`: `messages`,
`drafts`, `threads`, `labels`, `settings`, `history`, plus `getProfile`,
`watch`, `stop`. Helper skills:

| Skill | Command | Does |
|---|---|---|
| `gws-gmail-send` | `gws gmail +send` | Send mail; auto RFC 5322 / MIME / base64. Required `--to --subject --body`; optional `--cc --bcc --html --draft -a <file>` (attachments ≤ 25 MB), send-as alias. **Write — confirm first.** |
| `gws-gmail-reply` | `gws gmail +reply` | Threaded reply to sender. |
| `gws-gmail-reply-all` | `gws gmail +reply-all` | Threaded reply to everyone. |
| `gws-gmail-forward` | `gws gmail +forward` | Forward a message. |
| `gws-gmail-read` | `gws gmail +read` | Extract message body + headers. |
| `gws-gmail-triage` | `gws gmail +triage` | List unread: sender, subject, date. |
| `gws-gmail-watch` | `gws gmail +watch` | Stream incoming mail as NDJSON. |

```bash
gws gmail +send --to alice@example.com --subject 'Hello' --body 'Hi!' --cc bob@example.com
gws gmail +send --to alice@example.com --subject 'Files' --body 'Two files' -a a.pdf -a b.csv
gws gmail +send --to alice@example.com --subject 'Draft' --body 'Hi!' --draft
```

### Calendar — `gws-calendar`
Events, calendars, and free/busy. Helpers:
- `gws-calendar-insert` → `gws calendar +insert` — create an event (title, attendees, start/end).
- `gws-calendar-agenda` → `gws calendar +agenda` — timezone-aware list of today's events.
- Also exposes `gws calendar freebusy query` for availability windows.

### Drive — `gws-drive`
Files/folders, sharing, permissions. Helper:
- `gws-drive-upload` → `gws drive +upload ./report.pdf --name "Q1 Report"` (multipart upload).

### Sheets — `gws-sheets`
Spreadsheets, values, ranges. Helpers:
- `gws-sheets-append` → `gws sheets +append --spreadsheet ID --values "Alice,95"`
- `gws-sheets-read` → `gws sheets +read` — read a range.

### Docs — `gws-docs`
Documents and structured content. Helper:
- `gws-docs-write` → `gws docs +write` — write/insert content into a doc.

### Chat — `gws-chat`
Google Chat spaces/messages. Helper:
- `gws-chat-send` → `gws chat +send` — post a message to a space.

### Apps Script — `gws-script`
Manage Apps Script projects. Helper:
- `gws-script-push` → `gws script +push` — push local script code to a project.

### Events (push notifications) — `gws-events`
Subscribe to resource change notifications. Helpers:
- `gws-events-subscribe` → `gws events +subscribe`
- `gws-events-renew` → `gws events +renew` (renew an expiring channel)

### Model Armor — `gws-modelarmor`
Filter user-generated content for safety via templates. Helpers:
- `gws-modelarmor-sanitize-prompt` → `+sanitize-prompt` — vet user input before the model.
- `gws-modelarmor-sanitize-response` → `+sanitize-response` — vet model output before the user.
- `gws-modelarmor-create-template` → `+create-template` — define a new filtering template.

### Other single-service skills
| Skill | Service |
|---|---|
| `gws-slides` | Google Slides presentations |
| `gws-meet` | Google Meet spaces / conference records |
| `gws-tasks` | Google Tasks (task lists & tasks) |
| `gws-keep` | Google Keep notes |
| `gws-forms` | Google Forms (forms & responses) |
| `gws-classroom` | Google Classroom courses/rosters |
| `gws-people` | People API / contacts |
| `gws-admin-reports` | Admin SDK reports (audit/usage) |

---

## 5. Workflow skills (`gws-workflow-*`)

Cross-service, multi-step helpers, exposed as `gws workflow +<name>`.

| Skill | Command | Does |
|---|---|---|
| `gws-workflow-standup-report` | `+standup-report` | Combines **today's calendar agenda + open tasks** into a standup. Read-only. Supports `--format`. |
| `gws-workflow-meeting-prep` | `+meeting-prep` | Surfaces a meeting's attendees, description, and linked documents. |
| `gws-workflow-weekly-digest` | `+weekly-digest` | A comprehensive weekly overview. |
| `gws-workflow-email-to-task` | `+email-to-task` | Turn an email into a task. |
| `gws-workflow-file-announce` | `+file-announce` | Announce a new/shared file (e.g. to Chat). |

```bash
gws workflow +standup-report --format table
```

---

## 6. Persona skills (`persona-*`)

A persona **bundles several service skills + workflows** and adds procedural
guidance for a role (e.g. "always check for conflicts before scheduling,"
"confirm changes before finalizing"). Example — **`persona-exec-assistant`**
bundles `gws-gmail`, `gws-calendar`, `gws-drive`, `gws-chat` and the
standup-report / meeting-prep / weekly-digest workflows.

The ten personas:

| Persona | Role focus |
|---|---|
| `persona-exec-assistant` | Manage an executive's schedule, inbox, comms |
| `persona-project-manager` | Track projects, tasks, status |
| `persona-team-lead` | Team coordination, standups, reviews |
| `persona-hr-coordinator` | HR forms, onboarding, scheduling |
| `persona-it-admin` | Admin reports, provisioning, audits |
| `persona-customer-support` | Triage/respond to support email |
| `persona-sales-ops` | Deal tracking, CRM-style sheet updates |
| `persona-event-coordinator` | Invites, scheduling, materials |
| `persona-content-creator` | Docs/Slides creation & publishing |
| `persona-researcher` | Collect, organize, and summarize info |

---

## 7. Recipe skills (`recipe-*`)

Concrete, copy-paste task templates. Each recipe names a **prerequisite
`gws-*` skill**, then walks through `gws` commands step-by-step. Example —
**`recipe-find-free-time`**: requires `gws-calendar`, runs
`gws calendar freebusy query` across attendees for a window, finds a common
slot, then books it with `gws calendar +insert`.

### Calendar & scheduling
- `recipe-find-free-time` — find a slot everyone is free and book it.
- `recipe-block-focus-time` — block focus time on your calendar.
- `recipe-schedule-recurring-event` — set up a recurring event.
- `recipe-reschedule-meeting` — move an existing meeting.
- `recipe-batch-invite-to-event` — invite many people at once.
- `recipe-create-events-from-sheet` — bulk-create events from a spreadsheet.
- `recipe-plan-weekly-schedule` — lay out a week's schedule.
- `recipe-share-event-materials` — distribute materials to attendees.
- `recipe-review-meet-participants` — review Meet participation.
- `recipe-create-meet-space` — create a Meet space.

### Gmail
- `recipe-create-gmail-filter` — create a filter rule.
- `recipe-label-and-archive-emails` — label then archive.
- `recipe-forward-labeled-emails` — auto-forward by label.
- `recipe-create-vacation-responder` — set an out-of-office responder.
- `recipe-save-email-attachments` — save attachments to Drive.
- `recipe-save-email-to-doc` — capture an email into a Doc.
- `recipe-draft-email-from-doc` — draft an email from a Doc.
- `recipe-email-drive-link` — email a Drive link.
- `recipe-send-team-announcement` — broadcast to the team.

### Drive & files
- `recipe-organize-drive-folder` — tidy/organize a folder.
- `recipe-bulk-download-folder` — download a whole folder.
- `recipe-find-large-files` — locate space hogs.
- `recipe-create-shared-drive` — create a shared drive.
- `recipe-share-folder-with-team` — share a folder.
- `recipe-watch-drive-changes` — subscribe to change notifications.

### Sheets & reporting
- `recipe-backup-sheet-as-csv` — export a sheet to CSV.
- `recipe-compare-sheet-tabs` — diff two tabs.
- `recipe-copy-sheet-for-new-month` — clone a monthly template.
- `recipe-create-expense-tracker` — build an expense tracker.
- `recipe-generate-report-from-sheet` — build a report from data.
- `recipe-sync-contacts-to-sheet` — export contacts to a sheet.
- `recipe-log-deal-update` — append a sales-deal update.

### Docs, Slides & templates
- `recipe-create-doc-from-template` — instantiate a Doc template.
- `recipe-create-presentation` — build a Slides deck.
- `recipe-share-doc-and-notify` — share a Doc and notify people.

### Forms
- `recipe-create-feedback-form` — build a feedback form.
- `recipe-collect-form-responses` — gather responses.

### Tasks
- `recipe-create-task-list` — create a task list.
- `recipe-review-overdue-tasks` — surface overdue tasks.

### Classroom & misc
- `recipe-create-classroom-course` — create a Classroom course.
- `recipe-post-mortem-setup` — set up a post-mortem (doc/agenda).

---

## 8. Quick cheat-sheet

```bash
# Discover before you call
gws <service> --help
gws schema <service>.<resource>.<method>

# Generic call
gws <service> <resource> <method> --params '{...}'   # read
gws <service> <resource> <method> --json   '{...}'   # body
gws ... --dry-run                                    # preview, no send
gws ... --page-all --page-limit 100                  # paginate
gws ... --format table|yaml|csv                      # change output

# Common helpers
gws gmail +triage
gws gmail +send --to a@x.com --subject 'Hi' --body 'Hello'
gws calendar +agenda
gws drive +upload ./file.pdf --name 'File'
gws sheets +append --spreadsheet ID --values 'Alice,95'
gws workflow +standup-report --format table
```

### Golden rules (from `gws-shared`)
1. Never print secrets.
2. **Confirm with the user before any write/delete.**
3. Prefer `--dry-run` to validate first.
4. Load `gws-shared` (auth + conventions) before any service skill;
   load a service skill before its recipes.

---

*Generated as a study summary of all skills in `googleworkspace/cli`.
For authoritative, up-to-date details, read each skill's `SKILL.md` and run
`gws <service> --help` / `gws schema ...`.*
