### **Technical requirements are subject to change. Please check it before you want to contribute. I will try to update the task board in a timely manner.**

### 1. **Introduction**
#### 1.1. General description
Microservice **Cart** is designed to manage a user's shopping cart within the framework of e-commerce. The main task of the service is to provide functionality for adding, deleting, editing, and viewing items in the shopping cart. The service also provides the ability to calculate the total cost of goods, taking into account discounts and promotions, and also interacts with other microservices to check the availability of goods and place an order.

#### 1.2. Purpose
The purpose of the microservice development is to create a stable, scalable and secure system for working with user baskets. The service should support both registered users and anonymous sessions, ensuring convenience and speed of shopping cart operations.

#### 1.3. Usage contexts
Microservice **Cart** is used in the following scenarios:
1. **The user adds items to the cart**:
When viewing the items, the user adds them to the cart for later checkout.
2. **Viewing the shopping cart**:
   The user checks the composition of the basket, the relevance of prices, the availability of goods and the total cost.
3. **Basket editing**:
The user changes the number of products, deletes unnecessary items.
4. **Checkout**:
After editing is completed, the user transfers the shopping cart to the order microservice (**Order**) for making a purchase.
5. **Checking the availability of goods**:
When adding or editing a shopping cart, the microservice checks the availability of goods through the microservice Catalog that manages the warehouse (**Inventory**).

#### 1.4. Interaction with other systems
Microservice **Cart** interacts with:
- **Catalog Service** — to check the availability of goods.
- **Order Service** — to transfer the contents of the shopping cart when placing an order. Communication will be via a message broker
###### Questionable
- **Payment Service** — for calculating and pre-estimating the cost of an order.
- **User Service** — for user identification and authorization. This feature will be migrated to the GETWAY API and User Service.

#### 1.5. Restrictions
- The shopping cart must be unique for each user, but maintain temporary shopping carts for anonymous users.
- Storage time for inactive buckets (for example, 30 days for registered users and 7 days for anonymous users).
- Support for major currencies and languages depending on the user's region.

This section provides a framework for understanding the goals and place of microservices in the application ecosystem.


### 2. **Functional requirements**

#### 2.1. Main functions
1. **Create a basket**
- The microservice should automatically create a basket for the user at the first request (if the basket does not already exist).
   - For anonymous users, the shopping cart is created based on the session ID.
   - For an authorized user, a shopping cart is created based on a database.

2. **Adding an item to the cart**
- The user can add an item to the cart by specifying:
- The product ID.
     - The quantity of the product.
     - Additional parameters (for example, color, size) are transmitted as needed.
   - If the product is already in the cart, the quantity is increased by the specified value.
   - Return the added product.

3. **Deleting an item from the shopping cart**
- The user can delete a specific item from the shopping cart.
   - Return a message about successful deletion.

4. **Product quantity update**
- The ability to change the quantity of a specific product in the cart.
   - Checking the availability of the specified quantity through the **Inventory Service**.

5. **Basket View**
- The user can get information about the contents of the basket, including:
     - A list of products.
     - The quantity of each product.
     - Prices of goods.
     - The total cost of the basket.

6. **Order Confirmation**
- Transfer the contents of the shopping cart to the order microservice (**Order Service**) for order processing.
   - *This point can be changed*

7. **Checking the availability of goods**
- Each time an item is added or modified, the availability in the **Inventory Service** is checked.
   - In case of unavailability, the product is marked as "unavailable".

8. **Cost calculation**
- Automatic recalculation of the total cost of the basket, taking into account:
     - Promotions and discounts (through a separate service or built-in mechanisms).
     - Taxes (depending on the region).

10. **Anonymous User Support**
- The shopping cart should be saved for anonymous users based on the session ID.
    - When an anonymous user logs in, their shopping cart is combined with the shopping cart from their profile.

#### 2.2. Additional functions
1. **Saving the history of changes to the basket**
- Logging operations with the basket (adding, deleting, changing items).

