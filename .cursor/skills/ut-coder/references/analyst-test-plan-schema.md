# Analyst Test Plan — JSON Schema

This file documents the JSON structure the **Analyst role** must produce during test generation. Emit the full JSON to the user before pausing for review (unless `skipReview: true`).

> **Sync:** This file is replicated in `ut-analyst/references/` and `ut-coder/references/`. The canonical source is `.github/skills/ut-analyst/references/analyst-test-plan-schema.md`. Update both (and their `.cursor/skills/` mirrors) together.

## Schema

```json
{
  "className": "string — fully qualified class/function/component name",
  "language": "csharp | java | python | typescript",
  "testFilePath": "string — expected test file location relative to project root",

  "dependencies": [
    {
      "name": "string — parameter/field name",
      "typeName": "string — declared type name (e.g., IUserRepository, Address)",
      "classification": "interface | abstract | valueObject | dto | primitive",
      "mockStrategy": "mock | real — pre-populated by the Analyst using the deterministic classification rule (interface/abstract → mock; valueObject/dto/primitive → real). The Architect may override for edge cases."
    }
  ],

  "constructorNullGuards": [
    {
      "paramName": "string — parameter name",
      "typeName": "string — declared type",
      "expectedException": "string — e.g., ArgumentNullException, NullPointerException, TypeError"
    }
  ],

  "nonDeterministicCalls": [
    {
      "location": "string — method name where the call appears",
      "callExpression": "string — exact call, e.g., DateTime.UtcNow",
      "category": "time | randomId | randomNumber",
      "stabilityWarning": "string — brief description of why this is unstable",
      "suggestedAbstraction": {
        "interfaceName": "string — e.g., IDateTimeProvider",
        "methodSignature": "string — e.g., DateTimeOffset UtcNow { get; }",
        "note": "string — short guidance on injecting the abstraction"
      }
    }
  ],

  "methods": [
    {
      "name": "string — method name",
      "isAsync": true,
      "returnType": "string",
      "parameters": [
        {
          "name": "string",
          "typeName": "string",
          "classification": "interface | abstract | valueObject | dto | primitive"
        }
      ],
      "testCases": [
        {
          "id": "string — short unique id, e.g., TC-01",
          "technique": "EP | BVA | DT | ST",
          "category": "happyPath | edgeCase | errorCase | nullGuard | stateTransition",
          "scenario": "string — human-readable scenario description",
          "inputs": {
            "paramName": "value or description"
          },
          "expectedOutcome": "string — what should happen",
          "boundaryValues": [
            "string — list of boundary values tested, if BVA technique"
          ]
        }
      ]
    }
  ]
}
```

## Field Descriptions

### `dependencies[].classification` and `mockStrategy`

The Analyst classifies every dependency and pre-populates `mockStrategy` based on the following deterministic rule. The Architect reviews this and may override for edge cases (e.g., adding non-determinism abstractions).

| Classification | Meaning                                                                 | mockStrategy |
| -------------- | ----------------------------------------------------------------------- | ------------ |
| `interface`    | Declared as an interface                                                | `mock`       |
| `abstract`     | Declared as an abstract class                                           | `mock`       |
| `valueObject`  | Immutable type with value semantics (e.g., `Money`, `Address`, `Email`) | `real`       |
| `dto`          | Data transfer object / request / response class                         | `real`       |
| `primitive`    | Value type or `string`                                                  | `real`       |

### `testCases[].technique`

| Code  | Technique                |
| ----- | ------------------------ |
| `EP`  | Equivalence Partitioning |
| `BVA` | Boundary Value Analysis  |
| `DT`  | Decision Table           |
| `ST`  | State Transition         |

### `testCases[].category`

| Value             | Description                                          |
| ----------------- | ---------------------------------------------------- |
| `happyPath`       | Valid typical input — expected success               |
| `edgeCase`        | Boundary, empty, zero, single-item, null inputs      |
| `errorCase`       | Invalid input — expected exception or error          |
| `nullGuard`       | Constructor parameter null — expected null exception |
| `stateTransition` | Behavioral change due to internal state              |

## Example

```json
{
  "className": "OrderService",
  "language": "csharp",
  "testFilePath": "OrderService.Tests/Services/OrderServiceTests.cs",

  "dependencies": [
    {
      "name": "orderRepository",
      "typeName": "IOrderRepository",
      "classification": "interface",
      "mockStrategy": "mock"
    },
    {
      "name": "shippingAddress",
      "typeName": "Address",
      "classification": "valueObject",
      "mockStrategy": "real"
    }
  ],

  "constructorNullGuards": [
    {
      "paramName": "orderRepository",
      "typeName": "IOrderRepository",
      "expectedException": "ArgumentNullException"
    }
  ],

  "nonDeterministicCalls": [
    {
      "location": "PlaceOrder",
      "callExpression": "DateTime.UtcNow",
      "category": "time",
      "stabilityWarning": "Tests will fail non-deterministically if the expected timestamp is hardcoded. Time-sensitive assertions become brittle across time zones and CI environments.",
      "suggestedAbstraction": {
        "interfaceName": "IDateTimeProvider",
        "methodSignature": "DateTimeOffset UtcNow { get; }",
        "note": "Inject IDateTimeProvider into OrderService constructor, then mock it in tests to return a fixed value."
      }
    }
  ],

  "methods": [
    {
      "name": "PlaceOrder",
      "isAsync": true,
      "returnType": "Task<Order>",
      "parameters": [
        {
          "name": "customerId",
          "typeName": "int",
          "classification": "primitive"
        },
        {
          "name": "address",
          "typeName": "Address",
          "classification": "valueObject"
        }
      ],
      "testCases": [
        {
          "id": "TC-01",
          "technique": "EP",
          "category": "happyPath",
          "scenario": "valid customer ID and address",
          "inputs": {
            "customerId": 42,
            "address": "new Address(\"123 Main St\", \"Springfield\")"
          },
          "expectedOutcome": "Returns Order with assigned ID and saves to repository",
          "boundaryValues": []
        },
        {
          "id": "TC-02",
          "technique": "BVA",
          "category": "edgeCase",
          "scenario": "customer ID at lower boundary (0)",
          "inputs": { "customerId": 0, "address": "valid address" },
          "expectedOutcome": "Throws ArgumentOutOfRangeException",
          "boundaryValues": ["0", "1", "-1"]
        },
        {
          "id": "TC-03",
          "technique": "EP",
          "category": "errorCase",
          "scenario": "address is null",
          "inputs": { "customerId": 1, "address": "null" },
          "expectedOutcome": "Throws ArgumentNullException with param name 'address'",
          "boundaryValues": []
        },
        {
          "id": "TC-04",
          "technique": "EP",
          "category": "nullGuard",
          "scenario": "constructor called with null orderRepository",
          "inputs": { "orderRepository": "null" },
          "expectedOutcome": "Throws ArgumentNullException with param name 'orderRepository'",
          "boundaryValues": []
        }
      ]
    }
  ]
}
```
