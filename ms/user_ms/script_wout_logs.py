import os
from dotenv import load_dotenv
import subprocess as sp
import random

load_dotenv()
IMAGE_NAME = os.getenv("IMAGE_NAME")
CONTAINER_NAME = os.getenv("CONTAINER_NAME")
IMAGE_TAG = os.getenv("IMAGE_TAG")
RESOURCE_GROUP = os.getenv("RESOURCE_GROUP")
LOCATION = os.getenv("LOCATION")
ACR_NAME = os.getenv("ACR_NAME")
PORT_CONTAINER = int(os.getenv("PORT_CONTAINER"))
SERVICE_PRINCIPAL_NAME = os.getenv("SERVICE_PRINCIPAL_NAME")
image_name = f"{IMAGE_NAME}:{IMAGE_TAG}"

def log_step(step_name):
    print(f"\n--- Starting {step_name} ---")

def docker_run():
    log_step("Docker Run")
    imagen = sp.run(["docker", "images", "--format", "json", "--filter", f"reference={image_name}"], capture_output=True, text=True, check=True)
    
    if imagen.returncode != 0:
        try:
            print(f"Creando Imagen: {image_name}")
            docker_build = sp.run(["docker", "build", "-t", image_name, "."], capture_output=True, text=True)
            
            print("Procediendo a Tag de Imagen")
            docker_tag = sp.run(["docker", "tag", image_name, f"{ACR_NAME}.azurecr.io/{image_name}"], capture_output=True, text=True)
            print("Iniciando verificacion de vulnerabilidades")
            if not check_vulnerabilities():
                print("Vulnerabilities check failed or user decided not to continue")
                return
            
            print(f"iniciando push de: {image_name}")
            docker_push = sp.run(["docker", "push", f"{ACR_NAME}.azurecr.io/{image_name}"], capture_output=True, text=True)
            
            print("Iniciando check de Resource Group")
            az_container()
        except sp.CalledProcessError as e:
            print(f"error: {e}")
    else:
        print(f"Imagen: {image_name} ya existe")
        print(imagen.stdout)
        docker_tag = sp.run(["docker", "tag", image_name, f"{ACR_NAME}.azurecr.io/{image_name}"], capture_output=True, text=True)
        
        print("Iniciando verificacion de vulnerabilidades")
        if not check_vulnerabilities():
            print("Vulnerabilities check failed or user decided not to continue")
            return
        
        print(f"iniciando push de: {image_name}")
        docker_push = sp.run(["docker", "push", f"{ACR_NAME}.azurecr.io/{image_name}"], capture_output=True, text=True)
        
        
        
        print("Iniciando check de Resource Group")
        az_container()

def az_resource_group():
    log_step("Azure Resource Group Check")
    filtro = f"[?name=='{RESOURCE_GROUP}']"
    try:
        catch_groups = sp.run(["az", "group", "list", "--query", filtro], capture_output=True, text=True, check=True)
        
        if catch_groups.stdout.strip() != '[]':
            print(f"Grupo ya existe: {RESOURCE_GROUP}")
            print("Iniciando check de ACR")
            az_acr()
        else:
            print(f"creando grupo: {RESOURCE_GROUP}, \nen la localizacion: {LOCATION}")
            create_r_group = sp.run(["az", "group", "create", "--name", RESOURCE_GROUP, "--location", LOCATION], capture_output=True, text=True)
            print(f"Grupo creado: {RESOURCE_GROUP}\nIniciando check de ACR")
            az_acr()
    except sp.CalledProcessError as e:
        print(f"error en az: {e}")

