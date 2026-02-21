---
description: Populate your database with realistic test data
---

1. **Install Faker**:
   - Generate realistic fake data.
   // turbo
   - Run `npm install --save-dev @faker-js/faker`

2. **Create Seed Script**:
   - Create `prisma/seed.ts`.

   ```ts
   import { PrismaClient } from '@prisma/client';
   import { faker } from '@faker-js/faker';

   const prisma = new PrismaClient();

   async function main() {
     // Clear existing data
     await prisma.post.deleteMany();
     await prisma.user.deleteMany();

     // Create 10 users
     const users = await Promise.all(
       Array.from({ length: 10 }).map(() =>
         prisma.user.create({
           data: {
             email: faker.internet.email(),
             name: faker.person.fullName(),
             avatar: faker.image.avatar(),
           },
         })
       )
     );

     // Create 50 posts
     await Promise.all(
       Array.from({ length: 50 }).map(() =>
         prisma.post.create({
           data: {
             title: faker.lorem.sentence(),
             content: faker.lorem.paragraphs(3),
             authorId: faker.helpers.arrayElement(users).id,
           },
         })
       )
     );

     console.log('✅ Database seeded successfully');
   }

   main()
     .catch(console.error)
     .finally(() => prisma.$disconnect());
   ```

3. **Configure package.json**:
   - Add seed command.

   ```json
   {
     "prisma": {
       "seed": "ts-node --compiler-options {\"module\":\"CommonJS\"} prisma/seed.ts"
     },
     "scripts": {
       "db:seed": "prisma db seed"
     }
   }
   ```

4. **Run Seed**:
   - Populate your database.
   // turbo
   - Run `npm run db:seed`

5. **Reset Database**:
   - Wipe and re-seed.
   // turbo
   - Run `npx prisma migrate reset` (runs seed automatically)

6. **Pro Tips**:
   - Create different seed files for dev/staging/test.
   - Use deterministic seeds for consistent testing.
   - Seed only in development; never in production!
   - Consider using snapshots of production data (anonymized).
