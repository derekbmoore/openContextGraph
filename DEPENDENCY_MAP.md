# Voice Router Dependencies Map

## Overview

This document maps all dependencies required by the voice router and related components added from legacy engram.

## Status Legend

- ✅ **EXISTS** - Component exists in ctxEco
- ❌ **MISSING** - Component is missing and needs to be added
- ⚠️ **PARTIAL** - Component exists but may need updates
- 🔍 **NEEDS CHECK** - Component exists but usage needs verification

---

## 1. Core Context Dependencies

### 1.1 MessageRole Enum

- **Status**: ❌ **MISSING**
- **Location**: `backend/core/context.py`
- **Required by**: Voice router, memory persistence
- **Usage**: `voice.py` line 26, 614, 680, 728, etc.
- **Definition needed**:

```python
class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    TOOL = "tool"
```

### 1.2 Turn Class

- **Status**: ❌ **MISSING**
- **Location**: `backend/core/context.py`
- **Required by**: Voice router, episodic context
- **Usage**: `voice.py` lines 613-620, 679-687, 727-736
- **Definition needed**:

```python
class Turn(BaseModel):
    role: MessageRole
    content: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    agent_id: Optional[str] = None
    tool_calls: Optional[list[dict]] = None
    token_count: Optional[int] = None
```

### 1.3 EpisodicContext.add_turn() Method

- **Status**: ❌ **MISSING**
- **Location**: `backend/core/context.py` - EpisodicContext class
- **Current state**: EpisodicContext uses `recent_messages: list[Message]`
- **Needed change**: Replace with `recent_turns: list[Turn]` and add `add_turn()` method
- **Usage**: `voice.py` lines 612-620, 678-688, 726-738
- **Critical**: This is used extensively in voice router for memory persistence

### 1.4 SemanticContext.add_fact() Method

- **Status**: ❌ **MISSING**
- **Location**: `backend/core/context.py` - SemanticContext class
- **Usage**: `voice.py` line 335 (`voice_context.semantic.add_fact(fact)`)
- **Needed**: Method to add facts to semantic context

### 1.5 SemanticContext.get_context_summary() Method

- **Status**: ❌ **MISSING**
- **Location**: `backend/core/context.py` - SemanticContext class
- **Usage**: `voice.py` line 338 (`voice_context.semantic.get_context_summary()`)
- **Needed**: Method to generate summary string from semantic facts

### 1.6 EnterpriseContext Components

- **Status**: ✅ **EXISTS** (but incomplete)
- **Location**: `backend/core/context.py`
- **Current**: Has `EnterpriseContext` class with basic structure
- **Missing**:
  - EpisodicContext needs `recent_turns` and `add_turn()` method
  - SemanticContext needs `add_fact()` and `get_context_summary()` methods

---

## 2. Memory Module Dependencies

### 2.1 memory_client Singleton

- **Status**: ⚠️ **PARTIAL**
- **Location**: `backend/memory/client.py`
- **Current**: Defined in ZepMemoryClient class (line 688: `memory_client = property(...)`)
- **Needed**: Top-level singleton like legacy engram's `memory_client = ZepMemoryClient()`
- **Usage**: `voice.py` lines 262, 306, 325, 1706
- **Fix**: Add to `backend/memory/__init__.py`:

```python
from memory.client import ZepMemoryClient
memory_client = ZepMemoryClient()
```

### 2.2 persist_conversation() Function

- **Status**: ❌ **MISSING**
- **Location**: `backend/memory/__init__.py` and `backend/memory/client.py`
- **Usage**: `voice.py` lines 556, 737, 765, 1725
- **Needed**:
  1. `ZepMemoryClient.persist_conversation()` method
  2. Top-level `persist_conversation()` function in `memory/__init__.py`
- **Critical**: This is essential for voice conversation persistence

### 2.3 memory_client.get_facts() Method

- **Status**: ✅ **EXISTS**
- **Location**: `backend/memory/client.py` line 471
- **Usage**: `voice.py` line 326
- **Status**: Method exists, needs verification

### 2.4 memory_client.get_or_create_user() Method

- **Status**: 🔍 **NEEDS CHECK**
- **Location**: `backend/memory/client.py`
- **Usage**: `voice.py` lines 306-313
- **Action**: Verify method exists and signature matches

### 2.5 memory_client.get_or_create_session() Method

- **Status**: ✅ **EXISTS** (likely)
- **Location**: `backend/memory/client.py`
- **Usage**: `voice.py` lines 262-268, 1706-1710
- **Status**: Need to verify exact signature matches legacy engram's

---

## 3. Authentication Dependencies

### 3.1 get_auth() Function

- **Status**: ✅ **EXISTS**
- **Location**: `backend/api/middleware/auth.py` line 202
- **Usage**: `voice.py` line 206
- **Type**: Returns `OIDCAuth` instance (ctxEco) vs `EntraIDAuth` (legacy engram)
- **Status**: Should work, but may need method compatibility check

### 3.2 get_current_user() Function

- **Status**: ✅ **EXISTS**
- **Location**: `backend/api/middleware/auth.py` line 215
- **Usage**: `voice.py` line 1666 (Depends)
- **Status**: Should work correctly

### 3.3 SecurityContext

- **Status**: ✅ **EXISTS**
- **Location**: `backend/core/context.py`
- **Usage**: Voice router throughout
- **Status**: Compatible

### 3.4 Role Enum

- **Status**: ✅ **EXISTS**
- **Location**: `backend/core/context.py`
- **Usage**: `voice.py` line 225 (Role.ADMIN)
- **Status**: Compatible

