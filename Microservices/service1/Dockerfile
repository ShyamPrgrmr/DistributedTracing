FROM maven:latest AS build
WORKDIR /app
COPY . .
RUN mvn clean package -DskipTests

FROM bitnami/java:latest
WORKDIR /app
COPY --from=build /app/target/service1-0.0.1-SNAPSHOT.jar app.jar
COPY --from=build /app/agent/opentelemetry-javaagent.jar opentelemetry-javaagent.jar
ENTRYPOINT ["java","-javaagent:opentelemetry-javaagent.jar","-jar","/app/app.jar"]
