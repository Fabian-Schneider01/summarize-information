# Welcome to Summarize-Information! 👋

## Description 📝

Summarize-Information is a cloud computing project that summarizes input text using extractive summarization. It is built using Django and runs with uWSGI and NGINX on an Azure VM (IaaS). The infrastructure is created using Terraform, and to run it, you can use the Ansible playbook.

## Infrastructure 🏢

The infrastructure for the Summarize-Information project is created using Terraform. This includes the creation of the Azure VM and associated resources such as network security groups and storage accounts.

## Deployment 🚀

To deploy the Summarize-Information project, you can use the Ansible playbook. This automates the installation of the necessary dependencies and configuration of the NGINX and uWSGI services.


## Monitoring 📊

The Summarize-Information project includes monitoring tools such as Grafana and Prometheus. These tools provide insights into the performance of the application and the underlying infrastructure.

## CI/CD Pipeline 🛠️

The Summarize-Information project uses a CI/CD pipeline to automate the deployment process and ensure that code changes are tested before being deployed to the production environment. The pipeline consists of two main components: GitHub Actions and Jenkins.

image.png