2. **Basket synchronization**
   - The ability to synchronize the shopping cart between different user devices.

3. **Multi-currency support**
- Prices in the basket are displayed in the currency selected by the user.

4. **Notifications**
- Notifying the user about:
     - Changes in the availability of goods.
     - The validity period of discounts.

#### 2.3. Restrictions
1. The maximum number of items in the basket (for example, 100 items).
2. The limit on the quantity of one product (for example, 50 units).
3. Time limit for basket storage:
   - For registered users — 30 days.
   - For anonymous users — 24 hours.

#### 2.4. Usage Scenarios
1. **Adding an item to the shopping cart:**
- The user clicks "Add to cart", the product is added, the total price is updated, availability is checked.

2. **Making an order:**
- The user proceeds to checkout, the shopping cart data is transferred to the **Order Service**.

3. **Editing the shopping cart:**
- The user changes the number of products, adds or deletes items, and receives updated information about the cost.

4. **Pooling of baskets:**
   - An anonymous user logs in, his shopping cart is combined with the shopping cart associated with the profile.


###3. Non-functional requirements

#### 3.1. **Efficiency**
- **Response time to requests:**
- The maximum API response time should be no more than **200 ms** for most operations under standard load.
- **Number of supported simultaneous users:**
- The system must process up to **1000 simultaneous requests** without performance degradation.
- **System load:**
- Supports peak load handling up to **5000 RPS** (requests per second) via scaling.

---

#### 3.2. **Scalability**
- The system must support horizontal scaling to handle an increased number of users and data growth.
- The architecture of the microservice should be flexible and easily adaptable to an increase in the volume of operations.
- Bucket data caching (Redis) should be distributed efficiently when scaling.

---

#### 3.3. **Accessibility**
- The system must be accessible **24/7** .
- The maximum time of unavailability due to maintenance should not exceed **1 hour per month** (SLA 99.9%).
- Automatic switching to backup nodes in case of failure of the main ones.

---

#### 3.4. **Security**
- **Data transmission:**
- Using HTTPS protocol to encrypt data between client and server.
- **Authentication and authorization:**
- Implementation of JWT authentication for working with a basket of authorized users.
  - Restriction of API access based on roles and rights.
- **User data protection:**
- All personal data (for example, user IDs) must be protected in the database.
- **Countering attacks:**
- Implementation of protection against SQL injections, XSS, CSRF and other vulnerabilities.
  - Limit the number of requests to protect against DDoS attacks.

---

#### 3.5. **Backup**
- Daily automatic backup of trash data and history.
- Backup storage:
- Last **7 days** - locally.
  - For the last **30 days** - in cloud storage.
- The ability to restore trash data within **15 minutes** after a crash.

---

#### 3.6. **Errors and logging**
- **Error logging:**
- All errors must be recorded in a centralized log repository.
- **Collection of metrics:**
  - Integration with monitoring systems (e.g. Prometheus, Grafana) to track performance, availability, and load metrics.
- **Integration with the monitoring system:**
- Configure Sentry to track errors, exceptions, and events.
- **Log format:**
- Logs should be structured (for example, JSON) and contain:
- Date and time of the event.
    - Type of event (error, warning, information).
    - Call stack (for errors).
    - The request/user ID.

### 4. **Technical Requirements**

#### 4.1. Technology stack
1. **Programming language:**
- Python version 3.12.6
2. **Framework:**
- Django-Ninja version 1.3.0 for API creation.
3. **Database:**
   - PostgreSQL version
4. **Caching:**
- Redis version (for temporary storage of buckets and acceleration of work with data).
5. **Message queues:**
- RabbitMQ or Kafka version (for asynchronous interaction with other microservices, for example, notifications or processing large amounts of data).
6. **Containerization:**
   - Docker for microservice isolation and deployment.
