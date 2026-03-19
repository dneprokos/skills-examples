const fs = require("fs");
const path = require("path");

class APITestScenarioGenerator {
  constructor() {
    this.skillDir = path.dirname(path.dirname(__filename));
    this.loadConfig();
    this.loadTemplates();
  }

  loadConfig() {
    const validationRulesPath = path.join(
      this.skillDir,
      "config",
      "validation-rules.json",
    );
    const testTypesPath = path.join(this.skillDir, "config", "test-types.json");

    this.validationRules = JSON.parse(
      fs.readFileSync(validationRulesPath, "utf8"),
    );
    this.testTypes = JSON.parse(fs.readFileSync(testTypesPath, "utf8"));
  }

  loadTemplates() {
    const scenarioTablePath = path.join(
      this.skillDir,
      "templates",
      "scenario-table.md",
    );
    const fullReportPath = path.join(
      this.skillDir,
      "templates",
      "full-report.md",
    );

    this.templates = {
      scenarioTable: fs.readFileSync(scenarioTablePath, "utf8"),
      fullReport: fs.readFileSync(fullReportPath, "utf8"),
    };
  }

  parseEndpoint(endpoint) {
    const segments = endpoint.split("/").filter((s) => s);
    const hasPathParam = endpoint.includes("{") || endpoint.includes(":");
    const isCollection = !hasPathParam && segments.length > 0;
    const isResource = hasPathParam;

    return {
      segments,
      hasPathParam,
      isCollection,
      isResource,
      resourceName: segments[segments.length - 1]?.replace(/[{}:]/g, ""),
      pathParams: this.extractPathParams(endpoint),
    };
  }

