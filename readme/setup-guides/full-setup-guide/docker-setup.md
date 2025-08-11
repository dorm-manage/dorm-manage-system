# Docker Setup

The easiest way to run the application is using Docker. We provide automated scripts for setup.

see [readme-docker](../readme-docker/ "mention") for more detailed instructions.



### Option 1: Automated Setup (Recommended)

```
# Development mode
./scripts/docker-translation-setup.sh dev

# Production mode
./scripts/docker-translation-setup.sh
```



### Option 2: Manual Docker Setup

**Step 1: Build and Start Containers**

```
# Build and start all services
docker-compose up --build
```

**Step 2: Access the Application**

* **Development**: [http://localhost:8080](http://localhost:8080/)
* **Production**: [http://localhost:80](http://localhost/)



### Option 3: Update with Latest Changes

If you've made changes to translations or code:

```
./scripts/update-docker-translations.sh
```

\
