---
trigger: always_on
glob: "**/*.ts"
description: "NestJS: Modules, Dependency Injection, and Guards."
---
# NestJS Standards

## 1. Modules & Injection

- **Encapsulation**: Each feature (`UsersModule`) should declare its own controllers/providers.
- **Constructor Injection**: Use `private readonly` in constructor.

### Example: Service

**Good**

```ts
@Injectable()
export class UserService {
  constructor(
    @InjectRepository(User)
    private repo: Repository<User>
  ) {}
}
```

**Bad**

```ts
@Injectable()
export class UserService {
  repo = new Repository(User); // No DI, hard to test
}
```

## 2. DTOs & Validation

- **Pipes**: Use global `ValidationPipe`.
- **Class Validator**: Use decorators (`@IsString()`) on DTO classes.

### Example: DTO

**Good**

```ts
export class CreateUserDto {
  @IsEmail()
  email: string;
}
```

**Bad**

```ts
export class CreateUserDto {
  email: any; // No validation
}
```
