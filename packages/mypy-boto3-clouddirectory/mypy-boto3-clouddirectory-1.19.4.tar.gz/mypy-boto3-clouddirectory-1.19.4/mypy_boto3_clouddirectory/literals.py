"""
Type annotations for clouddirectory service literal definitions.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_clouddirectory/literals.html)

Usage::

    ```python
    from mypy_boto3_clouddirectory.literals import BatchReadExceptionTypeType

    data: BatchReadExceptionTypeType = "AccessDeniedException"
    ```
"""
import sys

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = (
    "BatchReadExceptionTypeType",
    "ConsistencyLevelType",
    "DirectoryStateType",
    "FacetAttributeTypeType",
    "FacetStyleType",
    "ListAppliedSchemaArnsPaginatorName",
    "ListAttachedIndicesPaginatorName",
    "ListDevelopmentSchemaArnsPaginatorName",
    "ListDirectoriesPaginatorName",
    "ListFacetAttributesPaginatorName",
    "ListFacetNamesPaginatorName",
    "ListIncomingTypedLinksPaginatorName",
    "ListIndexPaginatorName",
    "ListManagedSchemaArnsPaginatorName",
    "ListObjectAttributesPaginatorName",
    "ListObjectParentPathsPaginatorName",
    "ListObjectPoliciesPaginatorName",
    "ListOutgoingTypedLinksPaginatorName",
    "ListPolicyAttachmentsPaginatorName",
    "ListPublishedSchemaArnsPaginatorName",
    "ListTagsForResourcePaginatorName",
    "ListTypedLinkFacetAttributesPaginatorName",
    "ListTypedLinkFacetNamesPaginatorName",
    "LookupPolicyPaginatorName",
    "ObjectTypeType",
    "RangeModeType",
    "RequiredAttributeBehaviorType",
    "RuleTypeType",
    "UpdateActionTypeType",
    "ServiceName",
    "PaginatorName",
)


BatchReadExceptionTypeType = Literal[
    "AccessDeniedException",
    "CannotListParentOfRootException",
    "DirectoryNotEnabledException",
    "FacetValidationException",
    "InternalServiceException",
    "InvalidArnException",
    "InvalidNextTokenException",
    "LimitExceededException",
    "NotIndexException",
    "NotNodeException",
    "NotPolicyException",
    "ResourceNotFoundException",
    "ValidationException",
]
ConsistencyLevelType = Literal["EVENTUAL", "SERIALIZABLE"]
DirectoryStateType = Literal["DELETED", "DISABLED", "ENABLED"]
FacetAttributeTypeType = Literal["BINARY", "BOOLEAN", "DATETIME", "NUMBER", "STRING", "VARIANT"]
FacetStyleType = Literal["DYNAMIC", "STATIC"]
ListAppliedSchemaArnsPaginatorName = Literal["list_applied_schema_arns"]
ListAttachedIndicesPaginatorName = Literal["list_attached_indices"]
ListDevelopmentSchemaArnsPaginatorName = Literal["list_development_schema_arns"]
ListDirectoriesPaginatorName = Literal["list_directories"]
ListFacetAttributesPaginatorName = Literal["list_facet_attributes"]
ListFacetNamesPaginatorName = Literal["list_facet_names"]
ListIncomingTypedLinksPaginatorName = Literal["list_incoming_typed_links"]
ListIndexPaginatorName = Literal["list_index"]
ListManagedSchemaArnsPaginatorName = Literal["list_managed_schema_arns"]
ListObjectAttributesPaginatorName = Literal["list_object_attributes"]
ListObjectParentPathsPaginatorName = Literal["list_object_parent_paths"]
ListObjectPoliciesPaginatorName = Literal["list_object_policies"]
ListOutgoingTypedLinksPaginatorName = Literal["list_outgoing_typed_links"]
ListPolicyAttachmentsPaginatorName = Literal["list_policy_attachments"]
ListPublishedSchemaArnsPaginatorName = Literal["list_published_schema_arns"]
ListTagsForResourcePaginatorName = Literal["list_tags_for_resource"]
ListTypedLinkFacetAttributesPaginatorName = Literal["list_typed_link_facet_attributes"]
ListTypedLinkFacetNamesPaginatorName = Literal["list_typed_link_facet_names"]
LookupPolicyPaginatorName = Literal["lookup_policy"]
ObjectTypeType = Literal["INDEX", "LEAF_NODE", "NODE", "POLICY"]
RangeModeType = Literal["EXCLUSIVE", "FIRST", "INCLUSIVE", "LAST", "LAST_BEFORE_MISSING_VALUES"]
RequiredAttributeBehaviorType = Literal["NOT_REQUIRED", "REQUIRED_ALWAYS"]
RuleTypeType = Literal["BINARY_LENGTH", "NUMBER_COMPARISON", "STRING_FROM_SET", "STRING_LENGTH"]
UpdateActionTypeType = Literal["CREATE_OR_UPDATE", "DELETE"]
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
    "list_applied_schema_arns",
    "list_attached_indices",
    "list_development_schema_arns",
    "list_directories",
    "list_facet_attributes",
    "list_facet_names",
    "list_incoming_typed_links",
    "list_index",
    "list_managed_schema_arns",
    "list_object_attributes",
    "list_object_parent_paths",
    "list_object_policies",
    "list_outgoing_typed_links",
    "list_policy_attachments",
    "list_published_schema_arns",
    "list_tags_for_resource",
    "list_typed_link_facet_attributes",
    "list_typed_link_facet_names",
    "lookup_policy",
]
