# Outline-gigachat searcher

AI accelerated searcher for [outline](https://github.com/outline/outline)

## Requirements:
- Docker
- [Qdrant](https://qdrant.tech/)
- GigaChat API Key. You can get one [here](https://developers.sber.ru/portal/products/gigachat-api)

## Build:

```sh
docker build --network host .
```

## Run:
```sh
docker run  docker run -p 8000:8000 -p :6333 -e OUTLINE_TOKEN=${OUTLINE_TOKEN} -e OUTLINE_COLLECTION_ID=${OUTLINE_COLLECTION_ID} -e OUTLINE_API_URL=${OUTLINE_API_URL} -e QDRANT_URL=${QDRANT_URL} -e GIGACHAT_CREDENTIALS=${GIGACHAT_CREDENTIALS} ${CONTAINER_ID}
```

---

[MIT License](./LICENSE)
