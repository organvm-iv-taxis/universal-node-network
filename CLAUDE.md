# CLAUDE.md - AI Assistant Development Guide

## Overview

This document provides guidance for Claude and other AI assistants working on the **UniNode_IO** project. It documents the codebase structure, development workflows, conventions, and best practices for contributing to this repository.

**Project Name:** UniNode_IO
**Repository:** universal-node-network
**License:** Unlicense (Public Domain)
**Status:** Early-stage development - Foundation phase

---

## 1. Project Structure & Architecture

### Current State (Foundation Phase)

```
universal-node-network/
├── .git/                    # Git repository
├── README.md               # Project overview (needs expansion)
├── LICENSE                 # Unlicense (Public Domain)
├── CLAUDE.md               # This file - AI assistant guidance
├── package.json            # (To be created) Node.js dependencies
├── tsconfig.json           # (To be created) TypeScript configuration
├── .eslintrc.json          # (To be created) ESLint configuration
├── .prettier.config.js     # (To be created) Code formatting rules
├── .gitignore              # (To be created) Git ignore rules
├── jest.config.js          # (To be created) Testing configuration
└── src/                    # (To be created) Source code directory
    ├── index.ts            # Application entry point
    ├── lib/                # Utility libraries and shared code
    ├── types/              # TypeScript type definitions
    └── __tests__/          # Test files
```

### Future Architecture Considerations

- **Technology Stack:** TypeScript, Node.js, ESM modules
- **Package Manager:** npm (with lockfile)
- **Testing:** Jest with TypeScript support
- **Linting:** ESLint + Prettier for code quality
- **Build System:** tsc or esbuild for compilation
- **Environment:** Node.js 18+ (LTS recommended)

---

## 2. Technology Stack & Configuration

### Recommended Core Dependencies (To be implemented)

```json
{
  "devDependencies": {
    "typescript": "^5.x",
    "eslint": "^8.x",
    "@typescript-eslint/eslint-plugin": "^7.x",
    "@typescript-eslint/parser": "^7.x",
    "prettier": "^3.x",
    "jest": "^29.x",
    "ts-jest": "^29.x",
    "@types/jest": "^29.x",
    "@types/node": "^20.x"
  }
}
```

### TypeScript Configuration

Future `tsconfig.json` should include:
- `"target": "ES2020"` - Modern JavaScript target
- `"module": "ESNext"` - For ESM support
- `"strict": true` - Enable all strict type checks
- `"esModuleInterop": true` - Node.js compatibility
- `"skipLibCheck": true` - Skip type checking of declaration files
- `"moduleResolution": "node"` - Node.js resolution strategy

### Code Quality Standards

- **ESLint:** Enforce consistent code style and catch common errors
- **Prettier:** Automatic code formatting (2-space indentation)
- **TypeScript:** Strict mode enabled, no `any` types without justification
- **Comments:** JSDoc for public APIs, inline comments for complex logic

---

## 3. Development Workflow for AI Assistants

### Working with Git

#### Branch Strategy
- **Development Branch:** `claude/<feature>-<session-id>`
- **Main Branch:** Used for stable releases
- **Feature Branches:** Descriptive names reflecting the feature being worked on

#### Commit Guidelines

**Commit Message Format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `refactor:` Code refactoring without behavioral changes
- `test:` Test additions or modifications
- `chore:` Build process, dependencies, tooling
- `perf:` Performance improvements
- `style:` Code style changes (formatting, semicolons, etc.)

**Examples:**
```
feat(network): implement universal node communication protocol
fix(server): resolve connection timeout issue in request handler
docs(readme): add installation and usage instructions
refactor(types): simplify type definitions and remove redundancy
test(network): add unit tests for packet validation
```

**Commit Best Practices:**
1. Keep commits focused and atomic (one logical change per commit)
2. Write descriptive commit messages that explain the "why"
3. Include relevant ticket/issue numbers in footer if applicable
4. Never commit secrets, credentials, or sensitive data
5. All commits should pass linting and tests before pushing

#### Push and Pull Workflow

