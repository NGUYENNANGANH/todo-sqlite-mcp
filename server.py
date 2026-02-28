from mcp.server.fastmcp import FastMCP
import aiosqlite
from datetime import datetime
from pathlib import Path

mcp = FastMCP("todo-sqlite-mcp")

DB_PATH = Path(__file__).parent / "todos.db"

async def get_db():
    db = await aiosqlite.connect(DB_PATH)
    await db.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            completed BOOLEAN DEFAULT 0,
            created_at TEXT
        )
    ''')
    await db.commit()
    return db

@mcp.tool()
async def add_task(title: str):
    """Thêm một công việc mới vào danh sách todo"""
    if not title or not title.strip():
        return "Lỗi: Tiêu đề không được để trống"
    
    try:
        db = await get_db()
        created_at = datetime.now().isoformat()
        async with db.execute(
            "INSERT INTO todos (title, created_at) VALUES (?, ?) RETURNING id", 
            (title.strip(), created_at)
        ) as cursor:
            row = await cursor.fetchone()
            task_id = row[0]
        await db.commit()
        await db.close()
        return f"Đã thêm task #{task_id}: {title}"
    except Exception as e:
        return f"Lỗi: {str(e)}"

@mcp.tool()
async def list_tasks():
    """Hiển thị tất cả công việc"""
    try:
        db = await get_db()
        async with db.execute("SELECT id, title, completed FROM todos ORDER BY id DESC") as cursor:
            rows = await cursor.fetchall()
        await db.close()
        
        if not rows:
            return "Chưa có công việc nào."
        
        result = "Danh sách Todo:\n\n"
        for row in rows:
            status = "Hoàn thành" if row[2] else "Chưa hoàn thành"
            result += f"#{row[0]} - {row[1]} ({status})\n"
        return result
    except Exception as e:
        return f"Lỗi: {str(e)}"

@mcp.tool()
async def complete_task(task_id: int):
    """Đánh dấu công việc đã hoàn thành"""
    try:
        db = await get_db()
        await db.execute("UPDATE todos SET completed = 1 WHERE id = ?", (task_id,))
        changed = db.total_changes
        await db.commit()
        await db.close()
        return f"Đã hoàn thành task #{task_id}" if changed > 0 else f"Không tìm thấy task #{task_id}"
    except Exception as e:
        return f"Lỗi: {str(e)}"

@mcp.tool()
async def delete_task(task_id: int):
    """Xóa một công việc"""
    try:
        db = await get_db()
        await db.execute("DELETE FROM todos WHERE id = ?", (task_id,))
        changed = db.total_changes
        await db.commit()
        await db.close()
        return f"Đã xóa task #{task_id}" if changed > 0 else f"Không tìm thấy task #{task_id}"
    except Exception as e:
        return f"Lỗi: {str(e)}"

if __name__ == "__main__":
    mcp.run()