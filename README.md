# **Kubernetes (Kind) + Fluent Bit + LocalStack (Docker) - Setup Completo**

Este repositório contém a configuração para rodar um ambiente com **Kind (Kubernetes)**, **Fluent Bit** e **LocalStack (Docker Desktop)** para capturar logs e enviá-los para um bucket S3 simulado pelo LocalStack.

---

## **1️⃣ Estrutura do Projeto**

```plaintext
k8s_app_fluentbit_s3/
├── app/
│   ├── app.py                          # Código da aplicação que gera logs
│   ├── Dockerfile                       # Dockerfile da aplicação
│
├── k8s/
│   ├── check-fluentbit-cronjob.yaml     # CronJob para monitorar logs e reiniciar Fluent Bit se necessário
│   ├── deployment.yaml                   # Deployment da aplicação no Kubernetes
│   ├── fluent-bit-configmap.yaml         # Configuração do Fluent Bit (ConfigMap)
│   ├── fluent-bit-deployment.yaml        # Deployment do Fluent Bit no Kubernetes
│   ├── fluentbit-rbac.yaml               # Permissões RBAC para o CronJob e Fluent Bit
│   ├── kind.yaml                         # Configuração do cluster Kind com 1 master e 2 workers
│
├── localstack/
│   ├── volume/                           # Diretório persistente do LocalStack
│
├── docker-compose.yml                   # Docker Compose para rodar o LocalStack
├── README.md                            # Documentação com passo a passo da configuração
```

---

## **2️⃣ Configurando o Ambiente**

### **Passo 1: Criar o Cluster Kubernetes no Kind**
Criar um cluster Kubernetes local usando Kind.

```sh
kind create cluster --config=k8s/kind.yaml
```

Verifique se o cluster foi criado:
```sh
kubectl get nodes
```

---

### **Passo 2: Subir o LocalStack com Docker Compose**
O LocalStack será responsável por simular os serviços da AWS (S3, SQS, SNS).

Suba o LocalStack:

```sh
docker compose up -d
```

Verifique se o container do LocalStack está rodando:

```sh
docker ps | grep localstack
```

---

### **Passo 3: Criar o Bucket S3 no LocalStack**
O Fluent Bit precisa do bucket para armazenar os logs.

```sh
aws --endpoint-url=http://localhost:4566 s3 mb s3://log-bucket
```

Verifique se o bucket foi criado corretamente:
```sh
aws --endpoint-url=http://localhost:4566 s3 ls
```

---

### **Passo 4: Subir a Aplicação no Kubernetes**
Agora, vamos rodar a aplicação `log-generator`, que gera logs continuamente.

```sh
kubectl apply -f k8s/deployment.yaml
```

Verifique se o pod foi criado corretamente:

```sh
kubectl get pods -l app=log-generator
```

Testando os logs da aplicação:

```sh
kubectl logs -l app=log-generator --tail=50 -f
```

---

### **Passo 5: Subir o Fluent Bit no Kubernetes**
O Fluent Bit será responsável por coletar logs e enviá-los ao LocalStack.

1. Aplicar o ConfigMap do Fluent Bit:

```sh
kubectl apply -f k8s/fluent-bit-configmap.yaml
```

2. Implantar o Fluent Bit no Kubernetes:

```sh
kubectl apply -f k8s/fluent-bit-deployment.yaml
```

3. Verificar se o Fluent Bit está rodando:

```sh
kubectl get pods -l app=fluent-bit
```

4. Monitorar os logs do Fluent Bit:

```sh
kubectl logs -l app=fluent-bit --tail=50 -f
```

---

### **Passo 6: Configurar o Monitoramento Automático do Fluent Bit**
Para garantir que os logs estão sendo enviados continuamente ao LocalStack, criamos um **CronJob Kubernetes** que monitora o bucket do S3 e reinicia o Fluent Bit caso os logs parem de ser enviados.

#### **Criar as permissões RBAC para o CronJob**
```sh
kubectl apply -f k8s/fluentbit-rbac.yaml
```

#### **Aplicar o CronJob**
```sh
kubectl apply -f k8s/check-fluentbit-cronjob.yaml
```

#### **Verificar se o CronJob foi criado**
```sh
kubectl get cronjobs
```

#### **Rodar o CronJob manualmente para teste**
```sh
kubectl create job --from=cronjob/check-fluentbit-logs check-fluentbit-manual
```

#### **Verificar os logs do CronJob**
```sh
kubectl logs -l job-name=check-fluentbit-manual --tail=50
```

### **Resumo**
- **O CronJob monitora o bucket do S3 a cada 5 minutos** e verifica se há logs recentes.
- **Se os logs pararem de ser enviados, ele reinicia o Fluent Bit automaticamente.**
- **O RBAC garante que o CronJob tenha permissões para rodar `kubectl rollout restart` no Fluent Bit.**

---

## **7️⃣ Verificar se os Logs Foram Enviados para o LocalStack**
Agora, vamos verificar se os logs chegaram ao S3 do LocalStack:

```sh
aws --endpoint-url=http://localhost:4566 s3 ls s3://log-bucket/ --recursive
```

Se os logs aparecerem na listagem, significa que tudo está funcionando corretamente! 🎉

Se quiser baixar um arquivo de log e visualizar:

```sh
aws --endpoint-url=http://localhost:4566 s3 cp s3://log-bucket/<nome-do-arquivo>.gz .
gunzip <nome-do-arquivo>.gz
cat <nome-do-arquivo>
```

---

## **8️⃣ Conclusão**
Agora temos um ambiente funcionando onde:
✅ A aplicação gera logs.
✅ O Fluent Bit captura os logs.
✅ Os logs são enviados para o LocalStack simulando um bucket S3.
✅ O CronJob monitora e reinicia o Fluent Bit caso os logs parem de ser enviados.

Se precisar depurar algo, verifique os logs do Fluent Bit, da aplicação e do CronJob! 🚀🔥

