# Generic Agentic SDLC Framework v1.1.0 Migration Guide

## Purpose and scope

This guide supports generic migration from framework v1.0.1 to v1.1.0. It applies to compatible project workspaces and does not prescribe a language, operating system, application server, database, customer, or deployment platform.

Migration installs framework controls only. It does not approve implementation, merge, release, deployment, unauthorized remedial database changes, unauthorized remedial security changes, provider activation, or any governed phase transition.

## Prerequisites and backup

Use Windows PowerShell 5.1 (`powershell.exe`) and a Python validation environment. The installer scripts use Windows PowerShell-compatible behavior; `pwsh` may be used only when it provides equivalent compatibility. Before any force operation, create a versioned backup or commit of the target project and record the target path. Check whether the working tree is clean: resolve, commit, or separately preserve unrelated local changes before migration. A dirty tree can be migrated only with explicit understanding that non-force conflicts are skipped and force can replace framework-managed files.

Recovery and rollback never delete a target tree recursively. Restore only framework-managed files from the backup, retain unrelated project content, and report `REWORK_REQUIRED` if recovery or rollback cannot be completed.

## v1.1.0 additions

- Agents define who performs governed work; Skills define reusable how procedures.
- Agent and Skill registries, schemas, metadata reconciliation, and Ponytail minimum-change guardrails are included.
- Agent 00 and human approval remain the workflow authority.
- Graphify is optional supplemental code intelligence, disabled by default.
- Headroom is optional context optimisation with evidence authority `NONE`, disabled by default.
- Provider descriptors and configuration are framework files only; no external provider binary is installed.

## Project bootstrap

From the framework repository, run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\bootstrap-project.ps1 -ProjectPath "<target-project>"
```

Bootstrap recursively copies the current `project-template` structure, including workspace Agents, Skills, Copilot instructions, registries, schemas, configuration, tools, governance templates, protocols, and workflows. It does not copy framework work-item history or recovery backups because those are outside `project-template`.

The default non-force operation lists copied and skipped paths. Existing target files remain unchanged. Review listed conflicts and merge project-specific customisations deliberately. Unsafe target/template overlap and destinations that escape the supplied target are rejected before copying.

## Force migration

After backup and conflict review, overwrite only framework-managed template paths:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\bootstrap-project.ps1 -ProjectPath "<target-project>" -Force
```

Force remains bounded to the supplied target and replaces only matching framework-managed source files; unrelated sibling and nested user content is preserved. Unsafe or broad destinations are rejected. It does not change human approval authority, provider mode, provider evidence authority, requirements, architecture, implementation, release, or deployment status.

## Global installation

Global installation distributes reusable Agent contracts and Skill definitions only:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\install-global.ps1
```

It does not install project configuration, governance state, work-item records, approval or decision logs, project registries, provider runtime state, external providers, or activation decisions. Existing global files are skipped unless `-Force` is explicitly supplied. An explicit destination must be a non-root, non-file, non-profile-root directory and must not use parent traversal.

## Repeated installation and reconciliation

Repeated non-force installation is idempotent: existing framework-managed files are skipped, not duplicated. After force migration, reconcile project-specific configuration deliberately; preserve project customisations outside overwritten framework-managed paths. Reconcile Agent contracts, Skill metadata, registries, and schemas against the v1.1.0 template before accepting the result.

Graphify remains `DISABLED` with `SUPPLEMENTAL_ONLY` authority. Headroom remains `DISABLED` with authority `NONE`. Neither provider is installed, contacted, or executed by bootstrap, global installation, migration, recovery, or validation.

## Validation

Run from the framework repository or equivalent copied validation context:

```powershell
python -m unittest -v tests.test_framework
python scripts/validate_framework.py project-template
git diff --check
git status --short --untracked-files=all
```

Expected results are a passing test suite, validator exit code 0, `git diff --check` exit code 0, and a reviewed status listing. FWK-TST-066 executes a disposable migration fixture, backup, non-force and force migration, post-migration validation, bounded framework-file recovery, and incomplete-recovery classification. A skipped conflict, failed command, incomplete recovery, or unreviewed overwrite is non-success and must not be reported as complete migration. Recovery is operator-managed; installers do not automatically restore files.

## Troubleshooting and security

- Missing target path: supply an explicit writable project directory.
- Existing file conflict: use non-force output to merge, or back up and use force only for intended framework-managed paths.
- Partial copy: restore affected framework-managed files from backup, preserve unrelated files, and rerun validation.
- Secrets: never place credentials in configuration, migration commands, logs, or recovery evidence. Provider configuration accepts references only.

## Known limitations

This guide does not migrate external provider software, validate real-provider interoperability, or make a governed approval decision. Separate authorized work is required for provider trial, enablement, release, deployment, or downstream adoption.

## Wave 8 documentation and release-preparation status

The v1.1.0 documentation package is being prepared under explicit human authorization. The observed `VERSION` file remains `1.0.1`; Agent 100 does not modify it. The target reference and user guides, DOCX outputs, management roadmap, README, CHANGELOG, and this migration guide are preparation artifacts until Agent 50 review, human approval, and separately authorized Agent 90 packaging.

Wave 7 has an independent PASS. The current package documents implemented and tested framework behavior, optional disabled providers, migration/recovery boundaries, and known untested runtime interoperability. It does not claim framework release, tag, merge, deployment, provider activation, provider trial, or consuming-project adoption.

## Required evidence before adoption

Before a project adopts a future released package, retain the approved source/version, clean extraction or bootstrap evidence, validator output, full test output, configuration reconciliation, backup/recovery result, security and deployment approvals, DOCX/PPTX visual review, and human release decision. Preserve `NOT_TESTED`, `BLOCKED`, `UNKNOWN`, `PARTIAL`, `DEFERRED`, `FAILED`, and `REWORK_REQUIRED` rather than converting them to PASS.