7. **Monitoring systems:**
- Prometheus, Grafana for performance monitoring.
8. **Configuration Management:**
- Using `dotenv' to manage environment variables.

#### 4.2. Architecture
1. **Architecture type:**
- Microservice architecture with an emphasis on isolation and independence.
2. **Design pattern:**
- Clean Architecture to simplify modifications and testing.
3. **API:**
- REST API with versioning (for example, `/api/v1/cart/`).
   - Support for pagination, filtering and sorting of data.

#### 4.3. Integrations
1. **Integration with Users Service:**
- JWT tokens for verifying user identification.
2. **Integration with Catalog Service:**
- API requests for checking the availability of goods.
3. **Integration with Orders Service:**
- Transfer the contents of the shopping cart to create an order.

#### 4.4. Bucket Status Management
1. **TTL mechanism:**
- Anonymous buckets use the TTL (lifetime) set in Redis (for example, 14 days).
2. **Locking mechanism:**
   - When editing the trash, Redis locks are used to avoid simultaneous conflicting operations.

#### 4.5. Testing
1. **Types of tests:**
- Unit tests: Checking individual components.
   - Integration tests: Checking interaction with external services (Inventory, Order, User).
   - Load tests: Performance evaluation under high load.
2. **Tools:**
- Pytest for writing tests.
   - Locust or JMeter for load testing.

#### 4.6. Logs and metrics
1. **Log format:**
   - JSON format for compatibility with log aggregation systems (for example, ELK Stack).
2. **Stored data:**
- Incoming requests, service responses, operation execution time, errors.
3. **Metrics:**
- Response time, number of requests, number of errors (5xx).

#### 4.7. Deployment and CI/CD
1. **Deployment:**
- Using Docker and Kubernetes for deployment.
   - Automatic scaling (for example, using HPA in Kubernetes).
2. **CI/CD:**
- GitHub Actions or GitLab CI for automatic testing and deployment.
3. **Release Strategy:**
   - Canary releases or Blue-Green Deployment to minimize the risks of updates.

#### 4.8. Documentation
1. **API Documentation:**
- Automatic generation using the built-in mechanism **Django Ninja** (OpenAPI/Swagger).
2. **Description of configurations:**
- Documentation of environment variables and their values.

### 4. API and interaction with other services

#### 4.1. **REST API**
The Cart microservice API provides REST endpoints for managing user baskets.
Examples of the main endpoints:

1. **Create a shopping cart**
   **POST/cart**
- **Description:** Creates a new shopping cart (for an anonymous user or an authorized one).
   - **Request:**
     ```json
     {
"user_id": "12345"
}
``
- ** The answer:**
     ```json
     {
       "cart_id": "67890",
       "user_id": "12345",
       "created_at": "2025-01-14T12:00:00Z"
     }
     ```

2. **Adding an item to the cart**
   **POST /cart/items**
- **Description:** Adds an item to the user's shopping cart.
   - **Request:**
     ```json
     {
"cart_id": "67890",
"product_id": "98765",
"quantity": 2
}
``
- **Response:**
     ```json
     {
       "message": "Item added to cart successfully"
     }
     ```

3. **Getting all the items in the cart**
   **GET /cart**
- **Description:** Returns the contents of the trash.
   - **The answer:**
     ```json
     {
       "cart_id": "67890",
       "items": [
         {
           "product_id": "98765",
"name": "Product 1",
"quantity": 2,
"price": 500.0
},
         {
"product_id": "12345",
"name": "Product 2",
"quantity": 1,
"price": 300.0
}
],
       "total_price": 1300.0
     }
     ```

4. **Updating the product quantity**
   **PUT /cart/items**
- **Description:** Updates the quantity of the product in the basket.
   - **Request:**
     ```json
     {
"cart_id": "67890",
"product_id": "98765",
"quantity": 5
}
``
- **Response:**
     ```json
     {
       "message": "Item quantity updated successfully"
     }
     ```

5. **Removing an item from the shopping cart**
   **DELETE /cart/items**
