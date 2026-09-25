====================================================================================================
ARTIGO 1
Link de Origem: https://docs.cloud.google.com/architecture/big-data-analytics
====================================================================================================

Big data and analytics resources
Stay organized with collections
Save and categorize content based on your preferences.

Last reviewed 2025-05-02 UTC

The Architecture Center provides content resources across a wide variety of
big data and analytics subjects.

The documents that are listed in the "Big data and analytics" section of the
left navigation can help you make decisions about managing big data and
analytics.

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-05-02 UTC."],[],[]]


====================================================================================================
ARTIGO 2
Link de Origem: https://docs.cloud.google.com/architecture/blueprints/confidential-data-warehouse-blueprint
====================================================================================================

Many organizations deploy data warehouses that store sensitive data so that they can analyze the data for a variety of business purposes. This document is intended for data engineers and security administrators who deploy and secure data warehouses using BigQuery. It's part of a blueprint that includes the following:

- Two GitHub repositories
(`terraform-google-secured-data-warehouse` and`terraform-google-secured-data-warehouse-onprem-ingest` )
that contain Terraform configurations and scripts. The Terraform configuration
sets up a Google Cloud environment in Google Cloud for a data warehouse that
stores confidential data.
- A guide to the architecture, design, and security controls of this blueprint (this document).
- A walkthrough that deploys a sample environment.

This document discusses the following:

- The architecture and Google Cloud services that you can use to help secure a data warehouse in a production environment.
- Best practices for importing data into BigQuery from an external network such as an on-premises environment.
- Best practices for data governance when creating, deploying, and operating a data warehouse in Google Cloud, including the following: 
  - data de-identification
  - differential handling of confidential data
  - column-level encryption
  - column-level access controls

This document assumes that you have already configured a foundational set of security controls as described in the enterprise foundations blueprint. It helps you to layer additional controls onto your existing security controls to help protect confidential data in a data warehouse.

## Data warehouse use cases

The blueprint supports the following use cases:

- Use the
`terraform-google-secured-data-warehouse` repository to import data from Google Cloud into a
BigQuery data warehouse
- Use the
`terraform-google-secured-data-warehouse-onprem-ingest` repository to import data from an on-premises environment or another cloud
into a BigQuery data warehouse

## Overview

Data warehouses such as BigQuery let businesses analyze their business data for insights. Analysts access the business data that is stored in data warehouses to create insights. If your data warehouse includes confidential data, you must take measures to preserve the security, confidentiality, integrity, and availability of the business data while it is stored, while it is in transit, or while it is being analyzed. In this blueprint, you do the following:

- When importing data from external data sources, encrypt your data that's located outside of Google Cloud (for example, in an on-premises environment) and import it into Google Cloud.
- Configure controls that help secure access to confidential data.
- Configure controls that help secure the data pipeline.
- Configure an appropriate separation of duties for different personas.
- When importing data from other sources located in Google Cloud (also
known as *internal data sources* ), set up templates to find and de-identify
confidential data.
- Set up appropriate security controls and logging to help protect confidential data.
- Use data classification, policy tags, dynamic data masking, and column-level encryption to restrict access to specific columns in the data warehouse.

## Architecture

To create a confidential data warehouse, you need to import data securely and then store the data in a VPC Service Controls perimeter.

### Architecture when importing data from Google Cloud

The following image shows how ingested data is categorized, de-identified, and
stored when you import source data from Google Cloud using the
`terraform-google-secured-data-warehouse` repository. It also shows how you can
re-identify confidential data on demand for analysis.

### Architecture when importing data from external sources

The following image shows how data is ingested and stored when you import data
from an on-premises environment or another cloud into a BigQuery
warehouse using the `terraform-google-secured-data-warehouse-onprem-ingest`
repository.

### Google Cloud services and features

The architectures use a combination of the following Google Cloud services and features:

| Service or feature | Description | 
|---|---|
| BigQuery | Applicable to both internal and external data sources. However, different storage options exist, as follows:  BigQuery uses various security controls to help protect content, including access controls, column-level security for confidential data, and data encryption. | 
| Cloud Key Management Service (Cloud KMS) with Cloud HSM | Applicable to both internal and external sources. However, an additional use case for external data sources exists. Cloud HSM is a cloud-based hardware security module (HSM) service that hosts the key encryption key (KEK). When importing data from an external source, you use Cloud HSM to generate the encryption key that you use to encrypt the data in your network before sending it to Google Cloud. | 
| Cloud Logging | Applicable to both internal and external sources. Cloud Logging collects all the logs from Google Cloud services for storage and retrieval by your analysis and investigation tools. | 
| Cloud Monitoring | Applicable to both internal and external sources. Cloud Monitoring collects and stores performance information and metrics about Google Cloud services. | 
| Cloud Run functions | Applicable for external data sources only. Cloud Run functions is triggered by Cloud Storage and writes the data that Cloud Storage uploads to the ingestion bucket into BigQuery. | 
| Cloud Storage and Pub/Sub | Applicable to both internal and external sources. Cloud Storage and Pub/Sub receive data as follows:   | 
| Data Profiler for BigQuery | Applicable to both internal and external sources. Data Profiler for BigQuery automatically scans for sensitive data in all BigQuery tables and columns across the entire organization, including all folders and projects. | 
| Dataflow pipelines | Applicable to both internal and external sources; however, different pipelines exist. Dataflow pipelines import data, as follows:  | 
| Knowledge Catalog | Applicable to both internal and external sources. Knowledge Catalog automatically categorizes confidential data with metadata, also known as policy tags, during ingestion. Knowledge Catalog also uses metadata to manage access to confidential data. To control access to data within the data warehouse, you apply policy tags to columns that include confidential data. | 
| Dedicated Interconnect | Applicable for external data sources only. Dedicated Interconnect lets you move data between your network and Google Cloud. You can use another connectivity option, as described in Choosing a Network Connectivity product. | 
| IAM and Resource Manager | Applicable to both internal and external sources. Identity and Access Management (IAM) and Resource Manager restrict access and segment resources. The access controls and resource hierarchy follow the principle of least privilege. | 
| Security Command Center | Applicable to both internal and external sources. Security Command Center monitors and reviews security findings from across your Google Cloud environment in a central location. | 
| Sensitive Data Protection | Applicable to both internal and external sources; however, different scans occur. Sensitive Data Protection scans data, as follows:  | 
| VPC Service Controls | Applicable to both internal and external sources; however, different perimeters exist. VPC Service Controls creates security perimeters that isolate services and resources by setting up authorization, access controls, and secure data exchange. The perimeters are as follows:  These perimeters are designed to protect incoming content, isolate confidential data by setting up additional access controls and monitoring, and separate your governance from the actual data in the warehouse. Your governance includes key management, data catalog management, and logging. | 

## Organization structure

You group your organization's resources so that you can manage them and separate your testing environments from your production environment. Resource Manager lets you logically group resources by project, folder, and organization.

The following diagrams show you a resource hierarchy with folders that represent different environments such as bootstrap, common, production, non-production (or staging), and development. You deploy most of the projects in the architecture into the production folder and the data governance project in the common folder, which is used for governance.

### Organization structure when importing data from Google Cloud

The following diagram shows the organization structure when importing data from
Google Cloud using the `terraform-google-secured-data-warehouse` repository.

### Organization structure when importing data from external sources

The following diagram shows the organization structure when importing data from
an external source using the
`terraform-google-secured-data-warehouse-onprem-ingest` repository.

### Folders

You use folders to isolate your production environment and governance services from your non-production and testing environments. The following table describes the folders from the enterprise foundations blueprint that are used by this architecture.

| Folder | Description | 
|---|---|
| Bootstrap | Contains resources required to deploy the enterprise foundations blueprint. | 
| Common | Contains centralized services for the organization, such as the Data governance project. | 
| Production | Contains projects that have cloud resources that have been tested and are ready to use. In this architecture, the Production folder contains the Data ingestion project and data-related projects. | 
| Non-production | Contains projects that have cloud resources that are being tested and staged for release. In this architecture, the Non-production folder contains the Data ingestion project and data-related projects. | 
| Development | Contains projects that have cloud resources that are being developed. In this architecture, the Development folder contains the Data ingestion project and data-related projects. | 

You can change the names of these folders to align with your organization's folder structure, but we recommend that you maintain a similar structure. For more information, see the enterprise foundations blueprint.

### Projects

You isolate parts of your environment using projects. The following table describes the projects that are needed within the organization. You create these projects when you run the Terraform code. You can change the names of these projects, but we recommend that you maintain a similar project structure.

| Project | Description | 
|---|---|
| Data ingestion | Common project for both internal and external sources. Contains services that are required in order to receive data and de-identify confidential data. | 
| Data governance | Common project for both internal and external sources. Contains services that provide key management, logging, and data cataloging capabilities. | 
| Non-confidential data | Project for internal sources only. Contains services that are required in order to store data that has been de-identified. | 
| Confidential data | Project for internal sources only. Contains services that are required in order to store and re-identify confidential data. | 
| Data | Project for external sources only. Contains services that are required to store data. | 

In addition to these projects, your environment must also include a project that hosts a Dataflow Flex Template job. The Flex Template job is required for the streaming data pipeline.

## Mapping roles and groups to projects

You must give different user groups in your organization access to the projects that make up the confidential data warehouse. The following sections describe the architecture recommendations for user groups and role assignments in the projects that you create. You can customize the groups to match your organization's existing structure, but we recommend that you maintain a similar segregation of duties and role assignment.

### Data analyst group

Data analysts analyze the data in the warehouse. In the
`terraform-google-secured-data-warehouse-onprem-ingest` repository, this group can
view data after it has been loaded into the data warehouse and perform the same
operations as the Encrypted data viewer
group.

The following table describes the group's roles in different projects for the
`terraform-google-secured-data-warehouse` repository (internal data sources only).

| Project mapping | Roles | 
|---|---|
| Data ingestion |  Additional role for data analysts that require access to confidential data: | 
| Confidential data |  | 
| Non-confidential data |  | 

The following table describes the group's roles in different projects for the
`terraform-google-secured-data-warehouse-onprem-ingest` repository (external data
sources only).

| Scope of assignment | Roles | 
|---|---|
| Data ingestion project |  | 
| Data project |  | 
| Data policy level | Masked Reader (`roles/bigquerydatapolicy.maskedReader` ) | 

### Encrypted data viewer group (external sources only)

The Encrypted data viewer group in the
`terraform-google-secured-data-warehouse-onprem-ingest` repository can view
encrypted data from BigQuery reporting tables through
Data Studio and other reporting tools, such as SAP Business Objects.
The encrypted data viewer group can't view cleartext data from encrypted
columns.

This group requires the BigQuery User
(`roles/bigquery.jobUser`) role
in the Data project. This group also requires the Masked Reader
(`roles/bigquerydatapolicy.maskedReader`)
role at the data policy level.

### Plaintext reader group (external sources only)

The Plaintext reader group in the
`terraform-google-secured-data-warehouse-onprem-ingest` repository has the
required permission to call the decryption user-defined function (UDF) to view
plaintext data and the additional permission to read unmasked data.

This group requires the following roles in the Data project:

- BigQuery User (`roles/bigquery.user` )
- BigQuery User (`roles/bigquery.jobUser` )
- Cloud KMS Viewer (`roles/cloudkms.viewer` )

In addition, this group requires the Fine-Grained Reader
(`roles/datacatalog.categoryFineGrainedReader`) role at the
Knowledge Catalog level.

### Data engineer group

Data engineers set up and maintain the data pipeline and warehouse.

The following table describes the group's roles in different projects for the
`terraform-google-secured-data-warehouse` repository.

| Scope of assignment | Roles | 
|---|---|
| Data ingestion project |  | 
| Confidential data project |  | 
| Non-confidential data project |  | 

The following table describes the group's roles in different projects for the
`terraform-google-secured-data-warehouse-onprem-ingest` repository.

| Scope of assignment | Roles | 
|---|---|
| Data ingestion project |  | 
| Data project |  | 

### Network administrator group

Network administrators configure the network. Typically, they are members of the networking team.

Network administrators require the following roles at the organization level:

### Security administrator group

Security administrators administer security controls such as access, keys, firewall rules, VPC Service Controls, and the Security Command Center.

Security administrators require the following roles at the organization level:

### Security analyst group

Security analysts monitor and respond to security incidents and Sensitive Data Protection findings.

Security analysts require the following roles at the organization level:

### Example group access flows for external sources

The following sections describe access flows for two groups when importing data
from external sources using the
`terraform-google-secured-data-warehouse-onprem-ingest` repository.

#### Access flow for Encrypted data viewer group

The following diagram shows what occurs when a user from the Encrypted data viewer group tries to access encrypted data in BigQuery.

The steps to access data in BigQuery are as follows:

1. The Encrypted data viewer executes the following query on BigQuery to access confidential data: ```
SELECT ssn, pan FROM cc_card_table
```
2. BigQuery verifies access as follows: 
  - The user is authenticated using valid, unexpired Google Cloud credentials.
  - The user identity and the IP address that the request originated from are part of the allowlist in the access level or ingress rule on the VPC Service Controls perimeter.
  - IAM verifies that the user has the appropriate roles and is authorized to access selected encrypted columns on the BigQuery table.

BigQuery returns the confidential data in encrypted format.

#### Access flow for Plaintext reader group

The following diagram shows what occurs when a user from the Plaintext reader group tries to access encrypted data in BigQuery.

The steps to access data in BigQuery are as follows:

1. The Plaintext reader executes the following query on BigQuery to access confidential data in decrypted format: ```
SELECT decrypt_ssn(ssn) FROM cc_card_table
```
2. BigQuery calls the decrypt user-defined function (UDF) within the query to access protected columns.
3. Access is verified as follows: 
  - IAM verifies that the user has appropriate roles and is authorized to access the decrypt UDF on BigQuery.
  - The UDF retrieves the wrapped data encryption key (DEK) that was used to protect sensitive data columns.
4. The decrypt UDF calls the key encryption key (KEK) in Cloud HSM to unwrap the DEK. The decrypt UDF uses the BigQuery AEAD decrypt function to decrypt the sensitive data columns.
5. The user is granted access to the plaintext data in the sensitive data columns.

## Common security controls

The following sections describe the controls that apply to both internal and external sources.

### Data ingestion controls

To create your data warehouse, you must transfer data from another Google Cloud source (for example, a data lake), your on-premises environment, or another cloud. You can use one of the following options to transfer your data into the data warehouse on BigQuery:

- A batch job that uses Cloud Storage.
- A streaming job that uses Pub/Sub.

To help protect data during ingestion, you can use client-side encryption, firewall rules, and access level policies. The ingestion process is sometimes referred to as an extract, transform, load (ETL) process.

### Network and firewall rules

Virtual Private Cloud (VPC) firewall
rules control the flow of data
into the perimeters. You create firewall rules that deny all egress, except for
specific TCP port 443 connections from the `restricted.googleapis.com` special
domain names. The `restricted.googleapis.com` domain has the following benefits:

- It helps reduce your network attack surface by using Private Google Access when workloads communicate to Google APIs and services.
- It ensures that you only use services that support VPC Service Controls.

For more information, see Configuring Private Google Access.

When using the `terraform-google-secured-data-warehouse` repository, you must
configure separate subnets for each Dataflow job. Separate
subnets ensure that data that is being de-identified is properly separated from
data that is being re-identified.

The data pipeline requires you to open TCP ports in the firewall, as defined in
the `dataflow_firewall.tf` file in the respective repositories. For more
information, see Configuring internet access and firewall
rules.

To deny resources the ability to use external IP addresses, the Define allowed
external IPs for VM
instances (`compute.vmExternalIpAccess`)
organization policy is set to deny all.

### Perimeter controls

As shown in the architecture diagram, you place the resources for the data warehouse into separate perimeters. To enable services in different perimeters to share data, you create perimeter bridges.

Perimeter bridges let protected services make requests for resources outside of
their perimeter. These bridges make the following connections for the
`terraform-google-secured-data-warehouse` repository:

- They connect the data ingestion project to the governance project so that de-identification can take place during ingestion.
- They connect the non-confidential data project and the confidential data project so that confidential data can be re-identified when a data analyst requests it.
- They connect the confidential project to the data governance project so that re-identification can take place when a data analyst requests it.

These bridges make the following connections for the
`terraform-google-secured-data-warehouse-onprem-ingest` repository:

- They connect the Data ingestion project to the Data project so that data can be ingested into BigQuery.
- They connect the Data project to the Data governance project so that Sensitive Data Protection can scan BigQuery for unprotected confidential data.
- They connect the Data ingestion project to the Data governance project for access to logging, monitoring, and encryption keys.

In addition to perimeter bridges, you use egress rules to let resources protected by service perimeters access resources that are outside the perimeter. In this solution, you configure egress rules to obtain the external Dataflow Flex Template jobs that are located in Cloud Storage in an external project. For more information, see Access a Google Cloud resource outside the perimeter.

### Access policy

To help ensure that only specific identities (user or service) can access resources and data, you enable IAM groups and roles.

To help ensure that only specific sources can access your projects, you enable an access policy for your Google organization. We recommend that you create an access policy that specifies the allowed IP address range for requests and only allows requests from specific users or service accounts. For more information, see Access level attributes.

### Service accounts and access controls

Service accounts are identities that Google Cloud can use to run API
requests on your behalf. Service accounts ensure that user identities don't
have direct access to services. To permit separation of duties, you create
service accounts with different roles for specific purposes. These service
accounts are defined in the `data-ingestion` module and the `confidential-data`
module in each architecture.

For the `terraform-google-secured-data-warehouse` repository, the service
accounts are as follows:

- A Dataflow controller service account for the Dataflow pipeline that de-identifies confidential data.
- A Dataflow controller service account for the Dataflow pipeline that re-identifies confidential data.
- A Cloud Storage service account to ingest data from a batch file.
- A Pub/Sub service account to ingest data from a streaming service.
- A Cloud Scheduler service account to run the batch Dataflow job that creates the Dataflow pipeline.

The following table lists the roles that are assigned to each service account:

| Service Account | Name | Project | Roles | 
|---|---|---|---|
| Dataflow controller This account is used for de-identification. | `sa-dataflow-controller` | Data ingestion |  | 
| Dataflow controller This account is used for re-identification. | `sa-dataflow-controller-reid` | Confidential data |  | 
| Cloud Storage | `sa-storage-writer` | Data ingestion |  | 
| Pub/Sub | `sa-pubsub-writer` | Data ingestion |  | 
| Cloud Scheduler | `sa-scheduler-controller` | Data ingestion |  | 

For the `terraform-google-secured-data-warehouse-onprem-ingest` repository, the
service accounts are as follows:

- Cloud Storage service account runs the automated batch data upload process to the ingestion storage bucket.
- Pub/Sub service account enables streaming of data to Pub/Sub service.
- Dataflow controller service account is used by the Dataflow pipeline to transform and write data from Pub/Sub to BigQuery.
- Cloud Run functions service account writes subsequent batch data uploaded from Cloud Storage to BigQuery.
- Storage Upload service account allows the ETL pipeline to create objects.
- Pub/Sub Write service Account lets the ETL pipeline write data to Pub/Sub.

The following table lists the roles that are assigned to each service account:

| Name | Roles | Scope of Assignment | 
|---|---|---|
| Dataflow controller service account |  | Data ingestion project | 
|  |  | Data project | 
|  |  | Data governance | 
| Cloud Run functions service account |  | Data ingestion project | 
|  |  | Data project | 
| Storage Upload service account |  | Data ingestion Project | 
| Pub/Sub Write service account |  | Data ingestion Project | 

### Organizational policies

This architecture includes the organization policy constraints that the enterprise foundations blueprint uses and adds additional constraints. For more information about the constraints that the enterprise foundations blueprint uses, see Organization policy constraints.

The following table describes the additional organizational policy
constraints
that are defined in the `org_policies` module for the respective repositories:

| Policy | Constraint name | Recommended value | 
|---|---|---|
| Restrict resource deployments to specific physical locations. For additional values, see Value groups. | `gcp.resourceLocations` | One of the following: `in:us-locations` `in:eu-locations` `in:asia-locations` | 
| Disable service account creation | `iam.disableServiceAccountCreation` | `true` | 
| Enable OS Login for VMs created in the project. | `compute.requireOsLogin` | `true` | 
| Restrict new forwarding rules to be internal only, based on IP address. | `compute.restrictProtocolForwardingCreationForTypes` | `INTERNAL` | 
| Define the set of Shared VPC subnetworks that Compute Engine resources can use. | `compute.restrictSharedVpcSubnetworks` | `projects//regions//s ubnetworks/` . Replace with the resource ID of the private subnet that you want the architecture to use. | 
| Disable serial port output logging to Cloud Logging. | `compute.disableSerialPortLogging` | `true` | 
| Require CMEK protection (`terraform-google-secured-data-warehouse-onprem-ingest` only) | `gcp.restrictNonCmekServices` | `bigquery.googleapis.com` | 
| Disable service account key creation (`terraform-google-secured-data-warehouse-onprem-ingest only` ) | `disableServiceAccountKeyCreation` | true | 
| Enable OS Login for VMs created in the project (`terraform-google-secured-data-warehouse-onprem-ingest only` ) | `compute.requireOsLogin` | true | 
| Disable automatic role grants to default service account (`terraform-google-secured-data-warehouse-onprem-ingest only` ) | `automaticIamGrantsForDefaultServiceAccounts` | true | 
| Allowed ingress settings (Cloud Run functions) (`terraform-google-secured-data-warehouse-onprem-ingest only` ) | `cloudfunctions.allowedIngressSettings` | `ALLOW_INTERNAL_AND_GCLB` | 

