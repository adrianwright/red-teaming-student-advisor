# GitHub Copilot Instructions

## Repository Guidelines

### Git Operations
- **NEVER** run `git commit` commands without explicit user approval
- **NEVER** run `git push` commands without explicit user approval
- **NEVER** automatically commit changes, even if they appear complete
- **NEVER** suggest or execute git operations that would modify the repository history

### Workflow Requirements
- Always ask for permission before committing any changes
- Always ask for permission before pushing to remote repository
- When suggesting git commands, present them as suggestions that require user confirmation
- Respect the user's review process - they must approve all repository modifications

### Approved Operations
- ✅ Creating, editing, and modifying files
- ✅ Running tests and builds
- ✅ Installing dependencies
- ✅ Analyzing code and providing suggestions
- ✅ Reading git status and git diff for informational purposes

### Prohibited Operations
- ❌ `git commit` (without explicit approval)
- ❌ `git push` (without explicit approval)
- ❌ `git merge` (without explicit approval)
- ❌ `git rebase` (without explicit approval)
- ❌ Any destructive git operations

## Exception Handling
If the user explicitly requests a git operation by saying phrases like:
- "commit this"
- "push to github"
- "git commit"
- "git push"

Then proceed with the requested operation, but always confirm the action first.