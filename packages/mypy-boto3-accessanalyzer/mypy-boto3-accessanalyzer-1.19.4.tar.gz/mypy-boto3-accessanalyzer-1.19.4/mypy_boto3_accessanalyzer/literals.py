"""
Type annotations for accessanalyzer service literal definitions.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/literals.html)

Usage::

    ```python
    from mypy_boto3_accessanalyzer.literals import AccessPreviewStatusReasonCodeType

    data: AccessPreviewStatusReasonCodeType = "INTERNAL_ERROR"
    ```
"""
import sys

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = (
    "AccessPreviewStatusReasonCodeType",
    "AccessPreviewStatusType",
    "AclPermissionType",
    "AnalyzerStatusType",
    "FindingChangeTypeType",
    "FindingSourceTypeType",
    "FindingStatusType",
    "FindingStatusUpdateType",
    "JobErrorCodeType",
    "JobStatusType",
    "KmsGrantOperationType",
    "ListAccessPreviewFindingsPaginatorName",
    "ListAccessPreviewsPaginatorName",
    "ListAnalyzedResourcesPaginatorName",
    "ListAnalyzersPaginatorName",
    "ListArchiveRulesPaginatorName",
    "ListFindingsPaginatorName",
    "ListPolicyGenerationsPaginatorName",
    "LocaleType",
    "OrderByType",
    "PolicyTypeType",
    "ReasonCodeType",
    "ResourceTypeType",
    "TypeType",
    "ValidatePolicyFindingTypeType",
    "ValidatePolicyPaginatorName",
    "ServiceName",
    "PaginatorName",
)


