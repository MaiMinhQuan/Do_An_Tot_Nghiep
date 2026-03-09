# 🗺️ ROADMAP PHÁT TRIỂN FRONTEND
## IELTS Writing Task 2 E-Learning Platform

---

## 📋 TỔNG QUAN DỰ ÁN

**Tech Stack:**
- **Framework:** Next.js 14+ (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS + shadcn/ui
- **State Management:** Zustand + React Query (TanStack Query)
- **API Client:** Axios với Interceptors
- **Authentication:** Next-Auth v5 + JWT
- **Real-time:** Socket.IO Client
- **Form Handling:** React Hook Form + Zod
- **Charts:** Recharts
- **Rich Text Editor:** TipTap
- **Deployment:** Vercel

**API Backend:**
- Base URL: `http://localhost:3000/api`
- WebSocket: `http://localhost:3000`
- Tích hợp với NestJS Backend (xem ROADMAP_backend.md)

---

## ✅ **GIAI ĐOẠN 1: THIẾT LẬP DỰ ÁN & CORE INFRASTRUCTURE**
### Ước tính: 3-4 giờ

### 1.1. Khởi tạo Project
```bash
npx create-next-app@latest ielts-writing-frontend --typescript --tailwind --app --src-dir
cd ielts-writing-frontend
```

### 1.2. Cài đặt Dependencies
- [ ] Cài đặt core libraries:
```bash
npm install axios zustand @tanstack/react-query
npm install react-hook-form zod @hookform/resolvers
npm install next-auth@beta socket.io-client
npm install lucide-react class-variance-authority clsx tailwind-merge
npm install date-fns recharts
```

- [ ] Cài đặt shadcn/ui:
```bash
npx shadcn-ui@latest init
npx shadcn-ui@latest add button input card dialog form toast
npx shadcn-ui@latest add dropdown-menu table tabs badge progress
npx shadcn-ui@latest add select label textarea separator skeleton
npx shadcn-ui@latest add alert tooltip
```

- [ ] Cài đặt dev dependencies:
```bash
npm install -D @types/node @types/react prettier eslint-config-prettier
```

### 1.3. Tạo Folder Structure
- [ ] Tạo cấu trúc thư mục:
```
src/
├── app/
│   ├── (auth)/               # Authentication routes
│   │   ├── login/page.tsx
│   │   ├── register/page.tsx
│   │   └── layout.tsx
│   ├── (dashboard)/          # Protected student routes
│   │   ├── dashboard/page.tsx
│   │   ├── courses/
│   │   ├── lessons/
│   │   ├── essays/
│   │   ├── practice/
│   │   ├── submissions/
│   │   ├── notebook/
│   │   ├── flashcards/
│   │   └── layout.tsx
│   ├── (admin)/              # Admin routes
│   │   ├── admin/
│   │   │   ├── topics/
│   │   │   ├── courses/
│   │   │   ├── lessons/
│   │   │   ├── questions/
│   │   │   └── users/
│   │   └── layout.tsx
│   ├── api/
│   │   └── auth/[...nextauth]/route.ts
│   ├── layout.tsx
│   ├── page.tsx              # Landing page
│   └── globals.css
├── components/
│   ├── ui/                   # shadcn/ui components
│   ├── layouts/
│   │   ├── navbar.tsx
│   │   ├── sidebar.tsx
│   │   ├── footer.tsx
│   │   └── admin-sidebar.tsx
│   ├── auth/
│   ├── course/
│   ├── lesson/
│   ├── practice/
│   ├── essay/
│   └── shared/
├── lib/
│   ├── api/
│   │   ├── axios-client.ts
│   │   ├── auth.api.ts
│   │   ├── courses.api.ts
│   │   ├── lessons.api.ts
│   │   ├── essays.api.ts
│   │   ├── practice.api.ts
│   │   └── submissions.api.ts
│   ├── hooks/
│   │   ├── useAuth.ts
│   │   ├── useCourses.ts
│   │   ├── useSubmissions.ts
│   │   └── useWebSocket.ts
│   ├── store/
│   │   ├── auth-store.ts
│   │   ├── ui-store.ts
│   │   └── practice-store.ts
│   ├── utils/
│   │   ├── cn.ts
│   │   ├── format.ts
│   │   └── validators.ts
│   └── types/
│       ├── auth.types.ts
│       ├── course.types.ts
│       ├── lesson.types.ts
│       ├── essay.types.ts
│       ├── practice.types.ts
│       └── submission.types.ts
├── config/
│   ├── site.ts
│   └── api.ts
└── middleware.ts
```

### 1.4. Environment Configuration
- [ ] Tạo file `.env.local`:
```bash
NEXT_PUBLIC_API_URL=http://localhost:3000/api
NEXT_PUBLIC_WS_URL=http://localhost:3000
NEXTAUTH_SECRET=your-super-secret-key-change-in-production
NEXTAUTH_URL=http://localhost:3001
```

### 1.5. Axios Client Setup
- [ ] Tạo `lib/api/axios-client.ts`:
```typescript
import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  headers: { 'Content-Type': 'application/json' },
});

// Request Interceptor: Thêm JWT token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response Interceptor: Handle 401
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default apiClient;
```

### 1.6. TypeScript Types
- [ ] Tạo `lib/types/auth.types.ts`:
```typescript
export enum UserRole {
  STUDENT = 'STUDENT',
  ADMIN = 'ADMIN',
}

export interface User {
  id: string;
  email: string;
  fullName: string;
  role: UserRole;
  targetBand?: number;
  createdAt: Date;
}

export interface LoginDto {
  email: string;
  password: string;
}

export interface RegisterDto {
  email: string;
  password: string;
  fullName: string;
  targetBand?: number;
}

export interface AuthResponse {
  access_token: string;
  user: User;
}
```

- [ ] Tạo các types còn lại (course, lesson, essay, submission)

### 1.7. Tailwind Config
- [ ] Cấu hình `tailwind.config.js`:
```javascript
module.exports = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#3b82f6',
          50: '#eff6ff',
          500: '#3b82f6',
          600: '#2563eb',
        },
        severity: {
          minor: '#fef3c7',
          moderate: '#fed7aa',
          critical: '#fecaca',
        },
      },
    },
  },
};
```

**Output Giai đoạn 1:**
- ✅ Project Next.js setup hoàn chỉnh
- ✅ Folder structure rõ ràng
- ✅ Dependencies được cài đặt
- ✅ Axios client với interceptors
- ✅ TypeScript types đầy đủ
- ✅ Environment variables configured

---

## 🚧 **GIAI ĐOẠN 2: AUTHENTICATION & AUTHORIZATION**
### Ước tính: 3-4 giờ

### 2.1. Next-Auth Configuration
- [ ] Tạo `app/api/auth/[...nextauth]/route.ts`:
```typescript
import NextAuth from 'next-auth';
import CredentialsProvider from 'next-auth/providers/credentials';
import apiClient from '@/lib/api/axios-client';

export const authOptions = {
  providers: [
    CredentialsProvider({
      name: 'Credentials',
      credentials: {
        email: { label: "Email", type: "email" },
        password: { label: "Password", type: "password" }
      },
      async authorize(credentials) {
        try {
          const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/login`, {
            method: 'POST',
            body: JSON.stringify(credentials),
            headers: { "Content-Type": "application/json" }
          });

          const data = await response.json();
          if (response.ok && data) {
            return {
              id: data.user.id,
              email: data.user.email,
              name: data.user.fullName,
              role: data.user.role,
              accessToken: data.access_token,
            };
          }
          return null;
        } catch (error) {
          return null;
        }
      }
    })
  ],
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.accessToken = user.accessToken;
        token.role = user.role;
        token.id = user.id;
      }
      return token;
    },
    async session({ session, token }) {
      session.user.id = token.id;
      session.user.role = token.role;
      session.accessToken = token.accessToken;
      return session;
    }
  },
  pages: {
    signIn: '/login',
  },
  session: {
    strategy: 'jwt',
  },
};

