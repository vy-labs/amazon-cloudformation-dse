# Info and Prerequisites

The purpose of the files in this directory are to make is quick and simple to deploy a multi-datacenter DSE cluster
These scripts and templates use OpsCenter's Lifecycle Manager (LCM) to install and configure DSE. This is discussed [here](./LCM.md).

## Prerequisites

The only setup required is to install and configure the [AWS CLI](http://docs.aws.amazon.com/cli/latest/userguide/installing.html).  Documentation for the AWS CLI is [here](http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-using-cli.html).  To configure the AWS CLI run the command `aws configure` and follow the prompts.

These deploy scripts don't create any keypairs needed to deploy the EC2 instances used for OpsCenter or the DSE nodes. Before running them create a key for each region you are going to deploy to by running the command below setting `region` and `keyname`, or you can use existing keys. Note, omitting `--region $region` in the command below uses your account default.

```
region="us-west-1"
keyname="mykey"
aws ec2 create-key-pair --region $region --key-name $keyname --query 'KeyMaterial' --output text > ~/.ssh/$keyname.pem
```

SETUP
-----

```
cd multidc

run ./deploy_opscenter.sh
```

You can watch its progress either from the AWS web console [CloudFormation](https://console.aws.amazon.com/cloudformation/home) page or by running `aws cloudformation describe-stacks --stack-name opscenter-stack --query 'Stacks[0].StackStatus' `. Once the stataus of the stack is `CREATE_COMPLETE` You can view the outputs of the stack in the web console or with the command below.

```
aws cloudformation describe-stacks --stack-name opscenter-stack --query 'Stacks[0].Outputs[*]'

[
    {
        "Description": "URL for OpsCenter",
        "OutputKey": "OpsCenterURL",
        "OutputValue": "http://ec2-34-195-78-169.compute-1.amazonaws.com:8888"
    },
    {
        "Description": "URL for Lifecycle Manager",
        "OutputKey": "LCMURL",
        "OutputValue": "http://ec2-34-195-78-169.compute-1.amazonaws.com:8888/opscenter/lcm.html"
    },
    {
        "Description": "Public IP for OpsCenter",
        "OutputKey": "OpsCenterPublicIP",
        "OutputValue": "34.195.78.169"
    }
]
```
Change params like instance type, datacenter size, volume in ./deploy_datacenter.sh

```
run ./deploy_datacenter
```

Wait until the new datacenter is visible and installed succesfully in opscenter

```
run ./deploy_datacenter spark
```

Wait until the new datacenter is visible and installed succesfully in opscenter

Login into any node and do, (defualt credentails are username:cassandra, pwd:cassandra)

```
CQLSH_HOST=ip cqlsh -u cassandra -p cassandra

ALTER KEYSPACE "system_auth" 
WITH REPLICATION = {'class' : 'NetworkTopologyStrategy', 'dc-us-east' : 3, 'dc-us-east-spark' : 3};

ALTER KEYSPACE "dse_security" 
WITH REPLICATION = {'class' : 'NetworkTopologyStrategy', 'dc-us-east' : 3, 'dc-us-east-spark' : 3};

ALTER KEYSPACE "dse_pref" 
WITH REPLICATION = {'class' : 'NetworkTopologyStrategy', 'dc-us-east' : 3, 'dc-us-east-spark' : 3};
```

Run:
```
nodetool repair system_auth
nodetool repair dse_security
```

```
run `CQLSH_HOST=ip cqlsh -u cassandra -p cassandra`

CREATE ROLE admin WITH PASSWORD = 'xxx' 
    AND SUPERUSER = true 
    AND LOGIN = true;

CREATE ROLE root WITH PASSWORD = 'xxx' 
    AND SUPERUSER = false 
    AND LOGIN = true;

CREATE ROLE spark_user WITH PASSWORD = 'xxx'
	AND SUPERUSER = false
	AND LOGIN = true

GRANT SELECT ON ALL KEYSPACES TO spark_user;
GRANT ALL PERMISSIONS ON KEYSPACE "HiveMetaStore" TO spark_user;
GRANT ALL PERMISSIONS ON KEYSPACE cfs TO spark_user;
```

---logout---

---login----(with new creds)

```
ALTER ROLE cassandra WITH PASSWORD='<random_password>' AND SUPERUSER=false;

ALTER KEYSPACE "OpsCenter" WITH replication =
{'class': 'NetworkTopologyStrategy', 'dc-us-east': '2', 'dc-us-east-spark':'2'};

ALTER KEYSPACE cfs WITH REPLICATION = {'class' : 'NetworkTopologyStrategy', 'dc-us-east-spark' : 2};

ALTER KEYSPACE dse_leases WITH replication = {'class': 'NetworkTopologyStrategy', 'dc-us-east-spark':'2'};

ALTER KEYSPACE cfs_archive WITH REPLICATION= {'class' : 'NetworkTopologyStrategy', 'dc-us-east-spark' : 2};
	
ALTER KEYSPACE "HiveMetaStore" WITH REPLICATION= {'class' : 'NetworkTopologyStrategy', 'dc-us-east-spark' : 2};
```

```
run `nodetool repair`
```

On spark master:

add this at the end of /usr/share/dse/spark/spark-jobserver/dse.conf 

```
shiro {
 authentication = on
 config.path = "/usr/share/dse/spark/spark-jobserver/shiro.ini"
}
```


```
sudo touch /usr/share/dse/spark/spark-jobserver/shiro.ini
```

add these lines in shiro.ini

```
[users]
admin = <password>
```

```
sudo dse -u casssandra_superuser -p password spark-jobserver start
```

```
Create opscenter roles
https://docs.datastax.com/en/opscenter/6.0/opsc/configure/opscEnablingAuth.html
https://docs.datastax.com/en/opscenter/6.0/opsc/configure/opscManageUsers.html
```

Since we have less number of nodes, **we don't want autoscaling group to
terminate any instance as the new node will take too much time to boot up,
enable instance protection for the autoscaling group once you are done with the setup, also enable instance termination protection for already up instances**

Stress test
--
cassandra-stress write n=1000000 -mode native cql3 user=xxxx password=xxx -rate threads=50 -schema keyspace="stress" -node ip


Teardown (To teardown the complete cluster)
-------------------------------------------
The deploy scripts write the stack name and region to the tempfile `teardown.txt`. Running `teardown.sh` deletes these stacks and then the tempfile.

```
./teardown.sh
deleting stack: opscenter-stack 	 us-east-1 ...
deleting stack: dc-us-east-stack 	 us-east-1 ...
deleting stack: dc-us-west-stack 	 us-west-1 ...
Stacks deleted: 3
```


You can launch as many datacenter as you want, just change the params in deploy_datacenter.sh to launch a new one.

Why M4.xlarge: 

https://www.instaclustr.com/blog/2015/10/28/cassandra-on-aws-ebs-infrastructure/
