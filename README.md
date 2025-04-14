# [E-Commerce Platform](https://roadmap.sh/projects/scalable-ecommerce-platform)

An online store built with a **microservice architecture**.
This platform includes the following services:

- 🛒 **Cart**
- 📦 **Catalog**
- 🧾 **Order**
- 📩 **Notification**
- 👤 **User**

⚠️ **Note**: This project is under active development and may not be stable or feature-complete.

---

## 🤝 Contributing

Want to help? Contributions are welcome!
Check out the [Discussions](https://github.com/Rojf/Shop/discussions) and [Project Roadmap](https://github.com/Rojf/Shop/projects) to get started.

---

## 🛠️ Tech Stack

- **Languages**:
  - Python `3.12`

- **Frameworks**:
  - Django `5.1.4`
  - Django-Ninja `1.3.0` *(update if needed)*

- **Databases & Storage**:
  - PostgreSQL `17.2`
  - Redis `7.4`

- **Messaging & Tasks**:
  - Celery `5.x` *(add exact version)*
  - RabbitMQ `4.0`

- **API Gateway & Networking**:
  - NGINX
  - Traefik `3.3`

- **Payments & Notifications**:
  - Stripe
  - Twilio

- **Dev Tools**:
  - Docker
  - Poetry
  - Make
  - Pytest

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Rojf/Shop
cd Shop
```


---

### 2. Run Locally and Stop

⚠️ If `make local-down` fails due to `kill` permissions, try running with administrator rights:

```bash
# Install dependencies
make local-build

# Start services
make local-up

# Stop services
make local-down
```


---

### 3. Run Fully in Docker and Stop

```bash
# start app in docker
make up

# Stop app in docker
make down
```


---


### 📚 Documentation

Each microservice has its own documentation located in the `docs/` directory:

|Service|Documentation Path|Description|
|---|---|---|
|🧑‍💼 User|`docs/user/README.md`|Authentication and user profiles|
|📦 Catalog|`docs/catalog/README.md`|Product catalog and categories|
|🛒 Cart|`docs/cart/README.md`|Shopping cart logic|
|🧾 Order|`docs/order/README.md`|Order placement and status|
|🔔 Notification|`docs/notification/README.md`|Email/SMS/Push notifications|
|💳 Payment|`docs/payment/README.md`|Integration with Stripe (if exists)|

To explore APIs, expected request/response formats, and workflows, check the relevant `README.md` inside each subdirectory.

---

## 🧭 Product Roadmap

[Discussions](https://github.com/Rojf/Shop/discussions) | [Kanban Board](https://github.com/Rojf/Shop/projects)

✅ Completed – Deployed and functional
🔄 In Progress – Actively being developed
📅 Planned – Scheduled for the future

| Status | Feature      | Release  |
| ------ | ------------ | -------- |
| ✅      | Basic setup  | `v0.1.0` |
| 🔄     | Auth service | `v0.2.0` |
| 📅     | Admin panel  | `v0.3.0` |