const handler = NextAuth(authOptions);
export { handler as GET, handler as POST };
```

### 2.2. Auth Store (Zustand)
- [ ] Tạo `lib/store/auth-store.ts`:
```typescript
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import apiClient from '@/lib/api/axios-client';

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  register: (data: RegisterDto) => Promise<void>;
  setUser: (user: User) => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,

      login: async (email, password) => {
        const response = await apiClient.post('/auth/login', { email, password });
        const { access_token, user } = response.data;
        localStorage.setItem('access_token', access_token);
        set({ user, token: access_token, isAuthenticated: true });
      },

      logout: () => {
        localStorage.removeItem('access_token');
        set({ user: null, token: null, isAuthenticated: false });
      },

      register: async (data) => {
        const response = await apiClient.post('/auth/register', data);
        return response.data;
      },

      setUser: (user) => set({ user }),
    }),
    {
      name: 'auth-storage',
      partialize: (state) => ({
        user: state.user,
        token: state.token,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);
```

### 2.3. Auth API
- [ ] Tạo `lib/api/auth.api.ts`:
```typescript
import apiClient from './axios-client';
import { LoginDto, RegisterDto, AuthResponse } from '@/lib/types/auth.types';

export const authApi = {
  login: async (data: LoginDto): Promise<AuthResponse> => {
    const response = await apiClient.post('/auth/login', data);
    return response.data;
  },

  register: async (data: RegisterDto): Promise<AuthResponse> => {
    const response = await apiClient.post('/auth/register', data);
    return response.data;
  },

  getProfile: async () => {
    const response = await apiClient.get('/users/profile');
    return response.data;
  },
};
```

### 2.4. Login Page
- [ ] Tạo `app/(auth)/login/page.tsx`:
```typescript
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { useAuthStore } from '@/lib/store/auth-store';
import { toast } from '@/components/ui/use-toast';

const loginSchema = z.object({
  email: z.string().email('Email không hợp lệ'),
  password: z.string().min(6, 'Mật khẩu tối thiểu 6 ký tự'),
});

export default function LoginPage() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const login = useAuthStore((state) => state.login);

  const form = useForm({
    resolver: zodResolver(loginSchema),
    defaultValues: { email: '', password: '' },
  });

  const onSubmit = async (data: z.infer<typeof loginSchema>) => {
    setIsLoading(true);
    try {
      await login(data.email, data.password);
      toast({ title: 'Đăng nhập thành công!', variant: 'default' });
      router.push('/dashboard');
    } catch (error) {
      toast({ title: 'Lỗi đăng nhập', description: error.message, variant: 'destructive' });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center">
      <div className="w-full max-w-md space-y-6 p-8">
        <h1 className="text-2xl font-bold">Đăng nhập</h1>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
            <FormField
              control={form.control}
              name="email"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Email</FormLabel>
                  <FormControl>
                    <Input placeholder="your@email.com" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <FormField
              control={form.control}
              name="password"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Mật khẩu</FormLabel>
                  <FormControl>
                    <Input type="password" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            <Button type="submit" className="w-full" disabled={isLoading}>
              {isLoading ? 'Đang đăng nhập...' : 'Đăng nhập'}
            </Button>
          </form>
        </Form>
        <p className="text-center text-sm">
          Chưa có tài khoản?{' '}
          <a href="/register" className="text-primary hover:underline">
            Đăng ký ngay
          </a>
        </p>
      </div>
    </div>
  );
}
```

### 2.5. Register Page
- [ ] Tạo `app/(auth)/register/page.tsx` (tương tự Login)
- [ ] Form validation với Zod
- [ ] Call API `/auth/register`

### 2.6. Protected Route Middleware
- [ ] Tạo `middleware.ts`:
```typescript
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { getToken } from 'next-auth/jwt';

export async function middleware(request: NextRequest) {
  const token = await getToken({ req: request });

  const isAuthPage = request.nextUrl.pathname.startsWith('/login') ||
                     request.nextUrl.pathname.startsWith('/register');
  const isProtectedPage = request.nextUrl.pathname.startsWith('/dashboard') ||
                          request.nextUrl.pathname.startsWith('/practice') ||
                          request.nextUrl.pathname.startsWith('/admin');

  // Redirect unauthenticated users from protected pages
  if (isProtectedPage && !token) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  // Redirect authenticated users from auth pages
  if (isAuthPage && token) {
    return NextResponse.redirect(new URL('/dashboard', request.url));
  }

  // Admin-only routes
  if (request.nextUrl.pathname.startsWith('/admin') && token?.role !== 'ADMIN') {
    return NextResponse.redirect(new URL('/dashboard', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/dashboard/:path*', '/practice/:path*', '/admin/:path*', '/login', '/register'],
};
```

### 2.7. Auth Layout
- [ ] Tạo `app/(auth)/layout.tsx`:
```typescript
export default function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {children}
    </div>
  );
}
```

**Output Giai đoạn 2:**
- ✅ User có thể đăng ký tài khoản
- ✅ User có thể đăng nhập với JWT
- ✅ Protected routes với middleware
- ✅ Role-based access control (STUDENT/ADMIN)
- ✅ Token được lưu trong localStorage + Next-Auth session

---

## 🚧 **GIAI ĐOẠN 3: STUDENT DASHBOARD & COURSE SYSTEM**
### Ước tính: 4-5 giờ

### 3.1. Landing Page
- [ ] Tạo `app/page.tsx`:
  - Hero section với CTA
  - Features showcase (AI Grading, Courses, Practice)
  - Statistics (số học viên, số bài chấm, ...)
  - Testimonials
  - Footer với links

### 3.2. Dashboard Layout
- [ ] Tạo `app/(dashboard)/layout.tsx`:
```typescript
import Sidebar from '@/components/layouts/sidebar';
import Navbar from '@/components/layouts/navbar';

export default function DashboardLayout({ children }) {
  return (
    <div className="flex h-screen bg-gray-50">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Navbar />
        <main className="flex-1 overflow-y-auto p-6">
          {children}
        </main>
      </div>
    </div>
  );
}
```

- [ ] Tạo `components/layouts/sidebar.tsx`:
  - Dashboard
  - Courses
  - Practice
  - Submissions
  - Sample Essays
  - Notebook
  - Flashcards
  - User menu (Profile, Logout)

- [ ] Tạo `components/layouts/navbar.tsx`:
  - Breadcrumbs
  - Search bar
  - Notifications bell
  - User avatar dropdown

### 3.3. Dashboard Home
- [ ] Tạo `app/(dashboard)/dashboard/page.tsx`:
  - Welcome message với tên user
  - Learning progress card (số khóa học đã học, số bài đã làm)
  - Recent submissions (3 bài gần nhất)
  - Band score trend chart (Recharts)
  - Quick actions (Start Practice, Browse Courses)

### 3.4. Courses API
- [ ] Tạo `lib/api/courses.api.ts`:
```typescript
import apiClient from './axios-client';

export const coursesApi = {
  getAll: async (topicId?: string, isPublished?: boolean) => {
    const params = new URLSearchParams();
    if (topicId) params.append('topicId', topicId);
    if (isPublished !== undefined) params.append('isPublished', String(isPublished));

    const response = await apiClient.get(`/courses?${params}`);
    return response.data;
  },

  getOne: async (id: string) => {
    const response = await apiClient.get(`/courses/${id}`);
    return response.data;
  },
};
```

### 3.5. Topics & Courses Page
- [ ] Tạo `app/(dashboard)/courses/page.tsx`:
  - Topic filter sidebar (Environment, Education, Technology, ...)
  - Course grid view với CourseCard
  - Search bar
  - Filter by targetBand

- [ ] Tạo `components/course/course-card.tsx`:
```typescript
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';

interface CourseCardProps {
  course: {
    id: string;
    title: string;
    description: string;
    thumbnail: string;
    targetBand: string;
    lessonCount: number;
  };
}

export default function CourseCard({ course }: CourseCardProps) {
  return (
    <Card className="hover:shadow-lg transition-shadow cursor-pointer">
      <img src={course.thumbnail} alt={course.title} className="w-full h-48 object-cover" />
      <CardHeader>
        <div className="flex justify-between items-start">
          <CardTitle className="text-lg">{course.title}</CardTitle>
          <Badge>{course.targetBand}</Badge>
        </div>
      </CardHeader>
      <CardContent>
        <p className="text-sm text-gray-600 line-clamp-2">{course.description}</p>
        <p className="text-xs text-gray-500 mt-2">{course.lessonCount} bài học</p>
      </CardContent>
    </Card>
  );
}
```

### 3.6. Course Detail Page
- [ ] Tạo `app/(dashboard)/courses/[id]/page.tsx`:
  - Course header (title, description, targetBand)
  - Instructor info (nếu có)
  - Lessons list với accordions
  - Enroll/Continue button

### 3.7. Lessons API
- [ ] Tạo `lib/api/lessons.api.ts`:
```typescript
export const lessonsApi = {
  getByCourse: async (courseId: string, targetBand?: string) => {
    const params = new URLSearchParams();
    params.append('courseId', courseId);
    if (targetBand) params.append('targetBand', targetBand);

    const response = await apiClient.get(`/lessons?${params}`);
    return response.data;
  },

  getOne: async (id: string) => {
    const response = await apiClient.get(`/lessons/${id}`);
    return response.data;
  },
};
```

### 3.8. Lesson Detail Page
- [ ] Tạo `app/(dashboard)/lessons/[id]/page.tsx`:
  - Video player section (React Player hoặc HTML5 video)
  - Lesson content tabs:
    - Videos
    - Vocabularies (với audio pronunciation)
    - Grammars
    - Notes (personal notes)
  - Progress tracking (Mark as completed)

- [ ] Tạo `components/lesson/vocabulary-section.tsx`:
```typescript
interface VocabularyItem {
  word: string;
  pronunciation: string;
  meaning: string;
  example: string;
}

// Display vocabulary list với audio icons
// Add to flashcard button
```

- [ ] Tạo `components/lesson/grammar-section.tsx`:
  - Hiển thị grammar rules
  - Examples
  - Add to notebook button

### 3.9. React Query Integration
- [ ] Tạo `lib/hooks/useCourses.ts`:
```typescript
import { useQuery } from '@tanstack/react-query';
import { coursesApi } from '@/lib/api/courses.api';

export function useCourses(topicId?: string) {
  return useQuery({
    queryKey: ['courses', topicId],
    queryFn: () => coursesApi.getAll(topicId),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

export function useCourse(id: string) {
  return useQuery({
    queryKey: ['course', id],
    queryFn: () => coursesApi.getOne(id),
    enabled: !!id,
  });
}
```

- [ ] Tạo `lib/hooks/useLessons.ts` (tương tự)

**Output Giai đoạn 3:**
- ✅ Landing page đẹp với hero section
- ✅ Dashboard layout với sidebar + navbar
- ✅ Dashboard home với statistics
- ✅ Courses browsing với filters
- ✅ Course detail với lessons list
- ✅ Lesson detail với video, vocabularies, grammars
- ✅ React Query caching hoạt động

---

## 🚧 **GIAI ĐOẠN 4: SAMPLE ESSAYS & FAVORITES**
### Ước tính: 3 giờ

### 4.1. Sample Essays API
- [ ] Tạo `lib/api/essays.api.ts`:
```typescript
export const essaysApi = {
  getAll: async (topicId?: string, targetBand?: string) => {
    const params = new URLSearchParams();
    if (topicId) params.append('topicId', topicId);
    if (targetBand) params.append('targetBand', targetBand);

    const response = await apiClient.get(`/sample-essays?${params}`);
    return response.data;
  },

  getOne: async (id: string) => {
    const response = await apiClient.get(`/sample-essays/${id}`);
    return response.data;
  },
};

export const favoriteEssaysApi = {
  getAll: async () => {
    const response = await apiClient.get('/favorite-essays');
    return response.data;
  },

  add: async (essayId: string) => {
    const response = await apiClient.post('/favorite-essays', { essayId });
    return response.data;
  },

  remove: async (essayId: string) => {
    const response = await apiClient.delete(`/favorite-essays/${essayId}`);
    return response.data;
  },
};
```

### 4.2. Sample Essays Page
- [ ] Tạo `app/(dashboard)/essays/page.tsx`:
  - Essay cards grid
  - Filter by Topic (sidebar)
  - Filter by Band Score (dropdown)
  - Search functionality
  - Sort by (Date, Views, Band)

- [ ] Tạo `components/essay/essay-card.tsx`:
```typescript
<Card>
  <CardHeader>
    <div className="flex justify-between">
      <CardTitle>{essay.title}</CardTitle>
      <Badge variant={getBandColor(essay.band)}>{essay.band}</Badge>
    </div>
  </CardHeader>
  <CardContent>
    <p className="line-clamp-3 text-sm">{essay.content}</p>
    <div className="flex justify-between items-center mt-4">
      <span className="text-xs text-gray-500">{essay.viewCount} lượt xem</span>
      <Button variant="ghost" size="sm" onClick={handleFavorite}>
        <Heart className={isFavorited ? 'fill-red-500' : ''} />
      </Button>
    </div>
  </CardContent>
</Card>
```

### 4.3. Essay Detail Page
- [ ] Tạo `app/(dashboard)/essays/[id]/page.tsx`:
  - Essay header (title, band, topic)
  - Essay content với Error Highlighting
  - Highlight annotations với tooltips
  - Band breakdown (4 criteria với progress bars)
  - Examiner feedback section
  - Favorite button

### 4.4. Error Highlighting Component
- [ ] Tạo `components/essay/error-highlight.tsx`:
```typescript
interface HighlightAnnotation {
  startIndex: number;
  endIndex: number;
  category: string;
  severity: 'minor' | 'moderate' | 'critical';
  explanation: string;
  suggestion: string;
}

function highlightText(content: string, annotations: HighlightAnnotation[]) {
  // Sort by startIndex
  const sorted = [...annotations].sort((a, b) => a.startIndex - b.startIndex);

  let result: JSX.Element[] = [];
  let lastIndex = 0;

  sorted.forEach((annotation, idx) => {
    // Plain text before highlight
    if (lastIndex < annotation.startIndex) {
      result.push(<span key={`text-${idx}`}>{content.slice(lastIndex, annotation.startIndex)}</span>);
    }

    // Highlighted text with tooltip
    const highlightedText = content.slice(annotation.startIndex, annotation.endIndex);
    result.push(
      <Tooltip key={`highlight-${idx}`}>
        <TooltipTrigger>
          <mark className={`severity-${annotation.severity} cursor-help`}>
            {highlightedText}
          </mark>
        </TooltipTrigger>
        <TooltipContent>
          <div className="space-y-2">
            <Badge>{annotation.category}</Badge>
            <p className="text-sm font-semibold">{annotation.explanation}</p>
            {annotation.suggestion && (
              <p className="text-sm text-green-600">
                <strong>Gợi ý:</strong> {annotation.suggestion}
              </p>
            )}
          </div>
        </TooltipContent>
      </Tooltip>
    );

    lastIndex = annotation.endIndex;
  });

  // Remaining text
  if (lastIndex < content.length) {
    result.push(<span key="text-end">{content.slice(lastIndex)}</span>);
  }

  return result;
}

export default function EssayWithHighlights({ content, annotations }) {
  return (
    <div className="prose max-w-none">
      <TooltipProvider>
        {highlightText(content, annotations)}
      </TooltipProvider>
    </div>
  );
}
```

### 4.5. Favorites Page
- [ ] Tạo `app/(dashboard)/favorites/page.tsx`:
  - List of favorited essays
  - Remove from favorites button
  - Same filters as essays page

**Output Giai đoạn 4:**
- ✅ Sample essays browsing với filters
- ✅ Essay detail với highlighted errors (tooltips)
- ✅ Favorite/Unfavorite functionality
- ✅ Favorites management page
- ✅ Error highlighting với startIndex/endIndex từ backend

---

## 🚧 **GIAI ĐOẠN 5: NOTEBOOK & FLASHCARDS**
### Ước tính: 3 giờ

### 5.1. Notebook API
- [ ] Tạo `lib/api/notebook.api.ts`:
```typescript
export const notebookApi = {
  getAll: async () => {
    const response = await apiClient.get('/notebook');
    return response.data;
  },

  create: async (data: { title: string; content: string; tags?: string[] }) => {
    const response = await apiClient.post('/notebook', data);
    return response.data;
  },

  update: async (id: string, data: Partial<{ title: string; content: string; tags?: string[] }>) => {
    const response = await apiClient.patch(`/notebook/${id}`, data);
    return response.data;
  },

  delete: async (id: string) => {
    const response = await apiClient.delete(`/notebook/${id}`);
    return response.data;
  },
};
```

### 5.2. Notebook Page
- [ ] Tạo `app/(dashboard)/notebook/page.tsx`:
  - Notes grid view (Masonry layout)
  - Create new note button (dialog)
  - Search notes
  - Filter by tags
  - Sort by date

- [ ] Tạo `components/notebook/note-card.tsx`:
```typescript
<Card className="hover:shadow-md transition-shadow">
  <CardHeader>
    <div className="flex justify-between items-start">
      <CardTitle className="text-base">{note.title}</CardTitle>
      <DropdownMenu>
        <DropdownMenuTrigger><MoreVertical /></DropdownMenuTrigger>
        <DropdownMenuContent>
          <DropdownMenuItem onClick={handleEdit}>Sửa</DropdownMenuItem>
          <DropdownMenuItem onClick={handleDelete}>Xóa</DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  </CardHeader>
  <CardContent>
    <div className="prose prose-sm" dangerouslySetInnerHTML={{ __html: note.content }} />
    <div className="flex gap-1 mt-2">
      {note.tags?.map(tag => <Badge key={tag} variant="secondary">{tag}</Badge>)}
    </div>
  </CardContent>
</Card>
```

### 5.3. Note Editor Dialog
- [ ] Tạo `components/notebook/note-editor-dialog.tsx`:
  - TipTap rich text editor
  - Title input
  - Tags input (combobox)
  - Save/Cancel buttons

```typescript
import { useEditor, EditorContent } from '@tiptap/react';
import StarterKit from '@tiptap/starter-kit';
import Highlight from '@tiptap/extension-highlight';
import Link from '@tiptap/extension-link';

const editor = useEditor({
  extensions: [
    StarterKit,
    Highlight,
    Link,
  ],
  content: initialContent,
});

// Toolbar với Bold, Italic, Heading, List buttons
```

### 5.4. Flashcards API
- [ ] Tạo `lib/api/flashcards.api.ts`:
```typescript
export const flashcardsApi = {
  getAllSets: async () => {
    const response = await apiClient.get('/flashcard-sets');
    return response.data;
  },

  getSet: async (setId: string) => {
    const response = await apiClient.get(`/flashcard-sets/${setId}`);
    return response.data;
  },

  createSet: async (data: { name: string; description?: string }) => {
    const response = await apiClient.post('/flashcard-sets', data);
    return response.data;
  },

  addCard: async (setId: string, data: { front: string; back: string }) => {
    const response = await apiClient.post(`/flashcard-sets/${setId}/cards`, data);
    return response.data;
  },

  updateCard: async (cardId: string, data: { repetitions: number; easeFactor: number; interval: number }) => {
    const response = await apiClient.patch(`/flashcards/${cardId}`, data);
    return response.data;
  },
};
```

### 5.5. Flashcard Sets Page
- [ ] Tạo `app/(dashboard)/flashcards/page.tsx`:
  - Flashcard sets grid
  - Create new set button
  - Set card hiển thị số lượng cards, due cards

- [ ] Tạo `components/flashcard/set-card.tsx`:
```typescript
<Card>
  <CardHeader>
    <CardTitle>{set.name}</CardTitle>
  </CardHeader>
  <CardContent>
    <p className="text-sm text-gray-600">{set.description}</p>
    <div className="flex justify-between mt-4">
      <span>{set.cardCount} thẻ</span>
      <Button onClick={() => router.push(`/flashcards/${set.id}/study`)}>
        Ôn tập
      </Button>
    </div>
  </CardContent>
</Card>
```

### 5.6. Flashcard Study Mode
- [ ] Tạo `app/(dashboard)/flashcards/[setId]/study/page.tsx`:
  - Flashcard flip animation
  - Show front → User clicks "Show Answer" → Show back
  - User rates difficulty: Again (0), Hard (1), Good (2), Easy (3)
  - Update spaced repetition schedule (SM-2 algorithm)
  - Progress bar (X/Y cards)
  - Session complete screen với statistics

- [ ] Tạo `components/flashcard/flashcard-flip.tsx`:
```typescript
'use client';

import { useState } from 'react';
import { motion } from 'framer-motion'; // Optional: for smooth animation

export default function FlashcardFlip({ front, back, onRate }) {
  const [isFlipped, setIsFlipped] = useState(false);

  return (
    <div className="perspective">
      <motion.div
        className="card"
        animate={{ rotateY: isFlipped ? 180 : 0 }}
        transition={{ duration: 0.6 }}
      >
        <div className="card-front">
          <p className="text-2xl">{front}</p>
          <Button onClick={() => setIsFlipped(true)}>Hiện đáp án</Button>
        </div>
        <div className="card-back">
          <p className="text-xl">{back}</p>
          <div className="flex gap-2 mt-4">
            <Button variant="destructive" onClick={() => onRate(0)}>Lại</Button>
            <Button variant="outline" onClick={() => onRate(1)}>Khó</Button>
            <Button variant="secondary" onClick={() => onRate(2)}>Tốt</Button>
            <Button onClick={() => onRate(3)}>Dễ</Button>
          </div>
        </div>
      </motion.div>
    </div>
  );
}
```

### 5.7. Spaced Repetition Logic
- [ ] Tạo `lib/utils/spaced-repetition.ts`:
```typescript
interface Card {
  repetitions: number;
  easeFactor: number;
  interval: number;
  nextReview: Date;
}

export function calculateNextReview(card: Card, quality: 0 | 1 | 2 | 3): Card {
  // SM-2 Algorithm
  let { repetitions, easeFactor, interval } = card;

  if (quality >= 2) {
    // Correct response
    if (repetitions === 0) {
      interval = 1;
    } else if (repetitions === 1) {
      interval = 6;
    } else {
      interval = Math.round(interval * easeFactor);
    }
    repetitions += 1;
  } else {
    // Incorrect response
    repetitions = 0;
    interval = 1;
  }

  easeFactor = easeFactor + (0.1 - (3 - quality) * (0.08 + (3 - quality) * 0.02));
  if (easeFactor < 1.3) easeFactor = 1.3;

  const nextReview = new Date();
  nextReview.setDate(nextReview.getDate() + interval);

  return { repetitions, easeFactor, interval, nextReview };
}
```

**Output Giai đoạn 5:**
- ✅ Notebook với rich text editor (TipTap)
- ✅ Create/Edit/Delete notes
- ✅ Flashcard sets management
- ✅ Flashcard study mode với flip animation
- ✅ Spaced repetition algorithm (SM-2)
- ✅ Progress tracking trong study session

---

## 🚧 **GIAI ĐOẠN 6: PRACTICE & AI GRADING (CORE USP)**
### Ước tính: 5-6 giờ (Phần quan trọng nhất!)

### 6.1. Practice API
- [ ] Tạo `lib/api/practice.api.ts`:
```typescript
export const practiceApi = {
  getAllQuestions: async (topicId?: string, difficultyLevel?: string) => {
    const params = new URLSearchParams();
    if (topicId) params.append('topicId', topicId);
    if (difficultyLevel) params.append('difficultyLevel', difficultyLevel);

    const response = await apiClient.get(`/exam-questions?${params}`);
    return response.data;
  },

  getQuestion: async (id: string) => {
    const response = await apiClient.get(`/exam-questions/${id}`);
    return response.data;
  },

  getRandomQuestion: async (topicId?: string) => {
    const params = new URLSearchParams();
    if (topicId) params.append('topicId', topicId);

    const response = await apiClient.get(`/exam-questions/random?${params}`);
    return response.data;
  },
};
```

### 6.2. Submissions API
- [ ] Tạo `lib/api/submissions.api.ts`:
```typescript
export const submissionsApi = {
  create: async (data: { examQuestionId: string; content: string }) => {
    const response = await apiClient.post('/submissions', data);
    return response.data;
  },

  update: async (id: string, content: string) => {
    const response = await apiClient.patch(`/submissions/${id}`, { content });
    return response.data;
  },

  submit: async (id: string, timeSpent: number) => {
    const response = await apiClient.post(`/submissions/${id}/submit`, { timeSpent });
    return response.data; // { submissionId, status: 'SUBMITTED' }
  },

  getAll: async () => {
    const response = await apiClient.get('/submissions');
    return response.data;
  },

  getOne: async (id: string) => {
    const response = await apiClient.get(`/submissions/${id}`);
    return response.data;
  },
};
```

### 6.3. Practice Questions Page
- [ ] Tạo `app/(dashboard)/practice/page.tsx`:
  - Question bank grid
  - Filter by Topic (sidebar)
  - Filter by Difficulty
  - "Start Practice" button
  - "Random Question" button
  - Recent submissions section

- [ ] Tạo `components/practice/question-card.tsx`:
```typescript
<Card>
  <CardHeader>
    <div className="flex justify-between">
      <Badge>{question.topicName}</Badge>
      <Badge variant={getDifficultyColor(question.difficultyLevel)}>
        {question.difficultyLevel}
      </Badge>
    </div>
  </CardHeader>
  <CardContent>
    <p className="text-sm font-medium">{question.questionText}</p>
    <Button className="mt-4 w-full" onClick={handleStartPractice}>
      Bắt đầu làm bài
    </Button>
  </CardContent>
</Card>
```

### 6.4. Essay Writing Page
- [ ] Tạo `app/(dashboard)/practice/[questionId]/write/page.tsx`:
  - Question prompt (sticky header)
  - Essay editor (textarea với word count)
  - Timer (optional)
  - Auto-save draft every 30s
  - Save Draft button
  - Submit button

- [ ] Tạo `components/practice/essay-editor.tsx`:
```typescript
'use client';

import { useState, useEffect } from 'react';
import { Textarea } from '@/components/ui/textarea';
import { Button } from '@/components/ui/button';
import { useDebounce } from '@/lib/hooks/useDebounce';
import { submissionsApi } from '@/lib/api/submissions.api';

export default function EssayEditor({ submissionId, initialContent = '' }) {
  const [content, setContent] = useState(initialContent);
  const [wordCount, setWordCount] = useState(0);
  const [isSaving, setIsSaving] = useState(false);
  const [timeSpent, setTimeSpent] = useState(0);

  const debouncedContent = useDebounce(content, 3000);

  // Auto-save draft
  useEffect(() => {
    if (debouncedContent && submissionId) {
      setIsSaving(true);
      submissionsApi.update(submissionId, debouncedContent)
        .then(() => setIsSaving(false))
        .catch(() => setIsSaving(false));
    }
  }, [debouncedContent, submissionId]);

  // Timer
  useEffect(() => {
    const interval = setInterval(() => {
      setTimeSpent(prev => prev + 1);
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  // Word count
  useEffect(() => {
    const words = content.trim().split(/\s+/).filter(w => w.length > 0);
    setWordCount(words.length);
  }, [content]);

  const handleSubmit = async () => {
    if (wordCount < 250) {
      alert('Bài viết phải tối thiểu 250 từ');
      return;
    }

    await submissionsApi.submit(submissionId, timeSpent);
    // Redirect to grading status page
    window.location.href = `/practice/grading/${submissionId}`;
  };

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <div className="flex gap-4">
          <span className={wordCount < 250 ? 'text-red-500' : 'text-green-500'}>
            {wordCount} từ
          </span>
          <span className="text-gray-500">
            {Math.floor(timeSpent / 60)}:{(timeSpent % 60).toString().padStart(2, '0')}
          </span>
        </div>
        <div className="flex gap-2">
          {isSaving && <span className="text-sm text-gray-500">Đang lưu...</span>}
          <Button variant="outline" onClick={() => submissionsApi.update(submissionId, content)}>
            Lưu nháp
          </Button>
          <Button onClick={handleSubmit} disabled={wordCount < 250}>
            Nộp bài
          </Button>
        </div>
      </div>

      <Textarea
        value={content}
        onChange={(e) => setContent(e.target.value)}
        placeholder="Viết bài của bạn ở đây..."
        className="min-h-[500px] font-mono"
      />

      {wordCount < 250 && (
        <p className="text-sm text-red-500">
          Cần thêm {250 - wordCount} từ để đạt yêu cầu tối thiểu
        </p>
      )}
    </div>
  );
}
```

### 6.5. WebSocket Integration
- [ ] Tạo `lib/hooks/useWebSocket.ts`:
```typescript
import { useEffect, useState } from 'react';
import { io, Socket } from 'socket.io-client';

export function useGradingStatus(submissionId: string) {
  const [status, setStatus] = useState<'PENDING' | 'PROCESSING' | 'COMPLETED' | 'FAILED'>('PENDING');
  const [socket, setSocket] = useState<Socket | null>(null);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    const newSocket = io(process.env.NEXT_PUBLIC_WS_URL!, {
      auth: { token },
    });

    newSocket.on('connect', () => {
      console.log('WebSocket connected');
      newSocket.emit('join', { submissionId });
    });

    newSocket.on('grading:status', (data: { status: string }) => {
      setStatus(data.status as any);
    });

    newSocket.on('grading:completed', (data: { submissionId: string }) => {
      setStatus('COMPLETED');
      // Navigate to result page
      setTimeout(() => {
        window.location.href = `/practice/results/${submissionId}`;
      }, 1000);
    });

    newSocket.on('grading:failed', () => {
      setStatus('FAILED');
    });

    setSocket(newSocket);

    return () => {
      newSocket.disconnect();
    };
  }, [submissionId]);

  return { status, socket };
}
```

### 6.6. Grading Status Page
- [ ] Tạo `app/(dashboard)/practice/grading/[submissionId]/page.tsx`:
```typescript
'use client';

import { useGradingStatus } from '@/lib/hooks/useWebSocket';
import { Loader2 } from 'lucide-react';
import { Progress } from '@/components/ui/progress';

export default function GradingStatusPage({ params }: { params: { submissionId: string } }) {
  const { status } = useGradingStatus(params.submissionId);

  const getProgress = () => {
    switch (status) {
      case 'PENDING': return 25;
      case 'PROCESSING': return 50;
      case 'COMPLETED': return 100;
      case 'FAILED': return 0;
      default: return 0;
    }
  };

  const getMessage = () => {
    switch (status) {
      case 'PENDING': return 'Đang chờ trong hàng đợi...';
      case 'PROCESSING': return 'AI đang chấm bài của bạn...';
      case 'COMPLETED': return 'Hoàn tất! Đang chuyển hướng...';
      case 'FAILED': return 'Lỗi khi chấm bài. Vui lòng thử lại.';
      default: return 'Đang xử lý...';
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-6">
      <Loader2 className="h-16 w-16 animate-spin text-primary" />
      <h2 className="text-2xl font-semibold">{getMessage()}</h2>
      <Progress value={getProgress()} className="w-64" />

      {status === 'PROCESSING' && (
        <p className="text-sm text-gray-500">
          Quá trình này có thể mất 30-60 giây...
        </p>
      )}

      {status === 'FAILED' && (
        <Button onClick={() => window.location.reload()}>
          Thử lại
        </Button>
      )}
    </div>
  );
}
```

### 6.7. Grading Results Page
- [ ] Tạo `app/(dashboard)/practice/results/[submissionId]/page.tsx`:
  - Band score card (overall + 4 criteria)
  - Essay với error highlights
  - Error list grouped by category
  - General feedback
  - Suggestions for improvement
  - Download PDF button
  - Share button

- [ ] Tạo `components/practice/band-score-card.tsx`:
```typescript
import { Progress } from '@/components/ui/progress';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

interface BandScores {
  taskResponse: number;
  coherence: number;
  lexical: number;
  grammar: number;
  overall: number;
}

export default function BandScoreCard({ scores }: { scores: BandScores }) {
  const getBandColor = (band: number) => {
    if (band >= 7) return 'text-green-500';
    if (band >= 6) return 'text-yellow-500';
    return 'text-red-500';
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>Kết quả chấm điểm</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="text-center">
          <div className={`text-6xl font-bold ${getBandColor(scores.overall)}`}>
            {scores.overall.toFixed(1)}
          </div>
          <p className="text-sm text-gray-500 mt-2">Overall Band Score</p>
        </div>

        <div className="space-y-3">
          <div>
            <div className="flex justify-between text-sm mb-1">
              <span>Task Response</span>
              <span className={getBandColor(scores.taskResponse)}>{scores.taskResponse.toFixed(1)}</span>
            </div>
            <Progress value={scores.taskResponse * 10} />
          </div>

          <div>
            <div className="flex justify-between text-sm mb-1">
              <span>Coherence & Cohesion</span>
              <span className={getBandColor(scores.coherence)}>{scores.coherence.toFixed(1)}</span>
            </div>
            <Progress value={scores.coherence * 10} />
          </div>

          <div>
            <div className="flex justify-between text-sm mb-1">
              <span>Lexical Resource</span>
              <span className={getBandColor(scores.lexical)}>{scores.lexical.toFixed(1)}</span>
            </div>
            <Progress value={scores.lexical * 10} />
          </div>

          <div>
            <div className="flex justify-between text-sm mb-1">
              <span>Grammar & Accuracy</span>
              <span className={getBandColor(scores.grammar)}>{scores.grammar.toFixed(1)}</span>
            </div>
            <Progress value={scores.grammar * 10} />
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
```

- [ ] Tạo `components/practice/error-list.tsx`:
```typescript
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';

interface Error {
  category: string;
  severity: 'minor' | 'moderate' | 'critical';
  originalText: string;
  suggestion: string;
  explanation: string;
  startIndex: number;
  endIndex: number;
}

export default function ErrorList({ errors }: { errors: Error[] }) {
  const groupedErrors = errors.reduce((acc, error) => {
    if (!acc[error.category]) acc[error.category] = [];
    acc[error.category].push(error);
    return acc;
  }, {} as Record<string, Error[]>);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Phân tích lỗi ({errors.length} lỗi)</CardTitle>
      </CardHeader>
      <CardContent>
        <Tabs defaultValue={Object.keys(groupedErrors)[0]}>
          <TabsList>
            {Object.keys(groupedErrors).map(category => (
              <TabsTrigger key={category} value={category}>
                {category} ({groupedErrors[category].length})
              </TabsTrigger>
            ))}
          </TabsList>

          {Object.entries(groupedErrors).map(([category, categoryErrors]) => (
            <TabsContent key={category} value={category} className="space-y-3">
              {categoryErrors.map((error, idx) => (
                <div key={idx} className="border rounded-lg p-3 space-y-2">
                  <div className="flex gap-2">
                    <Badge variant={error.severity === 'critical' ? 'destructive' : 'secondary'}>
                      {error.severity}
                    </Badge>
                  </div>
                  <p className="text-sm">
                    <span className="font-medium">Lỗi:</span>{' '}
                    <span className="text-red-600">{error.originalText}</span>
                  </p>
                  <p className="text-sm">
                    <span className="font-medium">Gợi ý:</span>{' '}
                    <span className="text-green-600">{error.suggestion}</span>
                  </p>
                  <p className="text-sm text-gray-600">{error.explanation}</p>
                </div>
              ))}
            </TabsContent>
          ))}
        </Tabs>
      </CardContent>
    </Card>
  );
}
```

### 6.8. Submissions History Page
- [ ] Tạo `app/(dashboard)/submissions/page.tsx`:
  - Table of submissions
  - Filter by date
  - Filter by status (COMPLETED, FAILED)
  - Sort by band score
  - View details button
  - Band score trend chart

**Output Giai đoạn 6:**
- ✅ Practice questions browsing
- ✅ Essay writing interface với auto-save
- ✅ Real-time grading status với WebSocket
- ✅ Grading results với band scores + error highlights
- ✅ Error list grouped by category
- ✅ Submissions history với statistics
- ✅ **CORE FEATURE hoàn chỉnh!**

---

## 🚧 **GIAI ĐOẠN 7: REAL-TIME NOTIFICATIONS & POLISH**
### Ước tính: 2-3 giờ

### 7.1. Notification System
- [ ] Tạo `lib/hooks/useNotifications.ts`:
```typescript
import { useEffect, useState } from 'react';
import { io } from 'socket.io-client';

interface Notification {
  id: string;
  type: 'grading_complete' | 'system';
  message: string;
  read: boolean;
  createdAt: Date;
}

export function useNotifications() {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [unreadCount, setUnreadCount] = useState(0);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    const socket = io(process.env.NEXT_PUBLIC_WS_URL!, { auth: { token } });

    socket.on('notification:new', (notification: Notification) => {
      setNotifications(prev => [notification, ...prev]);
      setUnreadCount(prev => prev + 1);

      // Show toast
      toast({
        title: notification.message,
        duration: 5000,
      });
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  const markAsRead = (id: string) => {
    setNotifications(prev =>
      prev.map(n => n.id === id ? { ...n, read: true } : n)
    );
    setUnreadCount(prev => Math.max(0, prev - 1));
  };

  return { notifications, unreadCount, markAsRead };
}
```

### 7.2. Notification Bell Component
- [ ] Tạo `components/layouts/notification-bell.tsx`:
```typescript
import { Bell } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { useNotifications } from '@/lib/hooks/useNotifications';

export default function NotificationBell() {
  const { notifications, unreadCount, markAsRead } = useNotifications();

  return (
    <DropdownMenu>
      <DropdownMenuTrigger className="relative">
        <Bell className="h-5 w-5" />
        {unreadCount > 0 && (
          <Badge className="absolute -top-2 -right-2 h-5 w-5 flex items-center justify-center p-0">
            {unreadCount}
          </Badge>
        )}
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end" className="w-80">
        {notifications.length === 0 ? (
          <div className="p-4 text-center text-sm text-gray-500">
            Không có thông báo mới
          </div>
        ) : (
          notifications.slice(0, 5).map(notif => (
            <DropdownMenuItem
              key={notif.id}
              className={!notif.read ? 'bg-blue-50' : ''}
              onClick={() => markAsRead(notif.id)}
            >
              <div className="flex-1">
                <p className="text-sm">{notif.message}</p>
                <p className="text-xs text-gray-500">
                  {new Date(notif.createdAt).toLocaleString()}
                </p>
              </div>
            </DropdownMenuItem>
          ))
        )}
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
```

### 7.3. Toast Notifications
- [ ] Integrate toast notifications cho:
  - Grading complete
  - Draft saved
  - Errors
  - Success messages

### 7.4. Loading States
- [ ] Tạo skeleton loaders cho:
  - Course cards
  - Essay cards
  - Dashboard widgets
  - Tables

- [ ] Tạo `components/shared/loading-skeleton.tsx`:
```typescript
import { Skeleton } from '@/components/ui/skeleton';

export function CourseCardSkeleton() {
  return (
    <div className="space-y-3">
      <Skeleton className="h-48 w-full" />
      <Skeleton className="h-4 w-3/4" />
      <Skeleton className="h-4 w-1/2" />
    </div>
  );
}
```

### 7.5. Error Boundaries
- [ ] Tạo `components/shared/error-boundary.tsx`:
```typescript
'use client';

import { Component, ReactNode } from 'react';
import { Button } from '@/components/ui/button';

export class ErrorBoundary extends Component<
  { children: ReactNode },
  { hasError: boolean }
> {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="flex flex-col items-center justify-center min-h-[60vh]">
          <h2 className="text-xl font-semibold mb-4">Đã xảy ra lỗi</h2>
          <Button onClick={() => window.location.reload()}>
            Tải lại trang
          </Button>
        </div>
      );
    }

    return this.props.children;
  }
}
```

### 7.6. Responsive Design Check
- [ ] Test tất cả pages trên mobile, tablet, desktop
- [ ] Adjust layouts cho mobile:
  - Sidebar → Bottom navigation
  - Tables → Cards
  - Multi-column → Single column

**Output Giai đoạn 7:**
- ✅ Real-time notifications với WebSocket
- ✅ Notification bell với unread count
- ✅ Toast notifications cho user actions
- ✅ Loading skeletons cho better UX
- ✅ Error boundaries để handle crashes
- ✅ Responsive design cho mọi màn hình

---

## 🚧 **GIAI ĐOẠN 8: ADMIN PANEL**
### Ước tính: 4-5 giờ

### 8.1. Admin Layout
- [ ] Tạo `app/(admin)/layout.tsx`:
  - Admin sidebar với modules
  - Dashboard
  - Topics
  - Courses
  - Lessons
  - Questions
  - Users
  - Analytics

### 8.2. Admin Dashboard
- [ ] Tạo `app/(admin)/admin/page.tsx`:
  - Statistics cards (Total users, Total submissions, Avg band)
  - Recent activity table
  - Band score distribution chart
  - Popular topics chart

### 8.3. Topics Management
- [ ] Tạo `app/(admin)/admin/topics/page.tsx`:
  - Topics table (DataTable)
  - Create/Edit/Delete modals
  - Search & Filter

### 8.4. Courses Management
- [ ] Tạo `app/(admin)/admin/courses/page.tsx`:
  - Courses table
  - Create course form
  - Edit course
  - Publish/Unpublish toggle
  - Assign to topic

### 8.5. Lessons Management
- [ ] Tạo `app/(admin)/admin/lessons/page.tsx`:
  - Lessons table grouped by course
  - Create lesson form
  - Add videos (file upload)
  - Add vocabularies (array input)
  - Add grammar rules
  - Reorder lessons (drag-and-drop)

### 8.6. Questions Management
- [ ] Tạo `app/(admin)/admin/questions/page.tsx`:
  - Questions table
  - Create/Edit question form
  - Assign to topic/difficulty
  - Preview question

### 8.7. Users Management
- [ ] Tạo `app/(admin)/admin/users/page.tsx`:
  - Users table
  - Role management (promote to admin)
  - Ban/Unban users
  - View user activity

**Output Giai đoạn 8:**
- ✅ Admin panel hoàn chỉnh
- ✅ CRUD operations cho tất cả entities
- ✅ Analytics dashboard
- ✅ User management
- ✅ **Platform hoàn thiện 100%!**

---

## 📊 TỔNG KẾT

| Giai đoạn | Nội dung | Ước tính | Status |
|-----------|----------|----------|--------|
| **1** | Project Setup & Core Infrastructure | 3-4h | ⏳ Chưa bắt đầu |
| **2** | Authentication & Authorization | 3-4h | ⏳ Chưa bắt đầu |
| **3** | Student Dashboard & Course System | 4-5h | ⏳ Chưa bắt đầu |
| **4** | Sample Essays & Favorites | 3h | ⏳ Chưa bắt đầu |
| **5** | Notebook & Flashcards | 3h | ⏳ Chưa bắt đầu |
| **6** | Practice & AI Grading (Core) | 5-6h | ⏳ Chưa bắt đầu |
| **7** | Real-time Notifications & Polish | 2-3h | ⏳ Chưa bắt đầu |
| **8** | Admin Panel | 4-5h | ⏳ Chưa bắt đầu |
| **TỔNG** | | **27-35 giờ** | **0% done** |

---

## 🎯 CHIẾN LƯỢC THỰC HIỆN

### Phương pháp làm việc:
1. **Tuần tự từng giai đoạn** - Hoàn thành 100% trước khi chuyển giai đoạn tiếp
2. **Test ngay** - Mỗi component/page test ngay sau khi code xong
3. **Commit thường xuyên** - Mỗi feature nhỏ = 1 commit
4. **Integration testing** - Test tích hợp với Backend API sau mỗi giai đoạn

### Timeline đề xuất:
- **Week 1:** Giai đoạn 1-2 (Setup + Auth)
- **Week 2:** Giai đoạn 3-4 (Dashboard + Essays)
- **Week 3:** Giai đoạn 5-6 (Notebook + Practice + AI)
- **Week 4:** Giai đoạn 7-8 (Notifications + Admin)

### Dependencies:
- Backend API phải hoàn thành ít nhất đến **Giai đoạn 6** trước khi test Practice & AI Grading
- WebSocket backend phải sẵn sàng trước **Giai đoạn 7**

---

## 🚀 SẴN SÀNG BẮT ĐẦU?

**Trước khi bắt đầu, cần kiểm tra:**
- [ ] Đã có Backend API chạy tại `localhost:3000` chưa?
- [ ] Đã có MongoDB + Redis setup chưa?
- [ ] Đã có Gemini API Key chưa? (cho AI grading)
- [ ] Đã cài Node.js 18+ chưa?

**Bạn có muốn tôi bắt đầu Giai đoạn 1 ngay không?** 🚀

Tôi sẽ hướng dẫn từng bước:
1. Setup Next.js project
2. Cài dependencies
3. Tạo folder structure
4. Setup Axios client
5. Config TypeScript types

**Thời gian ước tính:** 3-4 giờ
**Kết quả:** Frontend foundation hoàn chỉnh, sẵn sàng implement features
