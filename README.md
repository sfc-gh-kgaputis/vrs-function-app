# Setup
## Configure local Python environment
```
conda create -n vrs-functions python=3.10
conda activate vrs-functions
pip install -r requirements.txt
```

## Create Azure Functions app in a new RG
```
az login
az group create --name kgaputis-vrs-rg --location eastus
az storage account create --name kgaputisvrssa --location eastus --resource-group kgaputis-vrs-rg --sku Standard_LRS
az functionapp create --resource-group kgaputis-vrs-rg --consumption-plan-location eastus --runtime python --runtime-version 3.10 --functions-version 4 --name kgaputis-vrs-function-app --storage-account kgaputisvrssa --os-type Linux
```

## Configure CORS for testing in Azure Portal
```
az functionapp cors add --resource-group kgaputis-vrs-rg --name kgaputis-vrs-function-app --allowed-origins 'https://portal.azure.com'
```

# Build and deploy zip package
```
zip -r app.zip . -x '*.git*'
az functionapp deployment source config-zip -g kgaputis-vrs-rg -n kgaputis-vrs-function-app --src app.zip
```