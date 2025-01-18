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
tree = ET.ElementTree(root)
tree.write("build/reports/aggregate/combined.xml", encoding="UTF-8", xml_declaration=True)

