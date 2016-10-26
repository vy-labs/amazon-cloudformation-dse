import json

import multidc.opsCenter
from multidc import nodes, opsCenter

# This python script generates a CloudFormation template that deploys DSE across multiple regions.

with open('clusterParameters.json') as inputFile:
    clusterParameters = json.load(inputFile)

regions = clusterParameters['regions']
vmSize = clusterParameters['vmSize']
nodeCount = clusterParameters['nodeCount']

# This is the skeleton of the template that we're going to add resources to
generatedTemplate = {
    "AWSTemplateFormatVersion": "2010-09-09",
    "Description": "Amazon CloudFormation template for DataStax Enterprise",
    "Parameters": {
    },
    "Mappings": {
    },
    "Resources": {
        "EC2Instance": {
            "Type": "AWS::EC2::Instance",
            "Properties": {
                "UserData": {"Fn::Base64": {"Fn::Join": ["", ["IPAddress=", {"Ref": "IPAddress"}]]}},
                "InstanceType": {"Ref": "InstanceType"},
                "SecurityGroups": [{"Ref": "InstanceSecurityGroup"}],
                "KeyName": {"Ref": "KeyName"},
                "ImageId": {"Fn::FindInMap": ["AWSRegionArch2AMI", {"Ref": "AWS::Region"},
                                              {"Fn::FindInMap": ["AWSInstanceType2Arch", {"Ref": "InstanceType"},
                                                                 "Arch"]}]}
            }
        },
        "InstanceSecurityGroup": {
            "Type": "AWS::EC2::SecurityGroup",
            "Properties": {
                "GroupDescription": "Enable SSH access",
                "SecurityGroupIngress":
                    [{"IpProtocol": "tcp", "FromPort": "22", "ToPort": "22", "CidrIp": {"Ref": "SSHLocation"}}]
            }
        },
        "IPAddress": {
            "Type": "AWS::EC2::EIP"
        },
        "IPAssoc": {
            "Type": "AWS::EC2::EIPAssociation",
            "Properties": {
                "InstanceId": {"Ref": "EC2Instance"},
                "EIP": {"Ref": "IPAddress"}
            }
        }
    },
    "Outputs": {
    }
}

# Create DSE nodes in each location
for datacenterIndex in range(0, len(regions)):
    region = regions[datacenterIndex]
    resources = nodes.generate_template(region, datacenterIndex, vmSize, nodeCount, regions)
    # generatedTemplate['resources'] += resources

# Create the OpsCenter node
resources = opsCenter.generate_template(regions, nodeCount)
# generatedTemplate['resources'] += resources

with open('generatedTemplate.json', 'w') as outputFile:
    json.dump(generatedTemplate, outputFile, sort_keys=True, indent=4, ensure_ascii=False)