---

## 4. Agents Module Dependencies

### 4.1 agents.chat

- **Status**: ❌ **MISSING**
- **Location**: Voice router imports `from agents import chat as agent_chat`
- **Usage**: Voice router (may be unused if VoiceLive SDK works)
- **Action**: Verify if actually used - may be fallback for when VoiceLive unavailable

### 4.2 agents.get_agent

- **Status**: ❌ **MISSING**
- **Location**: Voice router imports `from agents import get_agent`
- **Usage**: Voice router (may be unused)
- **Current exports**: Only `get_agent_router` exists
- **Action**: Check if actually used in voice router

---

## 5. Settings Dependencies

### 5.1 get_settings() Function

- **Status**: ✅ **EXISTS**
- **Location**: `backend/core/config.py`
- **Usage**: Voice router throughout
- **Status**: Compatible

### 5.2 Settings.azure_voicelive_* Properties

- **Status**: 🔍 **NEEDS CHECK**
- **Location**: `backend/core/config.py`
- **Required properties**:
  - `azure_voicelive_endpoint`
  - `azure_voicelive_key`
  - `azure_voicelive_model`
  - `azure_voicelive_project_name`
  - `azure_voicelive_api_version`
  - `azure_voicelive_voice`
  - `marcus_voicelive_voice`
  - `sage_voicelive_voice`
  - `azure_speech_key`
  - `azure_speech_region`
  - `onedrive_docs_path` (for stories)
  - `auth_required` (for voice WebSocket auth)

---

## 6. Voice Module Dependencies

### 6.1 voicelive_service

- **Status**: ✅ **EXISTS** (just created)
- **Location**: `backend/voice/voicelive_service.py`
- **Usage**: Voice router throughout
- **Status**: Should work correctly

### 6.2 webrtc_signaling_service

- **Status**: ❌ **MISSING**
- **Location**: `backend/voice/webrtc_signaling.py` (doesn't exist)
- **Usage**: `voice.py` lines 838, 883 (avatar WebRTC connection)
- **Critical**: Required for Avatar video feature
- **Optional**: Feature can work without (audio-only mode)
- **Action**: Can be added later if Avatar video is needed

---

## 7. Import Path Dependencies

### 7.1 core Module Exports

- **Status**: ⚠️ **PARTIAL**
- **Location**: `backend/core/__init__.py`
- **Missing exports**:
  - `MessageRole` ❌
  - `Turn` ❌
- **Current exports**: Role, SecurityContext, EnterpriseContext, etc.
- **Fix needed**: Add `MessageRole` and `Turn` to `__all__` list

---

## 8. Critical Missing Dependencies Summary

### High Priority (Blocks Voice Router)

1. ❌ **MessageRole** enum - Used extensively
2. ❌ **Turn** class - Used for all conversation turns
3. ❌ **EpisodicContext.add_turn()** - Required for memory persistence
4. ❌ **persist_conversation()** - Required for saving conversations
5. ❌ **memory_client** singleton - Required for memory operations

### Medium Priority (Affects Features)

1. ❌ **SemanticContext.add_fact()** - Used for context enrichment
2. ❌ **SemanticContext.get_context_summary()** - Used for personalized instructions
3. ⚠️ **EpisodicContext.recent_turns** - Need to migrate from `recent_messages`

### Low Priority (Optional Features)

1. ❌ **webrtc_signaling_service** - Only needed for Avatar video (audio works without)
2. ❌ **agents.chat / get_agent** - May be unused (fallback for VoiceLive)

---

## 9. Recommended Action Plan

### Phase 1: Critical Dependencies (Voice Router Core)

1. Add `MessageRole` enum to `backend/core/context.py`
2. Add `Turn` class to `backend/core/context.py`
3. Update `EpisodicContext` to use `recent_turns: list[Turn]` instead of `recent_messages`
4. Add `EpisodicContext.add_turn()` method
5. Add `persist_conversation()` method to `ZepMemoryClient`
6. Add `persist_conversation()` function to `backend/memory/__init__.py`
7. Add `memory_client` singleton to `backend/memory/__init__.py`
8. Update `backend/core/__init__.py` to export `MessageRole` and `Turn`

### Phase 2: Context Enrichment (Personalization)

1. Add `SemanticContext.add_fact()` method
2. Add `SemanticContext.get_context_summary()` method

### Phase 3: Optional Features (Avatar Video)

1. Create `backend/voice/webrtc_signaling.py` (if Avatar video is needed)

### Phase 4: Settings Verification

1. Verify all `azure_voicelive_*` settings exist in `config.py`
2. Add missing settings if needed

---

## 10. Testing Checklist

After adding dependencies, verify:

- [ ] Voice router imports without errors
- [ ] `MessageRole` and `Turn` are accessible from `core`
- [ ] `memory_client.persist_conversation()` works with `EnterpriseContext`
- [ ] `EpisodicContext.add_turn()` correctly adds turns
- [ ] Voice WebSocket can persist conversations
- [ ] Context enrichment works (facts injection)
- [ ] Settings are loaded correctly from environment

---

## Notes

- The voice router uses legacy engram's exact pattern, so dependencies should match legacy engram's structure
- Some dependencies may be optional (WebRTC for Avatar) - audio-only mode can work without them
- `agents.chat` and `get_agent` may be unused - verify in voice router code before implementing
- Settings compatibility is critical - ensure all `azure_voicelive_*` environment variables are defined