## Security controls for external data sources

The following sections describe the controls that apply to ingesting data from external sources.

### Encrypted connection to Google Cloud

When importing data from external sources, you can use Cloud VPN or Cloud Interconnect to protect all data that flows between Google Cloud and your environment. This enterprise architecture recommends Dedicated Interconnect, because it provides a direct connection and high throughput, which are important if you're streaming a lot of data.

To permit access to Google Cloud from your environment, you must define allowlisted IP addresses in the access levels policy rules.

### Client-side encryption

Before you move your sensitive data into Google Cloud, encrypt your data locally to help protect it at rest and in transit. You can use the Tink encryption library, or you can use other encryption libraries. The Tink encryption library is compatible with BigQuery AEAD encryption, which the architecture uses to decrypt column-level encrypted data after the data is imported.

The Tink encryption library uses DEKs that you can generate locally or from Cloud HSM. To wrap or protect the DEK, you can use a KEK that is generated in Cloud HSM. The KEK is a symmetric CMEK encryption keyset that is stored securely in Cloud HSM and managed using IAM roles and permissions.

During ingestion, both the wrapped DEK and the data are stored in BigQuery. BigQuery includes two tables: one for the data and the other for the wrapped DEK. When analysts need to view confidential data, BigQuery can use AEAD decryption to unwrap the DEK with the KEK and decrypt the protected column.

Also, client-side encryption using Tink further protects your data by encrypting sensitive data columns in BigQuery. The architecture uses the following Cloud HSM encryption keys:

- A CMEK key for the ingestion process that's also used by Pub/Sub, Dataflow pipeline for streaming, Cloud Storage batch upload, and Cloud Run functions artifacts for subsequent batch uploads.
- The cryptographic key wrapped by Cloud HSM for the data encrypted on your network using Tink.
- CMEK key for the BigQuery warehouse in the Data project.

You specify the CMEK location, which determines the geographical location that the key is stored and is made available for access. You must ensure that your CMEK is in the same location as your resources. By default, the CMEK is rotated every 30 days.

If your organization's compliance obligations require that you manage your own keys externally from Google Cloud, you can enable Cloud External Key Manager. If you use external keys, you're responsible for key management activities, including key rotation.

### Dynamic data masking

To help with sharing and applying data access policies at scale, you can configure dynamic data masking. Dynamic data masking lets existing queries automatically mask column data using the following criteria:

- The masking rules that are applied to the column at query runtime.
- The roles that are assigned to the user who is running the query. To access unmasked column data, the data analyst must have the Fine-Grained Reader role.

To define access for columns in BigQuery, you create policy
tags. For
example, the taxonomy created in the standalone
example
creates the `1_Sensitive` policy tag for columns that include data that cannot
be made public, such as the credit limit. The default data masking rule is
applied to these columns to hide the value of the column.

Anything that isn't tagged is available to all users who have access to the data warehouse. These access controls ensure that, even after the data is written to BigQuery, the data in sensitive fields still cannot be read until access is explicitly granted to the user.

### Column-level encryption and decryption

Column-level encryption lets you encrypt data in BigQuery at a more granular level. Instead of encrypting an entire table, you select the columns that contain sensitive data within BigQuery, and only those columns are encrypted. BigQuery uses AEAD encryption and decryption functions that create the keysets that contain the keys for encryption and decryption. These keys are then used to encrypt and decrypt individual values in a table, and rotate keys within a keyset. Column-level encryption provides dual-access control on encrypted data in BigQuery, because the user must have permissions to both the table and the encryption key to read data in cleartext.

### Data profiler for BigQuery with Sensitive Data Protection

Data profiler lets you identify the locations of sensitive and high risk data in BigQuery tables. Data profiler automatically scans and analyzes all BigQuery tables and columns across the entire organization, including all folders and projects. Data profiler then outputs metrics such as the predicted infoTypes, the assessed data risk and sensitivity levels, and metadata about your tables. Using these insights, you can make informed decisions about how you protect, share, and use your data.

## Security controls for internal data sources

The following sections describe the controls that apply to ingesting data from Google Cloud sources.

### Key management and encryption for ingestion

Both ingestion options (Cloud Storage or Pub/Sub) use Cloud HSM to manage the CMEK. You use the CMEK keys to help protect your data during ingestion. Sensitive Data Protection further protects your data by encrypting confidential data, using the detectors that you configure.

To ingest data, you use the following encryption keys:

- A CMEK key for the ingestion process that's also used by the Dataflow pipeline and the Pub/Sub service.
- The cryptographic key wrapped by Cloud HSM for the data de-identification process using Sensitive Data Protection.
- Two CMEK keys, one for the BigQuery warehouse in the non-confidential data project, and the other for the warehouse in the confidential data project. For more information, see Key management.

You specify the CMEK location, which determines the geographical location that the key is stored and is made available for access. You must ensure that your CMEK is in the same location as your resources. By default, the CMEK is rotated every 30 days.

If your organization's compliance obligations require that you manage your own keys externally from Google Cloud, you can enable Cloud EKM. If you use external keys, you are responsible for key management activities, including key rotation.

### Data de-identification

You use Sensitive Data Protection to de-identify your structured and
unstructured data during the ingestion phase. For structured data, you use
record
transformations
based on fields to de-identify data. For an example of this approach, see the
`/examples/de_identification_template/`
folder. This example checks structured data for any credit card numbers and card
PINs. For unstructured data, you use information
types
to de-identify data.

To de-identify data that is tagged as confidential, you use Sensitive Data Protection and a Dataflow pipeline to tokenize it. This pipeline takes data from Cloud Storage, processes it, and then sends it to the BigQuery data warehouse.

For more information about the data de-identification process, see data governance.

### Column-level access controls

To help protect confidential data, you use access controls for specific columns in the BigQuery warehouse. In order to access the data in these columns, a data analyst must have the Fine-Grained Reader role.

To define access for columns in BigQuery, you create policy
tags. For
example, the `taxonomy.tf` file in the
`bigquery-confidential-data` example
module creates the following tags:

- A `3_Confidential` policy tag for columns that include very sensitive
information, such as credit card numbers. Users who have access to this tag
also have access to columns that are tagged with the`2_Private` or`1_Sensitive` policy tags.
- A `2_Private` policy tag for columns that include sensitive personal
identifiable information (PII), such as a person's first name.
Users who have access to this tag also have access to columns that are tagged
with the`1_Sensitive` policy tag. Users don't have access to columns that
are tagged with the`3_Confidential` policy tag.
- A `1_Sensitive` policy tag for columns that include data that cannot be made
public, such as the credit limit. Users who have access to this tag don't
have access to columns that are tagged with the`2_Private` or`3_Confidential` policy tags.

Anything that is not tagged is available to all users who have access to the data warehouse.

These access controls ensure that, even after the data is re-identified, the data still cannot be read until access is explicitly granted to the user.

**Note**: You can use the default definitions to run the examples. For more best
practices, see Best practices for using policy tags in
BigQuery.

### Service accounts with limited roles

You must limit access to the confidential data project so that only authorized
users can view the confidential data. To do so, you create a service account
with the Service Account
User (`roles/iam.serviceAccountUser`)
role that authorized users must impersonate. Service Account
impersonation
helps users to use service accounts without downloading the service account
keys, which improves the overall security of your project. Impersonation creates
a short-term token that authorized users who have the Service Account Token
Creator (`roles/iam.serviceAccountTokenCreator`)
role are allowed to download.

### Key management and encryption for storage and re-identification

You manage separate CMEK keys for your confidential data so that you can re-identity the data. You use Cloud HSM to protect your keys. To re-identify your data, use the following keys:

- A CMEK key that the Dataflow pipeline uses for the re-identification process.
- The original cryptographic key that Sensitive Data Protection uses to de-identify your data.
- A CMEK key for the BigQuery warehouse in the confidential data project.

As mentioned in Key management and encryption for ingestion, you can specify the CMEK location and rotation periods. You can use Cloud EKM if it is required by your organization.

## Operations

You can enable logging and Security Command Center Premium or Enterprise tier features such as Security Health Analytics and Event Threat Detection. These controls help you to do the following:

- Monitor who is accessing your data.
- Ensure that proper auditing is put in place.
- Generate findings for misconfigured cloud resources
- Support the ability of your incident management and operations teams to respond to issues that might occur.

### Access Transparency

Access Transparency provides you with real-time notification when Google personnel require access to your data. Access Transparency logs are generated whenever a human accesses content, and only Google personnel with valid business justifications (for example, a support case) can obtain access.

### Logging

To help you to meet auditing requirements and get insight into your projects,
you configure the Google Cloud Observability
with data logs for services you want to track. The `centralized-logging` module
in the repositories configures the following best practices:

- Creating an aggregated log sink across all projects.
- Storing your logs in the appropriate region.
- Adding CMEK keys to your logging sink.

For all services within the projects, your logs must include information about data reads and writes, and information about what administrators read. For additional logging best practices, see Detective controls.

### Alerts and monitoring

After you deploy the architecture, you can set up alerts to notify your security operations center (SOC) that a security incident might be occurring. For example, you can use alerts to let your security analyst know when an IAM permission has changed. For more information about configuring Security Command Center alerts, see Setting up finding notifications. For additional alerts that aren't published by Security Command Center, you can set up alerts with Cloud Monitoring.

## Additional security considerations

In addition to the security controls described in this document, you should review and manage the security and risk in key areas that overlap and interact with your use of this solution. These include the following:

- The security of the code that you use to configure, deploy, and run Dataflow jobs and Cloud Run functions.
- The data classification taxonomy that you use with this solution.
- Generation and management of encryption keys.
- The content, quality, and security of the datasets that you store and analyze in the data warehouse.
- The overall environment in which you deploy the solution, including the
following:
  - The design, segmentation, and security of networks that you connect to this solution.
  - The security and governance of your organization's IAM controls.
  - The authentication and authorization settings for the actors to whom you grant access to the infrastructure that's part of this solution, and who have access to the data that's stored and managed in that infrastructure.

## Bringing it all together

To implement the architecture described in this document, do the following:

1. Determine whether you will deploy the architecture with the enterprise foundations blueprint or on its own. If you choose not to deploy the enterprise foundations blueprint, ensure that your environment has a similar security baseline in place.
2. For importing data from external sources, set up a Dedicated Interconnect connection with your network.
3. Review the `terraform-google-secured-data-warehouse` README
or`terraform-google-secured-data-warehouse-onprem-ingest` README
and ensure that you meet all the prerequisites.
4. Verify that your user identity has the Service Account User ( `roles/iam.serviceAccountUser` )
and Service Account Token Creator
(`roles/iam.serviceAccountTokenCreator` )
roles for your organization's development folder, as described in
Organization structure. If you don't have a folder
that you use for testing, create a
folder
and configure
access.
5. Record your billing account ID, organization's display name, folder ID for your test or demo folder, and the email addresses for the following user groups: 
  - Data analysts
  - Encrypted data viewer
  - Plaintext reader
  - Data engineers
  - Network administrators
  - Security administrators
  - Security analysts
6. Create the projects. For a list of APIs that you must enable, see the README.
7. Create the service account for Terraform and assign the appropriate roles for all projects.
8. Set up the Access Control Policy.
9. For Google Cloud data sources using the `terraform-google-secured-data-warehouse` repository, in your testing
environment, deploy the
walkthrough
to see the solution in action. As part of your testing process, consider the
following:
  1. Add your own sample data into the BigQuery warehouse.
  2. Work with a data analyst in your enterprise to test their access to the confidential data and whether they can interact with the data from BigQuery in the way that they would expect.
10. For external data sources using the `terraform-google-secured-data-warehouse-onprem-ingest` repository, in your
testing environment, deploy the solution:
  1. Clone and run the Terraform scripts to set up an environment in Google Cloud.
  2. Install the Tink encryption library on your network.
  3. Set up Application Default Credentials so that you can run the Tink library on your network.
  4. Create encryption keys with Cloud KMS.
  5. Generate encrypted keysets with Tink.
  6. Encrypt data with Tink using one of the following methods: 
    - Using deterministic encryption.
    - Using a helper script with sample data.
  7. Upload encrypted data to BigQuery using streaming or batch uploads.
11. For external data sources, verify that authorized users can read unencrypted data from BigQuery using the BigQuery AEAD decrypt function. For example, run the following create decryption function: Run the create view query: ```
CREATE OR REPLACE VIEW `{project_id}.{bigquery_dataset}.decryption_view` AS
SELECT
 Card_Type_Code,
 Issuing_Bank,
 Card_Number,
 `bigquery_dataset.decrypt`(Card_Number) AS Card_Number_Decrypted
FROM `project_id.dataset.table_name`
```
Run the select query from view: ```
SELECT
  Card_Type_Code,
  Issuing_Bank,
  Card_Number,
  Card_Number_Decrypted
FROM
`{project_id}.{bigquery_dataset}.decrypted_view`
```
For additional queries and use cases, see Column-level encryption with Cloud KMS.
12. Use Security Command Center to scan the newly created projects against your compliance requirements.
13. Deploy the architecture into your production environment.

## What's next

- Review the enterprise foundations blueprint for a baseline secure environment.
- To see the details of the architecture, read the Terraform configuration
README
for internal data sources (`terraform-google-secured-data-warehouse` repository) or read the Terraform configuration
README
for external data sources (`terraform-google-secured-data-warehouse-onprem-ingest` repository).


====================================================================================================
ARTIGO 3
Link de Origem: https://docs.cloud.google.com/architecture/data-mesh
====================================================================================================

A data mesh is an architectural and organizational framework which treats data
as a product (referred to in this document as *data products*). In this
framework, data products are developed by the teams that best understand that
data, and who follow an organization-wide set of data governance standards. Once
data products are deployed to the data mesh, distributed teams in an organization
can discover and access data that's relevant to their needs more quickly and
efficiently. To achieve such a well-functioning data mesh, you must first establish
the high-level architectural components and organizational roles that this document
describes.

This document is part of a series which describes how to implement a data mesh on Google Cloud. It assumes that you have read and are familiar with the concepts described in Build a modern, distributed Data Mesh with Google Cloud.

The series has the following parts:

- Architecture and functions in a data mesh (this document)
- Design a self-service data platform for a data mesh
- Build data products in a data mesh
- Discover and consume data products in a data mesh

In this series, the data mesh that's described is internal to an organization. Although it's possible to extend a data mesh architecture to provide data products to third-parties, this extended approach is outside the scope of this document. Extending a data mesh involves additional considerations beyond just the usage within an organization.

## Architecture

The following key terms are used to define the architectural components which are described in this series:

- **Data product:** A data product is a logical container or grouping of
one or more related data resources.
- **Data resource:** A data resource is a physical asset in a storage
system which holds structured data or stores a query that yields structured
data.
- **Data attribute:** A data attribute is a field or element of a data
resource.

The following diagram provides an overview of the key architectural components in a data mesh implemented on Google Cloud.

The preceding diagram shows the following:

- Central services enable the creation and management of data products, including organizational policies that affect the data mesh participants, access controls (through Identity and Access Management groups), and the infrastructure-specific artifacts. Examples of such commitments and reservations, and infrastructure that facilitates the functioning of the data mesh are described in Create platform components and solutions.
- Central services primarily supply the Data Catalog for all the data products in the data mesh and the discovery mechanism for potential customers of these products.
- Data domains expose subsets of their data as data products through well-defined data consumption interfaces. These data products could be a table, view, structured file, topic, or stream. In BigQuery, it would be a dataset, and in Cloud Storage, it would be a folder or bucket. There can be different types of interfaces that can be exposed as a data product. An example of an interface is a BigQuery view over a BigQuery table. The types of interfaces most commonly used for analytical purposes are discussed in Build data products in a data mesh.

### Data mesh reference implementation

You can find a reference implementation of this architecture in
the `data-mesh-demo` repository.
The Terraform scripts that are used in the reference implementation demonstrate
data mesh concepts and are not intended for production use. By running these
scripts, you'll learn how to do the following:

- Separate product definitions from the underlying data.
- Create Data Catalog templates for describing product interfaces.
- Tag product interfaces with these templates.
- Grant permissions to the product consumers.

For the product interfaces, the reference implementation creates and uses the following interface types:

- Authorized views over BigQuery tables.
- Data streams based on Pub/Sub topics.

For further details, refer to the README file in the repository.

## Functions in a data mesh

For a data mesh to operate well, you must define clear roles for the people who perform tasks within the data mesh. Ownership is assigned to team archetypes, or functions. These functions hold the core user journeys for people who work in the data mesh. To clearly describe user journeys, they have been assigned to user roles. These user roles can be split and combined based on the circumstances of each enterprise. You don't need to map the roles directly with employees or teams in your organization.

A data domain is aligned with a business unit (BU), or a function within an
enterprise. Common examples of business domains might be the mortgage
department in a bank, or the customer, distribution, finance, or HR departments
of an enterprise. Conceptually, there are two domain-related functions in a data
mesh: the *data producer* teams and the *data consumer* teams. It's important to
understand that a single data domain is likely to serve both functions at once.
A data domain team *produces* data products from data that it owns. The team
also *consumes* data products for business insight, and to produce derived-data
products for the use of other domains.

In addition to the domain-based functions, a data mesh also has a set of functions that are performed by centralized teams within the organization. These central teams enable the operation of the data mesh by providing cross-domain oversight, services, and governance. They reduce the operational burden for data domains in producing and consuming data products, and facilitate the cross-domain relationships that are required for the data mesh to operate.

This document only describes functions that have a data mesh-specific role. There are several other roles that are required in any enterprise, regardless of the architecture being employed for the platform. However, these other roles are out of scope for this document.

The four main functions in a data mesh are as follows:

- **Data domain-based producer teams:** Create and maintain data products over their lifecycle. These teams are
often referred to as the**data producers** .
- **Data domain-based consumer teams:** Discover data products and use them in various analytic applications. These
teams might consume data products to create new data products. These teams
are often referred to as the**data consumers** .
- **Central data governance team:** Defines and enforces data governance policies among data producers,
ensuring high data quality and data trustworthiness for consumers. This
team is often referred to as the**data governance team** .
- **Central self-service data infrastructure platform team:** Provides a self-service data platform for data producers. This team also
provides the tooling for central data discovery and data product
observability that both data consumers and data producers use. This team is
often referred to as the**data platform team** .

An optional extra function to consider is that of a Center of Excellence (COE) for the data mesh. The purpose of the COE is to provide management of the data mesh. The COE is also the designated arbitration team that resolves any conflicts raised by any of the other functions. This function is useful for helping to connect the other four functions.

### Data domain-based producer team

Typically, data products are built on top of a physical repository of data (either single or multiple data warehouses, lakes, or streams). An organization needs traditional data platform roles to create and maintain these physical repositories. However, these traditional data platform roles are not typically the people who create the data product.

To create data products from these physical repositories, an organization needs a mix of data practitioners, such as data engineers and data architects. The following table lists all the domain-specific user roles that are needed in data producer teams.

| **Role** | **Responsibilities** | **Required skills** | **Desired outcomes** | 
|---|---|---|---|
| Data product owner |    | Data analytics Data architecture Product management |   | 
| Data product technical lead |      | Data engineering Data architecture Software engineering |    | 
| Data product support |   | Software engineering Site reliability engineering (SRE) |   | 
| Subject matter expert (SME) for data domain |   | Data analytics Data architecture |     | 
| Data owner |     |    |    | 

### Data domain-based consumer teams

In a data mesh, the people that consume a data product are typically data users who are outside of the data product domain. These data consumers use a central data catalog to find data products that are relevant to their needs. Because it's possible that more than one data product might meet their needs, data consumers can end up subscribing to multiple data products.

If data consumers are unable to find the required data product for their use case, it's their responsibility to consult directly with the data mesh COE. During that consultation, data consumers can raise their data needs and seek advice on how to get those needs met by one or more domains.

When looking for a data product, data consumers are looking for data that help them achieve various use cases such as persistent analytics dashboards and reports, individual performance reports, and other business performance metrics. Alternatively, data consumers might be looking for data products that can be used in artificial intelligence (AI) and machine learning (ML) use cases. To achieve these various use cases, data consumers require a mix of data practitioner personas, which are as follows:

| **Role** | **Responsibilities** | **Required skills** | **Desired outcomes** | 
|---|---|---|---|
| Data analyst | Searches for, identifies, evaluates, and subscribes to single-domain or cross-domain data products to create a foundation for business intelligence frameworks to operate. | Analytics engineering Business analytics |    | 
| Application developer | Develops an application framework for consumption of data across one or more data products, either inside or outside of the domain. | Application development Data engineering |   | 
| Data visualization specialist |       | Requirement analysis Data visualization |   | 
| Data scientist |     | ML engineering Analytics engineering |   | 

### Central data governance team

The data governance team enables data producers and consumers to safely share, aggregate, and compute data in a self-service manner, without introducing compliance risks to the organization.

To meet the compliance requirements of the organization, the data governance team is a mix of data practitioner personas, which are as follows:

| **Role** | **Responsibilities** | **Required skills** | **Desired outcomes** | 
|---|---|---|---|
| Data governance specialist |       | Legal SME Security SME Data privacy SME |    | 
| Data steward (sits within each domain) |      | Data architecture Data stewardship |   | 
| Data governance engineer |    | Software engineering |    | 

### Central self-service data infrastructure platform team