- **Description:** Removes an item from the shopping cart.
   - **Request:**
     ```json
     {
"cart_id": "67890",
"product_id": "98765"
}
``
- ** The answer:**
     ```json
     {
       "message": "Item removed from cart successfully"
     }
     ```

6. **Emptying the trash**
   **DELETE /cart**
- **Description:** Removes all items from the shopping cart.
   - **Request:**
     ```json
     {
       "cart_id": "67890"
     }
``
- **Reply:**
     ```json
     {
       "message": "Cart cleared successfully"
     }
     ```

7. **Making an order**
   **POST /cart/checkout**
- **Description:** Transfers the shopping cart to the order service to create an order.
   - **Request:**
     ```json
     {
"cart_id": "67890",
"payment_method": "credit_card",
"delivery_address": "123 Main St, City"
}
``
- **Reply:**
     ```json
     {
       "order_id": "54321",
       "status": "Order created successfully"
     }
     ```

---

#### 4.2. **Authorization and authentication**
- Using **JWT tokens** for user authentication.
- Anonymous users receive a temporary bucket ID (stored in Redis).
- Authorization verification is performed on all secure routes (for example, `/cart/checkout').

---

#### 4.3. **Data formats**
- **Format of requests and responses:** JSON.
- Example of headers:
``
http

Content-Type: application/json
  Authorization: Bearer <JWT_TOKEN>
  ```

---

#### 4.4. **Data verification and validation**
- Checking the input data:
  - All request fields are checked for the presence and correctness of the types.
  - For example, the quantity of the product (`quantity') must be a positive integer.
- Checking the availability of the product in the Inventory Service before adding it to the cart.
- Error notification if the product is unavailable or exceeds the allowed quantity.

---

#### 4.5. **API Errors**
- **Error codes and descriptions:**
- `400` is an invalid query (for example, there are no required fields).
  - `401` — Authorization error (for example, invalid or missing token).
  - `404` — Not found (for example, the product does not exist).
  - `409` — Conflict (for example, the product is unavailable in the specified quantity).
  - `500` is an internal server error.

- **Error example:**
  ```json
  {
    "error": "Product not found",
    "code": 404
  }
  ```


### 5. Database requirements

#### 5.1. **Database structure**

The following tables will be used for the bucket microservice:

1. **Table `carts`** — stores information about user baskets.

    - **Columns:**
- `id' (UUID, PRIMARY KEY): The unique identifier of the bucket.
        - `user_id` (UUID, FOREIGN KEY): The identifier of the user to whom the shopping cart is linked. It can be NULL for anonymous users.
	    - `status'(): Indicates the status of the shopping cart (completed or still being assembled)
        - `created_at` (TIMESTAMP): Bucket creation time.
        - `updated_at' (TIMESTAMP): The time of the last bucket update.
2. **Table `cart_items'** — stores the items added to the cart.

    - **Columns:**
- `id' (UUID, PRIMARY KEY): The unique identifier of the record.
        - `cart_id` (UUID, FOREIGN KEY): The identifier of the cart to which the product is linked.
        - `product_id` (UUID, FOREIGN KEY): Product identifier.
        - `quantity' (INTEGER): The number of items in the cart.
        - `price' (DECIMAL): The price of the product at the time of adding to the cart (to prevent changes in the price of the product after adding to the cart).
        - `discount' (): Discount (if applicable).
        - `created_at' (TIMESTAMP): The time when the product was added to the cart.
        - `updated_at' (TIMESTAMP): The time of the last update of the quantity of the product.
    - **Connections:**
- `carts' (1) ↔ (n) `cart_items`: One basket can contain many items.

3. **Temporary data storage:**
- Redis for storing anonymous buckets.
#### 5.2. **Indexes and optimization**

The following indexes will be used to improve database performance:

1. **Indexes on fields used for search and filtering:**

    - An index on the `user_id` field in the `carts' table for quick basket search by user.

        - Index:
