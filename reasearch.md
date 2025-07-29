# Project Distributed Tracing - Research

## Microservice Architecture Monitoring
1. Possible Infra components (As per my understanding)
    * Load balancers - Nginx
    * API Gateway - Kong GW
    * Application server - Business logic code
    * Web server - Apache HTTP
    * Containerisation solution/Orchestration - K8/Docker etc.
    * Service Discovery - Netflix Eureka 
        * Client side
        * Server side 
    * Security Components - Firewalls/Identity and access management -  Ping 
    * Networking components (Softwares) - DNS / NAT / VPCs / Internet Gateways / Direct Connect 
    * Databases  

## Important concepts
1. Distributed Tracing - Mechanism to monitor the end to end request flow when it moves from on API to another API. It helps to identify the slowness/failures in Microservice flow. 
    * It can monitor - 
        * Time the service took
        * Logs 
        * Consumption of cpu and memory per request - HARD. 
        * Other Metadata 
    * Span - 
        * Trace id (Context)- Unique id for each request.
        * Span id - Unique id give to each service/component in request flow. 
        * Flow -
            * User Request → API Gateway → Auth Service → Payment Service → Database                                Span 1                Span 2                   Span 3                Span 4

## Possible approches to capture the traces :
1. Using agent on services - We can use OpenTelemetry automatic instrumentation as Approach_1. 
2. Embed the code directly in codebase - Not possible for big codebase. Backup_Approch
    * Write an interceptor in Microservice code ? 
    * What about API Gateways/Load balancers ?
        * Check how Dynatrace agent is capturing - 
        * Any way to monitor In and out traffic -
            * If so, Figure out which in out traffic data will come in traces ?
                * Will there be headers in request from which we can fetch trace id ?  

## Approach_1 [References](https://chatgpt.com/share/687be96c-cb2c-8010-a7c4-9ff0935c79a8)sds
1. Component to use
    * (Configuration) Opentelemetry agent - To collect traces
        * Java : opentelemetry-javaagent.jar 
        * Python : opentelemetry-instrument python manage.py runserver
        * NGINX : modules/ngx_http_opentelemetry_module.so; make sure the compiled version should be having this. 
    * (Development) Kafka Bridge between agent and kafka. 
    * (Configuration) Opentelemetry Collector - To convert the protobuf into json encoded within protobuf. OTLP - Open Telemetry Protocol. Works over http
    * (Development) Custom converter - Json encoded with protobuf to json
    * (Development) Custom Distributed Tracing App (DT APP) - to consume file from 
    * (Development) Kafka cluster to connect different components. 
2. Flow
App
  └──> OpenTelemetry Agent
         └──> OTLP-Kafka Bridge (Protobuf)
                 └──> Kafka Topic: otlp-protobuf
                         └──> OpenTelemetry Collector
                                 └──> Kafka Topic: otlp-json-protobuf
                                         └──> Custom JSON Converter
                                                 └──> Kafka Topic: clean-json
                                                         └──> Distributed Tracing App
                                                                 └──> DB