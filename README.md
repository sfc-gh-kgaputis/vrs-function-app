# VRS Azure Functions App 
This Azure Functions app enables use of the [GA4GH vrs-python library](https://github.com/ga4gh/vrs-python) with Snowflake external functions. 

The Functions app is designed to deployed to Azure, and then exposed to Snowflake using Azure API Management Service.  

Two example functions have been provided:
1) **parse_ga4gh_identifier:** this simple function parses a GA4GH identifier and returns the components of the identifier to Snowflake in a VARIANT column. This operation doesn't have any external dependencies on a VRS data source such as seqrepo, so it's a good way to test that everything is working.
2) **identify_allele:** this function can translate various genetic expressions, in formats such as HGVS or SPDI, into GA4GH allele IDs. This does require an external data source.

## Getting Started
It will be helpful to review the [Getting Started With External Functions on Azure](https://quickstarts.snowflake.com/guide/getting_started_external_functions_azure/index.html) Snowflake quickstart. This will walk you through the process of setting up a sample Functions app and API Management Service, configuring the trust relationship between Snowflake and your Azure instance, and then invoking Azure Functions using Snowflake external functions.

## Local Environment Setup
### Dependencies
- AZ CLI
- Azure Functions Core Tools
- Python 3.x (3.10 was used for testing)
### Configure local Python environment
```
conda create -n vrs-functions python=3.10
conda activate vrs-functions
pip install -r requirements.txt
```
### Populate local settings config file
Create a `local.settings.json` file in the project root folder. This will be used by Azure CLI and/or Azure Functions Core Tools to help develop, test and build your Functions app. 

An example has been provided in `local.settings.json.example`. By convention, this file is not usually versioned since it may contain connection strings.

## Azure Configuration
### Create Azure Functions app in a new RG
```
az login
az group create --name kgaputis-vrs-rg --location eastus
az storage account create --name kgaputisvrssa --location eastus --resource-group kgaputis-vrs-rg --sku Standard_LRS
az functionapp create --resource-group kgaputis-vrs-rg --consumption-plan-location eastus --runtime python --runtime-version 3.10 --functions-version 4 --name kgaputis-vrs-function-app --storage-account kgaputisvrssa --os-type Linux
```
### Configure CORS for testing in Azure Portal
```
az functionapp cors add --resource-group kgaputis-vrs-rg --name kgaputis-vrs-function-app --allowed-origins 'https://portal.azure.com'
```
### Next steps
#### API Management Service configuration
As outlined in the [Getting Started With External Functions on Azure](https://quickstarts.snowflake.com/guide/getting_started_external_functions_azure/index.html) quickstart, you will need to expose this new Functions app using the API Management Service.

If you have previously completed the quickstart, you can leverage the same API Management Service deployment for this use case.

#### Populate required environment variable(s) in your Azure Functions App
You will need to populate the `VRS_REPO_URL` in your Azure Functions App Settings.

For initial testing using a publicly available API backend, you can use:
```
seqrepo+https://services.genomicmedlab.org/seqrepo
```

## Azure Deployment
### Deploy function app with remote build 
There are multiple ways to deploy a Functions App, but I've been using a remote build to ensure that additional Python libraries, as listed in `requirements.txt`, are installed in the Azure Functions App Linux runtime. 
```
func azure functionapp publish kgaputis-vrs-function-app --build remote
```

## Snowflake Setup and Usage
Please refer to `worksheet.sql` for an example SQL worksheet. 