`CREATE INDEX idx_carts_user_id ON carts(user_id);`

    - Index on the `cart_id' field in the `cart_items` table for quick search of items in the cart.

        - Index:
`CREATE INDEX idx_cart_items_cart_id ON cart_items(cart_id);`

    - Index on the `product_id' field in the `cart_items` table for quick product search in the cart.

        - Index:
            `CREATE INDEX idx_cart_items_product_id ON cart_items(product_id);`

    - Index on the 'created_at` field in the `orders` table for quick search of orders by date.

        - Index:
`CREATE INDEX idx_order_created_at ON orders(created_at);`

3. **Query optimization:**
- When performing queries with filtering by fields (for example, `status` for orders), indexes will be used to improve performance.
    - Application of **caching** for frequently requested data, for example, for a list of products or a user's shopping cart.
4. **Regular performance check** of the database using query monitoring and profiling tools.

### 6. Testing requirements

**6.1. Unit tests:**
It is necessary to develop a set of unit tests to test individual functions and methods of the Cart microservice. The main focus is on the following aspects:
- Checking the correctness of the basic business logic (adding an item to the cart, deleting an item, changing the quantity).
- Testing boundary conditions (for example, adding the maximum quantity of goods).
- Error and exception handling.

**6.2. Integration tests:**
Testing the interaction of the Cart microservice with other microservices and external systems:
- Checking the correctness of the API, including interaction with microservices, such as:
- User service (user validation).
  - Product service (obtaining product data).
  - Payment service (processing of order data).
- Testing the sequence of operations in case of basket changes (for example, updating data after successful payment).

**6.3. Load tests:**
Conducting tests to evaluate the performance and scalability of the microservice:
- Checking the response time when the number of API requests increases.
- Testing the stability of the system with a large number of users (simulation of simultaneous operation of several thousand users).
- Performance measurement for large amounts of data (for example, a basket with a large number of items).

**6.4. Security:**
Conducting vulnerability testing of a microservice:
- Checking protection against SQL injections when working with a database.
- Checking protection against CSRF attacks and other types of attacks on the API.
- Testing the authorization and authentication system to prevent unauthorized access.
- Assessment of the security of data transmission between services (using HTTPS and encryption).

The results of all tests should be documented, the identified defects should be fixed, and appropriate adjustments should be made to the code.

### 7. Deployment and monitoring

**7.1. Infrastructure:**
The Cart microservice will be deployed in a containerized environment using **Docker** and **Kubernetes**. Microservice containers will be deployed and managed in a Kubernetes cluster to ensure scalability, fault tolerance, and ease of deployment. The infrastructure components used include:
- **Docker** for packaging and isolating microservices.
- **Kubernetes** for container orchestration, deployment management, and scaling.
- A suitable solution will be used for storing state and data, for example, **PostgreSQL** or **MongoDB**, depending on the needs of the microservice.
- **Ingress Controller** for routing requests and external access to microservices.

**7.2. Monitoring and alerting:**
A monitoring system consisting of the following components will be used to monitor the operation of the microservice:
- **Prometheus** for collecting and storing metrics such as CPU load, memory usage, API response time, and more.
- **Grafana** for visualizing metrics and creating dashboards with microservice performance indicators.
- **Alertmanager** for setting up alerts and notifications about potential problems (for example, high resource usage, query errors, microservice failures).
An alert will also be set up for critical errors, such as database connection failures or other critical events.

**7.3. Logging:**
The logging mechanism will use a distributed system that collects logs from all components of the microservice and stores them in a centralized location for subsequent analysis.
- Logs will be recorded in **JSON** format for convenience of parsing and analysis.
- **ELK Stack** (Elasticsearch, Logstash, Kibana) or similar solutions (for example, **EFK Stack** using Fluentd instead of Logstash) will be used for centralized collection, indexing and visualization of logs.
- Logs will include information about requests, errors, database status, and other critical events.
- Integration with the alert system will also be configured for notifications in case of errors.

