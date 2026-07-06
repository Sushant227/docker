############################
# Stage 1 - Build
############################
FROM maven:3.9.11-eclipse-temurin-21 AS builder
WORKDIR /build
COPY pom.xml .
RUN mvn dependency:go-offline
COPY src ./src
#to build jar file out of source code (/src)
RUN mvn clean package -DskipTests 
############################
# Stage 2 - Runtime
############################
FROM eclipse-temurin:21-jre
RUN groupadd -r spring && \
    useradd -r -g spring spring
WORKDIR /app
COPY --from=builder \
    /build/target/*.jar \
    app.jar
RUN chown spring:spring app.jar
USER spring
EXPOSE 8080
ENTRYPOINT ["java","-jar","app.jar"]
