Part 2 — Frontend (all files for comments UI)

Place these React components in your frontend src (e.g., src/components/comments/). Minimal dependencies; uses the browser Fetch API.

File 1 — src/components/comments/CommentForm.jsx

// src/components/comments/CommentForm.jsx
import React, { useState, useEffect } from "react";

export default function CommentForm({ onSubmit, initial = { body: "", author: "" }, onCancel, submitLabel = "Submit" }) {
  const [body, setBody] = useState(initial.body || "");
  const [author, setAuthor] = useState(initial.author || "");

  useEffect(() => {
    setBody(initial.body || "");
    setAuthor(initial.author || "");
  }, [initial]);

  const handleSubmit = (e) => {
    e.preventDefault();
    const trimmed = (body || "").trim();
    if (!trimmed) return alert("Comment body is required");
    onSubmit({ body: trimmed, author: (author || "").trim() || null });
    // reset when adding (but avoid clearing when editing)
    if (!onCancel) {
      setBody("");
      setAuthor("");
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ marginBottom: "8px" }}>
      <div>
        <textarea
          value={body}
          onChange={(e) => setBody(e.target.value)}
          placeholder="Write a comment..."
          rows={3}
          style={{ width: "100%", padding: "8px" }}
        />
      </div>
      <div style={{ marginTop: "6px" }}>
        <input
          value={author}
          onChange={(e) => setAuthor(e.target.value)}
          placeholder="Your name (optional)"
          style={{ width: "100%", padding: "8px" }}
        />
      </div>
      <div style={{ marginTop: "8px" }}>
        <button type="submit">{submitLabel}</button>
        {onCancel && (
          <button type="button" onClick={onCancel} style={{ marginLeft: "8px" }}>
            Cancel
          </button>
        )}
      </div>
    </form>
  );
}

File 2 — src/components/comments/CommentsList.jsx

// src/components/comments/CommentsList.jsx
import React, { useEffect, useState } from "react";
import CommentForm from "./CommentForm";

export default function CommentsList({ taskId }) {
  const [comments, setComments] = useState([]);
  const [editingId, setEditingId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchComments = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`/api/tasks/${taskId}/comments`);
      if (!res.ok) throw new Error(`Failed to load comments (${res.status})`);
      const data = await res.json();
      setComments(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (taskId) fetchComments();
  }, [taskId]);

  const addComment = async (payload) => {
    try {
      const res = await fetch(`/api/tasks/${taskId}/comments`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!res.ok) {
        const err = await res.json().catch(()=>({error: "unknown"}));
        throw new Error(err.error || `Failed to add comment (${res.status})`);
      }
      const newComment = await res.json();
      setComments((prev) => [...prev, newComment]);
    } catch (err) {
      alert("Error adding comment: " + err.message);
    }
  };

  const editComment = async (id, payload) => {
    try {
      const res = await fetch(`/api/comments/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.error || `Failed to edit comment (${res.status})`);
      }
      const updated = await res.json();
      setComments((prev) => prev.map((c) => (c.id === id ? updated : c)));
      setEditingId(null);
    } catch (err) {
      alert("Error editing comment: " + err.message);
    }
  };

  const deleteComment = async (id) => {
    if (!window.confirm("Delete this comment?")) return;
    try {
      const res = await fetch(`/api/comments/${id}`, { method: "DELETE" });
      if (!res.ok) throw new Error(`Failed to delete comment (${res.status})`);
      setComments((prev) => prev.filter((c) => c.id !== id));
    } catch (err) {
      alert("Error deleting comment: " + err.message);
    }
  };

  return (
    <div style={{ border: "1px solid #ddd", padding: "12px", borderRadius: "6px" }}>
      <h3>Comments</h3>
      <CommentForm onSubmit={addComment} />
      {loading && <div>Loading comments...</div>}
      {error && <div style={{ color: "red" }}>{error}</div>}
      <ul style={{ listStyle: "none", padding: 0 }}>
        {comments.map((c) => (
          <li key={c.id} style={{ borderTop: "1px solid #eee", padding: "8px 0" }}>
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <div>
                <strong>{c.author || "Anonymous"}</strong>
                <div style={{ fontSize: "12px", color: "#666" }}>
                  {new Date(c.created_at).toLocaleString()}
                </div>
              </div>
              <div>
                <button onClick={() => setEditingId(c.id)}>Edit</button>
                <button onClick={() => deleteComment(c.id)} style={{ marginLeft: "8px" }}>Delete</button>
              </div>
            </div>
            <p style={{ whiteSpace: "pre-wrap" }}>{c.body}</p>

            {editingId === c.id && (
              <CommentForm
                initial={{ body: c.body, author: c.author }}
                onSubmit={(payload) => editComment(c.id, payload)}
                onCancel={() => setEditingId(null)}
                submitLabel="Update"
              />
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}

File 3 — Example usage in Task detail page src/pages/TaskDetail.jsx

// src/pages/TaskDetail.jsx
import React from "react";
import CommentsList from "../components/comments/CommentsList";

export default function TaskDetail({ match }) {
  // If using react-router, taskId could be in match.params.id
  const taskId = match?.params?.id || 1; // replace fallback with actual logic

  return (
    <div>
      <h2>Task detail (id: {taskId})</h2>
      {/* task content */}
      <CommentsList taskId={taskId} />
    </div>
  );
}

File 4 — package.json proxy (development) Add or update in frontend package.json to avoid CORS during local dev:

{
  // ... other package.json fields ...
  "proxy": "http://localhost:5000"
}
