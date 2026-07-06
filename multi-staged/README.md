# demo

Minimal Spring Boot 3 (Java 21) application set up to build with the included
multi-stage `Dockerfile`.

## Project structure

```
project/
├── Dockerfile
├── pom.xml
├── .dockerignore
├── README.md
└── src/
    └── main/
        ├── java/com/example/demo/
        │   ├── DemoApplication.java
        │   └── controller/HelloController.java
        └── resources/
            └── application.properties
```

## Build and run locally (without Docker)

```bash
mvn clean package
java -jar target/app.jar
```

Then visit http://localhost:8080/ and http://localhost:8080/health.

## Build and run with Docker

From inside the `project` folder:

```bash
docker build -t demo-app .
docker run -p 8080:8080 demo-app
```

Then visit http://localhost:8080/.

### How the Dockerfile works

- **Stage 1 (builder)**: uses `maven:3.9.11-eclipse-temurin-21` to resolve
  dependencies (`mvn dependency:go-offline`) and package the app into
  `target/app.jar` (name fixed via `<finalName>app</finalName>` in `pom.xml`),
  skipping tests for a faster image build.
- **Stage 2 (runtime)**: uses the slim `eclipse-temurin:21-jre` image, creates
  a non-root `spring` user/group, copies only the built jar from stage 1,
  and runs the app as that non-root user on port `8080`.
