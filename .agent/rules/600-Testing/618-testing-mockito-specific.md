---
trigger: always_on
glob: "**/*.java"
description: "Mockito: Mocking, Stubbing, Verification, and Best Practices."
---
# Mockito Standards

## 1. Mock Creation

- **@Mock**: Use annotation with `@ExtendWith(MockitoExtension.class)`.
- **@InjectMocks**: Auto-inject mocks into the class under test.

### Example: Setup

**Good**

```java
@ExtendWith(MockitoExtension.class)
class UserServiceTest {
    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private UserService userService;

    @Test
    void shouldFindUser() {
        when(userRepository.findById(1L)).thenReturn(Optional.of(new User("Alice")));
        User user = userService.getUser(1L);
        assertThat(user.getName()).isEqualTo("Alice");
    }
}
```

**Bad**

```java
// Creating mocks manually everywhere
UserRepository mockRepo = Mockito.mock(UserRepository.class);
```

## 2. Stubbing

- **when().thenReturn()**: For return values.
- **when().thenThrow()**: For exception testing.
- **doAnswer()**: For complex custom logic.

### Example: Stubbing

**Good**

```java
when(repo.save(any(User.class))).thenAnswer(invocation -> {
    User user = invocation.getArgument(0);
    user.setId(1L);
    return user;
});
```

## 3. Verification

- **verify()**: Confirm method was called.
- **times()**: Verify exact call count.
- **never()**: Verify method was NOT called.

### Example: Verify

**Good**

```java
verify(userRepository, times(1)).findById(1L);
verify(emailService, never()).sendEmail(any());
```

## 4. Argument Matchers

- **any()**: Match any argument.
- **eq()**: Match exact value.
- **argThat()**: Custom matcher.

## 5. Avoid Over-Mocking

- **Real Objects**: Use real objects when possible.
- **Spies**: Use `@Spy` for partial mocking.