The self-service data infrastructure platform team, or just the data platform team, is responsible for creating a set of data infrastructure components. Distributed data domain teams use these components to build and deploy their data products. The data platform team also promotes best practices and introduces tools and methodologies which help to reduce cognitive load for distributed teams when adopting new technology.

Platform infrastructure should provide easy integration with operations toolings for global observability, instrumentation, and compliance automation. Alternatively, the infrastructure should facilitate such integration to set up distributed teams for success.

The data platform team has a shared responsibility model that it uses with the distributed domain teams and the underlying infrastructure team. The model shows what responsibilities are expected from the consumers of the platform, and what platform components the data platform team supports.

As the data platform is itself an internal product, the platform doesn't support every use case. Instead, the data platform team continuously releases new services and features according to a prioritized roadmap.

The data platform team might have a standard set of components in place and in development. However, data domain teams might choose to use a different, unique set of components if the needs of a team don't align with those provided by the data platform. If data domain teams choose a different approach, they must ensure that any platform infrastructure that they build and maintain complies with organization-wide policies and guardrails for security and data governance. For data platform infrastructure that is developed outside of the central data platform team, the data platform team might either choose to co-invest or embed their own engineers into the domain teams. Whether the data platform team chooses to co-invest or embed engineers might depend on the strategic importance of the data domain platform infrastructure to the organization. By staying involved in the development of infrastructure by data domain teams, organizations can provide the alignment and technical expertise required to repackage any new platform infrastructure components that are in development for future reuse.

You might need to limit autonomy in the early stages of building a data mesh if your initial goal is to get approval from stakeholders for scaling up the data mesh. However, limiting autonomy risks creating a bottleneck at the central data platform team. This bottleneck can inhibit the data mesh from scaling. So, any centralization decisions should be taken carefully. For data producers, making their technical choices from a limited set of available options might be preferable to evaluating and choosing from an unlimited list of options themselves. Promoting autonomy of data producers doesn't equate to creating an ungoverned technology landscape. Instead, the goal is to drive compliance and platform adoption by striking the right balance between freedom of choice and standardization.

Finally, a good data platform team is a central source of education and best practices for the rest of the company. Some of the most impactful activities that we recommend central data platform teams undertake are as follows:

- Fostering regular architectural design reviews for new functional projects and proposing common ways of development across development teams.
- Sharing knowledge and experiences, and collectively defining best practices and architectural guidelines.
- Ensuring engineers have the right tools in place to validate and check for common pitfalls like issues with code, bugs, and performance degradations.
- Organizing internal hackathons so development teams can surface their requirements for internal tooling needs.

Example roles and responsibilities for the central data platform team might include the following:

| **Role** | **Responsibilities** | **Required skills** | **Desired outcomes** | 
|---|---|---|---|
| Data platform product owner |   | Data strategy and operations Product management Stakeholder management |      | 
| Data platform engineer |   | Data engineering Software engineering |       | 
| Platform and security engineer (a representative from the central IT teams such as networking and security, who is embedded in the data platform team) |   | Infrastructure engineering Software engineering |       | 
| Enterprise architect |   | Data architecture Solution iteration and problem solving Consensus building |   | 

## Additional considerations for a data mesh

There are multiple architectural options for an analytics data platform, each option with different prerequisites. To enable each data mesh architecture, we recommend that your organization follow the best practices described in this section.

### Acquire platform funding

As explained in the blog post, "If you want to transform start with finance", the platform is never finished: it's always operating based on a prioritized roadmap. Therefore, the platform must be funded as a product, not as a project with a fixed endpoint.

The first adopter of the data mesh bears the cost. Usually, the cost is shared between the business that forms the first data domain to initiate the data mesh, and the central technology team, which generally houses the central data platform team.

To convince finance teams to approve funding for the central platform, we recommend that you make a business case for the value of the centralized platform being realized over time. That value comes from reimplementing the same components in individual delivery teams.

### Define the minimum viable platform for the data mesh

To help you to define the minimum viable platform for the data mesh, we recommend that you pilot and iterate with one or more business cases. For your pilot, find use cases that are needed, and where there's a consumer ready to adopt the resulting data product. The use cases should already have funding to develop the data products, but there should be a need for input from technical teams.

Make sure the team that is implementing the pilot understands the data mesh operating model as follows:

- The business (that is, the data producer team) owns the backlog, support, and maintenance.
- The central team defines the self-service patterns and helps the business build the data product, but passes the data product to the business to run and own when it's complete.
- The primary goal is to prove the business operating model (domains produce, domains consume). The secondary goal is to prove the technical operating model (self-service patterns developed by the central team).
- Because platform team resources are limited, use the trunk and branch teams model to pool knowledge but still allow for the development of specialized platform services and products.

We also recommend that you do the following:

- Plan roadmaps rather than letting services and features evolve organically.
- Define minimum viable platform capabilities spanning ingest, storage, processing, analysis, and ML.
- Embed data governance in every step, not as a separate workstream.
- Put in place the minimum capabilities across governance, platform, value-stream, and change management. Minimum capabilities are those which meet 80% of business cases.

### Plan for the co-existence of the data mesh with an existing data platform

Many organizations that want to implement a data mesh likely already have an existing data platform, such as a data lake, data warehouse, or a combination of both. Before implementing a data mesh, these organizations must make a plan for how their existing data platform can evolve as the data mesh grows.

These organizations should consider factors such as the following:

- The data resources that are most effective on the data mesh.
- The assets that must stay within the existing data platform.
- Whether assets have to move, or whether they can be maintained on the existing platform and still participate in the data mesh.

## What's next

- To learn more about designing and operating a cloud topology, see the Google Cloud Well-Architected Framework.
- For more reference architectures, diagrams, and best practices, explore the Cloud Architecture Center.


====================================================================================================
ARTIGO 4
Link de Origem: https://docs.cloud.google.com/architecture/design-self-service-data-platform-data-mesh
====================================================================================================

In a data mesh, a self-service data platform enables users to generate value from data by enabling them to autonomously build, share, and use data products. To fully realize these benefits, we recommend that your self-service data platform provide the capabilities described in this document.

This document is part of a series which describes how to implement a data mesh on Google Cloud. It assumes that you have read and are familiar with the concepts described in Build a modern, distributed Data Mesh with Google Cloud and Architecture and functions in a data mesh.

The series has the following parts:

- Architecture and functions in a data mesh
- Design a self-service data platform for a data mesh (this document)
- Build data products in a data mesh
- Discover and consume data products in a data mesh

Data platform teams typically create central self-service data platforms, as described in this document. This team builds the solutions and components that domain teams (both data producers and data consumers) can use to both create and consume data products. Domain teams represent functional parts of a data mesh. By building these components, the data platform team enables a smooth development experience and reduces the complexity of building, deploying, and maintaining data products that are secure and interoperable.

Ultimately, the data platform team should allow domain teams to move faster. They help increase the efficiency of domain teams by providing those teams with a limited set of tools that address their needs. In providing these tools, the data platform team removes the burden of having the domain team build and source these tools themselves. The tooling choices should be customizable to different needs and not force an inflexible way of working on the data domain teams.

The data platform team shouldn't focus on building custom solutions for data pipeline orchestrators or for continuous integration and continuous deployment (CI/CD) systems. Solutions such as CI/CD systems are readily available as managed cloud services, for example, Cloud Build. Using managed cloud services can reduce operational overheads for the data platform team and let them focus on the specific needs of the data domain teams as the users of the platform. With reduced operational overhead, the data platform team can focus more time on addressing the specific needs of the data domain teams.

## Architecture

The following diagram illustrates the architecture components of a self-service data platform. The diagram also shows how these components can support teams as they develop and consume data products across the data mesh.

As shown in the preceding diagram, the self-service data platform provides the following:

- **Platform solutions:** These solutions consist of composable
components for provisioning Google Cloud projects and resources, which users
select and assemble in different combinations to meet their specific
requirements. Instead of directly interacting with the components, users of
the platform can interact with platform solutions to help them to achieve a
specific goal. Data domain teams should design platform solutions to solve common
pain-points and friction areas that cause slowdowns in data product
development and consumption. For example, data domain teams onboarding onto
the data mesh can use an
infrastructure-as-code (IaC) 
template. Using IaC templates lets them quickly create a set of
Google Cloud projects with standard Identity and Access Management (IAM)
permissions, networking, security policies, and relevant Google Cloud
APIs enabled for data product development. We recommend that each solution is
accompanied with documentation such as "how to get started" guidance and code
samples. Data platform solutions and their components must be secure and
compliant by default.
- **Common services:** These services provide data product
discoverability, management, sharing, and observability. These services
facilitate data consumers' trust in data products, and are an effective way
for data producers to alert data consumers to issues with their data products.

Data platform solutions and common services might include the following:

- IaC templates to set up foundational data product development workspace
environments, which include the following:
  - IAM
  - Logging and monitoring
  - Networking
  - Security and compliance guardrails
  - Resource tagging for billing attribution
  - Data product storage, transformation, and publishing
  - Data product registration, cataloging, and metadata tagging
- IaC templates which follow organizational security guardrails and best practices that can be used to deploy Google Cloud resources into existing data product development workspaces.
- Application and data pipeline templates that can be used to bootstrap
new projects or used as reference for existing projects. Examples of such
templates include the following:
  - Usage of common libraries and frameworks
  - Integration with platform logging, monitoring, and observability tooling
  - Build and test tooling
  - Configuration management
  - Packaging and CI/CD pipelines for deployment
  - Authentication, deployment, and management of credentials
- Common services to provide data product observability and governance
which can include the following:
  - Uptime checks to show the overall state of data products.
  - Custom metrics to give helpful indicators about data products.
  - Operational support by the central team such that data consumer teams are alerted of changes in data products they use.
  - Product scorecards to show how data products are performing.
  - A metadata catalog for discovering data products.
  - A centrally defined set of computational policies that can be applied globally across the data mesh.
  - A data marketplace to facilitate data sharing across domain teams.

Create platform components and solutions using IaC templates discusses the advantages of IaC templates to expose and deploy data products. Provide common services discusses why it's helpful to provide domain teams with common infrastructure components that have been built and are managed by the data platform team.

## Create platform components and solutions using IaC templates

The goal of data platform teams is to set up self-service data platforms to get more value from data. To build these platforms, they create and provide domain teams with vetted, secure, and self-serviceable infrastructure templates. Domain teams use these templates to deploy their data development and data consumption environments. IaC templates help data platform teams achieve that goal and enable scale. Using vetted and trusted IaC templates simplifies the resource deployment process for domain teams by allowing those teams to reuse existing CI/CD pipelines. This approach lets domain teams quickly get started and become productive within the data mesh.

IaC templates can be created using an IaC tool. Although there are multiple IaC
tools, including
Cloud Config Connector,
Pulumi,
Chef,
and
Ansible,
this document provides examples for
Terraform-based
IaC tools. Terraform is an open source IaC tool that allows the data platform
team to efficiently create composable platform components and solutions for
Google Cloud resources. Using Terraform, the data platform team writes
code that specifies the chosen end-state and lets the tool figure out how to
achieve that state. This declarative approach lets the data platform team treat
infrastructure resources as immutable artifacts for deployment across
environments. It also helps to reduce the risk of inconsistencies arising
between deployed resources and the declared code in source control (referred to
as *configuration drift*). Configuration drift caused by ad hoc and manual
changes to infrastructure hinders safe and repeatable deployment of IaC
components into production environments.

Common IaC templates for composable platform components include using Terraform modules for deploying resources such as a BigQuery dataset, Cloud Storage bucket, or Cloud SQL database. Terraform modules can be combined into end-to-end solutions for deploying complete Google Cloud projects, including relevant resources deployed using the composable modules. Example Terraform modules can be found in the Terraform blueprints for Google Cloud.

Each Terraform module should by default satisfy security guardrails and compliance policies that your organization uses. These guardrails and policies can also be expressed as code and be automated using automated compliance verification tooling such as Google Cloud policy validation tool.

Your organization should continuously test the platform-provided Terraform modules, using the same automated compliance guardrails that it uses to promote changes into production.

To make IaC components and solutions discoverable and consumable for domain teams that have minimal experience with Terraform, we recommend that you use services such as Service Catalog. Users who have significant customization requirements should be allowed to create their own deployment solutions from the same composable Terraform templates used by existing solutions.

When using Terraform, we recommend that you follow the Google Cloud best-practices as outlined in Best practices for using Terraform.

To illustrate how Terraform can be used to create platform components, the following sections discuss examples of how Terraform can be used to expose consumption interfaces and to consume a data product.

### Expose a consumption interface

A consumption interface for a data product is a set of guarantees on the data quality and operational parameters provided by the data domain team to enable other teams to discover and use their data products. Each consumption interface also includes a product support model and product documentation. A data product may have different types of consumption interfaces, such as APIs or streams, as described in Build data products in a data mesh. The most common consumption interface might be a BigQuery authorized dataset, authorized view, or authorized function. This interface exposes a read-only virtual table, which is expressed as a query into the data mesh. The interface does not grant reader permissions to directly access the underlying data.

Google provides an example
Terraform module for creating authorized views 
without granting teams permissions to the underlying authorized datasets. The
following code from this Terraform module grants these IAM
permissions on the `dataset_id` authorized view:

```
module "add_authorization" {
  source = "terraform-google-modules/bigquery/google//modules/authorization"
  version = "~> 4.1"
  dataset_id = module.dataset.bigquery_dataset.dataset_id
  project_id = module.dataset.bigquery_dataset.project
  roles = [
    {
      role           = "roles/bigquery.dataEditor"
      group_by_email = "ops@mycompany.com"
    }
  ]
  authorized_views = [
    {
      project_id = "view_project"
      dataset_id = "view_dataset"
      table_id   = "view_id"
    }
  ]
  authorized_datasets = [
    {
      project_id = "auth_dataset_project"
      dataset_id = "auth_dataset"
    }
  ]
}
```
If you need to grant users access to multiple views, granting access to each authorized view can be both time consuming and harder to maintain. Instead of creating multiple authorized views, you can use an authorized dataset to automatically authorize any views created in the authorized dataset.

### Consume a data product

For most analytics use cases, consumption patterns are determined by the application that the data is being used in. The main use of a centrally provided consumption environment is for data exploration before the data is used within the consuming application. As discussed in Discover and consume products in a data mesh, SQL is the most commonly used method for querying data products. For this reason, the data platform should provide data consumers with a SQL application for exploration of the data.

Depending on the analytics use case, you may be able to use Terraform to deploy the consumption environment for data consumers. For example, data science is a common use case for data consumers. You can use Terraform to deploy Gemini Enterprise Agent Platform user-managed notebooks to be used as a data science development environment. From the data science notebooks, data consumers can use their credentials to sign in to the data mesh to explore data to which they have access and develop ML models based on this data.

To learn how to use Terraform to deploy and help to secure a notebook environment on Google Cloud, see Build and deploy generative AI and machine learning models in an enterprise.

## Provide common services

In addition to self-service IaC components and solutions, the data platform team might also take ownership over building and operating common shared platform services used by multiple data domain teams. Common examples of shared platform services include self-hosted third-party software such as business intelligence visualization tools or a Kafka cluster. In Google Cloud, the data platform team might choose to manage resources such as Knowledge Catalog and Cloud Logging sinks on behalf of data domain teams. Managing resources for the data domain teams lets the data platform team facilitate centralized policy management and auditing across the organization.

The following sections show how to use Knowledge Catalog for central management and governance within a data mesh on Google Cloud, and the implementation of data observability features in a data mesh.

### Knowledge Catalog for data governance

Knowledge Catalog provides a data management platform that helps you to build independent data domains within a data mesh that spans the organization. Knowledge Catalog lets you maintain central controls for governing and monitoring the data across domains.

With Knowledge Catalog an organization can logically organize their data (supported data sources) and related artifacts such as code, notebooks, and logs, into a Knowledge Catalog lake that represents a data domain. In the following diagram, a sales domain uses Knowledge Catalog to organize its assets, including data quality metrics and logs, into Knowledge Catalog zones.

As shown in the preceding diagram, Knowledge Catalog can be used to manage domain data across the following assets:

- Knowledge Catalog allows data domain teams to consistently manage their data assets in a logical group called a Knowledge Catalog lake. The data domain team can organize their Knowledge Catalog assets within the same Knowledge Catalog lake without physically moving data or storing it into a single storage system. Knowledge Catalog assets can refer to Cloud Storage buckets and BigQuery datasets stored in multiple Google Cloud projects other than the Google Cloud project containing the Knowledge Catalog lake. Knowledge Catalog assets can be structured or unstructured, or be stored in an analytical data lake or data warehouse. In the diagram, there are data lakes for the sales domain, supply chain domain, and product domain.
- Knowledge Catalog zones enable the data domain team to further organize data assets into smaller subgroups within the same Knowledge Catalog lake and add structures that capture key aspects of the subgroup. For example, Knowledge Catalog zones can be used to group associated data assets in a data product. Grouping data assets into a single Knowledge Catalog zone allows data domain teams to manage access policies and data governance policies consistently across the zone as a single data product. In the diagram, there are data zones for offline sales, online sales, supply chain warehouses, and products.

Knowledge Catalog lakes and zones enable an organization to unify distributed data and organize it based on the business context. This arrangement forms the foundation for activities such as managing metadata, setting up governance policies, and monitoring data quality. Such activities allow the organization to manage its distributed data at scale, such as in a data mesh.

### Data observability

Each data domain should implement its own monitoring and alerting mechanisms, ideally using a standardized approach. Each domain can apply the monitoring practices described in Concepts in service monitoring, making the necessary adjustments to the data domains. Observability is a large topic, and is outside of the scope of this document. This section only addresses patterns which are useful in data mesh implementations.

For products with multiple data consumers, providing timely information to each consumer about the status of the product can become an operational burden. Basic solutions, such as manually managed email distributions, are typically prone to error. They can be helpful for notifying consumers of planned outages, upcoming product launches, and deprecations, but they don't provide real-time operational awareness.

Central services can play an important role in monitoring the health and quality of the products in the data mesh. Although not a prerequisite for a successful implementation of the data mesh, implementing observability features can improve satisfaction of the data producers and consumers, and reduce overall operational and support costs. The following diagram shows an architecture of data mesh observability based on Cloud Monitoring.

The following sections describe the components shown in the diagram, which are as follows:

- Uptime checks to show the overall state of data products.
- Custom metrics to give helpful indicators about data products.
- Operational support by the central data platform team to alert data consumers of changes in the data products that they use.
- Product scorecards and dashboards to show how data products are performing.

#### Uptime checks

Data products can create simple custom applications that implement uptime checks. These checks can serve as high-level indicators of the overall state of the product. For example, if the data product team discovers a sudden drop in data quality of its product, the team can mark that product unhealthy. Uptime checks that are close to real time are especially important to data consumers who have derived products that rely on the constant availability of the data in the upstream data product. Data producers should build their uptime checks to include checking their upstream dependencies, thus providing an accurate picture of the health of their product to their data consumers.

Data consumers can include product uptime checks into their processing. For example, a composer job that generates a report based on the data provided by a data product can, as the first step, validate whether the product is in the "running" state. We recommend that your uptime check application returns a structured payload in the message body of its HTTP response. This structured payload should indicate whether there's a problem, the root cause of the problem in human readable form, and if possible, the estimated time to restore the service. This structured payload can also provide more fine-grained information about the state of the product. For example, it can contain the health information for each of the views in the authorized dataset exposed as a product.

#### Custom metrics

Data products can have various custom metrics to measure their usefulness. Data producer teams can publish these custom metrics to their designated domain-specific Google Cloud projects. To create a unified monitoring experience across all data products, a central data mesh monitoring project can be given access to those domain-specific projects.

Each type of data product consumption interface has different metrics to measure its usefulness. Metrics can also be specific to the business domain. For example, the metrics for BigQuery tables exposed through views or through the Storage Read API can be as follows:

- The number of rows.
- Data freshness (expressed as the number of seconds before the measurement time).
- The data quality score.
- The data that's available. This metric can indicate that the data is available for querying. An alternative is to use the uptime checks mentioned earlier in this document.

These metrics can be viewed as service level indicators (SLI) for a particular product.

For data streams (implemented as Pub/Sub topics), this list can be the standard Pub/Sub metrics, which are available through topics.

#### Operational support by the central data platform team

The central data platform team can expose custom dashboards to display different levels of details to the data consumers. A simple status dashboard that lists the products in the data mesh and uptime status for those products can help answer multiple end-user requests.

The central team can also serve as a notification distribution hub to notify data consumers about various events in the data products they use. Typically, this hub is made by creating alerting policies. Centralizing this function can reduce the work that must be done by each data producer team. Creating these policies doesn't require knowledge of the data domains and should help avoid bottlenecks in data consumption.

An ideal end state for data mesh monitoring is for the data product tag template to expose the SLIs and service-level objectives (SLOs) that the product supports when the product becomes available. The central team can then automatically deploy the corresponding alerting using service monitoring with the Monitoring API.

#### Product scorecards

As part of the central governance agreement, the four functions in a data mesh can define the criteria to create scorecards for data products. These scorecards can become an objective measurement of data product performance.

Many of the variables used to calculate the scorecards are the percentage of time that data products are meeting their SLO. Useful criteria can be the percentage of uptime, average data quality scores, and percentage of products with data freshness that does not fall below a threshold. To calculate these metrics automatically using Prometheus Query Language (PromQL), the custom metrics and the results of the uptime checks from the central monitoring project should be sufficient.

## What's next

- Learn more about BigQuery.
- Read about Dataplex.
- For more reference architectures, diagrams, and best practices, explore the Cloud Architecture Center.