```bash
# Create feature branch (if needed)
git checkout -b claude/feature-name-<session-id>

# Make changes and commit regularly
git add <files>
git commit -m "feat(scope): description"

# Push to remote with tracking
git push -u origin claude/feature-name-<session-id>

# Create Pull Request on GitHub (if applicable)
gh pr create --title "Feature: description" --body "PR body"
```

**Push Retry Logic:**
- Automatic retry with exponential backoff on network failures (2s, 4s, 8s, 16s)
- Maximum 4 retry attempts before failure
- Branch names must start with `claude/` to ensure proper routing

### Code Review Expectations

When creating pull requests:
1. Provide clear description of changes and motivation
2. Reference any related issues or tickets
3. Include test coverage for new features
4. Ensure all linting and tests pass
5. Update documentation if API changes
6. Request review from maintainers

---

## 4. File Organization Conventions

### Source Code Layout

```
src/
├── index.ts                 # Main entry point
├── types/
│   ├── index.ts            # Type exports
│   ├── network.ts          # Network-related types
│   └── common.ts           # Common/shared types
├── lib/
│   ├── network/            # Network functionality
│   │   ├── index.ts
│   │   ├── node.ts
│   │   └── protocol.ts
│   ├── utils/              # Utility functions
│   │   ├── index.ts
│   │   └── helpers.ts
│   └── config/             # Configuration management
│       └── index.ts
└── __tests__/
    ├── unit/
    │   ├── lib.test.ts
    │   └── utils.test.ts
    └── integration/
        └── network.test.ts
```

### Naming Conventions

- **Files:** kebab-case (e.g., `network-handler.ts`)
- **Directories:** kebab-case (e.g., `src/network-handlers/`)
- **Classes:** PascalCase (e.g., `NetworkNode`)
- **Functions:** camelCase (e.g., `initializeNode()`)
- **Constants:** UPPER_SNAKE_CASE (e.g., `MAX_RETRY_ATTEMPTS`)
- **Types/Interfaces:** PascalCase (e.g., `NetworkConfig`)
- **Private members:** Leading underscore (e.g., `_internalMethod()`)

### Import/Export Patterns

**Barrel Exports (index.ts):**
```typescript
// src/lib/network/index.ts
export { NetworkNode } from './node';
export { Protocol } from './protocol';
export type { NetworkConfig } from '../types/network';
```

**Avoid:**
- Circular dependencies
- Default exports (use named exports for consistency)
- Importing from nested paths (use barrel exports instead)

---

## 5. Coding Standards & Best Practices

### TypeScript Guidelines

1. **Type Safety:**
   - Enable strict mode in tsconfig
   - Avoid `any` type (use `unknown` with type guards if needed)
   - Provide explicit return types for functions
   - Define interfaces/types for object parameters

2. **Example:**
   ```typescript
   interface NodeConfig {
     id: string;
     port: number;
     timeout?: number;
   }

   export function createNode(config: NodeConfig): Promise<Node> {
     // Implementation
   }
   ```

3. **Error Handling:**
   - Use typed Error classes
   - Provide meaningful error messages
   - Use try-catch for async operations
   - Document error scenarios in JSDoc

4. **Async/Await:**
   - Prefer async/await over `.then()` chains
   - Handle promise rejections appropriately
   - Use `Promise.all()` for parallel operations

### Code Quality Standards

1. **Line Length:** Maximum 100 characters (configurable in Prettier)
2. **Indentation:** 2 spaces (no tabs)
3. **Semicolons:** Required (enforced by Prettier)
4. **Quotes:** Double quotes (enforced by Prettier)
5. **Trailing Commas:** ES5 compatibility

### Documentation Requirements

**Public APIs:**
```typescript
/**
 * Initializes a network node with the provided configuration.
 *
 * @param config - The node configuration object
 * @param config.id - Unique identifier for the node
 * @param config.port - Port number to listen on
 * @param config.timeout - Optional timeout in milliseconds (default: 5000)
 * @returns Promise resolving to the initialized node instance
 * @throws {ValidationError} If configuration is invalid
 *
 * @example
 * const node = await initializeNode({
 *   id: "node-1",
 *   port: 3000,
 *   timeout: 10000
 * });
 */
export async function initializeNode(config: NodeConfig): Promise<Node> {
  // Implementation
}
```

