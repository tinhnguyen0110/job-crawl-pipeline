# Dockerfile (cho frontend - phiên bản cập nhật)

# Stage 1: Build React app
FROM node:18-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Serve app with Nginx
FROM nginx:1.25-alpine
# Copy các file đã build từ stage 1
COPY --from=builder /app/dist /usr/share/nginx/html

# === DÒNG MỚI ĐƯỢC THÊM VÀO ===
# Sao chép file cấu hình Nginx tùy chỉnh vào container
# Nó sẽ ghi đè lên file cấu hình mặc định của Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]