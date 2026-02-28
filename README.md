# Todo SQLite MCP Server for Antigravity

MCP Server quản lý danh sách công việc (Todo List) sử dụng SQLite, được phát triển và tối ưu hóa để chạy trực tiếp trên **Antigravity IDE**. Công cụ này cho phép AI Agent tương tác với cơ sở dữ liệu để quản lý công việc thông qua ngôn ngữ tự nhiên ngay trong môi trường lập trình.

## Tính năng nổi bật

- **Quản lý Task thông minh**: Thêm, xem, hoàn thành và xóa công việc bằng lệnh chat
- **Lưu trữ Persistent**: Dữ liệu được lưu trữ an toàn trong SQLite database (`todos.db`)
- **Tối ưu cho Antigravity**: Tích hợp sâu với khung chat Agent, hỗ trợ hiển thị trạng thái trực quan
- **Kiến trúc ổn định**: Sử dụng FastMCP và thực thi bất đồng bộ (Async) để đảm bảo hiệu năng

## Cài đặt & Thiết lập

### 1. Chuẩn bị môi trường

Yêu cầu máy tính đã cài đặt Python 3.8+ và các thư viện cần thiết:

```bash
pip install mcp aiosqlite
```

### 2. Cấu trúc thư mục Project

```
todo-mcp/
├── server.py       # Source code chính của MCP Server
├── todos.db        # SQLite database (tự động tạo khi chạy lần đầu)
└── README.md       # Tài liệu hướng dẫn
```

### 3. Cấu hình trên Antigravity IDE

1. Mở **Antigravity**
2. Truy cập: **Manage MCP Servers** → **View raw config**
3. Thêm đoạn JSON sau vào phần `"mcpServers"`:

```json
{
  "mcpServers": {
    "todo-mcp": {
      "command": "python",
      "args": ["C:\\mcp\\todo-mcp\\server.py"]
    }
  }
}
```

4. Nhấn **Ctrl + S** để lưu file cấu hình và để Antigravity nạp lại server

> **Lưu ý**: Thay đổi đường dẫn cho phù hợp với vị trí project

## Cách sử dụng với Agent

Sau khi cấu hình, có thể ra lệnh cho Agent trong khung chat của Antigravity bằng ngôn ngữ tự nhiên:

- _"Sử dụng todo-mcp liệt kê các công việc hiện tại"_
- _"Thêm task mới: Hoàn thành báo cáo thực tập"_
- _"Đánh dấu hoàn thành task số 1"_
- _"Xóa những task đã hoàn thành khỏi danh sách"_

## Chi tiết Kỹ thuật

### Tool API Reference

#### `add_task(title: str)`

Khởi tạo task mới vào cơ sở dữ liệu.

**Tham số:**

- `title` (str): Tiêu đề công việc

**Trả về:** Thông báo xác nhận với ID của task mới

**Ví dụ:**

```
Đã thêm task #1: Hoàn thành báo cáo thực tập
```

---

#### `list_tasks()`

Truy vấn và hiển thị toàn bộ danh sách công việc.

**Trả về:** Danh sách công việc với format:

```
#1 - Tiêu đề task (Chưa hoàn thành)
#2 - Tiêu đề task (Hoàn thành)
```

---

#### `complete_task(task_id: int)`

Cập nhật trạng thái `completed = 1` cho task.

**Tham số:**

- `task_id` (int): ID của task cần đánh dấu hoàn thành

**Trả về:** Thông báo xác nhận hoặc lỗi nếu không tìm thấy task

---

#### `delete_task(task_id: int)`

Xóa bản ghi khỏi bảng `todos`.

**Tham số:**

- `task_id` (int): ID của task cần xóa

**Trả về:** Thông báo xác nhận hoặc lỗi nếu không tìm thấy task

### Database Schema

```sql
CREATE TABLE todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    completed BOOLEAN DEFAULT 0,
    created_at TEXT
)
```

**Mô tả các trường:**

- `id`: Khóa chính, tự động tăng
- `title`: Tiêu đề công việc (bắt buộc)
- `completed`: Trạng thái hoàn thành (0 = chưa, 1 = đã hoàn thành)
- `created_at`: Thời gian tạo task (ISO 8601 format)

## Tại sao chọn project này?

### 1. Tính thực tế cao

- Quản lý todo list là use case hữu ích trong công việc hàng ngày
- Có thể sử dụng thực tế để theo dõi công việc cá nhân và dự án

### 2. Kết nối Database

- Sử dụng SQLite để lưu trữ dữ liệu persistent
- Minh họa cách MCP server tương tác với database
- Dữ liệu không bị mất khi khởi động lại server

### 3. CRUD đầy đủ

- Implement đầy đủ 4 thao tác cơ bản: **C**reate, **R**ead, **U**pdate, **D**elete
- Dễ dàng mở rộng thêm tính năng (tìm kiếm, filter, sửa task...)

### 4. Tích hợp tự nhiên với Antigravity

- Người dùng có thể quản lý todo bằng ngôn ngữ tự nhiên
- Không cần giao diện phức tạp
- Agent hiểu ngữ cảnh và gợi ý task phù hợp

## Công nghệ sử dụng

- **Antigravity** - AI coding assistant để tạo và phát triển MCP server
- **FastMCP** - Framework để xây dựng MCP server nhanh chóng
- **aiosqlite** - Async SQLite driver cho Python
- **SQLite** - Embedded database, không cần cài đặt server riêng
- **Python 3.8+** - Ngôn ngữ lập trình chính

## Luồng hoạt động

```
User (Antigravity Chat)
    ↓
    "Thêm task: Học Python"
    ↓
Agent nhận lệnh
    ↓
Gọi add_task() từ MCP Server
    ↓
server.py xử lý
    ↓
INSERT vào SQLite database
    ↓
Trả về kết quả
    ↓
Agent hiển thị: "Đã thêm task #1: Học Python"
```

## Troubleshooting

### Lỗi: "Module not found: mcp"

**Giải pháp:** Cài đặt lại thư viện

```bash
pip install mcp aiosqlite
```

### Lỗi: Database locked

**Giải pháp:** Đóng tất cả kết nối database đang mở hoặc khởi động lại server

### Server không xuất hiện trong Antigravity

**Giải pháp:**

1. Kiểm tra lại đường dẫn trong config
2. Đảm bảo đã lưu config (Ctrl + S)
3. Restart Antigravity

## Ghi chú

- Project này được phát triển như một bài tập về **Custom MCP Server**
- Sử dụng **Antigravity** để tăng tốc quá trình phát triển
- Code được tối ưu hóa cho môi trường Antigravity IDE

## License

MIT License - Tự do sử dụng cho mục đích học tập và phát triển.