---

## 6. Testing Conventions

### Test Structure

- **Unit Tests:** Test individual functions and classes in isolation
- **Integration Tests:** Test interactions between multiple components
- **Test File Location:** Colocated with source files using `*.test.ts` pattern

### Writing Tests

```typescript
import { initializeNode } from '../lib/network/node';

describe('Network Node', () => {
  describe('initializeNode', () => {
    it('should create a node with valid configuration', async () => {
      const config = { id: 'test-node', port: 3000 };
      const node = await initializeNode(config);

      expect(node.id).toBe('test-node');
      expect(node.port).toBe(3000);
    });

    it('should throw error on invalid config', async () => {
      const invalidConfig = { id: '', port: -1 };

      await expect(initializeNode(invalidConfig))
        .rejects
        .toThrow(ValidationError);
    });
  });
});
```

### Test Coverage Goals

- Minimum 80% code coverage for source code
- 100% coverage for critical paths
- Integration tests for major workflows
- Run tests before committing: `npm test`

---

## 7. Building & Running the Project

### NPM Scripts (To be configured)

```json
{
  "scripts": {
    "build": "tsc",
    "dev": "ts-node src/index.ts",
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "lint": "eslint src/ --ext .ts",
    "lint:fix": "eslint src/ --ext .ts --fix",
    "format": "prettier --write src/",
    "format:check": "prettier --check src/",
    "clean": "rm -rf dist/ coverage/",
    "prepare": "npm run build"
  }
}
```

### Development Workflow

```bash
# Install dependencies
npm install

# Run in development mode
npm run dev

# Run tests
npm test

# Format code
npm run lint:fix
npm run format

# Build for production
npm run build
```

---

## 8. Environment Configuration

### Environment Variables

Create `.env.example` for template:
```
NODE_ENV=development
LOG_LEVEL=info
NETWORK_TIMEOUT=5000
MAX_CONNECTIONS=100
```

### .gitignore (To be created)

```
# Dependencies
node_modules/
package-lock.json
yarn.lock

# Build output
dist/
build/
*.tsbuildinfo

# Environment
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Testing
coverage/
.nyc_output/

# Logs
logs/
*.log
npm-debug.log*
```

---

## 9. CI/CD and Automation (Recommended)

### GitHub Actions Workflow (To be implemented)

Future `.github/workflows/test.yml`:
```yaml
name: Test & Lint

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [18.x, 20.x]

    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: ${{ matrix.node-version }}

      - run: npm ci
      - run: npm run lint
      - run: npm test -- --coverage
      - uses: codecov/codecov-action@v3
```

---

## 10. Common Tasks for AI Assistants

### Adding a New Feature

1. Create feature branch: `git checkout -b claude/feature-name-<session-id>`
2. Create feature files in appropriate `src/` location
3. Add TypeScript types in `src/types/`
4. Write unit tests in `src/__tests__/unit/`
5. Update barrel exports if creating new module
6. Run tests: `npm test`
7. Lint and format: `npm run lint:fix && npm run format`
8. Commit with descriptive message: `git commit -m "feat(scope): description"`
9. Push: `git push -u origin claude/feature-name-<session-id>`

### Fixing a Bug

1. Create bug fix branch: `git checkout -b claude/fix-<bug-name>-<session-id>`
2. Write test that reproduces the bug
3. Implement the fix in source code
4. Verify test passes
5. Run all tests: `npm test`
6. Commit: `git commit -m "fix(scope): fix description"`
7. Push: `git push -u origin claude/fix-<bug-name>-<session-id>`

### Updating Documentation

1. Create docs branch: `git checkout -b claude/docs-<topic>-<session-id>`
2. Update relevant `.md` files
3. Ensure links are valid
4. Check formatting in markdown
5. Commit: `git commit -m "docs(section): description"`
6. Push: `git push -u origin claude/docs-<topic>-<session-id>`

### Running Tests Before Commit

```bash
# Full test suite with coverage
npm run clean
npm run lint:fix
npm run format
npm test -- --coverage

# Only commit if all pass
git add .
git commit -m "..."
git push -u origin <branch>
```

