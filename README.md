# Flare_mnist
Nvflare on mnist library

-nvflare provision -p project.yml (must have fix IP adress for each participant, you can get one with tailscale)

run start in: 
  -testnvflare/workspace/mnist_project/prod_00/IP/startup/start.sh for serveur
  -testnvflare/workspace/mnist_project/prod_00/site-1/startup/start.sh for serveur
  -testnvflare/workspace/mnist_project/prod_00/IP/startup/start.sh for serveur
-nvflare config -d testnvflare/workspace/mnist_project/prod_00/admin@nvidia.com/
-nvflare job submit -j testnvflare