**7.4. CI/CD:**
The microservice deployment process will be automated using the **CI/CD** system, using one of the popular tools such as **GitLab CI**, **Jenkins** or **GitHub Actions**. The main stages of the CI/CD process:
1. **Build**: Every time the code is changed, a Docker image is built with a microservice.
2. **Testing**: Running unit tests, integration and load tests.
3. **Publication**: The image is uploaded to a container repository (for example, Docker Hub or a private repository).
4. **Deployment**: The microservice is automatically deployed in a Kubernetes cluster using **Helm** or another configuration management tool.
5. **Monitoring**: After deployment, monitoring and logging processes are automatically enabled to monitor the status of the microservice.
6. **Rollbacks**: In case of errors at any stage of deployment, the CI/CD system must support rollback to the previous stable version.

This process will be fully automated to speed up development and ensure stable operation of the microservice at all stages of its lifecycle.

### 8. Terms and stages of implementation

**8.1. Stages of development:**

1. **Requirements planning and analysis** (1 week):
- Analysis of business requirements for the Cart microservice.
   - Architecture description and API design.
   - Approval of technologies and tools for development.

2. **Microservice development (Backend)** (3 weeks):
   - Development of the main functional blocks of the microservice (API for working with the shopping cart, interaction with other microservices).
   - Implementation of data models and logic of basket processing (adding, deleting goods, calculations).
   - Integration with external services such as the service of goods, users and payments.

3. **Integration tests and unit tests** (2 weeks):
- Writing and running unit tests for the main functions of the microservice.
   - Writing integration tests for interaction with other microservices.
   - Setting up the testing environment and running tests on CI/CD.

4. **Security and protection** (1 week):
- Implementation of security mechanisms: protection against SQL injections, CSRF attacks, authentication and authorization settings.
   - Conducting vulnerability testing.

5. **Monitoring and logging** (1 week):
- Set up monitoring using Prometheus and Grafana.
   - Setting up logging using the ELK Stack.
   - Integration with the alert system.

6. **Documentation and preparation for deployment** (1 week):
- Creation of documentation on the microservice API.
   - Description of instructions for deploying, configuring, and scaling the microservice.
   - Preparation of configurations for Kubernetes and Docker.

**8.2. Testing stages:**

1. **Unit testing** (1 week):
- Development of unit tests for each component of the microservice.

**8.2. Testing stages:**

1. **Unit testing** (1 week):
- Development of unit tests for each component of the microservice.
   - Test automation via CI/CD pipeline.

2. **Integration testing** (1 week):
- Testing the interaction of the microservice with other services.
   - Conducting integration tests with real and test data.

3. **Load Testing** (1 week):
- Simulation of system load to test performance and scalability.
   - Assessment of response time and stability with a large number of users.

4. **Security Testing** (1 week):
- Conducting security tests, including tests for SQL injection, CSRF and other vulnerabilities.
   - Verification of the authorization and authentication system.

**8.3. Deployment Stages:**

1. **CI/CD integration** (1 week):
- Configure the build and deployment process via GitLab CI, Jenkins or another tool.
   - Setting up pipelines for automatic assembly, testing and deployment.

2. **Deployment in a test environment** (1 week):
- Deployment of a microservice in a Kubernetes test environment.
   - Conducting tests after deployment (checking the health of all services).

3. **Deployment in a production environment** (1 week):
- Deployment of a microservice in production.
   - Monitoring the system operation and adjusting configurations if necessary.

**8.4. Important milestones and milestones:**

1. **Completion of the architecture design and approval phase** — final approval of the requirements and architecture of the microservice (end of the first week).
2. **Completion of API development and core business logic** — completion of development and testing of the main functions of the microservice (end of the fourth week).
3. **Completion of security and functionality testing** — Completion of security, performance and integration testing (end of the seventh week).
4. **Completion of CI configuration/CD and monitoring** — setup and verification of CI/CD pipelines and system monitoring (end of the eighth week).
5. **Deployment in production** — successful deployment of the microservice in the production environment (end of the ninth week).

Thus, the total duration of the microservice development and deployment will be about **10 weeks**.
