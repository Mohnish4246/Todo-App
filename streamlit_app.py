import streamlit as st
import requests
from datetime import date

API_URL = "http://localhost:8000"

# 📦 API interaction functions
def fetch_todos(completed=None):
    try:
        url = f"{API_URL}/todos"
        if completed is not None:
            url += f"?completed={str(completed).lower()}"
        res = requests.get(url)
        return res.json()
    except:
        st.error("⚠️ Failed to connect to backend.")
        return []

def add_todo(todo):
    res = requests.post(f"{API_URL}/todos", json=todo)
    return res.ok

def update_todo(todo_id, todo):
    res = requests.put(f"{API_URL}/todos/{todo_id}", json=todo)
    return res.ok

def delete_todo(todo_id):
    res = requests.delete(f"{API_URL}/todos/{todo_id}")
    return res.ok

# 🔍 Sidebar Filter
st.sidebar.title("🗂️ Filters")
filter_opt = st.sidebar.radio("Show", ["All", "Completed", "Incomplete"])
completed_filter = None
if filter_opt == "Completed":
    completed_filter = True
elif filter_opt == "Incomplete":
    completed_filter = False

# ➕ Add Todo Section
st.title("✅ Todo App (Streamlit + FastAPI)")
with st.expander("➕ Add New Todo"):
    title = st.text_input("Task Title")
    due = st.date_input("Due Date", value=date.today())
    tags = st.text_input("Tags (comma separated)")
    if st.button("Add"):
        if title.strip():
            new_todo = {
                "title": title,
                "completed": False,
                "due_date": due.isoformat(),
                "tags": tags
            }
            if add_todo(new_todo):
                st.success("✅ Added successfully!")
                st.stop()  # Clean stop to reload
            else:
                st.error("❌ Failed to add todo.")
        else:
            st.warning("⚠️ Title is required.")

# 📋 Display Todos
todos = fetch_todos(completed_filter)
st.subheader(f"📋 Your Todos ({len(todos)})")

for todo in todos:
    with st.container():
        col1, col2, col3 = st.columns([0.6, 0.2, 0.2])

        with col1:
            st.markdown(f"**{todo['title']}**")
            st.caption(f"📅 Due: {todo.get('due_date', '-')}, 🏷️ Tags: {todo.get('tags', '-')}")

        with col2:
            if st.checkbox("Done", value=todo["completed"], key=f"done-{todo['id']}"):
                update_data = {
                    "title": todo["title"],
                    "completed": True,
                    "due_date": todo.get("due_date", ""),
                    "tags": todo.get("tags", "")
                }
                if update_todo(todo["id"], update_data):
                    st.success("☑️ Marked as completed.")
                    st.stop()

        with col3:
            if st.button("🗑️ Delete", key=f"delete-{todo['id']}"):
                if delete_todo(todo["id"]):
                    st.success("🗑️ Deleted successfully.")
                    st.stop()

        # ✏️ Edit Section
        with st.expander("✏️ Edit Task"):
            new_title = st.text_input("Title", value=todo["title"], key=f"title-{todo['id']}")
            new_due = st.date_input("Due Date", value=date.fromisoformat(todo.get("due_date", date.today().isoformat())), key=f"due-{todo['id']}")
            new_tags = st.text_input("Tags", value=todo.get("tags", ""), key=f"tags-{todo['id']}")

            if st.button("Update", key=f"update-{todo['id']}"):
                update_data = {
                    "title": new_title,
                    "completed": todo["completed"],
                    "due_date": new_due.isoformat(),
                    "tags": new_tags
                }
                if update_todo(todo["id"], update_data):
                    st.success("✏️ Updated successfully.")
                    st.stop()
