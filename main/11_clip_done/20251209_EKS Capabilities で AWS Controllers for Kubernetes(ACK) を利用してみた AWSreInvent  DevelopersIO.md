---
title: "EKS Capabilities で AWS Controllers for Kubernetes(ACK) を利用してみた #AWSreInvent | DevelopersIO"
source: "https://dev.classmethod.jp/articles/eks-capabilities-aws-controller-for-kubernetes/"
author: ""
published: "2025-12-05"
created: "2025-12-09"
description: ""
tags:
  - ""
  - "raw"
---

先日 EKS Capabilities が登場しました。  
EKS Capabilities は EKS 上での開発を加速するためのフルマネージドな機能セットで、現在下記 3 つのツールを利用可能です。

- Argo CD
- AWS Controllers for Kubernetes(ACK)
- Kube Resource Orchestrator(kro)

今回は ACK を利用してみます。

## AWS Controllers for Kubernetes(ACK) とは？

Kubernetes API 経由で AWS リソースを構築するためのツールで、下記メリットがあります。

- アプリケーションリソースと関連するクラウドリソースを統一されたツールで扱うことができる
	- EKS 基盤の管理では Terraform 管理したとしても、少なくともアプリケーションチームはデプロイツールを統一できる
- 望ましい状態と実際の状態を継続的に調整して、ドリフトを修正できる (Reconciliation loop)
	- Argo CD と組み合わせることで、インフラ管理にも Kubernetes リソース同様の GitOps を導入可能
	- ただし、CPU 負荷を意識してドリフト検出は 10 時間ごと
		- [Reconcillation issue in s3 controller](https://github.com/aws-controllers-k8s/community/issues/1288)
		- [Reconciliation Loop | AWS Controllers for Kubernetes](https://aws-controllers-k8s.github.io/docs/concepts/#reconciliation-loop)

扱える AWS サービスは下記にまとまっており、2025 年 12 月時点で 50 以上のサービスを扱うことが可能です。

EKS Capabilities を利用している際、アップストリーム版の ACK で GA となっているサービスがサポートされます。

> All AWS services listed as Generally Available upstream are supported by the EKS Capability for ACK.  
> [https://docs.aws.amazon.com/eks/latest/userguide/ack.html#supported\_shared\_aws\_services](https://docs.aws.amazon.com/eks/latest/userguide/ack.html#supported_shared_aws_services)

## 環境セットアップ

v1.34 の Auto Mode を有効化した EKS クラスターを事前に用意します。  
今回は Terraform を利用して構築しました。

```
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 6.0.1"

  name = "eks-vpc"

  cidr = "10.0.0.0/16"

  azs             = ["ap-northeast-1a", "ap-northeast-1c", "ap-northeast-1d"]
  public_subnets  = ["10.0.0.0/24", "10.0.1.0/24", "10.0.2.0/24"]
  private_subnets = ["10.0.100.0/24", "10.0.101.0/24", "10.0.102.0/24"]

  enable_nat_gateway = true
  single_nat_gateway = true
  public_subnet_tags = {
    "kubernetes.io/role/elb" = 1
  }

  private_subnet_tags = {
    "kubernetes.io/role/internal-elb" = 1
  }
}

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 21.0.4"

  name               = "test-cluster"
  kubernetes_version = "1.34"

  endpoint_public_access  = true
  endpoint_private_access = true
  enable_irsa             = false

  authentication_mode = "API"

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  enable_cluster_creator_admin_permissions = true

  compute_config = {
    enabled    = true
    node_pools = ["general-purpose"]
  }
}
```

下記ドキュメントに従って AWS CLI で設定します。

EKS Capabilities では Capability ロールと呼ばれる IAM ロールが必要になります。  
各コンポーネントが AWS 管理領域にインストールされるので、Pod Identity など既存の仕組みとは別で設定する必要があるのでしょう。  
まず、信頼ポリシーを定義したファイルを作成します。  
EKS Capabilities では `capabilities.eks.amazonaws.com` に対して権限を許可する必要があります。

```
cat > ack-trust-policy.json << 'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "capabilities.eks.amazonaws.com"
      },
      "Action": [
        "sts:AssumeRole",
        "sts:TagSession"
      ]
    }
  ]
}
EOF
```

IAM ロールを作成します。

```
aws iam create-role \
  --role-name ACKCapabilityRole \
  --assume-role-policy-document file://ack-trust-policy.json
```

今回は AdministratorAccess を付与します。

```
aws iam attach-role-policy \
  --role-name ACKCapabilityRole \
  --policy-arn arn:aws:iam::aws:policy/AdministratorAccess
```

AWS インフラをデプロイする都合上強い権限が必要になりますが、可能であればカスタムポリシーを定義して権限を制限することが推奨されています。

> ACK: When possible, limit IAM permissions to specific AWS services and resources your teams need, based on use case and requirements  
> [https://docs.aws.amazon.com/eks/latest/userguide/capabilities-security.html#\_security\_best\_practices](https://docs.aws.amazon.com/eks/latest/userguide/capabilities-security.html#_security_best_practices)

```
aws eks create-capability \
  --region $REGION \
  --cluster-name $CLUSTER_NAME \
  --capability-name ack \
  --type ACK \
  --role-arn arn:aws:iam::$(aws sts get-caller-identity --query Account --output text):role/ACKCapabilityRole \
  --delete-propagation-policy RETAIN
```

しばらくすると Capability のステータスが ACTIVE になります。

```
% aws eks describe-capability \
  --region $REGION \
  --cluster-name $CLUSTER_NAME \
  --capability-name ack \
  --query 'capability.status' \
  --output text
ACTIVE
```

この状態で xxx.services.k8s.aws という API リソース郡を利用できるようになっています。

```
% kubectl api-resources | grep services.k8s.aws
certificates                                     acm.services.k8s.aws/v1alpha1                       true         Certificate
apiintegrationresponses                          apigateway.services.k8s.aws/v1alpha1                true         APIIntegrationResponse
apikeys                                          apigateway.services.k8s.aws/v1alpha1                true         APIKey
apimethodresponses                               apigateway.services.k8s.aws/v1alpha1                true         APIMethodResponse
authorizers                                      apigateway.services.k8s.aws/v1alpha1                true         Authorizer
deployments                                      apigateway.services.k8s.aws/v1alpha1                true         Deployment
integrations                                     apigateway.services.k8s.aws/v1alpha1                true         Integration
methods                                          apigateway.services.k8s.aws/v1alpha1                true         Method
resources                                        apigateway.services.k8s.aws/v1alpha1                true         Resource
restapis                                         apigateway.services.k8s.aws/v1alpha1                true         RestAPI
stages                                           apigateway.services.k8s.aws/v1alpha1                true         Stage
vpclinks                                         apigateway.services.k8s.aws/v1alpha1                true         VPCLink
apimappings                                      apigatewayv2.services.k8s.aws/v1alpha1              true         APIMapping
apis                                             apigatewayv2.services.k8s.aws/v1alpha1              true         API
authorizers                                      apigatewayv2.services.k8s.aws/v1alpha1              true         Authorizer
deployments                                      apigatewayv2.services.k8s.aws/v1alpha1              true         Deployment
domainnames                                      apigatewayv2.services.k8s.aws/v1alpha1              true         DomainName
integrations                                     apigatewayv2.services.k8s.aws/v1alpha1              true         Integration
routes                                           apigatewayv2.services.k8s.aws/v1alpha1              true         Route
stages                                           apigatewayv2.services.k8s.aws/v1alpha1              true         Stage
vpclinks                                         apigatewayv2.services.k8s.aws/v1alpha1              true         VPCLink
scalabletargets                                  applicationautoscaling.services.k8s.aws/v1alpha1    true         ScalableTarget
scalingpolicies                                  applicationautoscaling.services.k8s.aws/v1alpha1    true         ScalingPolicy
preparedstatements                               athena.services.k8s.aws/v1alpha1                    true         PreparedStatement
workgroups                                       athena.services.k8s.aws/v1alpha1                    true         WorkGroup
inferenceprofiles                                bedrock.services.k8s.aws/v1alpha1                   true         InferenceProfile
agents                                           bedrockagent.services.k8s.aws/v1alpha1              true         Agent
agentruntimeendpoints                            bedrockagentcorecontrol.services.k8s.aws/v1alpha1   true         AgentRuntimeEndpoint
agentruntimes                                    bedrockagentcorecontrol.services.k8s.aws/v1alpha1   true         AgentRuntime
cachepolicies                                    cloudfront.services.k8s.aws/v1alpha1                true         CachePolicy
distributions                                    cloudfront.services.k8s.aws/v1alpha1                true         Distribution
functions                                        cloudfront.services.k8s.aws/v1alpha1                true         Function
originaccesscontrols                             cloudfront.services.k8s.aws/v1alpha1                true         OriginAccessControl
originrequestpolicies                            cloudfront.services.k8s.aws/v1alpha1                true         OriginRequestPolicy
responseheaderspolicies                          cloudfront.services.k8s.aws/v1alpha1                true         ResponseHeadersPolicy
vpcorigins                                       cloudfront.services.k8s.aws/v1alpha1                true         VPCOrigin
eventdatastores                                  cloudtrail.services.k8s.aws/v1alpha1                true         EventDataStore
trails                                           cloudtrail.services.k8s.aws/v1alpha1                true         Trail
dashboards                                       cloudwatch.services.k8s.aws/v1alpha1                true         Dashboard
metricalarms                                     cloudwatch.services.k8s.aws/v1alpha1                true         MetricAlarm
metricstreams                                    cloudwatch.services.k8s.aws/v1alpha1                true         MetricStream
loggroups                                        cloudwatchlogs.services.k8s.aws/v1alpha1            true         LogGroup
domains                                          codeartifact.services.k8s.aws/v1alpha1              true         Domain
packagegroups                                    codeartifact.services.k8s.aws/v1alpha1              true         PackageGroup
userpools                                        cognitoidentityprovider.services.k8s.aws/v1alpha1   true         UserPool
dbclusters                                       documentdb.services.k8s.aws/v1alpha1                true         DBCluster
dbinstances                                      documentdb.services.k8s.aws/v1alpha1                true         DBInstance
dbsubnetgroups                                   documentdb.services.k8s.aws/v1alpha1                true         DBSubnetGroup
backups                                          dynamodb.services.k8s.aws/v1alpha1                  true         Backup
globaltables                                     dynamodb.services.k8s.aws/v1alpha1                  true         GlobalTable
tables                                           dynamodb.services.k8s.aws/v1alpha1                  true         Table
capacityreservations                             ec2.services.k8s.aws/v1alpha1                       true         CapacityReservation
dhcpoptions                                      ec2.services.k8s.aws/v1alpha1                       true         DHCPOptions
elasticipaddresses                               ec2.services.k8s.aws/v1alpha1                       true         ElasticIPAddress
flowlogs                                         ec2.services.k8s.aws/v1alpha1                       true         FlowLog
instances                                        ec2.services.k8s.aws/v1alpha1                       true         Instance
internetgateways                                 ec2.services.k8s.aws/v1alpha1                       true         InternetGateway
launchtemplates                                  ec2.services.k8s.aws/v1alpha1                       true         LaunchTemplate
natgateways                                      ec2.services.k8s.aws/v1alpha1                       true         NATGateway
networkacls                                      ec2.services.k8s.aws/v1alpha1                       true         NetworkACL
routetables                                      ec2.services.k8s.aws/v1alpha1                       true         RouteTable
securitygroups                                   ec2.services.k8s.aws/v1alpha1                       true         SecurityGroup
subnets                                          ec2.services.k8s.aws/v1alpha1                       true         Subnet
transitgateways                                  ec2.services.k8s.aws/v1alpha1                       true         TransitGateway
transitgatewayvpcattachments                     ec2.services.k8s.aws/v1alpha1                       true         TransitGatewayVPCAttachment
vpcendpoints                                     ec2.services.k8s.aws/v1alpha1                       true         VPCEndpoint
vpcendpointserviceconfigurations                 ec2.services.k8s.aws/v1alpha1                       true         VPCEndpointServiceConfiguration
vpcpeeringconnections                            ec2.services.k8s.aws/v1alpha1                       true         VPCPeeringConnection
vpcs                                             ec2.services.k8s.aws/v1alpha1                       true         VPC
pullthroughcacherules                            ecr.services.k8s.aws/v1alpha1                       true         PullThroughCacheRule
repositories                                     ecr.services.k8s.aws/v1alpha1                       true         Repository
repositories                                     ecrpublic.services.k8s.aws/v1alpha1                 true         Repository
clusters                                         ecs.services.k8s.aws/v1alpha1                       true         Cluster
services                                         ecs.services.k8s.aws/v1alpha1                       true         Service
taskdefinitions                                  ecs.services.k8s.aws/v1alpha1                       true         TaskDefinition
accesspoints                                     efs.services.k8s.aws/v1alpha1                       true         AccessPoint
filesystems                                      efs.services.k8s.aws/v1alpha1                       true         FileSystem
mounttargets                                     efs.services.k8s.aws/v1alpha1                       true         MountTarget
accessentries                                    eks.services.k8s.aws/v1alpha1                       true         AccessEntry
addons                                           eks.services.k8s.aws/v1alpha1                       true         Addon
clusters                                         eks.services.k8s.aws/v1alpha1                       true         Cluster
fargateprofiles                                  eks.services.k8s.aws/v1alpha1                       true         FargateProfile
identityproviderconfigs                          eks.services.k8s.aws/v1alpha1                       true         IdentityProviderConfig
nodegroups                                       eks.services.k8s.aws/v1alpha1                       true         Nodegroup
podidentityassociations                          eks.services.k8s.aws/v1alpha1                       true         PodIdentityAssociation
cacheclusters                                    elasticache.services.k8s.aws/v1alpha1               true         CacheCluster
cacheparametergroups                             elasticache.services.k8s.aws/v1alpha1               true         CacheParameterGroup
cachesubnetgroups                                elasticache.services.k8s.aws/v1alpha1               true         CacheSubnetGroup
replicationgroups                                elasticache.services.k8s.aws/v1alpha1               true         ReplicationGroup
serverlesscaches                                 elasticache.services.k8s.aws/v1alpha1               true         ServerlessCache
serverlesscachesnapshots                         elasticache.services.k8s.aws/v1alpha1               true         ServerlessCacheSnapshot
snapshots                                        elasticache.services.k8s.aws/v1alpha1               true         Snapshot
usergroups                                       elasticache.services.k8s.aws/v1alpha1               true         UserGroup
users                                            elasticache.services.k8s.aws/v1alpha1               true         User
listeners                                        elbv2.services.k8s.aws/v1alpha1                     true         Listener
loadbalancers                                    elbv2.services.k8s.aws/v1alpha1                     true         LoadBalancer
rules                                            elbv2.services.k8s.aws/v1alpha1                     true         Rule
targetgroups                                     elbv2.services.k8s.aws/v1alpha1                     true         TargetGroup
jobruns                                          emrcontainers.services.k8s.aws/v1alpha1             true         JobRun
virtualclusters                                  emrcontainers.services.k8s.aws/v1alpha1             true         VirtualCluster
archives                                         eventbridge.services.k8s.aws/v1alpha1               true         Archive
endpoints                                        eventbridge.services.k8s.aws/v1alpha1               true         Endpoint
eventbuses                          eb,bus       eventbridge.services.k8s.aws/v1alpha1               true         EventBus
rules                               er           eventbridge.services.k8s.aws/v1alpha1               true         Rule
groups                                           iam.services.k8s.aws/v1alpha1                       true         Group
instanceprofiles                                 iam.services.k8s.aws/v1alpha1                       true         InstanceProfile
openidconnectproviders                           iam.services.k8s.aws/v1alpha1                       true         OpenIDConnectProvider
policies                                         iam.services.k8s.aws/v1alpha1                       true         Policy
roles                                            iam.services.k8s.aws/v1alpha1                       true         Role
servicelinkedroles                               iam.services.k8s.aws/v1alpha1                       true         ServiceLinkedRole
users                                            iam.services.k8s.aws/v1alpha1                       true         User
clusters                                         kafka.services.k8s.aws/v1alpha1                     true         Cluster
configurations                                   kafka.services.k8s.aws/v1alpha1                     true         Configuration
serverlessclusters                               kafka.services.k8s.aws/v1alpha1                     true         ServerlessCluster
keyspaces                                        keyspaces.services.k8s.aws/v1alpha1                 true         Keyspace
tables                                           keyspaces.services.k8s.aws/v1alpha1                 true         Table
streams                                          kinesis.services.k8s.aws/v1alpha1                   true         Stream
aliases                                          kms.services.k8s.aws/v1alpha1                       true         Alias
grants                                           kms.services.k8s.aws/v1alpha1                       true         Grant
keys                                             kms.services.k8s.aws/v1alpha1                       true         Key
aliases                                          lambda.services.k8s.aws/v1alpha1                    true         Alias
codesigningconfigs                               lambda.services.k8s.aws/v1alpha1                    true         CodeSigningConfig
eventsourcemappings                              lambda.services.k8s.aws/v1alpha1                    true         EventSourceMapping
functions                                        lambda.services.k8s.aws/v1alpha1                    true         Function
functionurlconfigs                               lambda.services.k8s.aws/v1alpha1                    true         FunctionURLConfig
acls                                             memorydb.services.k8s.aws/v1alpha1                  true         ACL
clusters                                         memorydb.services.k8s.aws/v1alpha1                  true         Cluster
parametergroups                                  memorydb.services.k8s.aws/v1alpha1                  true         ParameterGroup
snapshots                                        memorydb.services.k8s.aws/v1alpha1                  true         Snapshot
subnetgroups                                     memorydb.services.k8s.aws/v1alpha1                  true         SubnetGroup
users                                            memorydb.services.k8s.aws/v1alpha1                  true         User
brokers                                          mq.services.k8s.aws/v1alpha1                        true         Broker
firewallpolicies                                 networkfirewall.services.k8s.aws/v1alpha1           true         FirewallPolicy
firewalls                                        networkfirewall.services.k8s.aws/v1alpha1           true         Firewall
rulegroups                                       networkfirewall.services.k8s.aws/v1alpha1           true         RuleGroup
domains                                          opensearchservice.services.k8s.aws/v1alpha1         true         Domain
pipes                                            pipes.services.k8s.aws/v1alpha1                     true         Pipe
alertmanagerdefinitions                          prometheusservice.services.k8s.aws/v1alpha1         true         AlertManagerDefinition
loggingconfigurations                            prometheusservice.services.k8s.aws/v1alpha1         true         LoggingConfiguration
rulegroupsnamespaces                rgn          prometheusservice.services.k8s.aws/v1alpha1         true         RuleGroupsNamespace
workspaces                                       prometheusservice.services.k8s.aws/v1alpha1         true         Workspace
permissions                                      ram.services.k8s.aws/v1alpha1                       true         Permission
resourceshares                                   ram.services.k8s.aws/v1alpha1                       true         ResourceShare
dbclusterendpoints                               rds.services.k8s.aws/v1alpha1                       true         DBClusterEndpoint
dbclusterparametergroups                         rds.services.k8s.aws/v1alpha1                       true         DBClusterParameterGroup
dbclusters                                       rds.services.k8s.aws/v1alpha1                       true         DBCluster
dbclustersnapshots                               rds.services.k8s.aws/v1alpha1                       true         DBClusterSnapshot
dbinstances                                      rds.services.k8s.aws/v1alpha1                       true         DBInstance
dbparametergroups                                rds.services.k8s.aws/v1alpha1                       true         DBParameterGroup
dbproxies                                        rds.services.k8s.aws/v1alpha1                       true         DBProxy
dbsnapshots                                      rds.services.k8s.aws/v1alpha1                       true         DBSnapshot
dbsubnetgroups                                   rds.services.k8s.aws/v1alpha1                       true         DBSubnetGroup
globalclusters                                   rds.services.k8s.aws/v1alpha1                       true         GlobalCluster
rules                                            recyclebin.services.k8s.aws/v1alpha1                true         Rule
healthchecks                                     route53.services.k8s.aws/v1alpha1                   true         HealthCheck
hostedzones                                      route53.services.k8s.aws/v1alpha1                   true         HostedZone
recordsets                                       route53.services.k8s.aws/v1alpha1                   true         RecordSet
resolverendpoints                                route53resolver.services.k8s.aws/v1alpha1           true         ResolverEndpoint
resolverrules                                    route53resolver.services.k8s.aws/v1alpha1           true         ResolverRule
buckets                                          s3.services.k8s.aws/v1alpha1                        true         Bucket
accesspoints                                     s3control.services.k8s.aws/v1alpha1                 true         AccessPoint
apps                                             sagemaker.services.k8s.aws/v1alpha1                 true         App
dataqualityjobdefinitions                        sagemaker.services.k8s.aws/v1alpha1                 true         DataQualityJobDefinition
domains                                          sagemaker.services.k8s.aws/v1alpha1                 true         Domain
endpointconfigs                                  sagemaker.services.k8s.aws/v1alpha1                 true         EndpointConfig
endpoints                                        sagemaker.services.k8s.aws/v1alpha1                 true         Endpoint
featuregroups                                    sagemaker.services.k8s.aws/v1alpha1                 true         FeatureGroup
hyperparametertuningjobs                         sagemaker.services.k8s.aws/v1alpha1                 true         HyperParameterTuningJob
inferencecomponents                              sagemaker.services.k8s.aws/v1alpha1                 true         InferenceComponent
labelingjobs                                     sagemaker.services.k8s.aws/v1alpha1                 true         LabelingJob
modelbiasjobdefinitions                          sagemaker.services.k8s.aws/v1alpha1                 true         ModelBiasJobDefinition
modelexplainabilityjobdefinitions                sagemaker.services.k8s.aws/v1alpha1                 true         ModelExplainabilityJobDefinition
modelpackagegroups                               sagemaker.services.k8s.aws/v1alpha1                 true         ModelPackageGroup
modelpackages                                    sagemaker.services.k8s.aws/v1alpha1                 true         ModelPackage
modelqualityjobdefinitions                       sagemaker.services.k8s.aws/v1alpha1                 true         ModelQualityJobDefinition
models                                           sagemaker.services.k8s.aws/v1alpha1                 true         Model
monitoringschedules                              sagemaker.services.k8s.aws/v1alpha1                 true         MonitoringSchedule
notebookinstancelifecycleconfigs                 sagemaker.services.k8s.aws/v1alpha1                 true         NotebookInstanceLifecycleConfig
notebookinstances                                sagemaker.services.k8s.aws/v1alpha1                 true         NotebookInstance
pipelineexecutions                               sagemaker.services.k8s.aws/v1alpha1                 true         PipelineExecution
pipelines                                        sagemaker.services.k8s.aws/v1alpha1                 true         Pipeline
processingjobs                                   sagemaker.services.k8s.aws/v1alpha1                 true         ProcessingJob
spaces                                           sagemaker.services.k8s.aws/v1alpha1                 true         Space
trainingjobs                                     sagemaker.services.k8s.aws/v1alpha1                 true         TrainingJob
transformjobs                                    sagemaker.services.k8s.aws/v1alpha1                 true         TransformJob
userprofiles                                     sagemaker.services.k8s.aws/v1alpha1                 true         UserProfile
secrets                                          secretsmanager.services.k8s.aws/v1alpha1            true         Secret
iamroleselectors                                 services.k8s.aws/v1alpha1                           false        IAMRoleSelector
configurationsets                                ses.services.k8s.aws/v1alpha1                       true         ConfigurationSet
activities                                       sfn.services.k8s.aws/v1alpha1                       true         Activity
statemachines                                    sfn.services.k8s.aws/v1alpha1                       true         StateMachine
platformapplications                             sns.services.k8s.aws/v1alpha1                       true         PlatformApplication
platformendpoints                                sns.services.k8s.aws/v1alpha1                       true         PlatformEndpoint
subscriptions                                    sns.services.k8s.aws/v1alpha1                       true         Subscription
topics                                           sns.services.k8s.aws/v1alpha1                       true         Topic
queues                                           sqs.services.k8s.aws/v1alpha1                       true         Queue
documents                                        ssm.services.k8s.aws/v1alpha1                       true         Document
patchbaselines                                   ssm.services.k8s.aws/v1alpha1                       true         PatchBaseline
resourcedatasyncs                                ssm.services.k8s.aws/v1alpha1                       true         ResourceDataSync
ipsets                                           wafv2.services.k8s.aws/v1alpha1                     true         IPSet
rulegroups                                       wafv2.services.k8s.aws/v1alpha1                     true         RuleGroup
webacls                                          wafv2.services.k8s.aws/v1alpha1                     true         WebACL
```

## ACK で AWS リソースを作成してみる

[ACK の公式ドキュメント](https://aws-controllers-k8s.github.io/docs/intro#crd-design-philosophy) で紹介されている、S3 バケットを作成するための設定ファイルで試してみます。  
普通に作成すると S3 バケット名が重複しそうなので、バケット名の末尾にアカウント ID を埋め込みます。  
また、ライフサイクルルールのフィルターを設定しないで作成した所、 `Message: api error MalformedXML: The XML you provided was not well-formed or did not validate against our published schema` と怒られたので設定を追加しています。

```
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)
export BUCKET_NAME=my-production-bucket-$AWS_ACCOUNT_ID

read -r -d '' BUCKET_MANIFEST <<EOF
apiVersion: s3.services.k8s.aws/v1alpha1
kind: Bucket
metadata:
  name: $BUCKET_NAME
spec:
  name: $BUCKET_NAME
  versioning:
    status: Enabled
  encryption:
    rules:
      - applyServerSideEncryptionByDefault:
          sseAlgorithm: AES256
  lifecycle:
    rules:
      - id: delete-old-versions
        filter: # 追加
          prefix: "" # 追加
        status: Enabled
        noncurrentVersionExpiration:
          noncurrentDays: 90
  publicAccessBlock:
    blockPublicACLs: true
    blockPublicPolicy: true
    ignorePublicACLs: true
    restrictPublicBuckets: true
EOF

echo "${BUCKET_MANIFEST}" > bucket.yaml
kubectl apply -f bucket.yaml
```

下記のようなレスポンスが返ってくれば作成完了です。

```
bucket.s3.services.k8s.aws/my-production-bucket-xxxxxxxxxxxx created
```

Statis が `ACK.ResourceSynced` になっていることを確認できました。

```
% kubectl describe bucket.s3.services.k8s.aws
Name:         my-production-bucket-xxxxxxxxxxxx
Namespace:    default
Labels:       <none>
Annotations:  <none>
API Version:  s3.services.k8s.aws/v1alpha1
Kind:         Bucket
Metadata:
  Creation Timestamp:  2025-12-04T14:38:30Z
  Finalizers:
    finalizers.s3.services.k8s.aws/Bucket
  Generation:        1
  Resource Version:  1015714
  UID:               c41ca28d-cda3-4a4b-9605-4bd7659c2c83
Spec:
  Encryption:
    Rules:
      Apply Server Side Encryption By Default:
        Sse Algorithm:  AES256
  Lifecycle:
    Rules:
      Filter:
        Prefix:
      Id:        delete-old-versions
      Noncurrent Version Expiration:
        Noncurrent Days:  90
      Status:             Enabled
  Name:                   my-production-bucket-xxxxxxxxxxxx
  Public Access Block:
    Block Public AC Ls:       true
    Block Public Policy:      true
    Ignore Public AC Ls:      true
    Restrict Public Buckets:  true
  Versioning:
    Status:  Enabled
Status:
  Ack Resource Metadata:
    Arn:               arn:aws:s3:::my-production-bucket-xxxxxxxxxxxx
    Owner Account ID:  xxxxxxxxxxxx
    Region:            ap-northeast-1
  Conditions:
    Last Transition Time:  2025-12-04T14:38:52Z
    Message:               Resource synced successfully
    Reason:
    Status:                True
    Type:                  ACK.ResourceSynced
    Last Transition Time:  2025-12-04T14:38:52Z
    Message:               Resource synced successfully
    Reason:
    Status:                True
    Type:                  Ready
  Location:                http://my-production-bucket-xxxxxxxxxxxx.s3.amazonaws.com/
Events:
  Type    Reason  Age    From                       Message
  ----    ------  ----   ----                       -------
  Normal  Ready   2m50s  operatorpkg.bucket.status  Status condition transitioned, Type: Ready, Status: Unknown -> True, Reason: , Message: Resource synced successfully
```

また、対応する S3 バケットが作成されることを確認できました。

```
% aws s3 ls | grep "my-production-bucket"
2025-12-04 23:25:16 my-production-bucket-xxxxxxxxxxxx
```

## アップストリーム版と比較して制限されている機能

Argo CD の場合は The Notifications controller など、アップストリーム版と比較して制限されている機能がありました。

ACK の場合はアップストリームと比較して制限される機能は無いです。  
ただし、コントローラが GA しているサービスのみ利用可能です。

> Resource compatibility: ACK custom resources work identically to upstream ACK with no changes to your ACK resource YAML files. The capability uses the same Kubernetes APIs and CRDs, so tools like kubectl work the same way. All GA controllers and resources from upstream ACK are supported.  
> [https://docs.aws.amazon.com/eks/latest/userguide/ack-comparison.html#\_differences\_from\_upstream\_ack](https://docs.aws.amazon.com/eks/latest/userguide/ack-comparison.html#_differences_from_upstream_ack)

## Reconciliation Loop について

ACK には望ましい設定と実際の AWS の設定を比較して修正する仕組みがあります。

![スクリーンショット 2025-12-05 2.49.19.png](https://devio2024-2-media.developers.io/upload/0DJgoYo7YSbuU0EIsaoxh1/2025-12-04/B7Zbv7Vi7TVb.png)

ただし、常に監視しているわけでは無く、下記のいずれかでドリフトを確認する形になります。

> The reconciliation loop triggers when:  
> ・You create, update, or delete a resource in Kubernetes  
> ・The periodic sync interval expires (default: 10 hours, configurable per controller)  
> ・Controller restarts

[Reconciliation Loop | AWS Controllers for Kubernetes](https://aws-controllers-k8s.github.io/docs/concepts/#reconciliation-loop)

マネジメントコンソールから S3 のパブリックアクセスブロックを外してみた結果、10 時間程度後に修正してくれてました。

**私がマネジメントコンソールから変更**

![スクリーンショット 2025-12-05 16.30.14.png](https://devio2024-2-media.developers.io/upload/0DJgoYo7YSbuU0EIsaoxh1/2025-12-05/cWHfPyR0d4T8.png)

**ACK のサービスコントローラが修正**

![スクリーンショット 2025-12-05 16.30.27.png](https://devio2024-2-media.developers.io/upload/0DJgoYo7YSbuU0EIsaoxh1/2025-12-05/aD38fRWBPgKk.png)

## 料金

各機能ごとに料金が決まっており、機能有効化自体の料金と扱う Kubernetes リソース数に依る追加料金が存在します。  
東京 (ap-northeast-1) で ACK を利用した場合の料金は下記です。

| 項目 | 料金 | 備考 |
| --- | --- | --- |
| ACK base charge | $0.00649 per ACK Capability hour | 4.74 USD/月程度 |
| ACK usage charge | $0.000065 ACK resource hour | 0.05 USD/月程度 |

base charge はかなり安いので、どれだけ多くの AWS リソースを扱うか次第ですね。

## 最後に

アプリケーションのデプロイに必要な AWS インフラを Kubernetes API 経由で管理することで、デプロイフローを単純化できて良さそうです。  
まだまだ本番運用しているケースは少ないと思っていますが、EKS Capabilities が登場したことで採用される場面が増えるかもしれませんね。  
また、EKS Capbilities は Argo CD と kro と ACK を合わせて利用することでより大きなメリットを享受しやすくなります。  
Argo CD については下記ブログで試してみたので、こちらも参考にしていただけると嬉しいです。

この記事をシェアする