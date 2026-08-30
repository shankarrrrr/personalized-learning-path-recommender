# Frontend Dockerfile - multi-stage build.
# Stage 1 builds the Vite bundle; Stage 2 serves the static assets with nginx.

FROM node:20-alpine AS builder

WORKDIR /build

# Install deps with the lockfile for reproducible installs.
COPY package.json package-lock.json ./
RUN npm ci

# Build with the backend API URL baked in at build time.
ARG VITE_API_BASE_URL=http://localhost:8000
ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}

COPY . .
RUN npm run build

# ---- runtime: nginx serves the static bundle ----
FROM nginx:alpine AS runtime

# Copy the SPA build into nginx's document root.
COPY --from=builder /build/dist /usr/share/nginx/html

# nginx config that SPA-routes unknown paths to index.html so React Router works.
RUN printf 'server {\n\
    listen 80;\n\
    server_name _;\n\
    root /usr/share/nginx/html;\n\
    index index.html;\n\
    location / { try_files $uri $uri/ /index.html; }\n\
}\n' > /etc/nginx/conf.d/default.conf

EXPOSE 80

# nginx healthcheck.
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget -qO- http://127.0.0.1/ >/dev/null 2>&1 || exit 1

CMD ["nginx", "-g", "daemon off;"]
