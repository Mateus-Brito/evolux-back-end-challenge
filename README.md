# Telecom Carrier, the challenge Solution.

Read more about the challenge here: [Telecom Carrier, the backend project.](https://github.com/EvoluxBR/back-end-test)

### Postman project

[Download exported Postman project](https://github.com/Mateus-Brito/evolux-back-end-challenge/files/9834898/evolux_backend.postman_collection.zip)

### Running the production environment

```bash
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml run --rm web flask db upgrade
docker-compose -f docker-compose.prod.yml up -d
```

### Running the dev environment

```bash
docker-compose build
docker-compose run --rm web flask db upgrade
docker-compose up -d
```

### Running the tests

```bash
docker-compose run --rm web flask test
```

------------------------------------------------------------------------------------------

#### Authentication

<details>
 <summary><code>POST</code> <code><b>/auth/login</b></code> <code>(Get credentials access)</code></summary>

##### Parameters

> | name      |  type     | data type               | description                                                           |
> |-----------|-----------|-------------------------|-----------------------------------------------------------------------|
> | username  |  required | string                  | The registered username                                          |
> | password  |  required | string                  | The registered password                                          |


##### Responses

> | http code     | content-type                      | response                                                            |
> |---------------|-----------------------------------|---------------------------------------------------------------------|
> | `200`         | `application/json`                | `{"access_token": access_token, "refresh_token": refresh_token}`    |
> | `400`         | `application/json`                | `{"message": "Missing JSON in request"}`                            |
> | `400`         | `application/json`                | `{"message": "Missing username or password"}`                       |
> | `400`         | `application/json`                | `{"message": "Bad credentials"}`                                    |

##### Example cURL

> ```javascript
> curl -X POST -H "Content-Type: application/json" -d '{"username": "admin", "password": "123456789"}' http://127.0.0.1:8000/auth/login
> ```

</details>

<details>
 <summary><code>POST</code> <code><b>/auth/refresh</b></code> <code>(Refresh access token)</code></summary>

##### Parameters

> None

##### Responses

> | http code     | content-type                      | response                                                  |
> |---------------|-----------------------------------|-----------------------------------------------------------|
> | `200`         | `application/json`                | `{"access_token": "new token"}`                           |
> | `401`         | `application/json`                | `{"message": "Token has been revoked"}`                   |

##### Example cURL

> ```javascript
> curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer {refresh_token}" http://127.0.0.1:8000/auth/refresh
> ```

</details>

<details>
 <summary><code>DELETE</code> <code><b>/auth/revoke_refresh</b></code> <code>(Revoke refresh token)</code></summary>

##### Parameters

> None

##### Responses

> | http code     | content-type                      | response                                                  |
> |---------------|-----------------------------------|-----------------------------------------------------------|
> | `200`         | `application/json`                | `{"message": "token revoked"}`                            |
> | `401`         | `application/json`                | `{"message": "Token has been revoked"}`                   |

##### Example cURL

> ```javascript
> curl -X DELETE -H "Content-Type: application/json" -H "Authorization: Bearer {refresh_token}" http://127.0.0.1:8000/auth/revoke_refresh
> ```

</details>

<details>
 <summary><code>DELETE</code> <code><b>/auth/revoke_access</b></code> <code>(Revoke access token)</code></summary>

##### Parameters

> None

##### Responses

> | http code     | content-type                      | response                                                  |
> |---------------|-----------------------------------|-----------------------------------------------------------|
> | `200`         | `application/json`                | `{"message": "token revoked"}`                            |
> | `401`         | `application/json`                | `{"message": "Token has been revoked"}`                   |

##### Example cURL

> ```javascript
> curl -X DELETE -H "Content-Type: application/json" -H "Authorization: Bearer {refresh_token}" http://127.0.0.1:8000/auth/revoke_access
> ```

</details>

------------------------------------------------------------------------------------------

#### User

<details>
 <summary><code>GET</code> <code><b>/api/users/self</b></code> <code>(get current authenticated user)</code></summary>

##### Headers

> | name           |  value                 | description                                                                   |
> |----------------|------------------------|-------------------------------------------------------------------------------|
> | Authorization  |  Bearer `access_token` | The user access_token                                                  |

##### Parameters

> None

##### Responses

> | http code     | content-type                      | response                                                            |
> |---------------|-----------------------------------|---------------------------------------------------------------------|
> | `200`         | `application/json`                | YAML string                                                         |

##### Example cURL

> ```javascript
> curl -X GET -H "Content-Type: application/json" -H "Authorization: Bearer {access_token}" http://127.0.0.1:8000/api/users/self
> ```

</details>

<details>
 <summary><code>POST</code> <code><b>/api/users/signup</b></code> <code>(Create new user account)</code></summary>

##### Parameters

> | name      |  type     | data type               | description                                                           |
> |-----------|-----------|-------------------------|-----------------------------------------------------------------------|
> | username  |  required | string                  | The registered user username                                          |
> | password  |  required | string                  | The registered user password                                          |


##### Responses

> | http code     | content-type                      | response                                                            |
> |---------------|-----------------------------------|---------------------------------------------------------------------|
> | `200`         | `application/json`                | `{"access_token": access_token, "refresh_token": refresh_token}`    |
> | `400`         | `application/json`                | `{"message": "Missing JSON in request"}`                            |
> | `400`         | `application/json`                | `{"message": "Missing username or password"}`                       |
> | `400`         | `application/json`                | `{"message": "Bad credentials"}`                                    |

##### Example cURL

> ```javascript
> curl -X POST -H "Content-Type: application/json" -d '{"username":"admin", "email":"admin@example.com", "password": "123456789"}' http://127.0.0.1:8000/api/users/signup
> ```
</details>

------------------------------------------------------------------------------------------

#### Phones records

<details>
 <summary><code>GET</code> <code><b>/api/phones</b></code> <code>(get availables phones)</code></summary>

##### Headers

> | name           |  value                 | description                                                                   |
> |----------------|------------------------|-------------------------------------------------------------------------------|
> | Authorization  |  Bearer `access_token` | The user access_token                                                         |

##### Parameters

> | name      |  type     | data type               | description                                                           |
> |-----------|-----------|-------------------------|-----------------------------------------------------------------------|
> | page      |  optional | int                     | The page number                                                       |

##### Responses

> | http code     | content-type                      | response                                                            |
> |---------------|-----------------------------------|---------------------------------------------------------------------|
> | `200`         | `application/json`                | `{ "count": 0, "next": None, "previous": None, "results": [] }`     |

##### Example cURL

> ```javascript
> curl -X GET -H "Content-Type: application/json" -H "Authorization: Bearer {access_token}" http://127.0.0.1:8000/api/phones/
> ```

</details>

<details>
 <summary><code>GET</code> <code><b>/api/phones/{id}</b></code> <code>(get phone by id)</code></summary>

##### Headers

> | name           |  value                 | description                                                                   |
> |----------------|------------------------|-------------------------------------------------------------------------------|
> | Authorization  |  Bearer `access_token` | The user access_token                                                         |

##### Parameters

> None

##### Responses

> | http code     | content-type                      | response                                                            |
> |---------------|-----------------------------------|---------------------------------------------------------------------|
> | `200`         | `application/json`                | `{ "id": "1", "value": "+55 84 91234-4321", "monthyPrice": "0.03", "setupPrice": "3.40", "currency": "US", }`    |

##### Example cURL

> ```javascript
> curl -X GET -H "Content-Type: application/json" -H "Authorization: Bearer {access_token}" http://127.0.0.1:8000/api/phones/{id}
> ```

</details>

<details>
 <summary><code>POST</code> <code><b>/api/phones</b></code> <code>(create new phone)</code></summary>

##### Headers

> | name           |  value                 | description                                                                   |
> |----------------|------------------------|-------------------------------------------------------------------------------|
> | Authorization  |  Bearer `access_token` | The user access_token                                                         |

##### Parameters

> | name         |  type      | data type               | description                                                       |
> |--------------|------------|-------------------------|-------------------------------------------------------------------|
> | value        |  required  | string                  | The phone number                                                  |
> | monthyPrice  |  required  | string                  | The monthy price                                                  |
> | setupPrice   |  required  | string                  | The setup price                                                   |
> | currency     |  required  | string                  | The currency                                                      |

##### Responses

> | http code     | content-type                      | response                                                            |
> |---------------|-----------------------------------|---------------------------------------------------------------------|
> | `200`         | `application/json`       | `{ "id": "1", "value": "+55 84 91234-4321", "monthyPrice": "0.03", "setupPrice": "3.40", "currency": "US" }`     |
> | `400`         | `application/json`       | `{ "errors": {"value": ["There is already a phone with this value."]} }`     |
> | `400`         | `application/json`       | `{ "errors": {"value": ["Please, enter with a valid phone number."]} }`      |
> | `400`         | `application/json`       | `{ "errors": {"monthyPrice": ["Value must be greater than 0."]} }`           |
> | `400`         | `application/json`       | `{ "errors": {"setupPrice": ["Value must be greater than 0."]} }`            |
> | `400`         | `application/json`       | `{ "errors": {"currency": ["There is no currency with code."]} }`            |

##### Example cURL

> ```javascript
> curl -X POST -d '{ "value": "+55 84 91234-4321", "monthyPrice": "0.03", "setupPrice": "3.40", "currency": "US" }' -H "Content-Type: application/json" -H "Authorization: Bearer {access_token}" http://127.0.0.1:8000/api/phones/
> ```

</details>

<details>
 <summary><code>PUT</code> <code><b>/api/phones/{id}</b></code> <code>(update phone)</code></summary>

##### Headers

> | name           |  value                 | description                                                                   |
> |----------------|------------------------|-------------------------------------------------------------------------------|
> | Authorization  |  Bearer `access_token` | The user access_token                                                         |

##### Parameters

> | name         |  type      | data type               | description                                                       |
> |--------------|------------|-------------------------|-------------------------------------------------------------------|
> | value        |  required  | string                  | The phone number                                                  |
> | monthyPrice  |  required  | string                  | The monthy price                                                  |
> | setupPrice   |  required  | string                  | The setup price                                                   |
> | currency     |  required  | string                  | The currency                                                      |

##### Responses

> | http code     | content-type                      | response                                                            |
> |---------------|-----------------------------------|---------------------------------------------------------------------|
> | `200`         | `application/json`       | `{ "id": "1", "value": "+55 84 91234-4321", "monthyPrice": "0.03", "setupPrice": "3.40", "currency": "US" }`     |
> | `400`         | `application/json`       | `{ "errors": {"value": ["There is already a phone with this value."]} }`     |
> | `400`         | `application/json`       | `{ "errors": {"value": ["Please, enter with a valid phone number."]} }`      |
> | `400`         | `application/json`       | `{ "errors": {"monthyPrice": ["Value must be greater than 0."]} }`           |
> | `400`         | `application/json`       | `{ "errors": {"setupPrice": ["Value must be greater than 0."]} }`            |
> | `400`         | `application/json`       | `{ "errors": {"currency": ["There is no currency with code."]} }`            |

##### Example cURL

> ```javascript
> curl -X PUT -d '{ "value": "+55 84 91234-4321", "monthyPrice": "0.03", "setupPrice": "3.40", "currency": "US" }' -H "Content-Type: application/json" -H "Authorization: Bearer {access_token}" http://127.0.0.1:8000/api/phones/{id}
> ```

</details>

<details>
 <summary><code>DELETE</code> <code><b>/api/phones/{id}</b></code> <code>(delete phone)</code></summary>

##### Headers

> | name           |  value                 | description                                                                   |
> |----------------|------------------------|-------------------------------------------------------------------------------|
> | Authorization  |  Bearer `access_token` | The user access_token                                                         |

##### Parameters

> None

##### Responses

> | http code     | content-type                      | response                                                            |
> |---------------|-----------------------------------|---------------------------------------------------------------------|
> | `200`         | `application/json`                | `{ "message": "Phone deleted." }`                                   |
> | `400`         | `application/json`                | `{ "message": "Phone not found." }`                              |

##### Example cURL

> ```javascript
> curl -X DELETE -H "Content-Type: application/json" -H "Authorization: Bearer {access_token}" http://127.0.0.1:8000/api/phones/{id}
> ```

</details>

------------------------------------------------------------------------------------------

#### Currencies records

<details>
 <summary><code>GET</code> <code><b>/api/currencies</b></code> <code>(get availables currencies)</code></summary>

##### Headers

> | name           |  value                 | description                                                                   |
> |----------------|------------------------|-------------------------------------------------------------------------------|
> | Authorization  |  Bearer `access_token` | The user access_token                                                         |

##### Parameters

> | name      |  type     | data type               | description                                                           |
> |-----------|-----------|-------------------------|-----------------------------------------------------------------------|
> | page      |  optional | int                     | The page number                                                       |

##### Responses

> | http code     | content-type                      | response                                                            |
> |---------------|-----------------------------------|---------------------------------------------------------------------|
> | `200`         | `application/json`                | `{ "count": 0, "next": None, "previous": None, "results": [] }`     |

##### Example cURL

> ```javascript
> curl -X GET -H "Content-Type: application/json" -H "Authorization: Bearer {access_token}" http://127.0.0.1:8000/api/currencies/
> ```

</details>

<details>
 <summary><code>GET</code> <code><b>/api/currencies/{code}</b></code> <code>(get currency by code)</code></summary>

##### Headers

> | name           |  value                 | description                                                                   |
> |----------------|------------------------|-------------------------------------------------------------------------------|
> | Authorization  |  Bearer `access_token` | The user access_token                                                         |

##### Parameters

> None

##### Responses

> | http code     | content-type                      | response                                                            |
> |---------------|-----------------------------------|---------------------------------------------------------------------|
> | `200`         | `application/json`                | `{ "code": "US", "name": "Dollar" }`                                |

##### Example cURL

> ```javascript
> curl -X GET -H "Content-Type: application/json" -H "Authorization: Bearer {access_token}" http://127.0.0.1:8000/api/currencies/{code}
> ```

</details>

<details>
 <summary><code>POST</code> <code><b>/api/currencies</b></code> <code>(create new currency)</code></summary>

##### Headers

> | name           |  value                 | description                                                                   |
> |----------------|------------------------|-------------------------------------------------------------------------------|
> | Authorization  |  Bearer `access_token` | The user access_token                                                         |

##### Parameters

> | name         |  type      | data type               | description                                                       |
> |--------------|------------|-------------------------|-------------------------------------------------------------------|
> | code         |  required  | string                  | The currency code                                                 |
> | name         |  required  | string                  | The currency namee                                                |

##### Responses

> | http code     | content-type             | response                                                                     |
> |---------------|--------------------------|------------------------------------------------------------------------------|
> | `200`         | `application/json`       | `{"code": "US", "name": "Dollar"}`                                           |
> | `400`         | `application/json`       | `{ "errors": {"code": ["Missing data for required field."]} }`               |
> | `400`         | `application/json`       | `{ "errors": {"name": ["Missing data for required field."]} }`               |
> | `400`         | `application/json`       | `{ "errors": {"code": ["There is already a currency with this code."]} }`    |

##### Example cURL

> ```javascript
> curl -X POST -d '{ "code": "US", "name": "Dollar" }' -H "Content-Type: application/json" -H "Authorization: Bearer {access_token}" http://127.0.0.1:8000/api/currencies/
> ```

</details>

<details>
 <summary><code>PUT</code> <code><b>/api/currencies/{code}</b></code> <code>(update currency)</code></summary>

##### Headers

> | name           |  value                 | description                                                                   |
> |----------------|------------------------|-------------------------------------------------------------------------------|
> | Authorization  |  Bearer `access_token` | The user access_token                                                         |

##### Parameters

> | name         |  type      | data type               | description                                                       |
> |--------------|------------|-------------------------|-------------------------------------------------------------------|
> | code         |  required  | string                  | The currency code                                                 |
> | name         |  required  | string                  | The currency namee                                                |

##### Responses

> | http code     | content-type                      | response                                                            |
> |---------------|-----------------------------------|---------------------------------------------------------------------|
> | `200`         | `application/json`       | `{"code": "US", "name": "Dollar"}`                                           |
> | `400`         | `application/json`       | `{ "errors": {"code": ["Missing data for required field."]} }`               |
> | `400`         | `application/json`       | `{ "errors": {"name": ["Missing data for required field."]} }`               |
> | `400`         | `application/json`       | `{ "errors": {"code": ["There is already a currency with this code."]} }`    |
> | `400`         | `application/json`       | `{ "message": "Currency not found" }`    |

##### Example cURL

> ```javascript
> curl -X PUT -d '{ "code": "US", "name": "Dollar" }' -H "Content-Type: application/json" -H "Authorization: Bearer {access_token}" http://127.0.0.1:8000/api/currencies/{code}
> ```

</details>

<details>
 <summary><code>DELETE</code> <code><b>/api/currencies/{code}</b></code> <code>(delete currency)</code></summary>

##### Headers

> | name           |  value                 | description                                                                   |
> |----------------|------------------------|-------------------------------------------------------------------------------|
> | Authorization  |  Bearer `access_token` | The user access_token                                                         |

##### Parameters

> None

##### Responses

> | http code     | content-type                      | response                                                            |
> |---------------|-----------------------------------|---------------------------------------------------------------------|
> | `200`         | `application/json`                | `{ "message": "Currency deleted." }`                                   |
> | `400`         | `application/json`                | `{ "message": "Currency not found." }`                              |

##### Example cURL

> ```javascript
> curl -X DELETE -H "Content-Type: application/json" -H "Authorization: Bearer {access_token}" http://127.0.0.1:8000/api/currencies/{code}
> ```

</details> 
