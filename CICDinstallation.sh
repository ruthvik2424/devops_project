#!/bin/bash
echo "This is the file for installation of tools of CICD Pipeline (Jenkins,minikube,kubectl,argocd)"
sleep 2
echo "Please ensure that the user running the script has sudo permissions and this script is designed for CentOS and RHEL Only"
sleep 2
echo "First Installation is of Jenkins requires some tools to be installed"
sleep 1
sudo yum update
sleep 1
echo "Need of Container Technology....."
sleep 1
sudo yum install -y podman
echo "Now lets install minikube for readytodeploy cluster for (x86_64 if your architecture is different refer offical documentation)"
sleep 1
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
echo "Starting the minikube cluster......"
sleep 1
minikube start
echo "Checking pods......"
sleep 1
kubectl get pods -A
echo "Ohh we have not install kubectl so we got an error so lets install it for accessing the cluster"
sleep 2
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
echo "validating the binary...."
sleep 1
curl -LO "https://dl.k8s.io/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl.sha256"
echo "$(cat kubectl.sha256)  kubectl" | sha256sum --check
echo "output is okk good to install"
sleep 1
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
echo "lets check its installed properly or not (fingers crossed)"
sleep 1
kubectl version --client
echo "Now the minikube and kubectl installation is done successfully lets install argocd on cluster we just started"
sleep 2
kubectl create namespace argocd
echo "Installing argocd on minikube cluster........."
sleep 1
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
curl -sSL -o argocd-linux-amd64 https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64
sudo install -m 555 argocd-linux-amd64 /usr/local/bin/argocd
rm argocd-linux-amd64
sleep 1
echo "run this commands after installation"
#argocd admin initial-password -n argocd
#kubectl port-forward svc/argocd-server -n argocd 8080:443
echo "Here the whole installation of all different tools finished get ready to configure this tools :-) :-)"
sleep 3
echo "Finishing ......."
sleep 2
