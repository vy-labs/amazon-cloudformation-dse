import json
import opsCenter
import nodes

# This python script generates a CloudFormation template that deploys DSE across multiple regions.

with open('clusterParameters.json') as inputFile:
    clusterParameters = json.load(inputFile)

regions = clusterParameters['regions']
vmSize = clusterParameters['vmSize']
nodeCount = clusterParameters['nodeCount']

# This is the skeleton of the template that we're going to add resources to
generatedTemplate = {
}

# Create DSE nodes in each location
for datacenterIndex in range(0, len(regions)):
    region = regions[datacenterIndex]
    resources = nodes.generate_template(region, datacenterIndex, vmSize, nodeCount, regions)
    generatedTemplate['resources'] += resources

# Create the OpsCenter node
resources = opsCenter.generate_template(regions, nodeCount)
generatedTemplate['resources'] += resources

with open('generatedTemplate.json', 'w') as outputFile:
    json.dump(generatedTemplate, outputFile, sort_keys=True, indent=4, ensure_ascii=False)
