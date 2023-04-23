# Konfiguration einer VM in der Azure Cloud
terraform {
  # Setzen der notwendigen Provider-Informationen
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=3.46.0"
    }
  }
}

# Konfiguration des Azure Providers
provider "azurerm" {
  features {}

  # Setzen der Subscription ID
  subscription_id = "subscription_id"
}

# Erzeugen einer Resource Group
resource "azurerm_resource_group" "example" {
  # Name der Resource Group
  name     = "your-resource-group"
  # Standort der Resource Group
  location = "francecentral"
}

# Erzeugen eines Virtual Networks
resource "azurerm_virtual_network" "example" {
  # Name des Virtual Networks
  name                = "my-virtual-network"
  # IP-Adresse des Virtual Networks
  address_space       = ["10.0.0.0/16"]
  # Standort des Virtual Networks
  location            = "${azurerm_resource_group.example.location}"
  # Name der Resource Group, in der das Virtual Network erzeugt wird
  resource_group_name = "${azurerm_resource_group.example.name}"
}

# Erzeugen eines Subnets
resource "azurerm_subnet" "example" {
  # Name des Subnets
  name                 = "my-subnet"
  # IP-Adresse des Subnets
  address_prefixes     = ["10.0.1.0/24"]
  # Name des Virtual Networks, zu dem das Subnet gehört
  virtual_network_name = "${azurerm_virtual_network.example.name}"
  # Name der Resource Group, in der das Subnet erzeugt wird
  resource_group_name  = "${azurerm_resource_group.example.name}"
}

# Erzeugen einer Network Interface
resource "azurerm_network_interface" "example" {
  # Name der Network Interface
  name                = "my-nic"
  # Standort der Network Interface
  location            = "${azurerm_resource_group.example.location}"
  # Name der Resource Group, in der die Network Interface erzeugt wird
  resource_group_name = "${azurerm_resource_group.example.name}"

  # Konfiguration der IP-Adresse
  ip_configuration {
    name                          = "my-ip-configuration"
    # ID des Subnets, zu dem die IP-Adresse gehört
    subnet_id                     = "${azurerm_subnet.example.id}"
    # Zuweisung der privaten IP-Adresse
    private_ip_address_allocation = "Dynamic"
    # ID der öffentlichen IP-Adresse
    public_ip_address_id          = "${azurerm_public_ip.example.id}"
  }
}

# Erzeugen einer öffentlichen IP-Adresse
resource "azurerm_public_ip" "example" {
  # Name der öffentlichen IP-Adresse
  name                = "my-public-ip"
  # Standort der öffentlichen IP-Adresse
  location            = "${azurerm_resource_group.example.location}"
  # Name der Resource Group, in der die öffentliche IP-Adresse erzeugt wird
  resource_group_name = "${azurerm_resource_group.example.name}"
  # Zuweisung der IP-Adresse
  allocation_method   = "Dynamic"
}

# Erzeugen einer Network Security Group
resource "azurerm_network_security_group" "example" {
  # Name der Network Security Group
  name                = "my-nsg"
  # Standort der Network Security Group
  location            = "${azurerm_resource_group.example.location}"
 # Name der Resource Group, in der die Network Security Group erzeugt wird
  resource_group_name = "${azurerm_resource_group.example.name}"

  # Konfiguration der Security Rule
    security_rule {
        name                       = "SSH"
        # Priorität der Security Rule
        priority                   = 1001
        # Richtung der Security Rule
        direction                  = "Inbound"
        # Zugriff auf die Security Rule
        access                     = "Allow"
        # Protokoll der Security Rule
        protocol                   = "Tcp"
        # Portbereich der Quelle
        source_port_range          = "*"
        # Portbereich des Ziels
        destination_port_range     = "22"
        # IP-Adresse der Quelle
        source_address_prefix      = "*"
        # IP-Adresse des Ziels
        destination_address_prefix = "*"
    }

    security_rule {
        name                       = "HTTP"
        priority                   = 1002
        direction                  = "Inbound"
        access                     = "Allow"
        protocol                   = "Tcp"
        source_port_range          = "*"
        destination_port_range     = "80"
        source_address_prefix      = "*"
        destination_address_prefix = "*"
    }

    security_rule {
        name                       = "HTTPS"
        priority                   = 1003
        direction                  = "Inbound"
        access                     = "Allow"
        protocol                   = "Tcp"
        source_port_range          = "*"
        destination_port_range     = "443"
        source_address_prefix      = "*"
        destination_address_prefix = "*"
    }
}

# Zuweisen der Network Security Group zur Network Interface
resource "azurerm_network_interface_security_group_association" "example" {
  # ID der Network Interface
  network_interface_id      = "${azurerm_network_interface.example.id}"
  # ID der Network Security Group
  network_security_group_id = "${azurerm_network_security_group.example.id}"
}

# Erzeugen einer virtuellen Maschine
resource "azurerm_virtual_machine" "example" {
  # Name der virtuellen Maschine
  name                  = "my-vm"
  # Standort der virtuellen Maschine
  location              = "${azurerm_resource_group.example.location}"
  # Name der Resource Group, in der die virtuelle Maschine erzeugt wird
  resource_group_name   = "${azurerm_resource_group.example.name}"
  # ID der Network Interface, die der virtuellen Maschine zugewiesen wird
  network_interface_ids = ["${azurerm_network_interface.example.id}"]
  # Größe der virtuellen Maschine
  vm_size               = "Standard_B1s"

  # Konfiguration der Identity
  identity {
    type = "SystemAssigned"
  }

  # Konfiguration des Storage Images
  storage_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }

  # Konfiguration des Storage OS Disk
  storage_os_disk {
    name              = "my-os-disk"
    caching           = "ReadWrite"
    create_option     = "FromImage"
    managed_disk_type = "Standard_LRS"
  }

  # Konfiguration des OS Profils
  os_profile {
    computer_name  = "my-vm"
    admin_username = "azureuser"
  }

  # Konfiguration des OS Profiles für Linux
  os_profile_linux_config {
    # Deaktivieren der Passwort-Authentifizierung
    disable_password_authentication = true
    ssh_keys {
      # Pfad zur SSH-Datei
      path     = "/home/azureuser/.ssh/authorized_keys"
      # SSH-Key
      key_data = "ssh-key"
    }
  }
}

# Create postgres db
resource "azurerm_postgresql_server" "example" {
  name                = "summarizeinformationdb"
  location            = "${azurerm_resource_group.example.location}"
  resource_group_name = "${azurerm_resource_group.example.name}"

  administrator_login          = "admin_name"
  administrator_login_password = "admin_password"

  sku_name   = "B_Gen5_1"
  version    = "11"
  storage_mb = 5120

  backup_retention_days        = 7
  geo_redundant_backup_enabled = false
  auto_grow_enabled            = false

  public_network_access_enabled    = false
  ssl_enforcement_enabled          = true
  ssl_minimal_tls_version_enforced = "TLS1_2"
}