  extractPathParams(endpoint) {
    const matches = endpoint.match(/\{([^}]+)\}/g) || [];
    return matches.map((match) => match.slice(1, -1));
  }

  generateScenarios(method, endpoint, additionalContext = "") {
    const endpointInfo = this.parseEndpoint(endpoint);
    const scenarios = [];

    // Happy path scenarios
    scenarios.push(
      ...this.generateHappyPathScenarios(method, endpoint, endpointInfo),
    );

    // Boundary scenarios
    scenarios.push(
      ...this.generateBoundaryScenarios(method, endpoint, endpointInfo),
    );

    // Negative scenarios
    scenarios.push(
      ...this.generateNegativeScenarios(method, endpoint, endpointInfo),
    );

    // Security scenarios
    scenarios.push(
      ...this.generateSecurityScenarios(method, endpoint, endpointInfo),
    );

    // Performance scenarios
    scenarios.push(
      ...this.generatePerformanceScenarios(method, endpoint, endpointInfo),
    );

    return scenarios;
  }

  generateHappyPathScenarios(method, endpoint, endpointInfo) {
    const scenarios = [];
    const methodConfig = this.validationRules.httpMethods[method];

    switch (method) {
      case "GET":
        if (endpointInfo.isCollection) {
          scenarios.push({
            scenario: "Retrieve all resources",
            testType: "Happy Path",
            description: `GET ${endpoint} returns list of all available resources`,
            expectedResult: "List of resources returned",
            httpStatus: 200,
            testLevel: "Integration",
          });

          scenarios.push({
            scenario: "Retrieve with pagination",
            testType: "Happy Path",
            description: `GET ${endpoint}?page=1&limit=10 returns paginated results`,
            expectedResult: "Paginated list with metadata",
            httpStatus: 200,
            testLevel: "Unit",
          });
        } else if (endpointInfo.isResource) {
          scenarios.push({
            scenario: "Retrieve existing resource",
            testType: "Happy Path",
            description: `GET ${endpoint} with valid ID returns resource details`,
            expectedResult: "Resource details returned",
            httpStatus: 200,
            testLevel: "Integration",
          });
        }
        break;

      case "POST":
        scenarios.push({
          scenario: "Create new resource",
          testType: "Happy Path",
          description: `POST ${endpoint} with valid data creates new resource`,
          expectedResult: "Resource created successfully",
          httpStatus: 201,
          testLevel: "Integration",
        });
        break;

      case "PUT":
        scenarios.push({
          scenario: "Update existing resource",
          testType: "Happy Path",
          description: `PUT ${endpoint} with valid data updates existing resource`,
          expectedResult: "Resource updated successfully",
          httpStatus: 200,
          testLevel: "Integration",
        });
        break;

      case "PATCH":
        scenarios.push({
          scenario: "Partial update resource",
          testType: "Happy Path",
          description: `PATCH ${endpoint} with partial data updates specified fields`,
          expectedResult: "Resource partially updated",
          httpStatus: 200,
          testLevel: "Integration",
        });
        break;

      case "DELETE":
        scenarios.push({
          scenario: "Delete existing resource",
          testType: "Happy Path",
          description: `DELETE ${endpoint} removes existing resource`,
          expectedResult: "Resource deleted successfully",
          httpStatus: 204,
          testLevel: "Integration",
        });
        break;
    }

    return scenarios;
  }

  generateBoundaryScenarios(method, endpoint, endpointInfo) {
    const scenarios = [];

    if (method === "GET" && endpointInfo.isCollection) {
      scenarios.push({
        scenario: "Empty collection",
        testType: "Boundary",
        description: `GET ${endpoint} when no resources exist`,
        expectedResult: "Empty array returned",
        httpStatus: 200,
        testLevel: "Unit",
      });

      scenarios.push({
        scenario: "Maximum page size",
        testType: "Boundary",
        description: `GET ${endpoint}?limit=1000 with maximum allowed limit`,
        expectedResult: "Results limited to max page size",
        httpStatus: 200,
        testLevel: "E2E",
      });
    }

    if (["POST", "PUT", "PATCH"].includes(method)) {
      scenarios.push({
        scenario: "Maximum field lengths",
        testType: "Boundary",
        description: `${method} ${endpoint} with maximum allowed field lengths`,
        expectedResult: "Data accepted and processed",
        httpStatus: method === "POST" ? 201 : 200,
        testLevel: "Unit",
      });

      scenarios.push({
        scenario: "Minimum field lengths",
        testType: "Boundary",
        description: `${method} ${endpoint} with minimum required field lengths`,
        expectedResult: "Data accepted and processed",
        httpStatus: method === "POST" ? 201 : 200,
        testLevel: "Unit",
      });
    }

    if (endpointInfo.hasPathParam) {
      scenarios.push({
        scenario: "Path parameter boundary values",
        testType: "Boundary",
        description: `${method} ${endpoint} with boundary ID values (0, max int)`,
        expectedResult: "Appropriate response based on ID validity",
        httpStatus: "Variable",
        testLevel: "Unit",
      });
    }

    return scenarios;
  }

  generateNegativeScenarios(method, endpoint, endpointInfo) {
    const scenarios = [];

    // Invalid path parameters
    if (endpointInfo.hasPathParam) {
      scenarios.push({
        scenario: "Invalid path parameter",
        testType: "Negative",
        description: `${method} ${endpoint} with invalid ID format`,
        expectedResult: "Bad request error",
        httpStatus: 400,
        testLevel: "Unit",
      });

      scenarios.push({
        scenario: "Non-existent resource",
        testType: "Negative",
        description: `${method} ${endpoint} with non-existent ID`,
        expectedResult: "Resource not found error",
        httpStatus: 404,
        testLevel: "Integration",
      });
    }

    // Invalid request body
    if (["POST", "PUT", "PATCH"].includes(method)) {
      scenarios.push({
        scenario: "Invalid request body",
        testType: "Negative",
        description: `${method} ${endpoint} with malformed JSON`,
        expectedResult: "Bad request error",
        httpStatus: 400,
        testLevel: "Unit",
      });

      scenarios.push({
        scenario: "Missing required fields",
        testType: "Negative",
        description: `${method} ${endpoint} with missing required fields`,
        expectedResult: "Validation error",
        httpStatus: 422,
        testLevel: "Integration",
      });

      scenarios.push({
        scenario: "Field validation failure",
        testType: "Negative",
        description: `${method} ${endpoint} with invalid field formats`,
        expectedResult: "Validation error",
        httpStatus: 422,
        testLevel: "Unit",
      });
    }

    // Invalid query parameters
    if (method === "GET") {
      scenarios.push({
        scenario: "Invalid query parameters",
        testType: "Negative",
        description: `GET ${endpoint} with invalid query parameter values`,
        expectedResult: "Bad request error",
        httpStatus: 400,
        testLevel: "E2E",
      });
    }

    return scenarios;
  }

  generateSecurityScenarios(method, endpoint, endpointInfo) {
    const scenarios = [];

    scenarios.push({
      scenario: "Missing authentication",
      testType: "Security",
      description: `${method} ${endpoint} without authentication token`,
      expectedResult: "Authentication required error",
      httpStatus: 401,
      testLevel: "Integration",
    });

    scenarios.push({
      scenario: "Invalid authentication",
      testType: "Security",
      description: `${method} ${endpoint} with invalid or expired token`,
      expectedResult: "Authentication failed error",
      httpStatus: 401,
      testLevel: "Integration",
    });

    scenarios.push({
      scenario: "Insufficient permissions",
      testType: "Security",
      description: `${method} ${endpoint} with valid token but insufficient permissions`,
      expectedResult: "Forbidden error",
      httpStatus: 403,
      testLevel: "Integration",
    });

    if (["POST", "PUT", "PATCH"].includes(method)) {
      scenarios.push({
        scenario: "Input sanitization",
        testType: "Security",
        description: `${method} ${endpoint} with potentially malicious input (XSS, SQL injection)`,
        expectedResult: "Input sanitized and processed safely",
        httpStatus: method === "POST" ? 201 : 200,
        testLevel: "Integration",
      });
    }

    return scenarios;
  }

  generatePerformanceScenarios(method, endpoint, endpointInfo) {
    const scenarios = [];

    if (method === "GET" && endpointInfo.isCollection) {
      scenarios.push({
        scenario: "Large dataset handling",
        testType: "Performance",
        description: `GET ${endpoint} with large number of resources`,
        expectedResult: "Acceptable response time with pagination",
        httpStatus: 200,
        testLevel: "E2E",
      });
    }

    scenarios.push({
      scenario: "Concurrent requests",
      testType: "Performance",
      description: `Multiple concurrent ${method} ${endpoint} requests`,
      expectedResult: "All requests handled correctly",
      httpStatus: "Variable",
      testLevel: "E2E",
    });

    scenarios.push({
      scenario: "Rate limiting",
      testType: "Performance",
      description: `${method} ${endpoint} exceeding rate limit threshold`,
      expectedResult: "Rate limit error returned",
      httpStatus: 429,
      testLevel: "Unit",
    });

    return scenarios;
  }

  determineTestLevel(testType, scenario) {
    // Critical happy paths -> Integration (need real API calls)
    if (testType === "Happy Path" && !scenario.includes("pagination")) {
      return "Integration";
    }

    // Security scenarios -> Integration (authentication/authorization)
    if (testType === "Security") {
      return "Integration";
    }

    // Performance scenarios -> E2E (only critical ones)
    if (testType === "Performance") {
      return "E2E";
    }

    // All validation, boundary, negative -> Unit (fast isolated tests)
    return "Unit";
  }

  formatScenarios(scenarios) {
    return scenarios
      .map(
        (s) =>
          `| ${s.scenario} | ${s.testType} | ${s.description} | ${s.expectedResult} | ${s.httpStatus} | ${s.testLevel} |`,
      )
      .join("\n");
  }

  generateReport(method, endpoint, additionalContext = "") {
    const scenarios = this.generateScenarios(
      method,
      endpoint,
      additionalContext,
    );
    const scenarioRows = this.formatScenarios(scenarios);

    const scenarioTable = this.templates.scenarioTable.replace(
      "{{SCENARIOS}}",
      scenarioRows,
    );

    const overview =
      `Generated ${scenarios.length} test scenarios for ${method} ${endpoint}. ` +
      `Covers happy path, boundary, negative, security, and performance testing.`;

    const implementationTips = this.generateImplementationTips(
      method,
      endpoint,
    );

    const fullReport = this.templates.fullReport
      .replace("{{METHOD}}", method)
      .replace("{{ENDPOINT}}", endpoint)
      .replace("{{DATE}}", new Date().toLocaleDateString())
      .replace("{{OVERVIEW}}", overview)
      .replace("{{SCENARIO_TABLE}}", scenarioTable)
      .replace("{{IMPLEMENTATION_TIPS}}", implementationTips);

    return {
      table: scenarioTable,
      fullReport: fullReport,
      scenarios: scenarios,
    };
  }

  generateImplementationTips(method, endpoint) {
    const tips = [];

    tips.push("- Implement scenarios in order of priority (H → M → L)");
    tips.push("- Use data builders/factories for test data generation");
    tips.push("- Group related scenarios into test suites");
    tips.push("- Mock external dependencies for unit tests");
    tips.push("- Use database transactions for test isolation");

    if (method === "GET") {
      tips.push("- Test pagination and sorting parameters");
      tips.push("- Verify response caching behavior");
    }

    if (["POST", "PUT", "PATCH"].includes(method)) {
      tips.push("- Validate request/response schema compliance");
      tips.push("- Test idempotency for PUT operations");
    }

    tips.push("- Monitor response times for performance scenarios");
    tips.push("- Use meaningful test data that reflects real usage");

    return tips.join("\n");
  }
}

// Main execution
if (require.main === module) {
  const args = process.argv.slice(2);

  if (args.length < 2) {
    console.error(
      "Usage: node generate-scenarios.js <HTTP_METHOD> <ENDPOINT> [additional_context]",
    );
    console.error("Example: node generate-scenarios.js POST /api/users");
    process.exit(1);
  }

  const [method, endpoint, ...contextArgs] = args;
  const additionalContext = contextArgs.join(" ");

  const generator = new APITestScenarioGenerator();
  const result = generator.generateReport(
    method.toUpperCase(),
    endpoint,
    additionalContext,
  );

  console.log(result.table);
}

module.exports = APITestScenarioGenerator;
