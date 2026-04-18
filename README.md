# MyMiniCloud Infrastructure

**Mini Cloud Platform**  
A complete simulation of cloud infrastructure with 9 services

## Project Objectives

Build the **MyMiniCloud** system consisting of **9 services** that simulates cloud infrastructure (AWS/Azure/GCP) using Docker Compose, including:
- Web Frontend (Nginx – supports Load Balancing with 2 instances)
- Application Backend (Flask API + OIDC)
- Relational Database (MariaDB)
- Authentication & Identity (Keycloak with Realm import)
- Object Storage (MinIO + bootstrap script)
- Internal DNS (Bind9)
- Monitoring (Prometheus + Node Exporter)
- Visualization (Grafana with provisioning)
- API Gateway / Reverse Proxy + Load Balancer (Nginx)

All services run in separate containers and communicate through the internal network `cloud-net`.

## Technologies Used

- **Containerization**: Docker + Docker Compose
- **Web Server**: Nginx (static + Load Balancing Round Robin)
- **Backend**: Python + Flask
- **Database**: MariaDB
- **Identity Provider**: Keycloak (OIDC / SSO)
- **Object Storage**: MinIO (S3-compatible)
- **DNS**: Bind9
- **Monitoring**: Prometheus + Node Exporter
- **Dashboard**: Grafana (provisioning)
- **Reverse Proxy & Load Balancer**: Nginx

## Project Directory Structure
MYMINICLOUD-INFRASTRUCTURE/
├── docker-compose.yml
├── docker-compose-aws.yml
├── docker-compose-aws.example.yml
├── README.md
├── .gitignore
├── web-frontend-server/                 
├── application-backend-server/
├── relational-database-server/
├── authentication-identity-server/       
├── object-storage-server/                
├── internal-dns-server/
├── monitoring-prometheus-server/
├── monitoring-grafana-dashboard-server/  
├── monitoring-node-exporter-server/
├── api-gateway-proxy-server/
└── scripts/

## Main Ports (Lab Specification)

| Service                          | External Port   | Internal Port  | Note                             |
|----------------------------------|-----------------|----------------|----------------------------------|
| Reverse Proxy                    | 80              | 80             | Main entry point                 |
| Web Frontend (Instance 1)        | 8080            | 80             | Load Balancing                   |
| Web Frontend (Instance 2)        | 8082            | 80             | Load Balancing                   |
| Application Backend              | 8085            | 8081           | Flask API                        |
| Authentication (Keycloak)        | 8081            | 8080           | OIDC / Realm                     |
| Database (MariaDB)               | 3306            | 3306           | -                                |
| Object Storage (MinIO)           | 9000, 9001      | 9000, 9001     | API + Console                    |
| Internal DNS                     | 1053/udp        | 53/udp         | -                                |
| Prometheus                       | 9090            | 9090           | Metrics                          |
| Node Exporter                    | 9100            | 9100           | -                                |
| Grafana                          | 3000            | 3000           | Dashboard                        |

## How to Run the Project (Local)

```bash
# 1. Clone repository
git clone https://github.com/TuanTruong125/myminicloud-infrastructure.git
cd myminicloud-infrastructure

# 2. Stop and remove all existing containers (including stuck ones)
docker rm -f $(docker ps -aq)

# 3. Clean up network and unused volumes (so Load Balancing gets new IP range)
docker network prune -f

# 4. Build the web service specifically (to force Docker to create the newest image for web)
docker compose build --no-cache web-frontend-server1

# 5. Build all remaining components
docker compose build

# 6. Start the entire system
docker compose up -d

# 7. Check the service list
docker compose ps
```

---

# MyMiniCloud Infrastructure

**Hệ thống Cloud thu nhỏ (Mini Cloud Platform)**  
Mô phỏng hạ tầng Cloud hoàn chỉnh với 9 services

## Mục tiêu dự án

Xây dựng hệ thống **MyMiniCloud** gồm **9 services** mô phỏng hạ tầng Cloud (AWS/Azure/GCP) sử dụng Docker Compose, bao gồm:
- Web Frontend (Nginx – hỗ trợ Load Balancing 2 instance)
- Application Backend (Flask API + OIDC)
- Relational Database (MariaDB)
- Authentication & Identity (Keycloak với Realm import)
- Object Storage (MinIO + bootstrap script)
- Internal DNS (Bind9)
- Monitoring (Prometheus + Node Exporter)
- Visualization (Grafana với provisioning)
- API Gateway / Reverse Proxy + Load Balancer (Nginx)

Tất cả các service chạy trong container riêng biệt, giao tiếp qua mạng nội bộ `cloud-net`.

## Công nghệ sử dụng

- **Containerization**: Docker + Docker Compose
- **Web Server**: Nginx (static + Load Balancing Round Robin)
- **Backend**: Python + Flask
- **Database**: MariaDB
- **Identity Provider**: Keycloak (OIDC / SSO)
- **Object Storage**: MinIO (S3-compatible)
- **DNS**: Bind9
- **Monitoring**: Prometheus + Node Exporter
- **Dashboard**: Grafana (provisioning)
- **Reverse Proxy & Load Balancer**: Nginx

## Cấu trúc thư mục dự án
MYMINICLOUD-INFRASTRUCTURE/
├── docker-compose.yml
├── docker-compose-aws.yml
├── docker-compose-aws.example.yml
├── README.md
├── .gitignore
├── web-frontend-server/                 
├── application-backend-server/
├── relational-database-server/
├── authentication-identity-server/       
├── object-storage-server/                
├── internal-dns-server/
├── monitoring-prometheus-server/
├── monitoring-grafana-dashboard-server/  
├── monitoring-node-exporter-server/
├── api-gateway-proxy-server/
└── scripts/

## Ports chính (theo lab)

| Service                          | Port ngoài      | Port trong     | Ghi chú                          |
|----------------------------------|-----------------|----------------|----------------------------------|
| Reverse Proxy                    | 80              | 80             | Cổng chính                       |
| Web Frontend (Instance 1)        | 8080            | 80             | Load Balancing                   |
| Web Frontend (Instance 2)        | 8082            | 80             | Load Balancing                   |
| Application Backend              | 8085            | 8081           | Flask API                        |
| Authentication (Keycloak)        | 8081            | 8080           | OIDC / Realm                     |
| Database (MariaDB)               | 3306            | 3306           | -                                |
| Object Storage (MinIO)           | 9000, 9001      | 9000, 9001     | API + Console                    |
| Internal DNS                     | 1053/udp        | 53/udp         | -                                |
| Prometheus                       | 9090            | 9090           | Metrics                          |
| Node Exporter                    | 9100            | 9100           | -                                |
| Grafana                          | 3000            | 3000           | Dashboard                        |

## Hướng dẫn chạy dự án (Local)

```bash
# 1. Clone repository
git clone https://github.com/TuanTruong125/myminicloud-infrastructure.git
cd myminicloud-infrastructure

# 2. Dừng và xóa toàn bộ container hiện có (kể cả container treo)
docker rm -f $(docker ps -aq)

# 3. Dọn dẹp hệ thống mạng và các volume thừa (để Load Balance nhận dải IP mới)
docker network prune -f

# 4. Build đích danh service web (để ép Docker tạo Image mới nhất cho web)
docker compose build --no-cache web-frontend-server1

# 5. Build tất cả các thành phần còn lại
docker compose build

# 6. Khởi chạy toàn bộ hệ thống
docker compose up -d

# 7. Kiểm tra lại danh sách
docker compose ps
```