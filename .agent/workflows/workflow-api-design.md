---
description: Design RESTful API with OpenAPI specification and best practices
---

1. **Define API requirements**

    Document API endpoints, resources, and operations needed.

    **Identify resources:**
    - Users
    - Products
    - Orders
    - etc.

    **Determine operations:**
    - CRUD operations (Create, Read, Update, Delete)
    - Custom actions (search, filter, bulk operations)
    - Relationships (user's orders, product reviews)

2. **Choose API design approach**

    Select REST, GraphQL, or both based on requirements.

    **REST API:**
    - ✅ Simple CRUD operations
    - ✅ Caching friendly
    - ✅ Wide tooling support

    **GraphQL:**
    - ✅ Complex data requirements
    - ✅ Multiple related resources
    - ✅ Mobile-first (reduce over-fetching)

    **Recommendation**: Start with REST for most cases.

3. **Design URL structure**

    Create consistent, RESTful URL patterns.

    **Best practices:**

    ```text
    # Resources (plural nouns)
    GET    /api/v1/users          # List users
    POST   /api/v1/users          # Create user
    GET    /api/v1/users/{id}     # Get specific user
    PUT    /api/v1/users/{id}     # Update user
    DELETE /api/v1/users/{id}     # Delete user

    # Nested resources
    GET    /api/v1/users/{id}/orders        # User's orders
    GET    /api/v1/products/{id}/reviews    # Product reviews

    # Query parameters for filtering/sorting
    GET    /api/v1/users?role=admin&sort=created_at&order=desc

    # Pagination
    GET    /api/v1/users?page=2&limit=20
    ```

    **Avoid:**
    - ❌ Verbs in URLs: `/api/getUsers`, `/api/createUser`
    - ❌ Inconsistent pluralization
    - ❌ Deep nesting (> 2 levels)

4. **Create OpenAPI specification**

    Document API using OpenAPI 3.0 specification.

    Create `openapi.yaml`:

    ```yaml
    openapi: 3.0.0
    info:
      title: My API
      version: 1.0.0
      description: API for managing users and products

    servers:
      - url: https://api.example.com/v1
        description: Production server
      - url: http://localhost:3000/v1
        description: Development server

    paths:
      /users:
        get:
          summary: List all users
          tags:
            - Users
          parameters:
            - in: query
              name: page
              schema:
                type: integer
                default: 1
            - in: query
              name: limit
              schema:
                type: integer
                default: 20
          responses:
            '200':
              description: Successful response
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      data:
                        type: array
                        items:
                          $ref: '#/components/schemas/User'
                      pagination:
                        $ref: '#/components/schemas/Pagination'
        
        post:
          summary: Create a new user
          tags:
            - Users
          requestBody:
            required: true
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/CreateUserRequest'
          responses:
            '201':
              description: User created
              content:
                application/json:
                  schema:
                    $ref: '#/components/schemas/User'
            '400':
              $ref: '#/components/responses/BadRequest'

      /users/{userId}:
        get:
          summary: Get user by ID
          tags:
            - Users
          parameters:
            - in: path
              name: userId
              required: true
              schema:
                type: string
          responses:
            '200':
              description: User found
              content:
                application/json:
                  schema:
                    $ref: '#/components/schemas/User'
            '404':
              $ref: '#/components/responses/NotFound'

    components:
      schemas:
        User:
          type: object
          properties:
            id:
              type: string
              format: uuid
            email:
              type: string
              format: email
            name:
              type: string
            createdAt:
              type: string
              format: date-time
          required:
            - id
            - email
            - name

        CreateUserRequest:
          type: object
          properties:
            email:
              type: string
              format: email
            name:
              type: string
            password:
              type: string
              minLength: 8
          required:
            - email
            - name
            - password

        Pagination:
          type: object
          properties:
            page:
              type: integer
            limit:
              type: integer
            total:
              type: integer
            pages:
              type: integer

        Error:
          type: object
          properties:
            error:
              type: string
            message:
              type: string
            details:
              type: array
              items:
                type: object

      responses:
        BadRequest:
          description: Bad request
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
        
        NotFound:
          description: Resource not found
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'

      securitySchemes:
        BearerAuth:
          type: http
          scheme: bearer
          bearerFormat: JWT

    security:
      - BearerAuth: []
    ```

5. **Generate API documentation**

    Create interactive API docs from OpenAPI spec.

    // turbo

    ```bash
    # Using Swagger UI
    npm install swagger-ui-express
    ```

    **For Express.js:**

    ```javascript
    const swaggerUi = require('swagger-ui-express');
    const YAML = require('yamljs');
    const swaggerDocument = YAML.load('./openapi.yaml');

    app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocument));
    ```

    **For FastAPI (automatic):**

    ```python
    from fastapi import FastAPI

    app = FastAPI(
        title="My API",
        description="API for managing users and products",
        version="1.0.0"
    )

    # Docs available at /docs (Swagger UI) and /redoc (ReDoc)
    ```

    Access docs at: `http://localhost:3000/api-docs`

6. **Define error responses**

    Standardize error response format.

    **Error response structure:**

    ```json
    {
      "error": "ValidationError",
      "message": "Invalid input data",
      "details": [
        {
          "field": "email",
          "message": "Invalid email format"
        },
        {
          "field": "password",
          "message": "Password must be at least 8 characters"
        }
      ],
      "timestamp": "2024-01-11T10:30:00Z",
      "path": "/api/v1/users"
    }
    ```

    **HTTP status codes:**
    - 200: Success
    - 201: Created
    - 204: No Content
    - 400: Bad Request (validation error)
    - 401: Unauthorized
    - 403: Forbidden
    - 404: Not Found
    - 409: Conflict (duplicate resource)
    - 422: Unprocessable Entity
    - 429: Too Many Requests (rate limit)
    - 500: Internal Server Error

7. **Implement versioning strategy**

    Add API versioning for backward compatibility.

    **URL versioning (recommended):**

    ```text
    /api/v1/users
    /api/v2/users
    ```

    **Header versioning:**

    ```text
    GET /api/users
    Accept: application/vnd.myapi.v1+json
    ```

    **Implementation:**

    ```javascript
    // Express.js
    const v1Router = require('./routes/v1');
    const v2Router = require('./routes/v2');

    app.use('/api/v1', v1Router);
    app.use('/api/v2', v2Router);
    ```

8. **Add rate limiting**

    Protect API from abuse.

    ```bash
    npm install express-rate-limit
    ```

    ```javascript
    const rateLimit = require('express-rate-limit');

    const limiter = rateLimit({
      windowMs: 15 * 60 * 1000, // 15 minutes
      max: 100, // Limit each IP to 100 requests per windowMs
      message: 'Too many requests, please try again later',
    });

    app.use('/api/', limiter);
    ```

9. **Implement pagination**

    Add pagination for list endpoints.

    **Cursor-based pagination (recommended for large datasets):**

    ```typescript
    interface PaginationParams {
      cursor?: string;
      limit?: number;
    }

    interface PaginatedResponse<T> {
      data: T[];
      nextCursor?: string;
      hasMore: boolean;
    }

    // Example response
    {
      "data": [...],
      "nextCursor": "eyJpZCI6MTIzfQ==",
      "hasMore": true
    }
    ```

    **Offset-based pagination (simpler):**

    ```typescript
    interface PaginationParams {
      page: number;
      limit: number;
    }

    interface PaginatedResponse<T> {
      data: T[];
      pagination: {
        page: number;
        limit: number;
        total: number;
        pages: number;
      };
    }
    ```

10. **Add authentication and authorization**

    Secure API endpoints.

    **JWT Authentication:**

    ```javascript
    const jwt = require('jsonwebtoken');

    function authenticateToken(req, res, next) {
      const authHeader = req.headers['authorization'];
      const token = authHeader && authHeader.split(' ')[1];

      if (!token) {
        return res.status(401).json({ error: 'No token provided' });
      }

      jwt.verify(token, process.env.JWT_SECRET, (err, user) => {
        if (err) {
          return res.status(403).json({ error: 'Invalid token' });
        }
        req.user = user;
        next();
      });
    }

    // Use middleware
    app.get('/api/v1/users', authenticateToken, getUsers);
    ```

11. **Validate requests**

    Add input validation.

    **Using Zod (TypeScript):**

    ```typescript
    import { z } from 'zod';

    const createUserSchema = z.object({
      email: z.string().email(),
      name: z.string().min(1).max(100),
      password: z.string().min(8),
    });

    app.post('/api/v1/users', async (req, res) => {
      try {
        const validatedData = createUserSchema.parse(req.body);
        // Create user with validated data
      } catch (error) {
        if (error instanceof z.ZodError) {
          return res.status(400).json({
            error: 'ValidationError',
            details: error.errors,
          });
        }
      }
    });
    ```

12. **Test API endpoints**

    Create automated tests for API.

    ```typescript
    import request from 'supertest';
    import app from './app';

    describe('Users API', () => {
      it('GET /api/v1/users should return users list', async () => {
        const response = await request(app)
          .get('/api/v1/users')
          .expect(200);

        expect(response.body.data).toBeInstanceOf(Array);
      });

      it('POST /api/v1/users should create user', async () => {
        const newUser = {
          email: 'test@example.com',
          name: 'Test User',
          password: 'password123',
        };

        const response = await request(app)
          .post('/api/v1/users')
          .send(newUser)
          .expect(201);

        expect(response.body.email).toBe(newUser.email);
      });

      it('POST /api/v1/users should validate email', async () => {
        const invalidUser = {
          email: 'invalid-email',
          name: 'Test',
          password: 'pass123',
        };

        await request(app)
          .post('/api/v1/users')
          .send(invalidUser)
          .expect(400);
      });
    });
    ```

    // turbo

    ```bash
    npm test
    ```

    **Next Steps:**
    - Review `agent/rules/200-Backend` for backend best practices
    - Add API monitoring (e.g., Sentry, Datadog)
    - Implement CORS properly for frontend access
    - Add request/response logging
    - Setup API analytics
    - Consider GraphQL for complex data requirements
