#!/bin/bash
docker run -it --name postgres-ono -e POSTGRES_PASSWORD=1q2w3e -p 5432:5432 -d postgres