====================================================================================================
ARTIGO 5
Link de Origem: https://docs.cloud.google.com/architecture/discover-consume-data-products-data-mesh
====================================================================================================

We recommend that you design your data mesh to support a wide variety of use cases for data consumption. The most common data consumption use cases in an organization are described in this document. The document also discusses what information data consumers must consider when determining the right data product for their use case, and how they discover and use data products. Understanding these factors can help organizations to ensure that they have the right guidance and tooling in place to support data consumers.

This document is part of a series which describes how to implement a data mesh on Google Cloud. It assumes that you have read and are familiar with the concepts described in Architecture and functions in a data mesh and Build a modern, distributed Data Mesh with Google Cloud.

The series has the following parts:

- Architecture and functions in a data mesh
- Design a self-service data platform for a data mesh
- Build data products in a data mesh
- Discover and consume data products in a data mesh (this document)

The design of a data consumption layer, specifically, how the data domain-based consumers use data products, depends on the data consumer requirements. As a prerequisite, it's assumed that consumers have a use case in mind. It's assumed that they have identified the data that they require, and can search the central data product catalog to find it. If that data is not in the catalog or is not in the preferred state (for example, if the interface is not appropriate, or the SLAs are insufficient), the consumer must contact the data producer.

Alternatively, the consumer can contact the center of excellence (COE) for the data mesh for advice on which domain is the best suited to produce that data product. The data consumers can also ask how to make their request. If your organization is large, there should be a process to make data product requests in a self-service manner.

Data consumers use data products through the applications that they run. The type of insights required drives the choice of design of the data-consuming application. When they develop the design of the application, the data consumer also identifies their preferred use of data products in the application. They establish the confidence that they need to have in the trustworthiness and reliability of that data. The data consumers can then establish a view on the data product interfaces and SLAs that the application requires.

## Data consumption use cases

For data consumers to create data applications, sources could be one or more data products and, perhaps, the data from the data consumer's own domain. As described in Build data products in a data mesh, analytical data products could be made from data products which are based on various physical data repositories.

Although data consumption can happen within the same domain, the most common consumption patterns are those that search for the right data product, regardless of domain, as the source for the application. When the right data product exists in another domain, the consumption pattern requires you to set up the subsequent mechanism for access and usage of the data across domains. The consumption of data products created in domains other than the consuming domain is discussed in Data consumption steps.

## Architecture

The following diagram shows an example scenario in which consumers use data products through a range of interfaces, including authorized datasets and APIs.

As shown in the preceding diagram, the data producer has exposed four data product interfaces: two BigQuery authorized datasets, a BigQuery dataset exposed by the BigQuery storage read API, and data access APIs hosted on Google Kubernetes Engine. In using the data products, data consumers use a range of applications that query or directly access the data resources within the data products. For this scenario, data consumers access data resources in one of two different ways based on their specific data access requirements. In the first way, Looker uses BigQuery SQL to query an authorized dataset. In the second way, Managed Service for Apache Spark directly accesses a dataset through the BigQuery API and then processes that ingested data to train a machine learning (ML) model.

The use of a data consumption application might not always result in a business intelligence (BI) report or a BI dashboard. Consumption of data from a domain can also result in ML models that further enrich analytical products, are used in data analysis, or are a part of operational processes, for example, fraud detection.

Some typical data product consumption use cases are as follows:

- **BI reporting and data analysis:** In this case, data applications are
built to consume data from multiple data products. For example, data
consumers from the customer relationship management (CRM) team need access
to data from multiple domains such as sales, customers, and finance. The
CRM application that is developed by these data consumers might need to
query both a BigQuery authorized view in one domain and
extract data from a Cloud Storage Read API in another domain.
For data consumers, the optimizing factors that influence their preferred
consumption interface are computing costs and any additional data
processing that is required after they query the data product. In BI and
data analysis use cases, BigQuery authorized views are
likely to be most commonly used.
- **Data science use cases and model training** : In this case, the data
consuming team is using the data products from other domains to enrich
their own analytical data product such as an ML model. By using
Managed Service for Apache Spark for Spark, Google Cloud provides data
pre-processing and feature engineering capabilities to enable data
enrichment before running ML tasks. The key considerations are availability
of sufficient amounts of training data at a reasonable cost, and confidence
that the training data is the appropriate data. To keep costs down, the
preferred consumption interfaces are likely to be direct read APIs. It's
possible for a data consuming team to build an ML model as a data product,
and in turn, that data consuming team also becomes a new data producing team.
- **Operator processes:** Consumption is a part of the operational process
within the data consuming domain. For example, a data consumer in a team
that deals with fraud might be using transaction data coming from
operational data sources in the merchant domain. By using a data
integration method like change data capture, this transaction data is
intercepted at near real time. You can then use Pub/Sub to define a
schema for this data and expose that information as events. In this case,
the appropriate interfaces would be data exposed as Pub/Sub topics.

## Data consumption steps

Data producers document their data product in the central catalog, including guidance on how to consume the data. For an organization with multiple domains, this documentation approach creates an architecture that's different from the traditional centrally built ELT/ETL pipeline, where processors create outputs without the boundary of business domains. Data consumers in a data mesh must have a well-designed discovery and consumption layer to create a data consumption lifecycle. The layer should include the following:

**Step 1: Discover data products through declarative search and exploration of
data product specifications:** Data consumers are free to search for any data
product that data producers have registered in the central catalog. For all data
products, the data product tag specifies how to make data access requests and
the mode to consume data from the required data product interface. The fields in
the data product tags are searchable using a search application. Data product
interfaces implement data URIs, which means data does not need to be moved to a
separate consumption zone to service consumers. In situations when real-time
data isn't needed, consumers query data products and create reports with the
results that are generated.

**Step 2: Exploring data through interactive data access and prototyping:** Data
consumers use interactive tools like BigQuery Studio and
Jupyter Notebooks to interpret and experiment with the data to refine the
queries that they need for production use. Interactive querying enables data
consumers to explore newer dimensions of data and improve the correctness of
insights generated in production scenarios.

**Step 3: Consuming data product through an application, with programmatic
access and production**:

- **BI reports.** Batch and near-real time reports and dashboards are the
most common group of analytic use cases required by data consumers. Reports
might require cross-data product access to help facilitate decision making.
For example, a customer data platform requires programmatically querying
both orders and CRM data products in a scheduled fashion. The results from
such an approach provide a holistic customer view to the business users who
consume the data.
- **AI/ML model for batch and real-time prediction.** Data scientists use
common MLOps principles to build and service ML models that consume data
products made available by the data product teams. ML models provide
real-time inference capabilities for transactional use-cases like fraud
detection. Similarly, with exploratory data analysis, data consumers can
enrich source data. For example, exploratory data analysis on sales and
marketing campaigns data shows demographic customer segments where sales
are expected to be highest and hence where campaigns should be run.

## What's next

- See a reference implementation of the data mesh architecture.
- Learn more about BigQuery.
- Read more about Gemini Enterprise Agent Platform.
- Learn about data science on Managed Service for Apache Spark.
- For more reference architectures, diagrams, and best practices, explore the Cloud Architecture Center.


====================================================================================================
ARTIGO 6
Link de Origem: https://docs.cloud.google.com/architecture/blueprints/deploy_enterprise_data_mesh
====================================================================================================

An enterprise data management and analytics platform provides an enclave where
you can store, analyze, and manipulate sensitive information while maintaining
security controls. You can use the *enterprise data mesh architecture* to deploy
a platform on Google Cloud for data management and analytics. The architecture
is designed to work in a hybrid environment, where Google Cloud components
interact with your existing on-premises components and operating processes.

The enterprise data mesh architecture includes the following:

- A GitHub
repository
that contains a set of Terraform configurations, scripts, and code to build
the following:
  - A governance project that lets you use Google's implementation of the Cloud Data Management Capabilities (CDMS) Key Controls Framework.
  - A data platform example that supports interactive and production workflows.
  - A producer environment within the data platform that supports multiple data domains. Data domains are logical groupings of data elements.
  - A consumer environment within the data platform that supports multiple consumer projects.
  - A data transfer service that uses Workload Identity Federation and the Tink encryption library to help you transfer data into Google Cloud in a secure manner.
  - A data domain example that contains ingestion, non-confidential, and confidential projects.
  - An example of a data access system that lets data consumers request access to data sets and data owners grant access to those data sets. The example also includes a workflow manager that changes the IAM permissions of those data sets accordingly.
- A guide to the architecture, design, security controls, and operational processes that you use this architecture to implement (this document).

The enterprise data mesh architecture is designed to be compatible with the enterprise foundations blueprint. The enterprise foundations blueprint provides a number of base-level services that this architecture relies on, such as VPC networks and logging. You can deploy this architecture without deploying the enterprise foundations blueprint if your Google Cloud environment provides the necessary functionality.

This document is intended for cloud architects, data scientists, data engineers, and security architects who can use the architecture to build and deploy comprehensive data services on Google Cloud. This document assumes that you are familiar with the concepts of data meshes, Google Cloud data services, and the Google Cloud implementation of the CDMC framework.

## Architecture

The enterprise data mesh architecture takes a layered approach to provide the capabilities that enable data ingestion, data processing, and governance. The architecture is intended to be deployed and controlled through a CI/CD workflow. The following diagram shows how the data layer that is deployed by this architecture relates to other layers in your environment.

This diagram includes the following:

- Google Cloud infrastructure provides security capabilities such as encryption at rest and encryption in transit, as well as basic building blocks such as compute and storage.
- The enterprise foundation provides a baseline of resources such as identity, networking, logging, monitoring, and deployment systems that enable you to adopt Google Cloud for your data workloads.
- The data layer provides various capabilities such as data ingestion, data storage, data access control, data governance, data monitoring, and data sharing.
- The application layer represents various different applications that use the data layer assets.
- CI/CD provides the tools to automate the provision, configuration, management, and deployment of infrastructure, workflows, and software components. These components help you ensure consistent, reliable, and auditable deployments; minimize manual errors; and accelerate the overall development cycle.

To show how the data environment is used, the architecture includes a sample data workflow. The sample data workflow takes you through the following processes: data governance, data ingestion, data processing, data sharing, and data consumption.

### Key architectural decisions

The following table summarizes the high-level decisions of the architecture.

| Decision area | Decision | 
|---|---|
| **Google Cloud architecture** |  | 
| Resource hierarchy | The architecture uses the resource hierarchy from the enterprise foundations blueprint. | 
| Networking | The architecture includes an example data transfer service that uses Workload Identity Federation and a Tink library. | 
| Roles and IAM permissions | The architecture includes segmented data producer roles, data consumer roles, data governance roles, and data platform roles. | 
| **Common data services** |  | 
| Metadata | The architecture uses Data Catalog to manage data metadata. | 
| Central policy management | To manage policies, the architecture uses Google Cloud's implementation of the CDMC framework. | 
| Data access management | To control access to data, the architecture includes an independent process that requires data consumers to request access to data assets from the data owner. | 
| Data quality | The architecture uses the Cloud Data Quality Engine to define and run data quality rules on specified table columns, measuring data quality based on metrics like correctness and completeness. | 
| Data security | The architecture uses tagging, encryption, masking, tokenization, and IAM controls to provide data security. | 
| **Data domain** |  | 
| Data environments | The architecture includes three environments. Two environments (non-production and production) are operational environments that are driven by pipelines. One environment (development) is an interactive environment. | 
| Data owners | Data owners ingest, process, expose, and grant access to data assets. | 
| Data consumers | Data consumers request access to data assets. | 
| **Onboarding and operations** |  | 
| Pipelines | The architecture uses the following pipelines to deploy resources:  | 
| Repositories | Each pipeline uses a separate repository to enable segregation of responsibility. | 
| Process flow | The process requires that changes to the production environment include a submitter and an approver. | 
| **Cloud operations** |  | 
| Data product scorecards | The Report Engine generates data product scorecards. | 
| Cloud Logging | The architecture uses the logging infrastructure from the enterprise foundations blueprint. | 
| Cloud Monitoring | The architecture uses the monitoring infrastructure from the enterprise foundations blueprint. | 

### Identity: Mapping roles to groups

The data mesh leverages the enterprise foundations blueprint's existing identity lifecycle management, authorization, and authentication architecture. Users are not assigned roles directly; instead groups are the primary method of assigning roles and permission in IAM. IAM roles and permissions are assigned during project creation through the foundation pipeline.

The data mesh associates groups with one of four key areas: infrastructure, data governance, domain-based data producers, and domain-based consumers.

The permission scopes for these groups are the following:

- The infrastructure group's permission scope is the data mesh as a whole.
- The data governance groups' permission scope is the data governance project.
- Domain-based producers and consumers permissions are scoped to their data domain.

The following tables show the various roles used in this data mesh implementation and their associated permissions.

#### Infrastructure

| Group | Description | Roles | 
|---|---|---|
| `data-mesh-ops@example.com` | Overall administrators of the data mesh | `roles/owner` (data platform) | 

#### Data governance

| Group | Description | Roles | 
|---|---|---|
| `gcp-dm-governance-admins@example.com` | Administrators of the data governance project | `roles/owner` on the data governance project | 
| `gcp-dm-governance-developers@example.com` | Developers who build and maintain the data governance components | Multiple roles on the data governance project, including `roles/viewer` , BigQuery roles, and Data Catalog roles | 
| `gcp-dm-governance-data-readers@example.com` | Readers of data governance information | `roles/viewer` | 
| `gcp-dm-governance-security-administrator@example.com` | Security administrators of the governance project | `roles/orgpolicy.policyAdmin` and`roles/iam.securityReviewer` | 
| `gcp-dm-governance-tag-template-users@example.com` | Group with permission to use tag templates | `roles/datacatalog.tagTemplateUser` | 
| `gcp-dm-governance-tag-users@example.com` | Group with permission to use tag templates and add tags | `roles/datacatalog.tagTemplateUser` and`roles/datacatalog.tagEditor` | 
| `gcp-dm-governance-scc-notifications@example.com` | Service account group for Security Command Center notifications | None. This is a group for membership, and a service account is created with this name, which has the necessary permissions. | 

#### Domain-based data producers

| Group | Description | Roles | 
|---|---|---|
| `gcp-dm-``{data_domain_name}` -admins@example.com | Administrators of a specific data domain | `roles/owner` on the data domain project | 
| `gcp-dm-``{data_domain_name}` -developers@example.com | Developers who build and maintain data products within a data domain | Multiple roles on the data domain project, including `roles/viewer` , BigQuery roles, and Cloud Storage roles | 
| `gcp-dm-``{data_domain_name}` -data-readers@example.com | Readers of the data domain information | `roles/viewer` | 
| `gcp-dm-``{data_domain_name}` -metadata-editors@`{var.domain}` | Editors of Data Catalog entries | Roles to edit Data Catalog entries | 
| `gcp-dm-``{data_domain_name}` -data-stewards@example.com | Data stewards for the data domain | Roles to manage metadata and data governance aspects | 

#### Domain-based data consumers

| Group | Description | Roles | 
|---|---|---|
| `gcp-dm-consumer-``{project_name}` -admins@example.com | Administrators of a specific consumer project | `roles/owner` on consumer project | 
| `gcp-dm-consumer-``{project_name}` -developers@example.com | Developers working within a consumer project | Multiple roles on the consumer project, including `roles/viewer` and BigQuery roles | 
| `gcp-dm-consumer-``{project_name}` -data-readers@example.com | Readers of the consumer project information | `roles/viewer` | 

## Organization structure

To differentiate between production operations and production data, the architecture uses different environments to develop and release workflows. Production operations include the governance, traceability, and repeatability of a workflow and the auditability of the results of the workflow. Production data refers to possibly sensitive data that you need to run your organization. All environments are designed to have security controls that let you ingest and operate your data.

To help data scientists and engineers, the architecture includes an interactive environment, where developers can work with the environment directly and add services through a curated catalog of solutions. Operational environments are driven through pipelines which have codified architecture and configuration.

This architecture uses the organizational structure of the enterprise foundations blueprint as a basis for deploying data workloads. The following diagram shows the top-level folders and projects used in the enterprise data mesh architecture.

The following table describes the top-level folders and projects that are part of the architecture.

| Folder | Component | Description | 
|---|---|---|
| `common` | `prj-c-artifact-pipeline` | Contains the deployment pipeline that's used to build out the code artifacts of the architecture. | 
|  | `prj-c-service-catalog` | Contains the infrastructure used by the Service Catalog to deploy resources in the interactive environment. | 
|  | `prj-c-datagovernance` | Contains all the resources used by Google Cloud's implementation of the CDMC framework. | 
| `development` | `fldr-d-dataplatform` | Contains the projects and resources of the data platform for developing use cases in interactive mode. | 
| `non-production` | `fldr-n-dataplatform` | Contains the projects and resources of the data platform for testing use cases that you want to deploy in an operational environment. | 
| `production` | `fldr-p-dataplatform` | Contains the projects and resources of the data platform for deployment into production. | 

### Data platform folder

The data platform folder contains all the data plane components and some of the CDMC resources. In addition, the data platform folder and the data governance project contain the CDMC resources. The following diagram shows the folders and projects that are deployed in the data platform folder.

Each data platform folder includes an environment folder (production, non-production, and development). The following table describes the folders within each data platform folder.

| Folders | Description | 
|---|---|
| Producers | Contains the data domains. | 
| Consumers | Contains the consumer projects. | 
| Data domain | Contains the projects associated with a particular domain. | 

### Producers folder

Each producers folder includes one or more data domains. A data domain refers to a logical grouping of data elements that share a common meaning, purpose, or business context. Data domains let you categorize and organize data assets within an organization. The following diagram shows the structure of a data domain. The architecture deploys projects in the data platform folder for each environment.

The following table describes the projects that are deployed in the data platform folder for each environment.

| Project | Description | 
|---|---|
| Ingestion | The ingestion project ingests data into the data domain. The architecture provides examples of how you can stream data into BigQuery, Cloud Storage, and Pub/Sub. The ingestion project also contains examples of Dataflow and Managed Service for Apache Airflow that you can use to orchestrate the transformation and movement of ingested data. | 
| Non-confidential | The non-confidential project contains data that has been de-identified. You can mask, containerize, encrypt, tokenize, or obfuscate data. Use policy tags to control how the data is presented. | 
| Confidential | The confidential project contains plaintext data. You can control access through IAM permissions. | 

### Consumer folder

The consumer folder contains consumer projects. Consumer projects provide a mechanism to segment data users based on their required trust boundary. Each project is assigned to a separate user group and the group is assigned access to the required data assets on a project-by-project basis. You can use the consumer project to collect, analyze, and augment the data for the group.

### Common folder

The common folder contains the services that are used by different environments and projects. This section describes the capabilities that are added to the common folder to enable the enterprise data mesh.

#### CDMC architecture

The architecture uses the CDMC architecture for data governance. The data governance functions reside in the data governance project in the common folder. The following diagram shows the components of the CDMC architecture. The numbers in the diagram represent the key controls that are addressed with Google Cloud services.

The following table describes the components of the CDMC architecture that the enterprise data mesh architecture uses.

| CDMC component | Google Cloud service | Description | 
|---|---|---|
| **Access and lifecycle components** |  |  | 
| Key management | Cloud KMS | A service that securely manages encryption keys that protect sensitive data. | 
| Record Manager | Cloud Run | An application that maintains comprehensive logs and records of data processing activities, ensuring organizations can track and audit data usage. | 
| Archiving policy | BigQuery | A BigQuery table that contains the storage policy for data. | 
| Entitlements | BigQuery | A BigQuery table that stores information about who can access sensitive data. This table ensures that only authorized users can access specific data based on their roles and privileges. | 
| **Scanning components** |  |  | 
| Data loss | Sensitive Data Protection | Service used to inspect assets for sensitive data. | 
| DLP findings | BigQuery | A BigQuery table that catalogs data classifications within the data platform. | 
| Policies | BigQuery | A BigQuery table that contains consistent data governance practices (for example, data access types). | 
| Billing export | BigQuery | A table that stores cost information that is exported from Cloud Billing to enable the analysis of cost metrics that are associated with data assets. | 
| Cloud Data Quality Engine | Cloud Run | An application that runs data quality checks for tables and columns. | 
| Data quality findings | BigQuery | A BigQuery table that records identified discrepancies between the defined data quality rules and the actual quality of the data assets. | 
| **Reporting components** |  |  | 
| Scheduler | Cloud Scheduler | A service that controls when the Cloud Data Quality Engine runs and when the Sensitive Data Protection inspection occurs. | 
| Report Engine | Cloud Run | An application that generates reports that help track and measure adherence to the CDMC framework's controls. | 
| Findings and assets | BigQuery and Pub/Sub | A BigQuery report of discrepancies or inconsistencies in data management controls, such as missing tags, incorrect classifications, or non-compliant storage locations. | 
| Tag exports | BigQuery | A BigQuery table that contains extracted tag information from Data Catalog. | 
| **Other components** |  |  | 
| Policy management | Organization Policy Service | A service that defines and enforces restrictions on where data can be stored geographically. | 
| Attribute-based access policies | Access Context Manager | A service that defines and enforces granular, attribute-based access policies so that only authorized users from permitted locations and devices can access sensitive information. | 
| Metadata | Data Catalog | A service that stores metadata information about the tables that are in use in the data mesh. | 
| Tag Engine | Cloud Run | An application that adds tags to data in BigQuery tables. | 
| CDMC reports | Data Studio | Dashboards that let your analysts view reports that were generated by the CDMC architecture engines. | 

#### CDMC implementation

The following table describes how the architecture implements the key controls in the CDMC framework.

