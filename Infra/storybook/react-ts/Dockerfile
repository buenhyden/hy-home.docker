# Build Stage
FROM node:23-alpine AS build-stage

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build-storybook

# Production Stage
FROM nginx:stable-alpine AS production-stage

COPY --from=build-stage /app/storybook-static /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]