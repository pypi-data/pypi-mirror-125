"""
Type annotations for chime service literal definitions.

[Open documentation](https://vemel.github.io/boto3_stubs_docs/mypy_boto3_chime/literals.html)

Usage::

    ```python
    from mypy_boto3_chime.literals import AccountStatusType

    data: AccountStatusType = "Active"
    ```
"""
import sys

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal

__all__ = (
    "AccountStatusType",
    "AccountTypeType",
    "AppInstanceDataTypeType",
    "ArtifactsStateType",
    "AudioMuxTypeType",
    "BotTypeType",
    "CallingNameStatusType",
    "CapabilityType",
    "ChannelMembershipTypeType",
    "ChannelMessagePersistenceTypeType",
    "ChannelMessageTypeType",
    "ChannelModeType",
    "ChannelPrivacyType",
    "ContentMuxTypeType",
    "EmailStatusType",
    "ErrorCodeType",
    "GeoMatchLevelType",
    "InviteStatusType",
    "LicenseType",
    "ListAccountsPaginatorName",
    "ListUsersPaginatorName",
    "MediaPipelineSinkTypeType",
    "MediaPipelineSourceTypeType",
    "MediaPipelineStatusType",
    "MemberTypeType",
    "NotificationTargetType",
    "NumberSelectionBehaviorType",
    "OrderedPhoneNumberStatusType",
    "OriginationRouteProtocolType",
    "PhoneNumberAssociationNameType",
    "PhoneNumberOrderStatusType",
    "PhoneNumberProductTypeType",
    "PhoneNumberStatusType",
    "PhoneNumberTypeType",
    "ProxySessionStatusType",
    "RegistrationStatusType",
    "RoomMembershipRoleType",
    "SipRuleTriggerTypeType",
    "SortOrderType",
    "TranscribeLanguageCodeType",
    "TranscribeMedicalLanguageCodeType",
    "TranscribeMedicalRegionType",
    "TranscribeMedicalSpecialtyType",
    "TranscribeMedicalTypeType",
    "TranscribeRegionType",
    "TranscribeVocabularyFilterMethodType",
    "UserTypeType",
    "VideoMuxTypeType",
    "VoiceConnectorAwsRegionType",
    "ServiceName",
    "PaginatorName",
)

AccountStatusType = Literal["Active", "Suspended"]
AccountTypeType = Literal["EnterpriseDirectory", "EnterpriseLWA", "EnterpriseOIDC", "Team"]
AppInstanceDataTypeType = Literal["Channel", "ChannelMessage"]
ArtifactsStateType = Literal["Disabled", "Enabled"]
AudioMuxTypeType = Literal["AudioOnly", "AudioWithActiveSpeakerVideo"]
BotTypeType = Literal["ChatBot"]
CallingNameStatusType = Literal["Unassigned", "UpdateFailed", "UpdateInProgress", "UpdateSucceeded"]
CapabilityType = Literal["SMS", "Voice"]
ChannelMembershipTypeType = Literal["DEFAULT", "HIDDEN"]
ChannelMessagePersistenceTypeType = Literal["NON_PERSISTENT", "PERSISTENT"]
ChannelMessageTypeType = Literal["CONTROL", "STANDARD"]
ChannelModeType = Literal["RESTRICTED", "UNRESTRICTED"]
ChannelPrivacyType = Literal["PRIVATE", "PUBLIC"]
ContentMuxTypeType = Literal["ContentOnly"]
EmailStatusType = Literal["Failed", "NotSent", "Sent"]
ErrorCodeType = Literal[
    "AccessDenied",
    "BadRequest",
    "Conflict",
    "Forbidden",
    "NotFound",
    "PhoneNumberAssociationsExist",
    "PreconditionFailed",
    "ResourceLimitExceeded",
    "ServiceFailure",
    "ServiceUnavailable",
    "Throttled",
    "Throttling",
    "Unauthorized",
    "Unprocessable",
    "VoiceConnectorGroupAssociationsExist",
]
GeoMatchLevelType = Literal["AreaCode", "Country"]
InviteStatusType = Literal["Accepted", "Failed", "Pending"]
LicenseType = Literal["Basic", "Plus", "Pro", "ProTrial"]
ListAccountsPaginatorName = Literal["list_accounts"]
ListUsersPaginatorName = Literal["list_users"]
MediaPipelineSinkTypeType = Literal["S3Bucket"]
MediaPipelineSourceTypeType = Literal["ChimeSdkMeeting"]
MediaPipelineStatusType = Literal["Failed", "InProgress", "Initializing", "Stopped", "Stopping"]
MemberTypeType = Literal["Bot", "User", "Webhook"]
NotificationTargetType = Literal["EventBridge", "SNS", "SQS"]
NumberSelectionBehaviorType = Literal["AvoidSticky", "PreferSticky"]
OrderedPhoneNumberStatusType = Literal["Acquired", "Failed", "Processing"]
OriginationRouteProtocolType = Literal["TCP", "UDP"]
PhoneNumberAssociationNameType = Literal[
    "AccountId", "SipRuleId", "UserId", "VoiceConnectorGroupId", "VoiceConnectorId"
]
PhoneNumberOrderStatusType = Literal["Failed", "Partial", "Processing", "Successful"]
PhoneNumberProductTypeType = Literal[
    "BusinessCalling", "SipMediaApplicationDialIn", "VoiceConnector"
]
PhoneNumberStatusType = Literal[
    "AcquireFailed",
    "AcquireInProgress",
    "Assigned",
    "DeleteFailed",
    "DeleteInProgress",
    "ReleaseFailed",
    "ReleaseInProgress",
    "Unassigned",
]
PhoneNumberTypeType = Literal["Local", "TollFree"]
ProxySessionStatusType = Literal["Closed", "InProgress", "Open"]
RegistrationStatusType = Literal["Registered", "Suspended", "Unregistered"]
RoomMembershipRoleType = Literal["Administrator", "Member"]
SipRuleTriggerTypeType = Literal["RequestUriHostname", "ToPhoneNumber"]
SortOrderType = Literal["ASCENDING", "DESCENDING"]
TranscribeLanguageCodeType = Literal[
    "de-DE",
    "en-AU",
    "en-GB",
    "en-US",
    "es-US",
    "fr-CA",
    "fr-FR",
    "it-IT",
    "ja-JP",
    "ko-KR",
    "pt-BR",
    "zh-CN",
]
TranscribeMedicalLanguageCodeType = Literal["en-US"]
TranscribeMedicalRegionType = Literal[
    "ap-southeast-2", "auto", "ca-central-1", "eu-west-1", "us-east-1", "us-east-2", "us-west-2"
]
TranscribeMedicalSpecialtyType = Literal[
    "CARDIOLOGY", "NEUROLOGY", "ONCOLOGY", "PRIMARYCARE", "RADIOLOGY", "UROLOGY"
]
TranscribeMedicalTypeType = Literal["CONVERSATION", "DICTATION"]
TranscribeRegionType = Literal[
    "ap-northeast-1",
    "ap-northeast-2",
    "ap-southeast-2",
    "auto",
    "ca-central-1",
    "eu-central-1",
    "eu-west-1",
    "eu-west-2",
    "sa-east-1",
    "us-east-1",
    "us-east-2",
    "us-west-2",
]
TranscribeVocabularyFilterMethodType = Literal["mask", "remove", "tag"]
UserTypeType = Literal["PrivateUser", "SharedDevice"]
VideoMuxTypeType = Literal["VideoOnly"]
VoiceConnectorAwsRegionType = Literal["us-east-1", "us-west-2"]
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
PaginatorName = Literal["list_accounts", "list_users"]
