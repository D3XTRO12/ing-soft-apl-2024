import os
from dotenv import load_dotenv
import subprocess as sp
import sys

load_dotenv()
parameters = {
    "image_name": os.getenv("IMAGE_NAME"),
    "image_version": os.getenv("IMAGE_TAG"),
    "resource-group": os.getenv("RESOURCE_GROUP"),
    "location": os.getenv("LOCATION"),
    "acr_name": os.getenv("ACR_NAME"),
    "container-name": os.getenv("CONTAINER_NAME"),
    "port_container": os.getenv("PORT_CONTAINER"),
    "service_principal_name": os.getenv("SERVICE_PRINCIPAL_NAME")
}
image_name = f"{parameters['image_name']}:{parameters['image_version']}"

def run_command(command):
    result = sp.run(command, capture_output=True, text=True, shell=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return None
    return result.stdout.strip()

def az_resource_group():
    print(f"Creating resource group: {parameters['resource-group']}")
    return run_command(f"az group create --name {parameters['resource-group']} --location {parameters['location']}")

def az_acr():
    print(f"Creating ACR: {parameters['acr_name']}")
    result = run_command(f"az acr create --resource-group {parameters['resource-group']} --name {parameters['acr_name']} --sku Basic")
    if result is None:
        return False
    return run_command(f"az acr login --name {parameters['acr_name']}") is not None

def docker_build_and_push():
    print(f"Building Docker image: {image_name}")
    if run_command(f"docker build -t {image_name} .") is None:
        return False
    
    print(f"Tagging Docker image: {image_name}")
    if run_command(f"docker tag {image_name} {parameters['acr_name']}.azurecr.io/{image_name}") is None:
        return False
    
    print(f"Pushing Docker image: {image_name}")
    return run_command(f"docker push {parameters['acr_name']}.azurecr.io/{image_name}") is not None

def create_service_principal():
    acr_registry_id = run_command(f"az acr show --name {parameters['acr_name']} --query id --output tsv")
    if not acr_registry_id:
        print("Failed to get ACR Registry ID")
        return None, None

    print(f"ACR Registry ID: {acr_registry_id}")
    print(f"Creating/updating service principal: {parameters['service_principal_name']}")
    sp_info = run_command(f"az ad sp create-for-rbac --name {parameters['service_principal_name']} --scopes {acr_registry_id} --role acrpull --query '[appId, password]' --output tsv")
    
    if sp_info:
        user_name, password = sp_info.split()
        print(f"Service Principal ID: {user_name}")
        print("Service Principal Password: [REDACTED]")
        return user_name, password
    else:
        print("Failed to create/update service principal")
        return None, None

def az_container():
    user_name, password = create_service_principal()
    print("Creating container instance")
    result = run_command(f"az container create --resource-group {parameters['resource-group']} "
                f"--name {parameters['container-name']} "
                f"--image {parameters['acr_name']}.azurecr.io/{image_name} "
                f"--cpu 1 --memory 1 "
                f"--registry-login-server {parameters['acr_name']}.azurecr.io "
                f"--ip-address Public --location {parameters['location']} "
                f"--registry-username {user_name} "
                f"--registry-password {password} "
                f"--dns-name-label {parameters['container-name']}-{parameters['acr_name']} "
                f"--ports {parameters['port_container']}")
    return result is not None

def check_vulnerabilities():
    print(f"Checking vulnerabilities in Docker image: {image_name}")

    grype_path = "/usr/local/bin/grype"
    result = run_command(f"{grype_path} {image_name}")
    
    if result is None:
        print("Error while scanning for vulnerabilities")
        return False
    print(result)
    
    decision = input("Do you want to push the image to Azure despite the vulnerabilities? (yes/no): ")
    return decision.lower() == "yes"


def main():
    

    if not az_resource_group():
        
        print("Failed to create resource group")
        return

    if not az_acr():
        print("Failed to create or login to ACR")
        return

    if not docker_build_and_push():
        print("Failed to build and push Docker image")
        return

    if not check_vulnerabilities():
        print("Deployment aborted due to vulnerabilities")
        return
    
    if not az_container():
        print("Failed to create container instance")
        return

    print("Deployment completed successfully")
if __name__ == "__main__":
    main()