---

## 11. Important Conventions for Claude

### When Writing Code

1. **Always use TypeScript strict mode** - No `any` types without justification
2. **Write tests first for bugs** - Reproduce issue with test, then fix
3. **Keep changes focused** - One logical change per commit
4. **Document public APIs** - Use JSDoc with examples
5. **Follow naming conventions** - Files: kebab-case, Classes: PascalCase, Functions: camelCase
6. **Use barrel exports** - Don't import from nested paths
7. **Handle errors explicitly** - Don't silently fail

### When Committing

1. **Write descriptive messages** - Explain the "why", not just "what"
2. **Keep commits atomic** - One logical change per commit
3. **Reference issues** - Use `Closes #123` in commit body if applicable
4. **Test before pushing** - Run `npm test` and linting checks
5. **Use proper commit types** - feat, fix, docs, refactor, test, chore, perf, style

### When Creating Pull Requests

1. **Clear title and description** - Explain what and why
2. **Include test coverage** - New features need tests
3. **Pass all checks** - Linting, tests, and build must pass
4. **Request review** - Tag relevant team members
5. **Update docs** - If API changes, update documentation

### When Reviewing Code (For other AI Assistants)

1. **Check TypeScript compliance** - Strict mode, no `any` types
2. **Verify test coverage** - New code should have tests
3. **Ensure consistency** - Follow existing patterns and conventions
4. **Validate error handling** - Errors should be caught and logged
5. **Review documentation** - Public APIs need JSDoc

---

## 12. Project Roadmap & Future Phases

### Phase 1: Foundation (Current)
- [ ] Set up TypeScript, ESLint, Prettier configuration
- [ ] Create package.json with core dependencies
- [ ] Implement build and test infrastructure
- [ ] Set up GitHub Actions CI/CD
- [ ] Create comprehensive README documentation

### Phase 2: Core Network Implementation
- [ ] Design network protocol specification
- [ ] Implement NetworkNode base class
- [ ] Create message/packet handling system
- [ ] Implement peer discovery mechanism
- [ ] Add comprehensive unit tests

### Phase 3: Advanced Features
- [ ] Implement consensus mechanism
- [ ] Add data persistence layer
- [ ] Create monitoring and metrics system
- [ ] Add performance optimizations
- [ ] Create integration tests

### Phase 4: Production Readiness
- [ ] Security audit and hardening
- [ ] Performance benchmarking
- [ ] Documentation completion
- [ ] Release management setup
- [ ] Docker containerization (optional)

---

## 13. References & Resources

- **TypeScript Documentation:** https://www.typescriptlang.org/docs/
- **Node.js Best Practices:** https://nodejs.org/en/docs/guides/
- **Jest Testing:** https://jestjs.io/
- **ESLint Rules:** https://eslint.org/docs/rules/
- **Prettier Configuration:** https://prettier.io/docs/
- **Unlicense:** https://unlicense.org/

---

## 14. Quick Reference: Common Commands

```bash
# Development
npm install                    # Install dependencies
npm run dev                   # Run in development mode
npm run build                 # Build for production

# Testing
npm test                      # Run all tests
npm run test:watch           # Watch mode for tests
npm run test:coverage        # Run with coverage report

# Code Quality
npm run lint                  # Check linting issues
npm run lint:fix             # Fix linting issues automatically
npm run format               # Format code with Prettier
npm run format:check         # Check formatting without changes

# Cleanup
npm run clean                # Remove build artifacts and coverage

# Git
git status                   # Check working tree status
git add <files>              # Stage changes
git commit -m "..."          # Create commit
git push -u origin <branch>  # Push to remote
```

---

## 15. Questions & Support

For questions about conventions or development process:
1. Review this CLAUDE.md document thoroughly
2. Check existing code examples in `src/`
3. Review recent commits for patterns
4. Consult TypeScript/Node.js documentation
5. Ask in project issues/discussions if available

---

**Document Version:** 1.0
**Last Updated:** 2025-11-18
**Maintained By:** Claude AI Assistant
**Status:** Active