| CDMC control requirement | Implementation | 
|---|---|
| Data control compliance | The Report Engine detects non-compliant data assets through and publishes findings to a Pub/Sub topic. These findings are also loaded into BigQuery for reporting using Data Studio. | 
| Data ownership is established for both migrated and cloud-generated data | Data Catalog automatically captures technical metadata from BigQuery. Tag Engine applies business metadata tags like owner name and sensitivity level from a reference table, which helps ensure that all sensitive data is tagged with owner information for compliance. This automated tagging process helps provide data governance and compliance by identifying and labeling sensitive data with the appropriate owner information. | 
| Data sourcing and consumption are governed and supported by automation | Data Catalog classifies data assets by tagging them with an `is_authoritative` flag when they are an authoritative source. Data Catalog automatically stores the information, along with the technical metadata, in a data register. The Report Engine and the Tag Engine can validate and report the data register of authoritative sources using Pub/Sub. | 
| Data sovereignty and cross-border data movement are managed | Organization Policy Service defines permitted storage regions for data assets and Access Context Manager restricts access based on user location. Data Catalog stores the approved storage locations as metadata tags. Report Engine compares these tags against the actual location of the data assets in BigQuery and publishes any discrepancies as findings using Pub/Sub. Security Command Center provides an additional layer of monitoring by generating vulnerability findings if data is stored or accessed outside the defined policies. | 
| Data catalogs are implemented, used, and interoperable | Data Catalog stores and updates the technical metadata for all BigQuery data assets, effectively creating a continuously synchronized Data Catalog. Data Catalog ensures that any new or modified tables and views are immediately added to the catalog, maintaining an up-to-date inventory of data assets. | 
| Data classifications are defined and used | Sensitive Data Protection inspects BigQuery data and identifies sensitive information types. These findings are then ranked based on a classification reference table, and the highest sensitivity level is assigned as a tag in Data Catalog at the column and table levels. Tag Engine manages this process by updating the Data Catalog with sensitivity tags whenever new data assets are added or existing ones are modified. This process ensures a constantly updated classification of data based on sensitivity, which you can monitor and report on using Pub/Sub and integrated reporting tools. | 
| Data entitlements are managed, enforced, and tracked | BigQuery policy tags control access to sensitive data at the column level, ensuring only authorized users can access specific data based on their assigned policy tag. IAM manages overall access to the data warehouse, while Data Catalog stores sensitivity classifications. Regular checks are performed to ensure all sensitive data has corresponding policy tags, with any discrepancies reported using Pub/Sub for remediation. | 
| Ethical access, use, and outcomes of data are managed | Data sharing agreements for both providers and consumers are stored in a dedicated BigQuery data warehouse to control consumption purposes. Data Catalog labels data assets with the provider agreement information, while consumer agreements are linked to IAM bindings for access control. Query labels enforce consumption purposes, requiring consumers to specify a valid purpose when querying sensitive data, which is validated against their entitlements in BigQuery. An audit trail in BigQuery tracks all data access and ensures compliance with the data sharing agreements. | 
| Data is secured, and controls are evidenced | Google's default encryption at rest helps protect data that is stored on disk. Cloud KMS supports customer-managed encryption keys (CMEK) for enhanced key management. BigQuery implements column-level dynamic data masking for de-identification and supports application-level de-identification during data ingestion. Data Catalog stores metadata tags for encryption and de-identification techniques that are applied to data assets. Automated checks ensure that the encryption and de-identification methods align with predefined security policies, with any discrepancies that are reported as findings using Pub/Sub. | 
| A data privacy framework is defined and operational | Data Catalog tags sensitive data assets with relevant information for impact assessment, such as subject location and assessment report links. Tag Engine applies these tags based on data sensitivity and a policy table in BigQuery, which defines the assessment requirements based on data and subject residency. This automated tagging process allows for continuous monitoring and reporting of compliance with impact assessment requirements, ensuring that data protection impact assessments (DPIAs) or protection impact assessment (PIAs) are conducted when necessary. | 
| The data lifecycle is planned and managed | Data Catalog labels data assets with retention policies, specifying retention periods and expiration actions (such as archive or purge). Record Manager automates the enforcement of these policies by purging or archiving BigQuery tables based on the defined tags. This enforcement ensures adherence to the data lifecycle policies and maintains compliance with data retention requirements, with any discrepancies detected and reported using Pub/Sub. | 
| Data quality is managed | The Cloud Data Quality Engine defines and runs data quality rules on specified table columns, measuring data quality based on metrics like correctness and completeness. Results from these checks, including success percentages and thresholds, are stored as tags in Data Catalog. Storing these results allows for continuous monitoring and reporting of data quality, with any issues or deviations from acceptable thresholds published as findings using Pub/Sub. | 
| Cost management principles are established and applied | Data Catalog stores cost-related metrics for data assets, such as query costs, storage costs, and data egress costs, which are calculated using billing information exported from Cloud Billing to BigQuery. Storing cost-related metrics allows for comprehensive cost tracking and analysis, ensuring adherence to cost policies and efficient resource utilization, with any anomalies reported using Pub/Sub. | 
| Data provenance and lineage are understood | Data Catalog's built-in data lineage features track the provenance and lineage of data assets, visually representing the flow of data. Additionally, data ingestion scripts identify and tag the original source of the data in Data Catalog, enhancing the traceability of data back to its origin. | 

## Data access management

The architecture's access to data is controlled through an independent process which separates operational control (for example, running Dataflow jobs) from data access control. A user's access to a Google Cloud service is defined by an environmental or operational concern and is provisioned and approved by a cloud engineering group. A user's access to Google Cloud data assets (for example, a BigQuery table) is a privacy, regulatory, or governance concern and is subject to an access agreement between the producing and consuming parties and controlled through the following processes. The following diagram shows how data access is provisioned through the interaction of different software components.

As shown in the previous diagram, onboarding of data accesses is handled by the following processes:

- Cloud data assets are collected and inventoried by Data Catalog.
- The workflow manager retrieves the data assets from Data Catalog.
- Data owners are onboarded to workflow manager.

The operation of the data access management is as follows:

1. A data consumer makes a request for a specific asset.
2. The data owner of the asset is alerted to the request.
3. The data owner approves or rejects the request.
4. If the request is approved, the workflow manager passes the group, asset, and associated tag to the IAM mapper.
5. The IAM mapper translates the workflow manager tags into IAM permissions, and gives the specified group IAM permissions for the data asset.
6. When a user wants to access the data asset, IAM evaluates access to the Google Cloud asset based on the permissions of the group.
7. If permitted, the user accesses the data asset.

## Networking

The data security process initiates at the source application, which might reside on-premises or in another environment external to the target Google Cloud project. Before any network transfer occurs, this application uses Workload Identity Federation to securely authenticate itself to Google Cloud APIs. Using these credentials, it interacts with Cloud KMS to obtain or wrap the necessary keys and then employs the Tink library to perform initial encryption and de-identification on the sensitive data payload according to predefined templates.

After the data payload is protected, the payload must be securely transferred into the Google Cloud ingestion project. For on-premise applications, you can use Cloud Interconnect or potentially Cloud VPN. Within the Google Cloud network, use Private Service Connect to route the data towards the ingestion endpoint within the target project's VPC network. Private Service Connect lets the source application connect to Google APIs using private IP addresses, ensuring traffic isn't exposed to the internet.

The entire network path and the target ingestion services (Cloud Storage, BigQuery, and Pub/Sub) within the ingestion project are secured by a VPC Service Controls perimeter. This perimeter enforces a security boundary, ensuring that the protected data originating from the source can only be ingested into the authorized Google Cloud services within that specific project.

## Logging

This architecture uses the Cloud Logging capabilities that are provided by the enterprise foundations blueprint.

## Pipelines

The enterprise data mesh architecture uses a series of pipelines to provision the infrastructure, orchestration, data sets, data pipelines, and application components. The architecture's resource deployment pipelines use Terraform as the infrastructure as code (IaC) tool and Cloud Build as the CI/CD service to deploy the Terraform configurations into the architecture environment. The following diagram shows the relationship between the pipelines.

The foundation pipeline and the infrastructure pipeline are part of the enterprise foundations blueprint. The following table describes the purpose of the pipelines and the resources that they provision.

| Pipeline | Provisioned by | Resources | 
|---|---|---|
| Foundation pipeline | Bootstrap |  | 
| Infrastructure pipeline | Foundation pipeline |  | 
| Service Catalog pipeline | Infrastructure pipeline |  | 
| Artifact pipelines | Infrastructure pipeline | Artifact pipelines produce the various containers and other components of the codebase used by the data mesh. | 

Each pipeline has its own set of repositories that it pulls code and configuration files from. Each repository has a separation of duties where submitters and approvals of operational code deployments are the responsibilities of different groups.

### Interactive deployment through Service Catalog

Interactive environments are the development environment within the architecture
and exist under the development folder. The main interface for the interactive
environment is Service Catalog, which lets developers use
preconfigured templates to instantiate Google services. These preconfigured
templates are known as *service templates*. Service templates help you to
enforce your security posture, such as making CMEK encryption mandatory, and
also prevents your users from having direct access to Google APIs.

The following diagram shows the components of the interactive environment and how data scientists deploy resources.

To deploy resources using the Service Catalog, the following steps occur:

1. The MLOps engineer puts a Terraform resource template for Google Cloud into a Git repository.
2. The Git Commit command triggers a Cloud Build pipeline.
3. Cloud Build copies the template and any associated configuration files to Cloud Storage.
4. The MLOps engineer sets up the Service Catalog solutions and Service Catalog manually. The engineer then shares the Service Catalog with a service project in the interactive environment.
5. The data scientist selects a resource from the Service Catalog.
6. Service Catalog deploys the template into the interactive environment.
7. The resource pulls any necessary configuration scripts.
8. The data scientist interacts with the resources.

### Artifact pipelines

The data ingestion process uses Managed Airflow and Dataflow to orchestrate the movement and transformation of data within the data domain. The artifact pipeline builds all necessary resources for data ingestion and moves the resources to the appropriate location for the services to access them. The artifact pipeline creates the container artifacts that the orchestrator uses.

## Security controls

The enterprise data mesh architecture uses a layered defense-in-depth security model that includes default Google Cloud capabilities, Google Cloud services, and security capabilities that are configured through the enterprise foundations blueprint. The following diagram shows the layering of the various security controls for the architecture.

The following table describes the security controls that are associated with the resources in each layer.

| Layer | Resource | Security control | 
|---|---|---|
| CDMC framework | Google Cloud CDMC implementation | Provides a governance framework that helps secure, manage and control your data assets. See CDMC Key Controls Framework for more information. | 
| Deployment | Infrastructure pipeline | Provides a series of pipelines that deploy infrastructure, build containers, and create data pipelines. The use of pipelines allows for auditability, traceability, and repeatability. | 
|  | Artifact pipeline | Deploys various components not deployed by the infrastructure pipeline. | 
|  | Terraform templates | Builds out the system infrastructure. | 
|  | Open Policy Agent | Helps ensure that the platform conforms to selected policies. | 
| Network | Private Service Connect | Provides data exfiltration protections around the architecture resources at the API layer and the IP layer. Lets you communicate with Google Cloud APIs using private IP addresses so that you can avoid exposing traffic to the internet. | 
|  | VPC network with private IP addresses | Helps remove exposure to internet-facing threats. | 
|  | VPC Service Controls | Helps protect sensitive resources against data exfiltration. | 
|  | Firewall | Helps protect the VPC network against unauthorized access. | 
| Access management | Access Context Manager | Controls who can access what resources and helps prevent unauthorized use of your resources. | 
|  | Workload Identity Federation | Removes the need for external credentials to transfer data onto the platform from on-premises environments. | 
|  | Data Catalog | Provides an index of assets available to users. | 
|  | IAM | Provides fine-grained access. | 
| Encryption | Cloud KMS | Lets you manage your encryption keys and secrets, and help protect your data through encryption at rest and encryption in transit. | 
|  | Secrets Manager | Provides a secret store for pipelines that are controlled by IAM. | 
|  | Encryption at rest | By default, Google Cloud encrypts data at rest. | 
|  | Encryption in transit | By default, Google Cloud encrypts data in transit. | 
| Detective | Security Command Center | Helps you to detect misconfigurations and malicious activity in your Google Cloud organization. | 
|  | Continuous architecture | Continually checks your Google Cloud organization against a series of OPA policies that you have defined. | 
|  | IAM Recommender | Analyzes user permissions and provides suggestions about reducing permissions to help enforce the principle of least privilege. | 
|  | Firewall Insights | Analyzes firewall rules, identifies overly-permissive firewall rules, and suggests more restrictive firewalls to help strengthen your overall security posture. | 
|  | Cloud Logging | Provides visibility into system activity and helps enable the detection of anomalies and malicious activity. | 
|  | Cloud Monitoring | Tracks key signals and events that can help identify suspicious activity. | 
| Preventative | Organization Policy | Lets you control and restrict actions within your Google Cloud organization. | 

## Workflows

The following sections outline the data producer workflow and data consumer workflow, ensuring appropriate access controls based on data sensitivity and user roles.

### Data producer workflow

The following diagram shows how data is protected as it is transferred to BigQuery.

The workflow for data transfer is the following:

1. An application that is integrated with Workload Identity Federation uses Cloud KMS to decrypt a wrapped encryption key.
2. The application uses the Tink library to de-identify or encrypt the data using a template.
3. The application transfers data to the ingestion project in Google Cloud.
4. The data arrives in Cloud Storage, BigQuery, or Pub/Sub.
5. In the ingestion project, the data is decrypted or re-identified using a template.
6. The decrypted data is encrypted or masked based on another de-identification template, then placed in the non-confidential project. Tags are applied by the tagging engine as appropriate.
7. Data from the non-confidential project is transferred over to the confidential project and re-identified.

The following data access is permitted:

- Users who have access to the confidential project can access all the raw plaintext data.
- Users who have access to the non-confidential project can access masked, tokenized, or encrypted data based on the tags associated with the data and their permissions.

### Data consumer workflow

The following steps describe how a consumer can access data that is stored in BigQuery.

1. The data consumer searches for data assets using Data Catalog.
2. After the consumer finds the assets that they are looking for, the data consumer requests access to the data assets.
3. The data owner decides whether to provide access to the assets.
4. If the consumer obtains access, the consumer can use a notebook and the Solution Catalog to create an environment in which they can analyze and transform the data assets.

## Bringing it all together

The GitHub repository provides you with detailed instructions on deploying the data mesh on Google Cloud after you deployed the enterprise foundation. The process to deploy the architecture involves modifying your existing infrastructure repositories and deploying new data mesh specific components.

Complete the following:

1. Complete all prerequisites, including the following:
  1. Install Google Cloud CLI, Terraform, Tink, Java, and Go.
  2. Deploy the enterprise foundations blueprint (v4.1).
  3. Maintain the following local repositories:
    - `gcp-data-mesh-foundations`
    - `gcp-bootstrap`
    - `gcp-environments`
    - `gcp-networks`
    - `gcp-org`
    - `gcp-projects`
2. Modify the existing foundation blueprint and then deploy the data mesh
applications. For each item, complete the following:
  1. In your target repository, check out the `Plan` branch.
  2. To add data mesh components, copy the relevant files and directories from
`gcp-data-mesh-foundations` into the appropriate foundation directory.
Overwrite files when required.
  3. Update the data mesh variables, roles, and settings in the Terraform
files (for
example, `*.tfvars` and`*.tf` ). Set the GitHub tokens as environment
variables.
  4. Perform the Terraform initialize, plan, and apply operations on each repository.
  5. Commit your changes, push the code to your remote repository, create pull requests and merge to your development, nonproduction, and production environments.
3. In your target repository, check out the 

## What's next

- Read about the architecture and functions in a data mesh.
- Import data from Google Cloud into a secured BigQuery data warehouse.
- Implement the CDMC key controls framework in a BigQuery data warehouse.
- Read about the enterprise foundations blueprint.


====================================================================================================
ARTIGO 7
Link de Origem: https://docs.cloud.google.com/architecture/scalable-bigquery-backup-automation
====================================================================================================

This architecture provides a framework and reference deployment to help you develop your BigQuery backup strategy. This recommended framework and its automation can help your organization do the following:

- Adhere to your organization's disaster recovery objectives.
- Recover data that was lost due to human errors.
- Comply with regulations.
- Improve operational efficiency.

The scope of BigQuery data can include (or exclude) folders, projects, datasets, and tables. This recommended architecture shows you how to automate the recurrent backup operations at scale. You can use two backup methods for each table: BigQuery snapshots and BigQuery exports to Cloud Storage.

This document is intended for cloud architects, engineers, and data governance officers who want to define and automate data policies in their organizations.

## Architecture

The following diagram shows the automated backup architecture:

 

The workflow that's shown in the preceding diagram includes the following phases:

1. Cloud Scheduler triggers a run to the dispatcher service through a Pub/Sub message, which contains the scope of the BigQuery data that's included and excluded. Runs are scheduled by using a cron expression.
2. The dispatcher service, which is built on Cloud Run, uses the BigQuery API to list the tables that are within the BigQuery scope.
3. The dispatcher service submits one request for each table to the configurator service through a Pub/Sub message.
4. The Cloud Run configurator service computes the backup policy of the table from one of the following defined options: 
  1. The table-level policy, which is defined by data owners.
  2. The fallback policy, which is defined by the data governance officer, for tables that don't have defined policies.
 For details about backup policies, see Backup policies.
5. The configurator service submits one request for each table to the next service, based on the computed backup policy.
6. Depending on the backup method, one of the following custom Cloud Run services submits a request to the BigQuery API and runs the backup process: 
  1. The service for BigQuery snapshots backs up the table as a snapshot.
  2. The service for data exports backs up the table as a data export to Cloud Storage.
7. When the backup method is a table data export, a Cloud Logging log sink listens to the export jobs completion events in order to enable the asynchronous execution of the next step.
8. After the backup services complete their operations, Pub/Sub triggers the tagger service.
9. For each table, the tagger service logs the results of the backup services and updates the backup state in the Cloud Storage metadata layer.

## Products used

This reference architecture uses the following Google Cloud products:

- BigQuery: An enterprise data warehouse that helps you manage and analyze your data with built-in features like machine learning, geospatial analysis, and business intelligence.
- Cloud Logging: A real-time log management system with storage, search, analysis, and alerting.
- Pub/Sub: An asynchronous and scalable messaging service that decouples services that produce messages from services that process those messages.
- Cloud Run: A serverless compute platform that lets you run containers directly on top of Google's scalable infrastructure.
- Cloud Storage: A low-cost, no-limit object store for diverse data types. Data can be accessed from within and outside Google Cloud, and it's replicated across locations for redundancy.
- Cloud Scheduler: A fully managed enterprise-grade cron job scheduler that lets you set up scheduled units of work to be executed at defined times or regular intervals.
- Datastore: A highly scalable NoSQL database for your web and mobile applications.

## Use cases

This section provides examples of use cases for which you can use this architecture.

### Backup automation

As an example, your company might operate in a regulated industry and use BigQuery as the main data warehouse. Even when your company follows best practices in software development, code review, and release engineering, there's still a risk of data loss or data corruption due to human errors. In a regulated industry, you need to minimize this risk as much as possible.

Examples of these human errors include the following:

- Accidental deletion of tables.
- Data corruption due to erroneous data pipeline logic.

These types of human errors can usually be resolved with the time travel feature, which lets you recover data from up to seven days ago. In addition, BigQuery also offers a fail-safe period, during which deleted data is retained in fail-safe storage for an additional seven days after the time travel window. That data is available for emergency recovery through Cloud Customer Care. However, if your company doesn't discover and fix such errors within this combined timeframe, the deleted data is no longer recoverable from its last stable state.

To mitigate this, we recommend that you execute regular backups for any BigQuery tables that can't be reconstructed from source data (for example, historical records or KPIs with evolving business logic).

Your company could use basic scripts to back up tens of tables. However, if you need to regularly back up hundreds or thousands of tables across the organization, you need a scalable automation solution that can do the following:

- Handle different Google Cloud API limits.
- Provide a standardized framework for defining backup policies.
- Provide transparency and monitoring capabilities for the backup operations.

### Backup policies

Your company might also require that the backup policies be defined by the following groups of people:

- Data owners, who are most familiar with the tables and can set the
appropriate *table-level backup policies* .
- Data governance team, who ensure that a *fallback policy* is in place to
cover any tables that don't have a table-level policy. The fallback policy
ensures that certain datasets, projects, and folders are backed up to
comply with your company's data retention regulations.

In the deployment for this reference architecture, there are two ways to define the backup policies for tables, and they can be used together:

- **Data owner configuration** (decentralized): a table-level backup policy,
which is manually attached to a table.
  - The data owner defines a table-level JSON file that's stored in a common bucket.
  - Manual policies take precedence over fallback policies when the solution determines the backup policy of a table.
  - For details in the deployment, see Set table-level backup policies.
- **Organization default configuration** (centralized): a fallback
policy, which applies only to tables that don't have manually-attached
policies.
  - A data governance team defines a central JSON file in Terraform, as part of the solution.
  - The fallback policy offers default backup strategies on folder, project, dataset, and table levels.
  - For details in the deployment, see Define fallback backup policies.

### Backup versus replication

