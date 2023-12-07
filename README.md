# Demonstration of Custom Deployment Rules
A repo that demostrates GitHub's Custom Deployment Protection Rules

## Introduction
Repository Environment configurations in GitHub allow you to define your own [custom deployment protection](https://docs.github.com/en/actions/deployment/protecting-deployments) rules.  This gives you the opportunity to have your own custom logic in an app/website/script/etc. to assist you in knowing if you can or cannot move forward with a workflow job targeting that specific environment.  

At a high level, the steps to create your own custom deployment protection rule are:

1. Create/edit a GitHub App to serve as your protection rule.  The app will subscribe to a deployment protection webhook and will be delivered the necessary payload when an approval/rejection is needed from it.
2. Determine how you want to implement your rule.  Will it be a website that users will interact with?  Will it be a third-party product like ServiceNow?
3. Provide an endpoint for the deployment protection webhook (configured in your GitHub App) so GitHub knows where to send the data.
4. When a webhook is received, parse the data to know how/where to repsond.
5. Do whatever custom logic you require in your app
6. Respond to the API endpoint you received in the webhook payload with the correct state of "approved" or "rejected"

Some links for more details on this process:
- [Protecting Deployments](https://docs.github.com/en/actions/deployment/protecting-deployments)
- [Creating a GitHub App](https://docs.github.com/en/apps/creating-github-apps/registering-a-github-app/registering-a-github-app)
- [Authenticating as a GitHub App Installation](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/authenticating-as-a-github-app-installation)
- [Deployment Protections REST API](https://docs.github.com/en/enterprise-cloud@latest/rest/actions/workflow-runs?apiVersion=2022-11-28#review-custom-deployment-protection-rules-for-a-workflow-run)


## Webhook setup
If you want an easy way to receive webhooks, you can use a free service like [Smee.io](https://smee.io) to quickly create an endpoint for a webhook.  Smee.io allows you to view all webhook data received.

## Website Implementation (Future Work - Not completed as of yet)
This repository uses GitHub Pages to run a website that is used to control approval and rejection of a workflow run.

## Python Implementation
In the [src/python](src/python) directory, the file [set-deployment-state,py](src/python/set-deployment-state.py) file will allow you to complete the process of approving or rejecting a deployment protection rule.  The python code demostrates this in a manual way for demo purposes only.  This is to avoid developing a fully automated system for the purpse of simplicity.  It shows the main steps of the process that you would eventually fully automate.

Pre-reqs we will assume are completed at this point:
- Your GitHub app is configured and installed in the appropriate Org/Account
- You have your webhook endpoint set up and ready to receive events
- You have added the custom protection to the environment you wish to target
- You have a workflow created that is targeting the protected environment

Python specific pre-reqs:
- Open the terminal of your choice and ensure you can run python code from it (ex: type "python3" and see if it recognizes the command)
- If you need to install Python, visit [Python.org](https://www.python.org/downloads/)
- The required Python dependencies are _jwt_, _requests_, and _time_
- Pip is required to install python dependencies, which may also need to be installed.  To install pip to add these dependencies, run the command:
```
  sudo apt install python3-pip
```
- If you have any problem installing pip (or any of the other dependencies), you may first have to run:
```
  sudo apt-get update
```
- To add any of the missing dependencies, run the appropriate install commands
```
  pip install jwt
  pip install requests
  pip install time
```
- In whatever manner you chose, have the [set-deplyment-state,py](src/python/set-deployment-state.py) script accessible from your terminal

To demostrate:
1. Grab the App ID for the GitHub App and set the value in the [set-deplyment-state,py](src/python/set-deployment-state.py) script
2. Grab the pem file you received when creating a Private Key for your GitHub App.  This should have be automatically downloaded when you created a Private Key (check your downloads folder)
3. Store the pem file in a location that is accessible in your terminal and add the path to the file in the [set-deplyment-state,py](src/python/set-deployment-state.py) script
4. Trigger the workflow
5. Wait for Webhook event to be received at your endpoint
6. View the webhook payload data
7. From the Payload, you will want the following data:
     - installation.id
     - deployment_callback_url
8. Set these values in the [set-deplyment-state,py](src/python/set-deployment-state.py)
9. In the [set-deplyment-state,py](src/python/set-deployment-state.py), select which command you want to perform (APPROVE or REJECTED) and comment out the other.
10. Run the script when ready:
```
  python3 set-deployment-state.py
```

The script will run and do the following:
- Get a JWT token for your GitHub App so that it can access the API
- Get an Installation token for your GitHub App so that it can call specific API endpoint(s) that use installation tokens
   - An "Installation" is a specific installation of the github app on an organization or in a users personal account
- Approves or Rejects the deployment based on which method call you make
