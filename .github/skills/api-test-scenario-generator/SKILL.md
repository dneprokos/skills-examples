---
name: api-test-scenario-generator
description: Generate comprehensive API test scenarios in table format based on prompt descriptions. Creates structured test cases with boundary analysis, validation testing, and testing pyramid principles for REST API endpoints.
---

# API Test Scenario Generator

This skill generates comprehensive API test scenarios in table format based on natural language descriptions. It applies testing pyramid principles, boundary analysis, and validation testing techniques to create structured test cases for REST API endpoints.

## Features

- **Comprehensive Coverage**: Generates positive, negative, boundary, and edge case scenarios
- **Testing Pyramid Application**: Balances unit, integration, and E2E test scenarios
- **Boundary Analysis**: Identifies critical boundary conditions and edge cases
- **Validation Testing**: Includes input validation, authentication, and authorization tests
- **Structured Output**: Formatted table with scenario descriptions, expected results, and test classifications

## Usage

Use this command format:

```
/api-test-scenario-generator {HTTP_METHOD} {ENDPOINT_PATH} [additional_context]
```

### Examples

```
/api-test-scenario-generator POST /api/users
/api-test-scenario-generator GET /api/users/{id}
/api-test-scenario-generator PUT /api/orders/{id}/status
```

### Example Output File Structure

**File**: `requirements/users/GET_users_id.md`

```markdown
# GET /api/users/{id} Test Scenarios

| Scenario   | Test Type  | Description                   | Expected Result      | HTTP Status | Recommended Test Level |
| ---------- | ---------- | ----------------------------- | -------------------- | ----------- | ---------------------- |
| Valid ID   | Happy Path | Get user with valid ID        | User object returned | 200         | Integration            |
| Invalid ID | Negative   | Get user with non-existent ID | Error message        | 404         | Unit                   |

## Warnings and Assumptions

⚠️ **Authentication Requirements**: Assumed endpoint requires authentication but not specified  
⚠️ **Rate Limiting**: Unknown if endpoint has rate limiting constraints  
⚠️ **User Permissions**: Assumed all authenticated users can access any user data
```

## Generated Table Format

| Scenario | Test Type | Description | Expected Result | HTTP Status | Recommended Test Level |
| -------- | --------- | ----------- | --------------- | ----------- | ---------------------- |
| ...      | ...       | ...         | ...             | ...         | ...                    |

## Output Requirements

### File Generation

- **Format**: Always save output in `.md` format
- **Location**: `requirements/{main_resource_name}/{method_name}_{resource_path}.md`
  - Example: `requirements/users/GET_users_id.md` for `GET /api/users/{id}`
  - Example: `requirements/orders/PUT_orders_id_status.md` for `PUT /api/orders/{id}/status`
- **Overwrite Check**: If file already exists, prompt user to confirm overwrite
- **File Structure**: Include table followed by any warnings/unknowns

### Warning Documentation

- **Location**: All warnings about unknowns must be listed at the end of the document
- **Format**: Use attention sign (⚠️) for each warning
- **Content**: Include specific details about what information was missing or assumed

### Plan Mode Behavior

- **No Implementation Questions**: Do not ask about test implementation details in Plan mode
- **Focus**: Generate scenarios only, separate test generation to different skill

## Testing Pyramid Guidelines

- **Unit Tests (70%)**: Validation, boundary cases, error conditions - fast isolated tests
- **Integration Tests (20%)**: API contracts, authentication, happy paths - moderate coverage
- **E2E Tests (10%)**: Critical user journeys only - minimal but essential coverage

This ensures minimal E2E test maintenance while maximizing coverage efficiency.

## Test Classifications

- **Happy Path**: Normal successful operations
- **Boundary**: Edge cases and limit testing
- **Negative**: Error conditions and invalid inputs
- **Security**: Authentication and authorization tests
- **Performance**: Load and stress testing scenarios

## Configuration

The skill uses configuration files to customize test generation:

- `config/validation-rules.json` - Input validation patterns
- `config/test-types.json` - Test classification definitions
- `templates/` - Table format templates

## Implementation

This skill analyzes the provided HTTP method and endpoint to generate appropriate test scenarios using:

1. **Pattern Recognition**: Identifies common API patterns (CRUD, pagination, filtering)
2. **Boundary Analysis**: Generates edge cases based on data types and constraints
3. **Security Testing**: Includes authentication, authorization, and input sanitization tests
4. **Error Scenarios**: Creates comprehensive error condition coverage
5. **Performance Considerations**: Suggests scenarios for load and stress testing

### File Generation Process

1. **Parse Input**: Extract HTTP method and resource path
2. **Generate Scenarios**: Create comprehensive test scenario table
3. **Collect Warnings**: Track any assumptions or missing information
4. **Check Existing File**: Verify if output file already exists in requirements folder
5. **Generate Output**: Create markdown file with table and warnings section
6. **Save File**: Write to `requirements/{resource}/{method}_{path}.md` format

### Warning Collection

During scenario generation, the skill tracks:

- Missing authentication requirements
- Unknown data types or constraints
- Assumed business rules or validations
- Unclear endpoint behavior or responses

All warnings are documented at the end with ⚠️ symbols for easy identification.