A *backup* process makes a copy of the table data from a certain point in time,
so that it can be restored if the data is lost or corrupted. Backups can be run
as a one-time occurrence or recurrently (through a scheduled query or workflow).
In BigQuery, point-in-time backups can be achieved with
snapshots.
You can use snapshots to keep copies of the data beyond the seven-day time travel
period within the same storage location as the source data.
BigQuery snapshots are particularly helpful for recovering data
after human errors that lead to data loss or corruption, rather than
recovering from regional failures. BigQuery offers a Service
Level Objective (SLO) of
99.9% to 99.99%,
depending on the edition.

By contrast, *replication* is the continuous process of copying database
changes to a secondary (or replica) database in a different location. In
BigQuery,
cross-region replication 
can help provide geo-redundancy by creating read-only copies of the data in
secondary Google Cloud regions, which are different from the source data
region. However, BigQuery cross-region replication isn't
intended for use as a disaster recovery plan for total-region
outage scenarios.
For resilience against regional disasters, consider using
BigQuery managed disaster recovery.

BigQuery cross-region replication provides a synchronized read-only copy of the data in a region that is close to the data consumers. These data copies enable collocated joins and avoid cross-regional traffic and cost. However, in cases of data corruption due to human error, replication alone can't help with recovery, because the corrupted data is automatically copied to the replica. In such cases, point-in-time backups (snapshots) are a better choice.

The following table shows a summarized comparison of backup methods and replication:

| Method | Frequency | Storage location | Use cases | Costs | 
|---|---|---|---|---|
| Backup (Snapshots or Cloud Storage export) | One-time or recurrently | Same as the source table data | Restore original data, beyond the time travel period | Snapshots incur storage charges for data changes in the snapshot only Exports can incur standard storage charges See Cost optimization | 
| Cross-region replication | Continuously | Remote | Create a replica in another region One-time migrations between regions | Incurs charges for storing data       in the replica Incurs data replication costs | 

## Design considerations

This section provides guidance for you to consider when you use this reference architecture to develop a topology that meets your specific requirements for security, reliability, cost optimization, operational efficiency, and performance.

### Security, privacy, and compliance

The deployment incorporates the following security measures in its design and implementation:

- The
network ingress 
setting for Cloud Run accepts only *internal* traffic, to
restrict access from the internet. It also allows only authenticated users
and service accounts to call the services.
- Each Cloud Run service and Pub/Sub subscription uses a separate service account, which has only the required permissions assigned to it. This mitigates the risks associated with using one service account for the system and follows the principle of least privilege.

For privacy considerations, the solution doesn't collect or process personally identifiable information (PII). However, if the source tables have exposed PII, the backups taken of those tables also include this exposed data. The owner of the source data is responsible for protecting any PII in the source tables (for example, by applying column-level security, data masking, or redaction). The backups are secure only when the source data is secured. Another approach is to make sure that projects, datasets, or buckets that hold backup data with exposed PII have the required Identity and Access Management (IAM) policies that restrict access to only authorized users.

As a general-purpose solution, the reference deployment doesn't necessarily comply with a particular industry's specific requirements.

### Reliability

This section describes features and design considerations for reliability.

#### Failure mitigation with granularity

To take backups of thousands of tables, it's likely that you might reach API limits for the underlying Google Cloud products (for example, snapshot and export operation limits for each project). However, if the backup of one table fails due to misconfiguration or other transient issues, that shouldn't affect the overall execution and ability to back up other tables.

To mitigate potential failures, the reference deployment decouples the processing steps by using granular Cloud Run services and connecting them through Pub/Sub. If a table backup request fails at the final tagger service step, Pub/Sub retries only this step and it doesn't retry the entire process.

Breaking down the flow into multiple Cloud Run services, instead of multiple endpoints hosted under one Cloud Run service, helps provide granular control of each service configuration. The level of configuration depends on the service's capabilities and the APIs that it communicates with. For example, the dispatcher service executes once per run, but it requires a substantial amount of time to list all the tables within the BigQuery backup scope. Therefore, the dispatcher service requires higher time-out and memory settings. However, the Cloud Run service for BigQuery snapshots executes once per table in a single run, and completes in less time than the dispatcher service. Therefore, the Cloud Run service requires a different set of configurations at the service level.

#### Data consistency

Data consistency across tables and views is crucial for maintaining a reliable backup strategy. Because data is continuously updated and modified, backups taken at different times might capture different states of your dataset. These backups in different states can lead to inconsistencies when you restore data, particularly for tables that belong to the same functional dataset. For example, restoring a sales table to a point in time that's different from its corresponding inventory table could create a mismatch in available stock. Similarly, database views that aggregate data from multiple tables can be particularly sensitive to inconsistencies. Restoring these views without ensuring that the underlying tables are in a consistent state could lead to inaccurate or misleading results. Therefore, when you design your BigQuery backup policies and frequencies, it's imperative to consider this consistency and ensure that your restored data accurately reflects the real-world state of your dataset at a given point in time.

For example, in the deployment for this reference architecture, data consistency is controlled through the following two configurations in the backup policies. These configurations compute the exact table snapshot time through time travel, without necessarily backing up all tables at the same time.

- `backup_cron` : Controls the frequency with which a table is backed
up. The start timestamp of a run is used as a reference point for time
travel calculation for all tables that are backed up in this run.
- `backup_time_travel_offset_days` : Controls how many days in the past
should be subtracted from the reference point in time (run start time), to
compute the exact time travel version of the table.

#### Automated backup restoration

Although this reference architecture focuses on backup automation at scale, you can consider restoring these backups in an automated way as well. This additional automation can provide similar benefits to those of the backup automation, including improved recovery efficiency and speed, with less downtime. Because the solution keeps track of all backup parameters and results through the tagger service, you could develop a similar architecture to apply the restoration operations at scale.

For example, you could create a solution based on an on-demand trigger that
sends a scope of BigQuery data to a dispatcher service, which
dispatches one request per table to a configurator service. The configurator
service could fetch the backup history that you want for a particular table.
The configurator service could then pass it on to either a *BigQuery
snapshot restoration service* or *Cloud Storage restoration service* to
apply the restoration operation accordingly. Lastly, a tagger service could store the results of
these operations in a state store. By doing so, the automated restoration
framework can benefit from the same design objectives as the backup framework
detailed in this document.

### Cost optimization

The framework of this architecture provides backup policies that set the following parameters for overall cost optimization:

- **Backup method** : The framework offers the following two backup
methods:
  - **BigQuery snapshots** , which incur storage costs
based on
updated and deleted data 
compared to the base table. Therefore, snapshots are more cost
effective for tables that are append-only or have limited updates.
  - **BigQuery exports to Cloud Storage** ,
which incur standard storage charges. However, for large tables that
follow a truncate and load approach, it's more cost effective to back
them up as exports in less expensive
storage classes.
- **Snapshot expiration** : The time to live (TTL) is set for a single
table snapshot, to avoid incurring storage costs
for the snapshot indefinitely. Storage costs can grow over time if tables
have no expiration.

### Operational efficiency

This section describes features and considerations for operational efficiency.

#### Granular and scalable backup policies

One of the goals of this framework is operational efficiency by scaling up business output while keeping business input relatively low and manageable. For example, the output is a high number of regularly backed up tables, while the input is a small number of maintained backup policies and configurations.

In addition to allowing backup policies at the table level, the framework also allows for policies at the dataset, project, folder, and global level. This means that with a few configurations at higher levels (for example, the folder or project level), hundreds or thousands of tables can be backed up regularly, at scale.

#### Observability

With an automation framework, it's critical that you understand the statuses of the processes. For example, you should be able to find the information for the following common queries:

- The backup policy that is used by the system for each table.
- The backup history and backup locations of each table.
- The overall status of a single run (the number of processed tables and failed tables).
- The fatal errors that occurred in a single run, and the components or steps of the process in which they occurred.

To provide this information, the deployment writes structured logs to Cloud Logging at each execution step that uses a Cloud Run service. The logs include the input, output, and errors, along with other progress checkpoints. A log sink routes these logs to a BigQuery table. You can run a number of queries to monitor runs and get reports for common observability use cases. For more information about logs and queries in BigQuery, see View logs routed to BigQuery.

### Performance optimization

To handle thousands of tables at each run, the solution processes backup requests in parallel. The dispatcher service lists all of the tables that are included within the BigQuery backup scope and it generates one backup request per table at each run. This enables the application to process thousands of requests and tables in parallel, not sequentially.

Some of these requests might initially fail for temporary reasons such as reaching the limits of the underlying Google Cloud APIs or experiencing network issues. Until the requests are completed, Pub/Sub automatically retries the requests with the exponential backoff retry policy. If there are fatal errors such as invalid backup destinations or missing permissions, the errors are logged and the execution of that particular table request is terminated without affecting the overall run.

#### Limits

The following quotas and limits apply to this architecture.

For table snapshots, the following applies for each backup operation project that you specify:

- One project can run up to 100 concurrent table snapshot jobs.
- One project can run up to 50,000 table snapshot jobs per day.
- One project can run up to 50 table snapshot jobs per table per day.

For details, see Table snapshots.

For export jobs (exports to Cloud Storage), the following applies:

- You can export up to 50 TiB of data per day from a project for free, by using the shared slot pool.
- One project can run up to 100,000 exports per day. To extend this limit, create a slot reservation.

For more information about extending these limits, see Export jobs.

Regarding concurrency limits, this architecture uses Pub/Sub to automatically retry requests that fail due to these limits, until they're served by the API. However, for other limits on the number of operations per project per day, these could be mitigated by either a quota-increase request, or by spreading the backup operations (snapshots or exports) across multiple projects. To spread operations across projects, configure the backup policies as described in the following deployment sections:

- Define fallback backup policies
- Configure additional backup operation projects
- Set table-level backup policies

## Deployment

To deploy this architecture, see Deploy scalable BigQuery backup automation.

## What's next

- Learn more about BigQuery:
- For more reference architectures, diagrams, and best practices, explore the Cloud Architecture Center.

## Contributors

Author: Karim Wadie | Strategic Cloud Engineer

Other contributors:

- Chris DeForeest | Site Reliability Engineer
- Eyal Ben Ivri | Cloud Solutions Architect
- Jason Davenport | Developer Advocate
- Jaliya Ekanayake | Engineering Manager
- Muhammad Zain | Strategic Cloud Engineer


====================================================================================================
ARTIGO 8
Link de Origem: https://docs.cloud.google.com/architecture/scalable-bigquery-backup-automation/deployment
====================================================================================================

This document describes how you deploy Scalable BigQuery backup automation.

This document is intended for cloud architects, engineers, and data governance officers who want to define and automate data policies in their organizations. Experience with Terraform is helpful.

## Architecture

The following diagram shows the automated backup architecture:

 

Cloud Scheduler triggers the run. The dispatcher service, using BigQuery API, lists the in-scope tables. Through a Pub/Sub message, the dispatcher service submits one request for each table to the configurator service. The configurator service determines the backup policies for the tables, and then submits one request for each table to the relevant Cloud Run service. The Cloud Run service then submits a request to the BigQuery API and runs the backup operations. Pub/Sub triggers the tagger service, which logs the results and updates the backup state in the Cloud Storage metadata layer.

For details about the architecture, see Scalable BigQuery backup automation.

## Objectives

- Build Cloud Run services.
- Configure Terraform variables.
- Run the Terraform and manual deployment scripts.
- Run the solution.

## Costs


In this document, you use the following billable components of Google Cloud:

  
  
  
  To generate a cost estimate based on your projected usage,
      use the pricing calculator.
  

When you finish the tasks that are described in this document, you can avoid continued billing by deleting the resources that you created. For more information, see Clean up.

## Before you begin

If you're re-deploying the solution, you can skip this section (for example, after new commits).

In this section, you create one-time resources.

1. In the Google Cloud console, activate Cloud Shell. Activate Cloud Shell
2. If you want to create a new Google Cloud project to use as the host project for the deployment, use the `gcloud projects create` command:   `gcloud projects create` `PROJECT_ID`
Replace `PROJECT_ID` with the ID of the project
   you want to create.
3. Install Maven: 
  1. Download Maven.
  2. In Cloud Shell, add Maven to `PATH` :```
export PATH=/DOWNLOADED_MAVEN_DIR/bin:$PATH
```
4. In Cloud Shell, clone the GitHub repository: ```
git clone https://github.com/GoogleCloudPlatform/bq-backup-manager.git
```
5. Set and export the following environment variables: `export PROJECT_ID=``PROJECT_ID` export TF_SA=bq-backup-mgr-terraform
export COMPUTE_REGION=`COMPUTE_REGION` export DATA_REGION=`DATA_REGION` export BUCKET_NAME=${PROJECT_ID}-bq-backup-mgr
export BUCKET=gs://${BUCKET_NAME}
export DOCKER_REPO_NAME=docker-repo
export CONFIG=bq-backup-manager
export ACCOUNT=`ACCOUNT_EMAIL` gcloud config configurations create $CONFIG
gcloud config set project $PROJECT_ID
gcloud config set account $ACCOUNT
gcloud config set compute/region $COMPUTE_REGION
gcloud auth login
gcloud auth application-default login
Replace the following: 
  - `PROJECT_ID` : the ID of the Google Cloud host project
that you want to deploy the solution to.
  - `COMPUTE_REGION` : the Google Cloud region where you want
to deploy compute resources like Cloud Run and Identity and Access Management (IAM).
  - `DATA_REGION` : the Google Cloud region you want to deploy
data resources (such as buckets and datasets) to.
  - `ACCOUNT_EMAIL` : the user account email address.
6. Enable the APIs: ```
./scripts/enable_gcp_apis.sh
```
The script enables the following APIs: 
  - Cloud Resource Manager API
  - IAM API
  - Data Catalog API
  - Artifact Registry API
  - BigQuery API
  - Pub/Sub API
  - Cloud Storage API
  - Cloud Run Admin API
  - Cloud Build API
  - Service Usage API
  - App Engine Admin API
  - Serverless VPC Access API
  - Cloud DNS API
7. Prepare the Terraform state bucket: ```
gcloud storage buckets create $BUCKET --project=$PROJECT_ID --location=$COMPUTE_REGION --uniform-bucket-level-access
```
8. Prepare the Terraform service account: ```
./scripts/prepare_terraform_service_account.sh
```
9. To publish images that this solution uses, prepare a Docker repository: ```
gcloud artifacts repositories create $DOCKER_REPO_NAME
  --repository-format=docker \
  --location=$COMPUTE_REGION \
  --description="Docker repository for backups"
```

## Deploy the infrastructure

Make sure that you've completed Before you begin at least once.

In this section, follow the steps to deploy or redeploy the latest codebase to the Google Cloud environment.

### Activate the gcloud CLI configuration

- In Cloud Shell, activate and authenticate the gcloud CLI configuration: ```
gcloud config configurations activate $CONFIG
gcloud auth login
gcloud auth application-default login
```

### Build Cloud Run services images

- In Cloud Shell, build and deploy docker images to be used by the Cloud Run service: ```
export DISPATCHER_IMAGE=${COMPUTE_REGION}-docker.pkg.dev/${PROJECT_ID}/${DOCKER_REPO_NAME}/bqsm-dispatcher-service:latest
export CONFIGURATOR_IMAGE=${COMPUTE_REGION}-docker.pkg.dev/${PROJECT_ID}/${DOCKER_REPO_NAME}/bqsm-configurator-service:latest
export SNAPSHOTER_BQ_IMAGE=${COMPUTE_REGION}-docker.pkg.dev/${PROJECT_ID}/${DOCKER_REPO_NAME}/bqsm-snapshoter-bq-service:latest
export SNAPSHOTER_GCS_IMAGE=${COMPUTE_REGION}-docker.pkg.dev/${PROJECT_ID}/${DOCKER_REPO_NAME}/bqsm-snapshoter-gcs-service:latest
export TAGGER_IMAGE=${COMPUTE_REGION}-docker.pkg.dev/${PROJECT_ID}/${DOCKER_REPO_NAME}/bqsm-tagger-service:latest
./scripts/deploy_services.sh
```

### Configure Terraform variables

This deployment uses Terraform for configurations and a deployment script.

1. In Cloud Shell, create a new Terraform TFVARS file in which you can override the variables in this section: `export VARS=``FILENAME` .tfvars
Replace `FILENAME` with the name of the variables file that you
created (for example,`my-variables` ). You can use the`example-variables` file as a reference.
2. In the TFVARS file, configure the project variables: `project = "``PROJECT_ID` "
compute_region = "`COMPUTE_REGION` "
data_region = "`DATA_REGION` "
You can use the default values that are defined in the variables.tf file or change the values.
3. Configure the Terraform service account, which you created and prepared earlier in Before you begin: ```
terraform_service_account =
"bq-backup-mgr-terraform@
```
`PROJECT_ID` .iam.gserviceaccount.com"
Make sure that you use the full email address of the account that you created.
4. Configure the Cloud Run services to use the container images that you built and deployed earlier: ```
dispatcher_service_image     = "${COMPUTE_REGION}-docker.pkg.dev/${PROJECT_ID}/${DOCKER_REPO_NAME}/bqsm-dispatcher-service:latest"
configurator_service_image   = "${COMPUTE_REGION}-docker.pkg.dev/${PROJECT_ID}/${DOCKER_REPO_NAME}/bqsm-configurator-service:latest"
snapshoter_bq_service_image  = "${COMPUTE_REGION}-docker.pkg.dev/${PROJECT_ID}/${DOCKER_REPO_NAME}/bqsm-snapshoter-bq-service:latest"
snapshoter_gcs_service_image = "${COMPUTE_REGION}-docker.pkg.dev/${PROJECT_ID}/${DOCKER_REPO_NAME}/bqsm-snapshoter-gcs-service:latest"
tagger_service_image         = "${COMPUTE_REGION}-docker.pkg.dev/${PROJECT_ID}/${DOCKER_REPO_NAME}/bqsm-tagger-service:latest"
```
This script instructs Terraform to use these published images in the Cloud Run services, which Terraform creates later. Terraform only links a Cloud Run service to an existing image. It doesn't build the images from the codebase, because that was completed in a previous step.
5. In the `schedulers` variable, define at least one scheduler. The scheduler
periodically lists and checks tables for required backups, based on their
table-level backup cron schedules.```
{
name    = "
```
`SCHEDULER_NAME` "
cron    = "`SCHEDULER_CRON` "
payload = {
    is_force_run =`FORCE_RUN` is_dry_run   =`DRY_RUN` folders_include_list  = [`FOLDERS_INCLUDED` ]
    projects_include_list = [`PROJECTS_INCLUDED` ]
    projects_exclude_list = [`PROJECTS_EXCLUDED` ]
    datasets_include_list =  [`DATASETS_INCLUDED` ]
    datasets_exclude_list =  [`DATASETS_EXCLUDED` ]
    tables_include_list   =  [`TABLES_INCLUDED` ]
    tables_exclude_list   =  [`TABLES_EXCLUDED` ]
    }
}
Replace the following: 
  - `SCHEDULER_NAME` : the display name of
the Cloud Scheduler.
  - `SCHEDULER_CRON` : the frequency with which the scheduler checks
whether a backup is due for the in-scope tables, based on their individual
backup schedules. This can be any
unix-cron 
compatible string. For example,`0 * * * *` is an hourly frequency.
  - `FORCE_RUN` : a boolean value. Set the value to`false` if you
want the scheduler to use the tables' cron schedules. If set to`true` , all
in-scope tables are backed up, regardless of their cron setting.
  - `DRY_RUN` : a boolean value. When set to`true` , no actual
backup operations take place. Only log messages are generated. Use`true` when you want to test and debug the solution without incurring backup costs.
  - `FOLDERS_INCLUDED` : a list of numerical
IDs for folders that contain BigQuery data
(for example,`1234, 456` ). When set, the solution backs up the
tables in the specified folders, and ignores the`projects_include_list` ,`datasets_include_list` , and`tables_include_list` field settings.
  - `PROJECTS_INCLUDED` : a list of project names (for example,`"project1", "project2"` ). When set, the solution backs up the tables in
the specified projects, and ignores the`datasets_include_list` and`tables_include_list` field settings. This setting is ignored if you set the`folders_include_list` field.
  - `PROJECTS_EXCLUDED` : a list of project names or regular expression
(for example,`"project1", "regex:^test_"` ). When set, the solution does*not* take backups of the tables in the specified projects. You can use this
setting in combination with the`folders_include_list` field.
  - `DATASETS_INCLUDED` : a list of datasets (for example,`"project1.dataset1", "project1.dataset2"` ). When set, the solution backs
up the tables in the specified datasets, and ignores the`tables_include_list` field setting. This setting is ignored if you set the`folders_include_list` or`projects_include_list` fields.
  - `DATASETS_EXCLUDED` : a list of datasets or regular expression
(for example,`"project1.dataset1", "regex:.*\\_landing$"` ). When set, the
solution does*not* take backups of the tables in the specified datasets. You
can use this setting in combination with the`folders_include_list` or`projects_include_list` fields.
  - `TABLES_INCLUDED` : a list of tables (for example,`"project1.dataset1.table 1", "project1.dataset2.table2"` ). When set, the
solution backs up the specified tables. This setting is ignored if you set
the`folders_include_list` ,`projects_include_list` , or`datasets_include_list` fields.
  - `TABLES_EXCLUDED` : a list of tables or regular expression (for
example,`"project1.dataset1.table 1", "regex:.*\_test"` ). When set, the solution
does*not* take backups of the specified tables. You can use this setting
in combination with the`folders_include_list` ,`projects_include_list` , or`datasets_include_list` fields.
 All exclusion lists accept regular expressions in the form `regex:``REGULAR_EXPRESSION`
