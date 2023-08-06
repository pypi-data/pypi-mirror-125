
<h1 align="center">AioMeiliSearch </h1>

<p align="center"> The MeiliSearch API asyncio client for Python </p>

## Introduction

**AioMeilisearch**  is a asynchronous python client for MeiliSearch.

[MeiliSearch](https://www.meilisearch.com) is an open source, blazingly fast and hyper relevant search-engine.
For more information about features in this [documentation](https://docs.meilisearch.com/).

### Summary 

MeiliSearch's API is a standard **RESTful HTTP API**, so it comes with SDKs for all kinds of programing languages.
One official python client is called [meilisearch-python](https://github.com/meilisearch/meilisearch-python), 
it does a good job, with a great python http library called [requests](https://docs.python-requests.org/en/latest/).

**async/await** is new feature of python3.4+. In some cases we need to support this feature, so here we are.

**AioMeilisearch** supprts async/await, writed with [aiohttp](https://github.com/aio-libs/aiohttp). 

Any python api in the [MeiliSearch officia document](https://docs.meilisearch.com) has a **awaitable** version by **AioMeilisearch**.

### Feature

- **async/await**

## Requirements

- python3.6+
- aiohttp

## Installation

```bash
pip3 install aiomeilisearch
```

## Usage

**Index**
```python
import aiomeilisearch

client = aiomeilisearch.Client('http://127.0.0.1:7700', 'masterKey')

async def create_index():
    # create a index, with primaryKey "id"
    # An index is where the documents are stored.
    return await client.create_index('movies', {'primaryKey': 'id'})

index = await create_index()
```
**Documents**
```python
async def add_documents():
    # add documents to index
    documents = [
          { 'id': 1, 'title': 'Carol', 'genres': ['Romance', 'Drama'] },
          { 'id': 2, 'title': 'Wonder Woman', 'genres': ['Action', 'Adventure'] },
          { 'id': 3, 'title': 'Life of Pi', 'genres': ['Adventure', 'Drama'] },
          { 'id': 4, 'title': 'Mad Max: Fury Road', 'genres': ['Adventure', 'Science Fiction'] },
          { 'id': 5, 'title': 'Moana', 'genres': ['Fantasy', 'Action']},
          { 'id': 6, 'title': 'Philadelphia', 'genres': ['Drama'] },
    ]
    await index.add_documents(documents) 
```
**Get a document**
```python
await index.get_document(1)
```
**Search documents**
```python
await client.index("movies").search('飞天大盗')
await client.index("movies").search('The Great Gatsby', filter=["is_tv=True", ["year=1925", "year=2013"]])
```

**settings**

```python
await client.index('movies').get_settings()
await client.index('movies').update_displayed_attributes(["id", 'title', 'year'])
await client.index('movies').update_filterable_attributes(["year", 'is_tv'])
await client.index('movies').update_searchable_attributes(['title', 'original_title', ])
...
```

### Demos

[https://github.com/ziyoubaba/aiomeilisearch/tree/main/demos](https://github.com/ziyoubaba/aiomeilisearch/tree/main/demos)

### Documentation

- [MeiliSearch](https://docs.meilisearch.com/) all the python apis here. Don't forget 'await'. 
- **AioMeilisearch**, Maybe later...

### License

Under MIT license.

## Changelog 

##### version 1.0.0

- based with the [version v0.23.0 of MeiliSearch](https://github.com/meilisearch/MeiliSearch/releases/tag/v0.23.0).

### welcom contribution

- 

### Source code

The latest developer version is available in a GitHub repository: [https://github.com/ziyoubaba/aiomeilisearch](https://github.com/ziyoubaba/aiomeilisearch)




