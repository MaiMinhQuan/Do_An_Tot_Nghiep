# ⚡ QUICK START - Development Workflow

## 🚀 Khởi Động Lần Đầu

```bash
# 1. Cài đặt dependencies
cd backend
npm install

# 2. Tạo file .env
cp .env.example .env
# Sửa file .env và thêm GEMINI_API_KEY của bạn

# 3. Start Docker containers (MongoDB + Redis)
npm run docker:up

# 4. Start development server
npm run start:dev
```

✅ Server chạy tại: `http://localhost:3000`

---

## 🔄 Khởi Động Hàng Ngày

```bash
# Start Docker containers
npm run docker:up

# Start dev server
npm run start:dev
```

---

## 📝 Khi Thay Đổi Schema (Database Models)

### ✅ **KHÔNG CẦN làm gì!**

MongoDB + Mongoose tự động apply schema mới:
1. Sửa file schema (VD: `user.schema.ts`)
2. Server tự động restart (vì đang chạy `--watch` mode)
3. ✨ Schema mới được áp dụng ngay!

**KHÔNG CẦN chạy migration như SQL!**

### 🔄 Nếu muốn reset database (xóa toàn bộ data)
```bash
npm run docker:reset
```

---

## 🛠️ NPM Scripts Hữu Ích

### Development
```bash
npm run start:dev      # Chạy server với watch mode
npm run start:debug    # Chạy với debugger
npm run build          # Build production
npm run start:prod     # Chạy production build
```

### Docker Management
```bash
npm run docker:up      # Start MongoDB + Redis (hoặc tạo mới nếu chưa có)
npm run docker:down    # Stop containers (giữ data)
npm run docker:reset   # Xóa containers và tạo mới (MẤT DATA)
npm run docker:logs    # Xem logs của MongoDB và Redis
```

### Database Tools
```bash
npm run db:shell       # Vào MongoDB shell
npm run redis:cli      # Vào Redis CLI
```

### Code Quality
```bash
npm run lint           # Chạy ESLint
npm run format         # Format code với Prettier
```

---

## 🗄️ Xem Data Trong Database

### MongoDB Shell
```bash
npm run db:shell

# Trong Mongo Shell:
use ielts-writing-db
show collections
db.users.find().pretty()
db.submissions.find().pretty()
exit
```

### Redis CLI
```bash
npm run redis:cli

# Trong Redis:
KEYS *
GET some_key
exit
```

---

## 🐛 Troubleshooting

### Server không restart khi sửa code
```bash
# Ctrl+C để stop
npm run start:dev
```

### MongoDB không kết nối được
```bash
# Check container
docker ps | grep mongodb

# Restart
docker restart mongodb

# Hoặc reset
npm run docker:reset
```

### Port đã được sử dụng
```bash
# Windows: Tìm process đang dùng port
netstat -ano | findstr :3000
netstat -ano | findstr :27017

# Kill process hoặc đổi PORT trong .env
```

---

## 📦 Khi Thêm Dependency Mới

```bash
# Install package
npm install package-name

# Restart server (Ctrl+C rồi)
npm run start:dev
```

---

## 🛑 Dừng Mọi Thứ

```bash
# Ctrl+C trong terminal đang chạy server

# Stop Docker containers
npm run docker:down
```

---

## 📚 Chi Tiết Hơn?

Xem các file:
- **DATABASE_GUIDE.md** - Hướng dẫn quản lý database chi tiết
- **ROADMAP.md** - Lộ trình phát triển dự án
- **README.md** - Tổng quan dự án

---

**TÓM TẮT:**
1. ✏️ Sửa schema → Server tự restart → ✅ Xong!
2. 🔄 Không cần chạy migration
3. 📊 Muốn xem data: `npm run db:shell`
4. 🗑️ Muốn reset: `npm run docker:reset`
