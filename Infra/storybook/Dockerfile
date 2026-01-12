# Stage 1: Build
FROM node:20-alpine AS build-stage

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 설치를 위해 패키지 파일 복사
COPY package*.json ./
RUN npm install

# 전체 소스 코드 복사 및 스토리북 빌드
COPY . .
RUN npm run build-storybook

# Stage 2: Serve
FROM nginx:stable-alpine AS production-stage

# 빌드된 결과물을 Nginx 기본 정적 파일 경로로 복사
COPY --from=build-stage /app/storybook-static /usr/share/nginx/html

# Nginx 설정 파일 커스텀 (필요시)
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# 80 포트 노출
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]