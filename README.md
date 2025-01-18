# **GitLab CI Integration with Gradle and JUnit**

This README provides steps to configure a Gradle project with GitLab CI to generate, retain, and aggregate test reports. The solution ensures HTML and JUnit XML reports are preserved even if pipeline summaries are overwritten by subsequent changes.

---

## **1. Gradle Configuration**

### **Generate Reports for All Tests**
Update `build.gradle` to ensure both HTML and JUnit XML reports are generated, even for failed tests.

```gradle
test {
    // Always generate test reports even on failures
    reports {
        html.required = true
        junitXml.required = true
    }
    useJUnitPlatform()
    testLogging {
        events "passed", "skipped", "failed"
    }
}

task test1(type: Test) {
    reports {
        html.required = true
        junitXml.required = true
        html.destination file("build/reports/tests/test-1")
    }
    useJUnitPlatform()
    testLogging {
        events "passed", "skipped", "failed"
    }
}

task test2(type: Test) {
    reports {
        html.required = true
        junitXml.required = true
        html.destination file("build/reports/tests/test-2")
    }
    useJUnitPlatform()
    testLogging {
        events "passed", "skipped", "failed"
    }
}
```

---

## **2. GitLab CI Configuration**

### **Test Job**
Each test task is configured to generate and store reports as artifacts, with a retention period of 14 days.

```yaml
test_job_1:
  stage: test
  script:
    - ./gradlew test1 --tests "com.example.project.CalculatorTests.addsTwoNumbers"  # Run specific test case
  artifacts:
    when: always
    paths:
      - build/reports/tests/test-1/index.html  # HTML report
      - build/test-results/test1/TEST-*.xml   # JUnit XML for GitLab test summary
    reports:
      junit: build/test-results/test1/TEST-*.xml
    expire_in: 14 days
```

---

## **3. Python Script for XML Aggregation**

Use the following Python script (`combine_junit_reports.py`) to merge multiple JUnit XML reports into a single file.

```python
import xml.etree.ElementTree as ET
import glob

# Create a root element for the combined XML
root = ET.Element("testsuites")

# Iterate through all test result XML files
for filename in glob.glob("build/test-results/test*/TEST-*.xml"):
    tree = ET.parse(filename)
    for testsuite in tree.getroot():
        root.append(testsuite)

# Write the combined XML to a file
ET.ElementTree(root).write("build/reports/aggregate/combined.xml")
```

---

## **4. Aggregate Batch Jobs**
Combine the outputs from multiple test jobs into a single aggregated report for clarity.

```yaml
aggregate_and_report_job:
  stage: report
  image: python:3.9
  script:
    - echo "Aggregating reports from batch jobs..."
    - mkdir -p build/reports/aggregate
    - python3 combine_junit_reports.py  # Combine XML reports
    - cat build/reports/tests/test-1/index.html build/reports/tests/test-2/index.html > build/reports/aggregate/combined_report.html
    - echo "HTML and JUnit reports aggregated successfully."
  artifacts:
    when: always
    paths:
      - build/reports/aggregate/combined_report.html  # Aggregated HTML report
      - build/reports/aggregate/combined.xml          # Aggregated JUnit XML report
    reports:
      junit: build/reports/aggregate/combined.xml
    expire_in: 14 days
```

---

## **5. Results**

### **Outputs**
- **HTML Reports**: Detailed test results are stored as artifacts and accessible via the GitLab pipeline UI.
  ![image](https://github.com/user-attachments/assets/2eb16065-842a-44e6-be79-a78dea12b52c)

- **JUnit XML Reports**: Enables the GitLab test summary widget.
- **Aggregated Reports**: Combines batch job outputs into a single HTML and XML report for clarity.

### **Benefits**
- **Persistent Reports**: Test results remain accessible even if new changes overwrite the pipeline’s test summary.
- **Clarity**: Aggregated reports provide a consolidated view of all test jobs.
- **GitLab UI Integration**: Reports are easily accessible through the artifacts browser or GitLab Pages (if configured).

---

For further assistance, feel free to reach out!
# junit5-jupiter-starter-gradle

The `junit5-jupiter-starter-gradle` project demonstrates how to run tests based on JUnit
Jupiter using [Gradle's native JUnit Platform support], Gradle's Groovy DSL
and code and tests written in Java.

[Gradle's native JUnit Platform support]: https://docs.gradle.org/current/userguide/java_testing.html#using_junit5
