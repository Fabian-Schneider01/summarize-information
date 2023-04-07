terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=3.46.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "summarize-information" {
  name     = "summarize-information"
  location = "francecentral"
  tags = {
    environment = "dev"
    owner = "Fabian Schneider" 
    source = "Terraform"
  }
}
