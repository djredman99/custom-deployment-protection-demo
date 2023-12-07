import requests
import jwt
import time
import sys

# Requests a JWT token for the GitHub App and then gets an installation token
def get_installation_token(app_id, private_key_path, installation_id):
    # Read the private key from the file
    with open(private_key_path, 'rb') as pem_file:
        signing_key = jwt.jwk_from_pem(pem_file.read())

    # Create the JWT payload
    payload = {
        "iat": int(time.time()),
        "exp": int(time.time()) + 600,
        "iss": app_id
    }

    # Generate the JWT token
    jwt_instance = jwt.JWT()
    jwt_token = jwt_instance.encode(payload, signing_key, alg='RS256')

    # Set the headers for the request
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Make the POST request to get the installation token
    url = f"https://api.github.com/app/installations/{installation_id}/access_tokens"
    response = requests.post(url, headers=headers)

    # Check the response status code
    if response.status_code == 201:
        print(f"Got Installation token. Status code: {response.status_code}")
        print(f"Token: {response.json().get('token')}")
        return response.json().get("token")
    else:    
        print(f"Failed to get installation token. Status code: {response.status_code}")
        print(response.text)
        return None

# Updates the deployment protection rule based on the state
def update_deployment_protection(installation_token, url, state):

    # Set the headers with the installation token
    headers = {
        "Authorization": f"Bearer {installation_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Set the request payload to approve the deployment
    payload = {
        "environment_name" : "PROD" ,
        "state": f"{state}",
        "comment": f"Deployment {state} by GitHub Deployment APP"
    }

    # Make the POST request to approve the deployment
    response = requests.post(url, headers=headers, json=payload)

    # Check the response status code
    if response.status_code == 204:
        print("Deployment state set successfully.")
    else:
        print(f"Failed to update the deployment. Status code: {response.status_code}")
        print(response.text)



# Set the GitHub App ID, private key path, and installation ID
app_id = "127751"
private_key_path = "/mnt/c/Source/custom-deploy-protection/privatekey.pem"
installation_id = "18421865"
# For each approval or rejection attempt, you should only have to update the deployment_callback_url
deployment_callback_url = "https://api.github.com/repos/djredman99-org/custom-deploy-protection/actions/runs/7118905524/deployment_protection_rule"

# Get the installation token
installation_token = get_installation_token(app_id, private_key_path, installation_id)

# Proceed if the installation token is obtained successfully
if installation_token:
    # Call the function to update deployment protection

    #APPROVE
    update_deployment_protection(installation_token, deployment_callback_url, "approved")

    #DENY
    #update_deployment_protection(installation_token, deployment_callback_url, "rejected")