.If the fully qualified entry name (for example, `"project.dataset.table"` )
matches any of the supplied regular expression, it's excluded from the backup
scope.The following are some common use cases: 
  - Exclude all dataset names that end with `_landing` :```
datasets_exclude_list
= ["regex:.*\\_landing$"]
```
  - Exclude all tables ending with `_test` ,`_tst` ,`_bkp` , or`_copy` :`tables_exclude_list = ["regex:.*\_(test|tst|bkp|copy)"]`

### Define fallback policies

On each run, the solution needs to determine the backup policy of each in-scope table. For more information about the types of policies, see Backup policies. This section shows you how to define a fallback policy.

A fallback policy is defined with a `default_policy` variable and a set of
exceptions or overrides on different levels (folder, project, dataset, and
table). This approach provides granular flexibility without the need for an
entry for each table.

There are additional sets of policy fields, depending on the backup method that you decide to use: BigQuery snapshots, exports to Cloud Storage, or both.

1. In the TFVARS file, for the `default_policy` variable, set the
following common fields for the default policy:```
fallback_policy = {
  "default_policy" : {
    "backup_cron" : "
```
`BACKUP_CRON` "
    "backup_method" : "`BACKUP_METHOD` ",
    "backup_time_travel_offset_days" : "`OFFSET_DAYS` ",
    "backup_storage_project" : "`BACKUP_STORAGE_PROJECT` ",
    "backup_operation_project" : "`BACKUP_OPERATIONS_PROJECT` ",
Replace the following: 
  - `BACKUP_CRON` : a cron expression to set the frequency with
which a table is backed up (for example, for backups every 6 hours, specify`0 0 */6 * * *` ). This must be a
Spring-Framework 
compatible cron expression.
  - `BACKUP_METHOD` : the method, which you specify as`BigQuery Snapshot` ,`GCS Snapshot` (to use the
export to Cloud Storage method), or`Both` . You need to provide the
required fields for each chosen backup method, as shown later.
  - `OFFSET_DAYS` : the number of days in the past that determines
the point in time from which to back up the tables. Values can be a number
between 0 and 7.
  - `BACKUP_STORAGE_PROJECT` : the ID of the project where all
snapshot and export operations are stored. This is the same project where
the`bq_snapshot_storage_dataset` and`gcs_snapshot_storage_location` resides.
Small deployments can use the host project, but large scale deployments
should use a separate project.
  - `BACKUP_OPERATIONS_PROJECT` : an optional setting, where you
specify the ID of the project where all snapshot and export operations run.
Snapshot and export job
quotas and limits
are applicable to this project. This can be the same value as`backup_storage_project` . If not set, the solution uses the source table's
project.
2. If you specified `BigQuery Snapshot` or`Both` as the`backup_method` , add the following fields after the common fields, in the`default_policy` variable:  `"bq_snapshot_expiration_days" : "``SNAPSHOT_EXPIRATION` ",
  "bq_snapshot_storage_dataset" : "`DATASET_NAME` ",
Replace the following: 
  - `SNAPSHOT_EXPIRATION` : the number of days to keep each
snapshot (for example,`15` ).
  - `DATASET_NAME` : the name of the dataset to store snapshots in
(for example,`backups` ). The dataset must already exist in the project
specified for`backup_storage_project` .
3. If you specified `GCS Snapshot` (to use the export
to Cloud Storage method) or`Both` as the`backup_method` , add the
following fields to the`default_policy` variable:  `"gcs_snapshot_storage_location" : "``STORAGE_BUCKET` ",
  "gcs_snapshot_format" : "`FILE_FORMAT` ",
  "gcs_avro_use_logical_types" :`AVRO_TYPE` ,
  "gcs_csv_delimiter" : "`CSV_DELIMITER` ",
  "gcs_csv_export_header" :`CSV_EXPORT_HEADER`
Replace the following: 
  - `STORAGE_BUCKET` : the Cloud Storage bucket in which
to store the exported data, in the format`gs://bucket/path/` . For example,`gs://bucket1/backups/` .
  - `FILE_FORMAT` : the file format and compression used to export a
BigQuery table to Cloud Storage. Available values
are`CSV` ,`CSV_GZIP` ,`JSON` ,`JSON_GZIP` ,`AVRO` ,`AVRO_DEFLATE` ,`AVRO_SNAPPY` ,`PARQUET` ,`PARQUET_SNAPPY` , and`PARQUET_GZIP` .
  - `AVRO_TYPE` : a boolean value. If set to`false` , the
BigQuery types are exported as strings. If set to`true` ,
the types are exported as their corresponding
Avro logical type.
This field is required when the`gcs_snapshot_format` is any Avro type format.
  - `CSV_DELIMITER` : the delimiter used for the exported CSV files,
and the value can be any ISO-8859-1 single-byte character. You can use`\t` or`tab` to specify tab delimiters. This field is required when the`gcs_snapshot_format` is any CSV type format.
  - `CSV_EXPORT_HEADER` : a boolean value. If set to`true` , the column
headers are exported to the CSV files. This field is required when the`gcs_snapshot_format` is any CSV type format.
 For details and Avro type mapping, see the following table: BigQuery Type Avro Logical Type `TIMESTAMP``timestamp-micros` (annotates Avro`LONG` )`DATE``date` (annotates Avro`INT` )`TIME``timestamp-micro` (annotates Avro`LONG` )`DATETIME``STRING` (custom named logical type`datetime` )
4. Add override variables for specific folders, projects, datasets, and tables: ```
  },
  "folder_overrides" : {
   "
```
`FOLDER_NUMBER` " : {
   },
  },
  "project_overrides" : {
   "`PROJECT_NAME` " : {
   }
  },
  "dataset_overrides" : {
   "`PROJECT_NAME` .`DATASET_NAME` " : {
   }
  },
  "table_overrides" : {
   "`PROJECT_NAME` .`DATASET_NAME` .`TABLE_NAME` " : {
   }
  }
}
Replace the following: 
  - `FOLDER_NUMBER` : specify the folder for which you want to set
override fields.
  - `PROJECT_NAME` : specify the project when you set override
fields for a particular project, dataset, or table.
  - `DATASET_NAME` : specify the dataset when you set override
fields for a particular dataset or table.
  - `TABLE_NAME` : specify the table for which you want to set
override fields.
 For each override entry, such as a specific project in the `project_overrides` variable, add the common fields and the required fields
for the backup method that you specified earlier in`default_policy` .If you don't want to set overrides for a particular level, set that variable to an empty map (for example, `project_overrides : {}` ).In the following example, override fields are set for a specific table that uses the BigQuery snapshot method: ```
  },
  "project_overrides" : {},
  "table_overrides" : {
   "example_project1.dataset1.table1" : {
    "backup_cron" : "0 0 */5 * * *", # every 5 hours each day
    "backup_method" : "BigQuery Snapshot",
    "backup_time_travel_offset_days" : "7",
    "backup_storage_project" : "project name",
    "backup_operation_project" : "project name",
    # bq settings
    "bq_snapshot_expiration_days" : "14",
    "bq_snapshot_storage_dataset" : "backups2"
    },
   }
}
```

For a full example of a fallback policy, see the `example-variables` file.

### Configure additional backup operation projects

- If you want to specify additional backup projects, such as those defined in external configurations (table-level backup policy) or the table source projects, configure the following variable: `additional_backup_operation_projects = [``ADDITIONAL_BACKUPS` ]
Replace `ADDITIONAL_BACKUPS` with a comma-separated list of
project names (for example,`"project1", "project2"` ). If you're using only
the fallback backup policy without table-level external policies, you can
set the value to an empty list.If you don't add this field, any projects that are specified in the optional `backup_operation_project` field are automatically included as backup
projects.

### Configure Terraform service account permissions

In the previous steps, you configured the backup projects where the backup operations run. Terraform needs to deploy resources to those backup projects.

The service account that Terraform uses must have the required permissions for these specified backup projects.

- In Cloud Shell, grant the service account permissions for all of the projects where backup operations run: `./scripts/prepare_backup_operation_projects_for_terraform.sh` `BACKUP_OPERATIONS_PROJECT``DATA_PROJECTS``ADDITIONAL_BACKUPS`
Replace the following: 
  - `BACKUP_OPERATIONS_PROJECT` : any projects defined in the`backup_operation_project` fields in any of the fallback policies and
table-level policies.
  - `DATA_PROJECTS` : if no`backup_operation_project` field is
defined in a fallback or table-level policy, include the projects for those
source tables.
  - `ADDITIONAL_BACKUPS` : any projects that are defined in the`additional_backup_operation_projects` Terraform variable.

### Run the deployment scripts

1. In Cloud Shell, run the Terraform deployment script: ```
cd terraform
terraform init \
    -backend-config="bucket=${BUCKET_NAME}" \
    -backend-config="prefix=terraform-state" \
    -backend-config="impersonate_service_account=$TF_SA@$PROJECT_ID.iam.gserviceaccount.com"
terraform plan -var-file=$VARS
terraform apply -var-file=$VARS
```
2. Add the time to live (TTL) policies for Firestore: ```
gcloud firestore fields ttls update expires_at \
    --collection-group=project_folder_cache \
    --enable-ttl \
    --async \
    --project=$PROJECT_ID
```
The solution uses Datastore as a cache in some situations. To save costs and improve lookup performance, the TTL policy allows Firestore to automatically delete entries that are expired.

### Set up access to sources and destinations

1. In Cloud Shell, set the following variables for the service accounts used by the solution: ```
export SA_DISPATCHER_EMAIL=dispatcher@${PROJECT_ID}.iam.gserviceaccount.com
export SA_CONFIGURATOR_EMAIL=configurator@${PROJECT_ID}.iam.gserviceaccount.com
export SA_SNAPSHOTER_BQ_EMAIL=snapshoter-bq@${PROJECT_ID}.iam.gserviceaccount.com
export SA_SNAPSHOTER_GCS_EMAIL=snapshoter-gcs@${PROJECT_ID}.iam.gserviceaccount.com
export SA_TAGGER_EMAIL=tagger@${PROJECT_ID}.iam.gserviceaccount.com
```
If you've changed the default names in Terraform, update the service account emails.
2. If you've set the `folders_include_list` field, and want to set the
scope of the BigQuery scan to include certain folders, grant
the required permissions on the folder level:`./scripts/prepare_data_folders.sh` `FOLDERS_INCLUDED`
3. To enable the application to execute the necessary tasks in different projects, grant the required permissions on each of these projects: `./scripts/prepare_data_projects.sh` `DATA_PROJECTS` ./scripts/prepare_backup_storage_projects.sh`BACKUP_STORAGE_PROJECT` ./scripts/prepare_backup_operation_projects.sh`BACKUP_OPERATIONS_PROJECT`
Replace the following: 
  - `DATA_PROJECTS` : the data projects (or source projects) that
contain the source tables that you want to back up (for example,```
project1
project2
```
). Include the following projects:
    - Projects that are specified in the inclusion lists in the Terraform
variable `schedulers` .
    - If you want to back up tables in the host project, include the host project.
  - Projects that are specified in the inclusion lists in the Terraform
variable 
  - `BACKUP_STORAGE_PROJECT` : the backup storage projects (or
destination projects) where the solution stores the backups (for example,`project1 project2` ). You need to include the projects that are specified in
the following fields:
    - The `backup_storage_project` fields in all of the fallback policies.
    - The `backup_storage_project` fields in all of the table-level policies.
 Include backup storage projects that are used in multiple fields or that are used as both the source and destination project
  - The 
  - `BACKUP_OPERATIONS_PROJECT` : the data operation projects where
the solution runs the backup operations (for example,`project1 project2` ).
You need to include the projects that are specified in the following fields:
    - The `backup_operation_project` fields in all of the fallback policies.
    - All inclusion lists in the scope of the BigQuery
scan (if you don't set the `backup_operation_project` field).
    - The `backup_operation_project` fields in all of the table-level
policies.
 Include backup operations projects that are used in multiple fields or that are used as both the source and destination project.
  - The 
4. For tables that use column-level access control, identify all policy tag taxonomies that are used by your tables (if any), and grant the solution's service accounts access to the table data: `TAXONOMY="projects/``TAXONOMY_PROJECT` /locations/`TAXONOMY_LOCATION` /taxonomies/`TAXONOMY_ID` "
gcloud data-catalog taxonomies add-iam-policy-binding \
$TAXONOMY \
--member="serviceAccount:${SA_SNAPSHOTER_BQ_EMAIL}" \
--role='roles/datacatalog.categoryFineGrainedReader'
gcloud data-catalog taxonomies add-iam-policy-binding \
$TAXONOMY \
--member="serviceAccount:${SA_SNAPSHOTER_GCS_EMAIL}" \
--role='roles/datacatalog.categoryFineGrainedReader'
Replace the following: 
  - `TAXONOMY_PROJECT` : the project ID in
the policy tag taxonomy
  - `TAXONOMY_LOCATION` : the location
specified in the policy tag taxonomy
  - `TAXONOMY_ID` : the taxonomy ID of the policy
tag taxonomy
5. Repeat the previous step for each policy tag taxonomy.

## Run the solution

After you deploy the solution, use the following sections to run and manage the solution.

### Set table-level backup policies

- In Cloud Shell, create a table-level policy with the required fields, and then store the policy in the Cloud Storage bucket for policies: ```
# Use the default backup policies bucket unless overwritten in the .tfvars
export POLICIES_BUCKET=${PROJECT_ID}-bq-backup-manager-policies
# set target table info
export TABLE_PROJECT='
```
`TABLE_PROJECT` '
export TABLE_DATASET='`TABLE_DATASET` '
export TABLE='`TABLE_NAME` '
# Config Source must be 'MANUAL' when assigned this way
export BACKUP_POLICY="{
'config_source' : 'MANUAL',
'backup_cron' : '`BACKUP_CRON` ',
'backup_method' : '`BACKUP_METHOD` ',
'backup_time_travel_offset_days' : '`OFFSET_DAYS` ',
'backup_storage_project' : '`BACKUP_STORAGE_PROJECT` ',
'backup_operation_project' : '`BACKUP_OPERATION_PROJECT` ',
'gcs_snapshot_storage_location' : '`STORAGE_BUCKET` ',
'gcs_snapshot_format' : '`FILE_FORMAT` ',
'gcs_avro_use_logical_types' : '`AVRO_TYPE` ',
'bq_snapshot_storage_dataset' : '`DATASET_NAME` ',
'bq_snapshot_expiration_days' : '`SNAPSHOT_EXPIRATION` '
}"
# File name MUST BE backup_policy.json
echo $BACKUP_POLICY >> backup_policy.json
gcloud storage cp backup_policy.json gs://${POLICIES_BUCKET}/policy/project=${TABLE_PROJECT}/dataset=${TABLE_DATASET}/table=${TABLE}/backup_policy.json
Replace the following: 
  - `TABLE_PROJECT` : the project in which the table resides
  - `TABLE_DATASET` : the dataset of the table
  - `TABLE_NAME` : the name of the table

### Trigger backup operations

The Cloud Scheduler jobs that you configured earlier run automatically based on their cron expression.

You can also manually run the jobs in the Google Cloud console. For more information, see Run your job.

### Monitor and report

With your host project (`PROJECT_ID`) selected, you
can run the following queries in BigQuery Studio to get reports and information.

- Get progress statistics of each run (including in-progress runs): ```
SELECT * FROM `bq_backup_manager.v_run_summary_counts`
```
- Get all fatal (non-retryable errors) for a single run: ```
SELECT * FROM `bq_backup_manager.v_errors_non_retryable`
WHERE run_id = '
```
`RUN_ID` '
Replace `RUN_ID` with the ID of the run.
- Get all runs on a table and their execution information: ```
SELECT * FROM `bq_backup_manager.v_errors_non_retryable`
WHERE tablespec = 'project.dataset.table'
```
You can also specify a `grouped` version:```
SELECT * FROM `bq_backup_manager.v_audit_log_by_table_grouped`, UNNEST(runs) r
WHERE r.run_has_retryable_error = FALSE
```
- For debugging, you can get detailed request and response information for each service invocation: ```
SELECT
jsonPayload.unified_target_table AS tablespec,
jsonPayload.unified_run_id AS run_id,
jsonPayload.unified_tracking_id AS tracking_id,
CAST(jsonPayload.unified_is_successful AS BOOL) AS configurator_is_successful,
jsonPayload.unified_error AS configurator_error,
CAST(jsonPayload.unified_is_retryable_error AS BOOL) AS configurator_is_retryable_error,
CAST(JSON_VALUE(jsonPayload.unified_input_json, '$.isForceRun') AS BOOL) AS is_force_run,
CAST(JSON_VALUE(jsonPayload.unified_output_json, '$.isBackupTime') AS BOOL) AS is_backup_time,
JSON_VALUE(jsonPayload.unified_output_json, '$.backupPolicy.method') AS backup_method,
CAST(JSON_VALUE(jsonPayload.unified_input_json, '$.isDryRun') AS BOOL) AS is_dry_run,
jsonPayload.unified_input_json AS request_json,
jsonPayload.unified_output_json AS response_json
FROM `bq_backup_manager.run_googleapis_com_stdout`
WHERE jsonPayload.global_app_log = 'UNIFIED_LOG'
-- 1= dispatcher, 2= configurator, 3=bq snapshoter, -3=gcs snapshoter and 4=tagger
AND jsonPayload.unified_component = "2"
```
- Get the backup policies that are manually added or assigned by the system based on fallbacks: ```
SELECT * FROM `bq_backup_manager.ext_backup_policies`
```

### Limitations

For more information about limits and quotas for each project that is specified
in the `backup_operation_project` fields, see
Limits.

## Clean up

To avoid incurring charges to your Google Cloud account for the resources used in this deployment, either delete the projects that contain the resources, or keep the projects and delete the individual resources.

### Delete the projects

1. 
    In the Google Cloud console, go to the **Manage resources** page.Go to Manage resources
2. 
    In the project list, select the project that you
    want to delete, and then click **Delete** .
3. 
    In the dialog, type the project ID, and then click
    **Shut down** to delete the project.

### Delete the new resources

As an alternative to deleting the projects, you can delete the resources created during this procedure.

- In Cloud Shell, delete the Terraform resources: ```
terraform destroy -var-file="${VARS}"
```
The command deletes almost all of the resources. Check to ensure that all the resources you want to delete are removed.

## What's next

- Learn more about BigQuery:
- For more reference architectures, diagrams, and best practices, explore the Cloud Architecture Center.

## Contributors

Author: Karim Wadie | Strategic Cloud Engineer

Other contributors:

- Chris DeForeest | Site Reliability Engineer
- Eyal Ben Ivri | Cloud Solutions Architect
- Jason Davenport | Developer Advocate
- Jaliya Ekanayake | Engineering Manager
- Muhammad Zain | Strategic Cloud Engineer


====================================================================================================
ARTIGO 9
Link de Origem: https://docs.cloud.google.com/architecture/partners/continuous-data-replication-bigquery-striim
====================================================================================================

This tutorial demonstrates how to migrate a MySQL database to BigQuery using Striim. Striim is a comprehensive streaming extract, transform, and load (ETL) platform that enables online database migrations and continuous streaming replication from on-premises and cloud data sources to Google Cloud data services.

This tutorial focuses on the implementation of a continuous replication from Cloud SQL for MySQL to BigQuery. It is intended for database administrators, IT professionals, and data architects interested in taking advantage of BigQuery capabilities.

## Objectives

- Launch the Stiim for BigQuery free trial.
- Use Striim to continuously replicate from Cloud SQL for MySQL to BigQuery.

## Costs

In this document, you use the following billable components of Google Cloud:

  
  
  
  To generate a cost estimate based on your projected usage,
      use the pricing calculator.
  

This tutorial also uses Striim, which includes a trial period. You can find Striim in the Cloud Marketplace.

When you finish the tasks that are described in this document, you can avoid continued billing by deleting the resources that you created. For more information, see Clean up.

## Before you begin

1. 
  
  
    
    
      In the Google Cloud console, on the project selector page, select or create a Google Cloud project. **Roles required to select or create a project**
  - 
      **Select a project** : Selecting a project doesn't require a specific
      IAM role—you can select any project that you've been
      granted a role on.
  - 
      **Create a project** : To create a project, you need the Project Creator role
      (`roles/resourcemanager.projectCreator` ), which contains the`resourcemanager.projects.create` permission. Learn how to grant
      roles.
 Go to project selector
2. 
      
3. 
  
    Verify that billing is enabled for your Google Cloud project.
4. 
Enable the Compute Engine and BigQuery APIs, if any are not already enabled. **Roles required to enable APIs**To enable APIs, you need the `serviceusage.services.enable` permission. If you
          created the project, then you likely already have this permission through the
          Owner role (`roles/owner` ). Otherwise, you can get this permission through the
          Service Usage Admin role (`roles/serviceusage.serviceUsageAdmin` ).
          Learn how to grant roles.Enable the APIs
5. 
  
  
  
    
    In the Google Cloud console, activate Cloud Shell. Activate Cloud Shell
6. Set the default compute zone to `us-central1-a` :```
gcloud config set compute/zone us-central1-a
export COMPUTE_ZONE=us-central1-a
```
This zone is where you deploy your database. For more information about zones, see Geography and regions.

## Create a Cloud SQL for MySQL instance

You create a Cloud SQL for MySQL instance that you later connect to Striim. In this case, the instance acts as the source transactional system that you later replicate. In a real-world scenario, the source database can be one of many transactional database systems.

