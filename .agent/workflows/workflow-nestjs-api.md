---
description: Step-by-step guide for building NestJS REST APIs.
---

1. **Project Scaffolding**

    Initialize project using NestJS CLI.

    // turbo

    ```bash
    # Verify CLI installed
    npm list -g @nestjs/cli || npm install -g @nestjs/cli
    ```

    ```bash
    nest new my-nest-project
    # Select package manager (npm/pnpm/yarn)
    ```

2. **Generate Resources**

    Create module, controller, and service structure.

    // turbo

    ```bash
    # Generate Users resource
    nest g resource modules/users --no-spec
    ```

3. **Define DTOs (Data Transfer Objects)**

    Create validation schemas in `dto/`.

    ```typescript
    // create-user.dto.ts
    import { IsString, IsEmail, MinLength } from 'class-validator';

    export class CreateUserDto {
      @IsEmail()
      readonly email: string;

      @IsString()
      @MinLength(8)
      readonly password: string;
    }
    ```

4. **Implement Service**

    Add business logic in `users.service.ts`.

    ```typescript
    import { Injectable } from '@nestjs/common';
    import { CreateUserDto } from './dto/create-user.dto';

    @Injectable()
    export class UsersService {
      private users = [];

      create(createUserDto: CreateUserDto) {
        const user = { id: Date.now(), ...createUserDto };
        this.users.push(user);
        return user;
      }
    }
    ```

5. **Implement Controller**

    Define endpoints in `users.controller.ts`.

    ```typescript
    import { Controller, Post, Body } from '@nestjs/common';
    import { UsersService } from './users.service';
    import { CreateUserDto } from './dto/create-user.dto';

    @Controller('users')
    export class UsersController {
      constructor(private readonly usersService: UsersService) {}

      @Post()
      create(@Body() createUserDto: CreateUserDto) {
        return this.usersService.create(createUserDto);
      }
    }
    ```

6. **Validation Setup**

    Enable global validation pipe in `main.ts`.

    ```typescript
    app.useGlobalPipes(new ValidationPipe());
    ```

// turbo
7. **Run and Test**

    Start server and enable watch mode.

    ```bash
    npm run start:dev
    ```
