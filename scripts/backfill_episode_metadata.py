#!/usr/bin/env python3
"""
Backfill metadata for existing episodes that have null metadata.

This script:
1. Lists all sessions with null metadata
2. For each episode, reads the first message to get the title
3. Updates the session metadata with title/summary

This fixes the bug where episodes were created before the 
/api/v1/user endpoint fix.
"""
import httpx
import asyncio


ZEP_URL = "https://zep.ctxeco.com"


async def backfill_metadata():
    async with httpx.AsyncClient(timeout=30) as client:
        # Get all sessions
        print("Fetching all sessions...")
        r = await client.get(f"{ZEP_URL}/api/v1/sessions?limit=500")
        if r.status_code != 200:
            print(f"Failed to get sessions: {r.text}")
            return
        
        sessions = r.json()
        print(f"Found {len(sessions)} sessions")
        
        fixed = 0
        skipped = 0
        
        for session in sessions:
            session_id = session.get("session_id", "")
            metadata = session.get("metadata")
            
            # Skip if already has metadata
            if metadata and metadata.get("title"):
                print(f"  ✓ {session_id} - already has metadata")
                skipped += 1
                continue
            
            # Skip non-episode sessions (stories, working-memory, etc.)
            if not session_id.startswith("episode-"):
                print(f"  - {session_id} - skipping (not an episode)")
                skipped += 1
                continue
            
            print(f"  → {session_id} - needs metadata backfill...")
            
            # Get the first message to extract title
            r = await client.get(f"{ZEP_URL}/api/v1/sessions/{session_id}/messages?limit=1")
            if r.status_code != 200:
                print(f"    Failed to get messages: {r.text}")
                continue
            
            messages = r.json()
            if not messages or not messages.get("messages"):
                print("    No messages found")
                continue
            
            first_msg = messages["messages"][0]
            msg_metadata = first_msg.get("metadata", {}) or {}
            content = first_msg.get("content", "")
            
            # Extract title from message metadata or content
            title = msg_metadata.get("title", "")
            if not title:
                # Try to extract from content (first line)
                lines = content.strip().split("\n")
                title = lines[0][:100] if lines else "Untitled Episode"
                # Remove markdown headers
                title = title.lstrip("# ").strip()
            
            # Generate summary from content
            summary = content[:200].replace("\n", " ").strip()
            if len(content) > 200:
                summary += "..."
            
            # Update session metadata
            new_metadata = {
                "type": "episode",
                "title": title,
                "summary": summary,
                "agent_id": "sage",
                "turn_count": len(messages.get("messages", [])),
                "backfilled": True
            }
            
            r = await client.patch(
                f"{ZEP_URL}/api/v1/sessions/{session_id}",
                json={"metadata": new_metadata}
            )
            
            if r.status_code == 200:
                print(f"    ✅ Fixed: {title[:50]}...")
                fixed += 1
            else:
                print(f"    ❌ Failed to update: {r.text}")
        
        print(f"\n{'='*50}")
        print(f"Backfill complete!")
        print(f"  Fixed: {fixed}")
        print(f"  Skipped: {skipped}")


if __name__ == "__main__":
    asyncio.run(backfill_metadata())