AccessPreviewStatusReasonCodeType = Literal["INTERNAL_ERROR", "INVALID_CONFIGURATION"]
AccessPreviewStatusType = Literal["COMPLETED", "CREATING", "FAILED"]
AclPermissionType = Literal["FULL_CONTROL", "READ", "READ_ACP", "WRITE", "WRITE_ACP"]
AnalyzerStatusType = Literal["ACTIVE", "CREATING", "DISABLED", "FAILED"]
FindingChangeTypeType = Literal["CHANGED", "NEW", "UNCHANGED"]
FindingSourceTypeType = Literal["BUCKET_ACL", "POLICY", "S3_ACCESS_POINT"]
FindingStatusType = Literal["ACTIVE", "ARCHIVED", "RESOLVED"]
FindingStatusUpdateType = Literal["ACTIVE", "ARCHIVED"]
JobErrorCodeType = Literal[
    "AUTHORIZATION_ERROR",
    "RESOURCE_NOT_FOUND_ERROR",
    "SERVICE_ERROR",
    "SERVICE_QUOTA_EXCEEDED_ERROR",
]
JobStatusType = Literal["CANCELED", "FAILED", "IN_PROGRESS", "SUCCEEDED"]
KmsGrantOperationType = Literal[
    "CreateGrant",
    "Decrypt",
    "DescribeKey",
    "Encrypt",
    "GenerateDataKey",
    "GenerateDataKeyPair",
    "GenerateDataKeyPairWithoutPlaintext",
    "GenerateDataKeyWithoutPlaintext",
    "GetPublicKey",
    "ReEncryptFrom",
    "ReEncryptTo",
    "RetireGrant",
    "Sign",
    "Verify",
]
ListAccessPreviewFindingsPaginatorName = Literal["list_access_preview_findings"]
ListAccessPreviewsPaginatorName = Literal["list_access_previews"]
ListAnalyzedResourcesPaginatorName = Literal["list_analyzed_resources"]
ListAnalyzersPaginatorName = Literal["list_analyzers"]
ListArchiveRulesPaginatorName = Literal["list_archive_rules"]
ListFindingsPaginatorName = Literal["list_findings"]
ListPolicyGenerationsPaginatorName = Literal["list_policy_generations"]
LocaleType = Literal["DE", "EN", "ES", "FR", "IT", "JA", "KO", "PT_BR", "ZH_CN", "ZH_TW"]
OrderByType = Literal["ASC", "DESC"]
PolicyTypeType = Literal["IDENTITY_POLICY", "RESOURCE_POLICY", "SERVICE_CONTROL_POLICY"]
ReasonCodeType = Literal[
    "AWS_SERVICE_ACCESS_DISABLED",
    "DELEGATED_ADMINISTRATOR_DEREGISTERED",
    "ORGANIZATION_DELETED",
    "SERVICE_LINKED_ROLE_CREATION_FAILED",
]
ResourceTypeType = Literal[
    "AWS::IAM::Role",
    "AWS::KMS::Key",
    "AWS::Lambda::Function",
    "AWS::Lambda::LayerVersion",
    "AWS::S3::Bucket",
    "AWS::SQS::Queue",
    "AWS::SecretsManager::Secret",
]
TypeType = Literal["ACCOUNT", "ORGANIZATION"]
ValidatePolicyFindingTypeType = Literal["ERROR", "SECURITY_WARNING", "SUGGESTION", "WARNING"]
ValidatePolicyPaginatorName = Literal["validate_policy"]
ServiceName = Literal[
    "accessanalyzer",
    "account",
    "acm",
    "acm-pca",
    "alexaforbusiness",
    "amp",
    "amplify",
    "amplifybackend",
    "apigateway",
    "apigatewaymanagementapi",
    "apigatewayv2",
    "appconfig",
    "appflow",
    "appintegrations",
    "application-autoscaling",
    "application-insights",
    "applicationcostprofiler",
    "appmesh",
    "apprunner",
    "appstream",
    "appsync",
    "athena",
    "auditmanager",
    "autoscaling",
    "autoscaling-plans",
    "backup",
    "batch",
    "braket",
    "budgets",
    "ce",
    "chime",
    "chime-sdk-identity",
    "chime-sdk-messaging",
    "cloud9",
    "cloudcontrol",
    "clouddirectory",
    "cloudformation",
    "cloudfront",
    "cloudhsm",
    "cloudhsmv2",
    "cloudsearch",
    "cloudsearchdomain",
    "cloudtrail",
    "cloudwatch",
    "codeartifact",
    "codebuild",
    "codecommit",
    "codedeploy",
    "codeguru-reviewer",
    "codeguruprofiler",
    "codepipeline",
    "codestar",
    "codestar-connections",
    "codestar-notifications",
    "cognito-identity",
    "cognito-idp",
    "cognito-sync",
    "comprehend",
    "comprehendmedical",
    "compute-optimizer",
    "config",
    "connect",
    "connect-contact-lens",
    "connectparticipant",
    "cur",
    "customer-profiles",
    "databrew",
    "dataexchange",
    "datapipeline",
    "datasync",
    "dax",
    "detective",
    "devicefarm",
    "devops-guru",
    "directconnect",
    "discovery",
    "dlm",
    "dms",
    "docdb",
    "ds",
    "dynamodb",
    "dynamodbstreams",
    "ebs",
    "ec2",
    "ec2-instance-connect",
    "ecr",
    "ecr-public",
    "ecs",
    "efs",
    "eks",
    "elastic-inference",
    "elasticache",
    "elasticbeanstalk",
    "elastictranscoder",
    "elb",
    "elbv2",
    "emr",
    "emr-containers",
    "es",
    "events",
    "finspace",
    "finspace-data",
    "firehose",
    "fis",
    "fms",
    "forecast",
    "forecastquery",
    "frauddetector",
    "fsx",
    "gamelift",
    "glacier",
    "globalaccelerator",
    "glue",
    "grafana",
    "greengrass",
    "greengrassv2",
    "groundstation",
    "guardduty",
    "health",
    "healthlake",
    "honeycode",
    "iam",
    "identitystore",
    "imagebuilder",
    "importexport",
    "inspector",
    "iot",
    "iot-data",
    "iot-jobs-data",
    "iot1click-devices",
    "iot1click-projects",
    "iotanalytics",
    "iotdeviceadvisor",
    "iotevents",
    "iotevents-data",
    "iotfleethub",
    "iotsecuretunneling",
    "iotsitewise",
    "iotthingsgraph",
    "iotwireless",
    "ivs",
    "kafka",
    "kafkaconnect",
    "kendra",
    "kinesis",
    "kinesis-video-archived-media",
    "kinesis-video-media",
    "kinesis-video-signaling",
    "kinesisanalytics",
    "kinesisanalyticsv2",
    "kinesisvideo",
    "kms",
    "lakeformation",
    "lambda",
    "lex-models",
    "lex-runtime",
    "lexv2-models",
    "lexv2-runtime",
    "license-manager",
    "lightsail",
    "location",
    "logs",
    "lookoutequipment",
    "lookoutmetrics",
    "lookoutvision",
    "machinelearning",
    "macie",
    "macie2",
    "managedblockchain",
    "marketplace-catalog",
    "marketplace-entitlement",
    "marketplacecommerceanalytics",
    "mediaconnect",
    "mediaconvert",
    "medialive",
    "mediapackage",
    "mediapackage-vod",
    "mediastore",
    "mediastore-data",
    "mediatailor",
    "memorydb",
    "meteringmarketplace",
    "mgh",
    "mgn",
    "migrationhub-config",
    "mobile",
    "mq",
    "mturk",
    "mwaa",
    "neptune",
    "network-firewall",
    "networkmanager",
    "nimble",
    "opensearch",
    "opsworks",
    "opsworkscm",
    "organizations",
    "outposts",
    "panorama",
    "personalize",
    "personalize-events",
    "personalize-runtime",
    "pi",
    "pinpoint",
    "pinpoint-email",
    "pinpoint-sms-voice",
    "polly",
    "pricing",
    "proton",
    "qldb",
    "qldb-session",
    "quicksight",
    "ram",
    "rds",
    "rds-data",
    "redshift",
    "redshift-data",
    "rekognition",
    "resource-groups",
    "resourcegroupstaggingapi",
    "robomaker",
    "route53",
    "route53-recovery-cluster",
    "route53-recovery-control-config",
    "route53-recovery-readiness",
    "route53domains",
    "route53resolver",
    "s3",
    "s3control",
    "s3outposts",
    "sagemaker",
    "sagemaker-a2i-runtime",
    "sagemaker-edge",
    "sagemaker-featurestore-runtime",
    "sagemaker-runtime",
    "savingsplans",
    "schemas",
    "sdb",
    "secretsmanager",
    "securityhub",
    "serverlessrepo",
    "service-quotas",
    "servicecatalog",
    "servicecatalog-appregistry",
    "servicediscovery",
    "ses",
    "sesv2",
    "shield",
    "signer",
    "sms",
    "sms-voice",
    "snow-device-management",
    "snowball",
    "sns",
    "sqs",
    "ssm",
    "ssm-contacts",
    "ssm-incidents",
    "sso",
    "sso-admin",
    "sso-oidc",
    "stepfunctions",
    "storagegateway",
    "sts",
    "support",
    "swf",
    "synthetics",
    "textract",
    "timestream-query",
    "timestream-write",
    "transcribe",
    "transfer",
    "translate",
    "voice-id",
    "waf",
    "waf-regional",
    "wafv2",
    "wellarchitected",
    "wisdom",
    "workdocs",
    "worklink",
    "workmail",
    "workmailmessageflow",
    "workspaces",
    "xray",
]
PaginatorName = Literal[
    "list_access_preview_findings",
    "list_access_previews",
    "list_analyzed_resources",
    "list_analyzers",
    "list_archive_rules",
    "list_findings",
    "list_policy_generations",
    "validate_policy",
]
