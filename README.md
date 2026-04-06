# Flare_mnist
# NVFlare Deployment Guide: MNIST
This guide assumes you are using **Tailscale** to provide stable, fixed IP addresses for your participants.

---

## 1. Provisioning the Project
First, we generate the startup kits based on your configuration file.

```bash
# Provision the project workspace
nvflare provision -p project.yml
```
> **Networking Note:** Ensure your `flare_mnist/project.yml` reflects the static IPs provided by Tailscale so the sites can actually find the server!

---

## 2. Starting the Infrastructure
You’ll need to run the startup scripts on each respective machine (Server, Site-1, and Site-2). 

| Component | Execution Path |
| :--- | :--- |
| **Server** | `flare_mnist/workspace/mnist_project/prod_00/IP/startup/start.sh` |
| **Site-1** | `flare_mnist/workspace/mnist_project/prod_00/site-1/startup/start.sh` |
| **Site-2** | `flare_mnist/workspace/mnist_project/prod_00/site-2/startup/start.sh` |

---

## 3. Admin Configuration
Before you can bark orders at the sites, you need to point your admin tool to the correct workspace directory.

```bash
# Set the directory for the admin console
nvflare config -d flare_mnist/workspace/mnist_project/prod_00/admin@nvidia.com/
```

---

## 4. Job Submission
Now that the server is up and the sites are connected, it's time to submit your MNIST job.

```bash
# Submit the MNIST job to the server
nvflare job submit -j flare_mnist
```

---

