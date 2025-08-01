# Kafka Cluster Implemetation
1. Centralized Kafka cluster to handle all Kafka topics, with the ability to scale the number of brokers with minimal changes.

## Kafka setup

### 1. Topic per Component

We will create a separate Kafka topic for each type of infrastructure component. Examples include:

* ApplicationService
* Database
* LoadBalancers
* ApplicationGateway


### 2. Partition per Application

Each application will be assigned a dedicated partition within the corresponding topic. For example, the Payment Service may be consistently assigned to partition 0 of each topic used in the tracing flow.

#### How will we achieve this?

* We will maintain a centralized relational database that stores the mapping between application name, topic name, and partition number.
* A relational database is preferred as it allows easy management of relationships and efficient retrieval.


### 3. Caching Strategy

To avoid querying the database on every trace:

* We will implement two layers of caching:

  * First-level cache at the container level (in-memory using Python dictionaries).
  * Second-level cache using Redis at the infrastructure level.

* The Redis cache will periodically refresh its data from the central database using a TTL-based mechanism. Additionally, we will implement a manual trigger or fallback to refresh Redis when needed.

* Each container will maintain its own short-lived in-memory cache, which will periodically sync with Redis to stay up-to-date.


### 4. OpenTelemetry Collector Consideration

Since we do not control the OpenTelemetry Collector code directly:

* We will rely on the service.name attribute (from the OTLP trace payload) to determine the appropriate partition for each application.
* This approach ensures consistent partitioning per service across the entire pipeline.
