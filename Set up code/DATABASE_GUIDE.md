# 🗄️ DATABASE MANAGEMENT GUIDE

## MongoDB + Mongoose trong NestJS

### ⚡ Điểm Khác Biệt với SQL
MongoDB là **schemaless database**, nên:
- ✅ **KHÔNG CẦN migration** khi thay đổi schema
- ✅ Mongoose schema chỉ áp dụng validation ở application layer
- ✅ Documents cũ vẫn tồn tại với cấu trúc cũ
- ✅ Documents mới sẽ follow schema mới

---

## 🔄 Workflow Khi Thay Đổi Schema

### 1️⃣ Sửa Schema File (VD: user.schema.ts)
```typescript
// Thêm field mới
@Prop()
phoneNumber?: string;
```

### 2️⃣ Server Tự Động Restart
```bash
# npm run start:dev đang watch, không cần làm gì
# Nếu không tự restart:
# Ctrl+C rồi npm run start:dev lại
```

### 3️⃣ Schema Mới Được Áp Dụng
- ✅ Documents mới sẽ có field `phoneNumber`
- ⚠️ Documents cũ KHÔNG tự động có field này
- ✅ Query vẫn hoạt động bình thường (undefined cho field mới)

---

## 🛠️ Các Lệnh Quản Lý Database

### 🚀 Khởi động lần đầu
```bash
cd backend
npm install

# Start Docker containers
docker run -d -p 27017:27017 --name mongodb mongo:latest
docker run -d -p 6379:6379 --name redis redis:latest

# Copy .env và cập nhật GEMINI_API_KEY
cp .env.example .env
# Chỉnh sửa .env với editor

# Run development server
npm run start:dev
```

### 🔄 Khởi động hàng ngày
```bash
# Check containers đã chạy chưa
docker ps

# Nếu chưa chạy, start lại
docker start mongodb redis

# Run dev server
cd backend
npm run start:dev
```

### 🗑️ Reset Database (Xóa toàn bộ data)
```bash
# Option 1: Xóa container và tạo mới (Nhanh nhất)
docker stop mongodb
docker rm mongodb
docker run -d -p 27017:27017 --name mongodb mongo:latest

# Option 2: Xóa database qua Mongo Shell
docker exec -it mongodb mongosh
> use ielts-writing-db
> db.dropDatabase()
> exit
```

### 🔍 Xem data trong MongoDB
```bash
# Vào Mongo Shell
docker exec -it mongodb mongosh

# Chọn database
> use ielts-writing-db

# List tất cả collections
> show collections

# Xem documents trong collection
> db.users.find().pretty()
> db.submissions.find().pretty()

# Count documents
> db.users.countDocuments()

# Xóa một collection
> db.users.drop()

# Thoát
> exit
```

### 🔍 Xem data trong Redis
```bash
# Vào Redis CLI
docker exec -it redis redis-cli

# Xem tất cả keys
> KEYS *

# Xem value của một key
> GET key_name

# Xóa tất cả keys (DANGER!)
> FLUSHALL

# Thoát
> exit
```

### 🛑 Dừng containers
```bash
# Dừng nhưng giữ data
docker stop mongodb redis

# Dừng và xóa containers (Mất data)
docker stop mongodb redis
docker rm mongodb redis
```

### 📊 Kiểm tra trạng thái
```bash
# Xem containers đang chạy
docker ps

# Xem logs
docker logs mongodb
docker logs redis

# Xem resource usage
docker stats mongodb redis
```

---

## 🌱 Seed Data (Sẽ tạo ở Giai đoạn 8)

### Script seed.ts (Coming soon)
```bash
# Seed sample data
npm run seed

# Seed specific collection
npm run seed:topics
npm run seed:courses
npm run seed:questions
```

---

## ⚠️ Migration Data Thủ Công (Nếu Cần)

### Trường hợp: Bạn muốn thêm field mới vào TẤT CẢ documents cũ

**Option 1: Dùng Mongoose migration script**
```typescript
// scripts/migrate-add-phone.ts
import { User } from './schemas/user.schema';

async function migrate() {
  await User.updateMany(
    { phoneNumber: { $exists: false } },
    { $set: { phoneNumber: null } }
  );
}
```

**Option 2: Dùng MongoDB Update**
```bash
docker exec -it mongodb mongosh
> use ielts-writing-db
> db.users.updateMany(
    { phoneNumber: { $exists: false } },
    { $set: { phoneNumber: null } }
  )
```

**⚠️ Thông thường KHÔNG CẦN làm này! Mongoose sẽ handle undefined fields.**

---

## 🐛 Troubleshooting

### Lỗi: "Cannot connect to MongoDB"
```bash
# Check MongoDB đang chạy
docker ps | grep mongodb

# Restart MongoDB
docker restart mongodb

# Check logs
docker logs mongodb
```

### Lỗi: "Redis connection refused"
```bash
# Check Redis đang chạy
docker ps | grep redis

# Restart Redis
docker restart redis

# Check logs
docker logs redis
```

### Lỗi: "Port already in use"
```bash
# Tìm process đang dùng port
# Windows:
netstat -ano | findstr :27017
netstat -ano | findstr :6379

# Kill process hoặc đổi port trong .env
```

### NestJS không restart khi sửa schema
```bash
# Ctrl+C để dừng server
# Chạy lại
npm run start:dev

# Hoặc dùng --watch flag
nest start --watch
```

---

## 📚 Best Practices

### ✅ DO:
- Commit code sau mỗi thay đổi schema
- Document schema changes trong comments
- Test với dữ liệu mẫu sau khi thay đổi
- Backup production DB trước khi deploy thay đổi lớn

### ❌ DON'T:
- Xóa field đang được sử dụng trong production
- Thay đổi type của field có data (string → number)
- Thêm required field cho collection đã có data
- Run seed scripts trên production database

---

## 📖 Tài Liệu Tham Khảo

- [Mongoose Schema Guide](https://mongoosejs.com/docs/guide.html)
- [MongoDB CRUD Operations](https://www.mongodb.com/docs/manual/crud/)
- [Docker MongoDB](https://hub.docker.com/_/mongo)
- [NestJS Mongoose](https://docs.nestjs.com/techniques/mongodb)

---

**TÓM LẠI:** Với MongoDB, bạn chỉ cần:
1. ✏️ Sửa schema trong code
2. 💾 Server tự động restart (npm run start:dev)
3. ✅ Schema mới được áp dụng ngay!

**KHÔNG CẦN chạy migration hay sync database!**