1. In Cloud Shell, create the environment variables to create the instance: ```
CSQL_NAME=striim-sql-src
CSQL_USERNAME=striim-user
CSQL_USER_PWD=$(openssl rand -base64 18)
CSQL_ROOT_PWD=$(openssl rand -base64 18)
```
If you close the Cloud Shell session, you lose the variables.
2. Make a note of the `CSQL_USER_PWD` and`CSQL_ROOT_PWD` passwords
generated by the following commands:```
echo $CSQL_USER_PWD and echo $CSQL_ROOT_PWD
```
3. Create the Cloud SQL for MySQL instance: ```
gcloud sql instances create $CSQL_NAME \
    --root-password=$CSQL_ROOT_PWD --zone=$COMPUTE_ZONE \
    --tier=db-n1-standard-2 --enable-bin-log
```
4. Create a Cloud SQL for MySQL user that Striim can connect to: ```
gcloud sql users create $CSQL_USERNAME --instance $CSQL_NAME \
    --password $CSQL_USER_PWD --host=%
```
The Cloud SQL for MySQL database is set up for Striim to read.
5. Find the IP address of the Cloud SQL for MySQL instance and make a note of it: ```
gcloud sql instances describe $CSQL_NAME --format='get(ipAddresses.ipAddress)'
```

## Set up Striim

To set up an instance of the Striim server software, you use the Cloud Marketplace.

1. In the Google Cloud console, go to the **Striim** page in the Cloud Marketplace.Go to Striim in the Cloud Marketplace
2. Click **Launch** .
3. In the **New Striim Deployment** window, complete the following fields:
  - Select the project that you created or selected to use for this tutorial.
  - In the **Zone** drop-down menu, select**`us-central1-a`** .
  - If you accept the terms for service, select the **I accept the
Google Cloud Marketplace Terms of Service** checkbox. Terms of Service** checkbox.Cloud Marketplace solutions typically come with various resources that launch to support the software. Review the monthly billing estimate before launching the solution.
  - Leave all other settings at their default values.
4. Click **Deploy** .
5. In the Google Cloud console, go to the **Deployments** page.Go to Deployments
6. To review the deployment details of the Striim instance, click the name of the Striim instance. Make a note of the name of the deployment and the name of the VM that has deployed.
7. To allow Striim to communicate with Cloud SQL for MySQL, add the Striim server's IP address to the Cloud SQL for MySQL instance's authorized networks: STRIIMVM_NAME= `STRIIM_VM_NAME` STRIIMVM_ZONE=us-central1-a
gcloud sql instances patch $CSQL_NAME \
    --authorized-networks=$(gcloud compute instances describe $STRIIM_VM_NAME \
    --format='get(networkInterfaces[0].accessConfigs[0].natIP)' \
    --zone=$STRIIMVM_ZONE)Replace the following: 
`STRIIM_VM_NAME`
8. In the Google Cloud console, on the deployment instance details page, click **Visit the site** to open the Striim web UI.
9. In the Striim configuration wizard, configure the following: 
  - Review the end-user license agreement. If you accept the terms,
click **Accept Striim EULA and Continue** .
  - Enter your contact information.
  - Enter the Cluster Name, Admin, Sys, and Striim Key passwords of
your choice. Make a note of these passwords. Click **Save and Continue** .
  - Leave the key field blank to enable the trial, and then click
**Save and Continue** .
10. Review the end-user license agreement. If you accept the terms,
click 
11. Click **Launch** . It takes about a minute for Striim to be configured.
When done, click**Log In** .
12. To log in to the Striim administrator console, log in with the `admin` user
and the administrator password that you previously set. Keep this window
open because you return to it in a later step.

### Set up Connector/J

Use MySQL Connector/J to connect Striim to your Cloud SQL for MySQL instance. As of this writing, 5.1.49 is the latest version of Connector/J.

1. In the Google Cloud console, go to the **Deployments** page.Go to Deployments
2. For the Striim instance, click **SSH** to automatically connect to the
instance.
3. Download the Connector/J to the instance and extract it: ```
wget https://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-java-5.1.49.tar.gz
tar -xvzf mysql-connector-java-5.1.49.tar.gz
```
4. Copy the file to the Striim library path, allow it to be executable, and change ownership of the file that you downloaded: ```
sudo cp ~/mysql-connector-java-5.1.49/mysql-connector-java-5.1.49.jar /opt/striim/lib
sudo chmod +x /opt/striim/lib/mysql-connector-java-5.1.49.jar
sudo chown striim /opt/striim/lib/mysql-connector-java-5.1.49.jar
```
5. To recognize the new library, restart the Striim server: ```
sudo systemctl stop striim-node
sudo systemctl stop striim-dbms
sudo systemctl start striim-dbms
sudo systemctl start striim-node
```
6. Go back to the browser window with the administration console in it. Reload the page, and then log in using the `admin` user credentials.It can take a couple minutes for the server to complete its restart from the previous step, so you might get a browser error during that time. If you encounter an error, reload the page and log in again.

## Load sample transactions to Cloud SQL

Before you can configure your first Striim app, load transactions into the MySQL instance.

1. In Cloud Shell, connect to the instance using the Cloud SQL for MySQL instance credentials that you previously set: ```
gcloud sql connect $CSQL_NAME --user=$CSQL_USERNAME
```
2. Create a sample database and load some transactions into it: ```
CREATE DATABASE striimdemo;
USE striimdemo;
CREATE TABLE ORDERS (ORDER_ID Integer, ORDER_DATE VARCHAR(50), ORDER_MODE VARCHAR(8), CUSTOMER_ID Integer, ORDER_STATUS Integer, ORDER_TOTAL Float, SALES_REP_ID Integer, PROMOTION_ID Integer, PRIMARY KEY (ORDER_ID));
INSERT INTO ORDERS (ORDER_ID, ORDER_DATE, ORDER_MODE, CUSTOMER_ID, ORDER_STATUS, ORDER_TOTAL, SALES_REP_ID, PROMOTION_ID) VALUES (1001, 1568927976017, 'In-Store', 1001, 9, 34672.59, 331, 9404);
INSERT INTO ORDERS (ORDER_ID, ORDER_DATE, ORDER_MODE, CUSTOMER_ID, ORDER_STATUS, ORDER_TOTAL, SALES_REP_ID, PROMOTION_ID) VALUES (1002, 1568928036017, 'In-Store', 1002, 1, 28133.14, 619, 2689);
INSERT INTO ORDERS (ORDER_ID, ORDER_DATE, ORDER_MODE, CUSTOMER_ID, ORDER_STATUS, ORDER_TOTAL, SALES_REP_ID, PROMOTION_ID) VALUES (1003, 1568928096017, 'CompanyB', 1003, 1, 37367.95, 160, 30888);
INSERT INTO ORDERS (ORDER_ID, ORDER_DATE, ORDER_MODE, CUSTOMER_ID, ORDER_STATUS, ORDER_TOTAL, SALES_REP_ID, PROMOTION_ID) VALUES (1004, 1568928156017, 'CompanyA', 1004, 1, 7737.02, 362, 89488);
INSERT INTO ORDERS (ORDER_ID, ORDER_DATE, ORDER_MODE, CUSTOMER_ID, ORDER_STATUS, ORDER_TOTAL, SALES_REP_ID, PROMOTION_ID) VALUES (1005, 1568928216017, 'CompanyA', 1005, 9, 15959.91, 497, 78454);
INSERT INTO ORDERS (ORDER_ID, ORDER_DATE, ORDER_MODE, CUSTOMER_ID, ORDER_STATUS, ORDER_TOTAL, SALES_REP_ID, PROMOTION_ID) VALUES (1006, 1568928276017, 'In-Store', 1006, 1, 82531.55, 399, 22488);
INSERT INTO ORDERS (ORDER_ID, ORDER_DATE, ORDER_MODE, CUSTOMER_ID, ORDER_STATUS, ORDER_TOTAL, SALES_REP_ID, PROMOTION_ID) VALUES (1007, 1568928336017, 'CompanyA', 1007, 7, 52929.61, 420, 66256);
INSERT INTO ORDERS (ORDER_ID, ORDER_DATE, ORDER_MODE, CUSTOMER_ID, ORDER_STATUS, ORDER_TOTAL, SALES_REP_ID, PROMOTION_ID) VALUES (1008, 1568928396017, 'Online', 1008, 1, 26912.56, 832, 7262);
INSERT INTO ORDERS (ORDER_ID, ORDER_DATE, ORDER_MODE, CUSTOMER_ID, ORDER_STATUS, ORDER_TOTAL, SALES_REP_ID, PROMOTION_ID) VALUES (1009, 1568928456017, 'CompanyA', 1009, 1, 97706.08, 124, 12185);
INSERT INTO ORDERS (ORDER_ID, ORDER_DATE, ORDER_MODE, CUSTOMER_ID, ORDER_STATUS, ORDER_TOTAL, SALES_REP_ID, PROMOTION_ID) VALUES (1010, 1568928516017, 'CompanyB', 1010, 1, 47539.16, 105, 17868);
```
3. To check the upload, count the records to ensure that 10 records were inserted: ```
SELECT COUNT(*) FROM ORDERS;
```
4. Leave the Cloud SQL for MySQL instance: ```
Exit
```

## Create a BigQuery target dataset

In this section, you create a BigQuery dataset, and load service account credentials so that Striim can write to the target database from the Google Cloud console.

1. In Cloud Shell, create a BigQuery dataset: ```
bq --location=US mk -d \
--description "Test Target for Striim." striimdemo
```
For this tutorial, you deploy BigQuery in the US.
2. Create a new target table: ```
bq mk \
    --table \
    --description "Striim Table" \
    --label organization:striimlab striimdemo.orders order_id:INTEGER,order_date:STRING,order_mode:STRING,customer_id:INTEGER,order_status:INTEGER,order_total:FLOAT,sales_rep_id:INTEGER,promotion_id:INTEGER
```
3. Create a service account for Striim to connect to BigQuery: ```
gcloud iam service-accounts create striim-bq \
    --display-name striim-bq
export sa_striim_bq=$(gcloud iam service-accounts list \
    --filter="displayName:striim-bq" --format='value(email)')
export PROJECT=$(gcloud info \
    --format='value(config.project)')
gcloud projects add-iam-policy-binding $PROJECT \
    --role roles/bigquery.dataEditor \
    --member serviceAccount:$sa_striim_bq
gcloud projects add-iam-policy-binding $PROJECT \
    --role roles/bigquery.user --member serviceAccount:$sa_striim_bq
gcloud iam service-accounts keys create ~/striim-bq-key.json \
    --iam-account $sa_striim_bq
```
A key called `striim-bq-key.json` is created in your home path.
4. Move the newly generated key to the server: ```
gcloud compute scp ~/striim-bq-key.json $STRIIM_VM_NAME:~ \
    --zone=$COMPUTE_ZONE
```
5. Move the key to the `/opt/striim` directory:```
gcloud compute ssh \
    --zone=$COMPUTE_ZONE $STRIIM_VM_NAME \
    -- 'sudo cp ~/striim-bq-key.json /opt/striim && sudo chown striim /opt/striim/striim-bq-key.json'
```
You are now ready to create a Striim app.

## Create an online database migration

An online database migration moves data from a source database (either on-premises or hosted on a cloud provider) to a target database or data warehouse in Google Cloud. The source database remains fully accessible by the business app and with minimal performance impact on the source database during this time.

In an online migration, you perform an initial bulkload, and also continuously capture any changes. You then synchronize the two databases to ensure that data isn't lost.

If you want to focus on creating a change data capture (CDC) pipeline, see the Create a continuous Cloud SQL for MySQL to BigQuery data pipeline section.

### Create the source connection

1. In the Google Cloud console, on the instance details page, click
**Visit the site** to open the Striim web UI.
2. In the Striim web UI, click **Apps** .
3. Click **Add App** .
4. Click **Start from Scratch** .
5. In the **Name** field, enter`MySQLToBigQuery_initLoad` .
6. In the **Namespace** drop-down menu, select the default**Admin
namespace** . This label is used to organize your apps.
7. Click **Save** .
8. On the **Flow Designer** page, to do a one-time initial bulkload of
data, from the**Sources** pane, drag**Database** to the flow design
palette in the center of the screen and enter the following connection
properties:
  - In the **Name** field, enter`mysql_source` .
  - Leave the **Adapter** field at the default value of**DatabaseReader** .
  - In the **Connection URL** field, enter`jdbc:mysql://``PRIMARY_ADDRESS` :3306/striimdemo
.
Replace`PRIMARY_ADDRESS`
  - In the **Username** field, enter the username that you set as
the`CSQL_USER` environment variable,`striim-user` .
  - In the **Password** field, enter the`CSQL_USER_PWD` value that
you made a note of when you
created a Cloud SQL for MySQL instance.
  - To see more configuration properties, click **Show optional
properties** .
  - In the **Tables** field, enter`striimdemo.ORDERS` .
  - For **Output to** , select**New output** .
  - In the **New output** field, enter`stream_CloudSQLMySQLInitLoad` .
  - Click **Save** .
9. In the 
10. To test the configuration settings to make sure that Striim can successfully connect to Cloud SQL for MySQL, click **Created** , and
then select**Deploy App** .
11. In the **Deployment** window, you can specify that you want to run parts
of your app on some of your deployment topology. For this tutorial, select**Default** , and click**Deploy** .
12. To preview your data as it flows through the Striim pipeline, click **`mysql_source DataBase reader`** , and then click**Preview on run** .
13. Click **Deployed** , and then click**Start App** .The Striim app starts running, and data flows through the pipeline. If there are any errors, there is an issue connecting to the source database because there is only a source component in the pipeline. If you see your app successfully run, but no data flows through, typically that means that you don't have any data in your database.
14. After you've successfully connected to your source database and tested that it can read data, click **Running** , and then select**Stop App** .
15. Click **Stopped** , and then select**Undeploy App** . You are now ready
to connect this flow to BigQuery.

### Perform an initial load into BigQuery

1. In the Striim web UI, click **`mysql_source Database reader`** .
2. Click **Connect to next component** , select**Connect next Target
component** , and then complete the following fields:
  - In the **Name** field, enter`bq_target` .
  - In the **Adapter** field, enter`BigQueryWriter` .
  - The **Tables property** is a source/target pair separated by commas. It
is in the format of`srcSchema1.srcTable1,tgtSchema1.tgtTable1;srcSchema2.srcTable2,tgtSchema2.tgtTable2` .
For this tutorial, enter`striimdemo.ORDERS,striimdemo.orders` .
  - The **Service Account Key** requires a fully qualified path and name of
the key file that was previously generated. For this tutorial, enter`/opt/striim/striim-bq-key.json` .
  - In the **Project ID** field, enter your Google Cloud project ID.
3. In the 
4. Click **Save** .
5. To deploy the app and preview the data flow, do the following: 
  - Click **Created** , and then select**Deploy App** .
  - In the **Deployment** window, select**Default** , and then click**Deploy** .
  - To preview your data as it flows through the Striim pipeline,
click 
**`mysql_source Database reader`** , and then click**Preview on run** .
  - Click **Deployed** , and then click**Start App** .
6. Click 
7. In the Google Cloud console, go to the **BigQuery** page.Go to BigQuery
8. Click the **`striimdemo`** database.
9. In the query editor, enter ```
SELECT COUNT(*) AS ORDERS, AVG(ORDER_TOTAL)
AS ORDERS_AVE, SUM(ORDER_TOTAL) AS ORDERS_SUM FROM striimdemo.orders;
```
and
then click**Run** . It can take up to 90 seconds for the transactions to
fully replicate to BigQuery due to the default configuration
settings. After it's successfully replicated, the results table outputs the
average order of`43148.952` and the total size of the orders,`431489.52` .You have successfully set up your Striim environment and pipeline to perform a batch load.

## Create a continuous data pipeline from Cloud SQL for MySQL to BigQuery

With an initial one-time bulkload in place, you can now set up a continuous replication pipeline. This pipeline is similar to the bulk pipeline that you created, but with a different source object.

### Create a CDC source

1. In the Striim web UI, click **Home** .
2. Click 
**Apps** .
3. Click **Start from Scratch** .
4. In the **Name** field, enter`MySQLToBigQuery_cdc` .
5. In the **Namespace** drop-down menu, select**Admin namespace** .
6. On the **Flow Designer** page, drag a**MySQL CDC** source reader to the
center of the design palette.
7. Configure your new MySQL CDC source with the following information: 
  - In the **Name** field, enter`mysql_cdc_source` .
  - Leave the **Adapter** field at the default value of**MysqlReader** .
  - In the **Connection URL** field, enter`jdbc:mysql://``PRIMARY_ADDRESS` :3306/striimdemo
.
  - Enter the username and password that you used in the previous section.
  - To see more configuration properties, click **Show optional
properties** .
  - In the **Tables** field, enter`striimdemo.ORDERS` .
  - For **Output to** , select**New output.**
  - In the **New output** field, enter`stream_CloudSQLMySQLCDCLoad` .
  - Click **Save** .
8. In the 

### Load new transactions into BigQuery

1. In the Striim web UI, click 
**MysqlReader** .
2. Click **Connect to next component** , and then select**Connect next
Target component** .
  - In the **Name** field, enter`bq_cdc_target` .
  - In the **Adapter** field, enter`BigQueryWriter` .
  - The **Tables property** is a source/target pair separated by
commas. It is in the format of`srcSchema1.srcTable1,tgtSchema1.tgtTable1;srcSchema2.srcTable2,tgtSchema2.tgtTable2` .
For this tutorial, use`striimdemo.ORDERS,striimdemo.orders` .
  - The **Service Account Key** requires a fully qualified path
and name of the key file that was previously generated. For this
tutorial, enter`/opt/striim/striim-bq-key.json`
  - In the **Project ID** field, enter your Google Cloud project ID.
3. In the 
4. Click **Save** .
5. To deploy the app and preview the data flow, do the following: 
  - Click **Created** , and then select**Deploy App** .
  - In the **Deployment** window, select**Default** , and then click**Deploy** .
  - To preview your data as it flows through the Striim pipeline, click
**MysqlReader** , and then click**Preview on Run** .
  - Click **Deployed** , and then click**Start App** .
6. Click 
7. In Cloud Shell, connect to your Cloud SQL for MySQL instance: ```
gcloud sql connect $CSQL_NAME --user=$CSQL_USERNAME
```
8. Connect to your database and load new transactions into it: ```
USE striimdemo;
INSERT INTO ORDERS (ORDER_ID, ORDER_DATE, ORDER_MODE, CUSTOMER_ID, ORDER_STATUS, ORDER_TOTAL, SALES_REP_ID, PROMOTION_ID) VALUES (1011, 1568928576017, 'In-Store', 1011, 9, 13879.56, 320, 88252);
INSERT INTO ORDERS (ORDER_ID, ORDER_DATE, ORDER_MODE, CUSTOMER_ID, ORDER_STATUS, ORDER_TOTAL, SALES_REP_ID, PROMOTION_ID) VALUES (1012, 1568928636017, 'CompanyA', 1012, 1, 19729.99, 76, 95203);
INSERT INTO ORDERS (ORDER_ID, ORDER_DATE, ORDER_MODE, CUSTOMER_ID, ORDER_STATUS, ORDER_TOTAL, SALES_REP_ID, PROMOTION_ID) VALUES (1013, 1568928696017, 'In-Store', 1013, 5, 7286.68, 164, 45162);
INSERT INTO ORDERS (ORDER_ID, ORDER_DATE, ORDER_MODE, CUSTOMER_ID, ORDER_STATUS, ORDER_TOTAL, SALES_REP_ID, PROMOTION_ID) VALUES (1014, 1568928756017, 'Online', 1014, 1, 87268.61, 909, 70407);
INSERT INTO ORDERS (ORDER_ID, ORDER_DATE, ORDER_MODE, CUSTOMER_ID, ORDER_STATUS, ORDER_TOTAL, SALES_REP_ID, PROMOTION_ID) VALUES (1015, 1568928816017, 'CompanyB', 1015, 1, 69744.13, 424, 79401);
```
9. In the Striim web UI, on the **Transactions view** page, transactions
now populate the page and show that data is flowing.
10. In the Google Cloud console, go to the **BigQuery** page.Go to BigQuery
11. Click the **`striimdemo`** database.
12. To verify that your data is successfully replicated, in the **Query
Editor** enter```
SELECT COUNT(*) AS ORDERS, AVG(ORDER_TOTAL) AS ORDERS_AVE,
SUM(ORDER_TOTAL) AS ORDERS_SUM FROM striimdemo.orders;
```
and then click**Run** . The results table outputs the average order of`43148.952` and the
total size of the orders,`431489.52` .It can take up to 90 seconds for the transactions to fully replicate to BigQuery due to the default configuration settings.

Congratulations, you have successfully set up a streaming replication pipeline from Cloud SQL for MySQL to BigQuery.

## Clean up

The easiest way to eliminate billing is to delete the Google Cloud project you created for the tutorial. Alternatively, you can delete the individual resources.
### Delete the project

1. 
    In the Google Cloud console, go to the **Manage resources** page.Go to Manage resources
2. 
    In the project list, select the project that you
    want to delete, and then click **Delete** .
3. 
    In the dialog, type the project ID, and then click
    **Shut down** to delete the project.

## What's next

- Explore reference architectures, diagrams, and best practices about Google Cloud. Take a look at our Cloud Architecture Center.
- Look at the Google Cloud Data Migration content.
- To learn about Striim, visit the website, schedule a demo with a Striim technologist, and subscribe to the Striim blog.
- To learn how to set up continuous data movement from Oracle to BigQuery, see Oracle to Google BigQuery – Continuous Movement of On-Premises Data via CDC and the Move Oracle to Google BigQuery in Real Time video.


