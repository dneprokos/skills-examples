# API Test Scenario Generator

A comprehensive VS Code agent skill for generating structured API test scenarios based on HTTP methods and endpoints.

## Quick Start

Use the skill with this command format:

```
/api-test-scenario-generator POST /api/users
```

This will generate a comprehensive test scenario table covering:

- ✅ Happy path scenarios
- ✅ Boundary and edge cases
- ✅ Negative test cases
- ✅ Security testing
- ✅ Performance scenarios

## Features

### 🎯 Comprehensive Coverage

- **Happy Path**: Normal successful operations
- **Boundary**: Edge cases and limit testing
- **Negative**: Error conditions and invalid inputs
- **Security**: Authentication, authorization, and input sanitization
- **Performance**: Load testing and rate limiting scenarios

### 📊 Testing Pyramid Application

- Balances unit (70%), integration (20%), and E2E (10%) test scenarios
- Prioritizes scenarios by importance (H/M/L)
- Applies boundary analysis techniques

### 📋 Structured Output

Generated scenarios include:

- Scenario name and classification
- Detailed test description
- Expected results
- HTTP status codes
- Priority levels

## Example Usage

```bash
# Basic endpoint
/api-test-scenario-generator GET /api/users

# Resource endpoint with path parameter
/api-test-scenario-generator PUT /api/users/{id}

# Complex endpoint
/api-test-scenario-generator POST /api/orders/{orderId}/items
```

## Generated Table Format

| Scenario                | Test Type  | Description                                          | Expected Result               | HTTP Status | Priority |
| ----------------------- | ---------- | ---------------------------------------------------- | ----------------------------- | ----------- | -------- |
| Create new resource     | Happy Path | POST /api/users with valid data creates new resource | Resource created successfully | 201         | H        |
| Missing required fields | Negative   | POST /api/users with missing required fields         | Validation error              | 422         | H        |
| Invalid authentication  | Security   | POST /api/users with invalid or expired token        | Authentication failed error   | 401         | H        |

## Files Structure

```
.github/skills/api-test-scenario-generator/
├── SKILL.md                    # Main skill definition
├── README.md                   # This documentation
├── templates/
│   ├── scenario-table.md       # Table format template
│   └── full-report.md         # Full report template
├── config/
│   ├── validation-rules.json  # Input validation patterns
│   └── test-types.json        # Test classifications
└── scripts/
    └── generate-scenarios.js  # Main generation script
```

## Configuration

### Validation Rules (`config/validation-rules.json`)

- Input validation patterns for different data types
- HTTP method configurations and expected status codes
- Authentication types and error codes

### Test Types (`config/test-types.json`)

- Test type definitions and priorities
- Testing pyramid level configurations
- Category classifications

## Test the Skill

Try it with a simple API endpoint:

```
/api-test-scenario-generator POST /api/flowsheets
```

This should generate comprehensive test scenarios including create operations, validation testing, security checks, and error handling.

## Implementation Tips

When using the generated scenarios in your tests:

1. **Prioritize by importance**: Implement H → M → L priority scenarios
2. **Use test builders**: Create data factories for consistent test data
3. **Group related tests**: Organize scenarios into logical test suites
4. **Mock dependencies**: Use mocks for external services in unit tests
5. **Test isolation**: Use database transactions or cleanup for test isolation

## Supported HTTP Methods

- **GET**: Retrieval operations with pagination, filtering, and error cases
- **POST**: Creation operations with validation and conflict scenarios
- **PUT**: Full update operations with idempotency testing
- **PATCH**: Partial update operations with field validation
- **DELETE**: Removal operations with dependency checking

## Architecture

The skill uses pattern recognition to identify common API patterns:

- Collection vs. resource endpoints
- Path parameter extraction
- CRUD operation mapping
- REST convention adherence

Generated scenarios follow testing best practices:

- Boundary value analysis
- Equivalence partitioning
- Error condition coverage
- Security testing principles

---

**Ready to generate comprehensive API test scenarios!** 🚀

Use `/api-test-scenario-generator {METHOD} {ENDPOINT}` to get started.
