# article feed app

The service provides a RESTful API that allows you to create a feed of articles for users.


## Technical stack, technologies

- Python 3.10
- Django
- Django Rest Framework
- PostgreSQL


## Application API

### 1. User registration
Creates new user.
The ability to create a user with the 'author' role was added only for testing.

```
POST /api/users/registrate
```

**Body**

| Name     | Type  | Description                  | Required field |
|----------|-------|------------------------------|----------------|
| email    | Email | mail                         | +              |
| password | Char  | password                     | +              |
| role     | Char  | subscriber(S) or author(A).  | +              |


**Response**

| Name    | Description          |
|---------|----------------------|
| success | successful execution |
| user    | user email           |

### 2. Articles (list and creation)

2.1 Returns all articles to users with the author and subscriber roles, and only public articles are issued to unauthorized users.

```
GET /api/articles
```

2.2 Creates an article.
Only the author is able to create an article.

```
POST /api/articles
```

**Body**

| Name      | Type    | Description         | Required field |
|-----------|---------|---------------------|----------------|
| title     | Char    | article title       | +              |
| content   | Char    | text                | -              |
| is_locked | Boolean | public article flag | -              |

**Response**


| Name    | Description          |
|---------|----------------------|
| success | successful execution |
| article | article title        |


2.3 Returns the article to users with the author and subscriber roles, and only the public article is issued to unauthorized users.

```
GET /api/articles/{id}
```

{id} - Article id.

2.4 Edits the article.
The author who created the article can edit it.

```
[PUT, PATCH] /api/articles/{id}
```
{id} - Article id.

**Body**

| Name      | Type    | Description         |
|-----------|---------|---------------------|
| title     | Char    | article title       |
| content   | Char    | text                |
| is_locked | Boolean | public article flag |

2.5 Deletes the article.
The author who created the article can delete it.
```
DELETE /api/articles/{id}
```
{id} - Article id.