def az_acr():
    log_step("Azure Container Registry Check")
    filtro = f"[?name=='{ACR_NAME}']"
    check_acr = sp.run(["az", "acr", "list", "--query", filtro], capture_output=True, text=True, check=True)
    
    if check_acr.stdout.strip() != '[]':
        print(f"ACR ya existe: {ACR_NAME}")
        print("Procediendo a Login de ACR")
        acr_login = sp.run(["az", "acr", "login", "--name", f"{ACR_NAME}"], capture_output=True, text=True)
        docker_run()
    else:
        try:
            print(f"creando ACR: {ACR_NAME}")
            create_acr = sp.run(["az", "acr", "create", "--resource-group", RESOURCE_GROUP, "--name", ACR_NAME, "--sku", "Basic"], capture_output=True, text=True)
            print(f"ACR creado: {ACR_NAME}")
            print("Procediendo a Login de ACR")
            acr_login = sp.run(["az", "acr", "login", "--name", ACR_NAME], capture_output=True, text=True)
            docker_run()
        except sp.CalledProcessError as e:
            print(f"error: {e}")

def catch_user_data():
    log_step("Catch User Data")
    acr_registry_id = sp.run(["az", "acr", "show", "--name", ACR_NAME, "--query", "id", "--output", "tsv"], capture_output=True, text=True).stdout.strip()
    print(f"ID del Registro ACR: {acr_registry_id}")
    
    try:
        print(f"Verificando si existe el principal de servicio {SERVICE_PRINCIPAL_NAME}")
        user_name = sp.run(["az", "ad", "sp", "list", "--display-name", SERVICE_PRINCIPAL_NAME, "--query", "[].appId", "--output", "tsv"], capture_output=True, text=True).stdout.strip()
        
        if user_name:
            print(f"Principal de servicio {SERVICE_PRINCIPAL_NAME} encontrado")
            user_password = sp.run(["az", "ad", "sp", "create-for-rbac", "--name", SERVICE_PRINCIPAL_NAME, "--scopes", acr_registry_id, "--role", "acrpull", "--query", "password", "--output", "tsv"], capture_output=True, text=True).stdout.strip()
        else:
            print(f"Creando nuevo principal de servicio {SERVICE_PRINCIPAL_NAME}")
            sp_create = sp.run(["az", "ad", "sp", "create-for-rbac", "--name", SERVICE_PRINCIPAL_NAME, "--scopes", acr_registry_id, "--role", "acrpull", "--query", "'[appId, password]'", "--output", "tsv"], capture_output=True, text=True)
            user_name, user_password = sp_create.stdout.split()
        
        print(f"ID de Aplicación del Principal de Servicio: {user_name}")
        print("Contraseña del Principal de Servicio: [REDACTADA]")
        
        return user_name, user_password
    except Exception as e:
        print(f"Error: {e}")
        return None, None

def az_container():
    log_step("Azure Container Creation")
    print("Iniciando creacion de contenedor")
    try:
        user_name, user_password = catch_user_data()
        print("user_name:", user_name, "user_password:", "[REDACTED]")
        dns_name_label = f"dns-um-{random.randint(1000, 9999)}"
        create_container = sp.run([
            "az", "container", "create", 
            "--resource-group", RESOURCE_GROUP, 
            "--name", CONTAINER_NAME, 
            "--image", f"{ACR_NAME}.azurecr.io/{IMAGE_NAME}:{IMAGE_TAG}", 
            "--cpu", "1", 
            "--memory", "1", 
            "--registry-login-server", f"{ACR_NAME}.azurecr.io", 
            "--ip-address", "Public", 
            "--location", LOCATION, 
            "--registry-username", user_name, 
            "--registry-password", user_password, 
            "--dns-name-label", dns_name_label, 
            "--ports", str(PORT_CONTAINER)
        ])
        print("Contenedor creado", create_container)
    except sp.CalledProcessError as e:
        print(f"error: {e}")

def check_vulnerabilities():
    log_step("Vulnerability Check")
    print(f"Checking vulnerabilities in Docker image: {image_name}")

    grype_path = "/usr/local/bin/grype"
    result = sp.run([grype_path, image_name], capture_output=True, text=True)
    
    if result.returncode != 0:
        print("Error while scanning for vulnerabilities")
        return False
    
    print("Vulnerability scan results:")
    print(result.stdout)
    
    decision = input("Do you want to push the image to Azure despite the vulnerabilities? (yes/no): ")
    return decision.lower() == "yes"

az_resource_group()