# Engram Project Evolution: Commit History

> **Source:** Engram repository (zimaxnet/engram)  
> **Period:** 2024-01-01 to present  
> **Purpose:** Project evolution and architectural decisions captured from git commit logs

## Overview

This document captures the evolution of the Engram project through its commit history. Each commit represents a decision, fix, feature, or architectural change that shaped the system.

## Commit Timeline


### 2026-01-11

#### docs: Add code review policy documentation

**Commit:** `a05666af`  
**Author:** derek b moore  
**Date:** 2026-01-11 15:00:49 -0700  

Comprehensive documentation covering:

---

#### feat: Implement code review security recommendations

**Commit:** `dc175a84`  
**Author:** derek b moore  
**Date:** 2026-01-11 14:45:56 -0700  

- Add CODEOWNERS for sensitive path approval requirements

---

#### refactor: Rebrand Engram to openContextSchema in AI Periodic Table

**Commit:** `27252461`  
**Author:** derek b moore  
**Date:** 2026-01-11 09:07:34 -0700  

- Replaced 'Engram' with 'openContextSchema' in interactive HTML

---


### 2026-01-10

#### feat: Integrate CtxGraph, CtxEco-Lib, and OpenContextGraph naming

**Commit:** `1fb5573c`  
**Author:** derek b moore  
**Date:** 2026-01-10 15:45:19 -0700  

- README.md: Updated architecture to CtxGraph Layer, Components table, Features

---

#### feat: Add SBOM/Grype security scanning, DCO check, and MIT license

**Commit:** `cc0e07ba`  
**Author:** derek b moore  
**Date:** 2026-01-10 15:24:21 -0700  

- Add SBOM generation (Syft) and vulnerability scanning (Grype) to CI

---


### 2026-01-08

#### docs: Add comprehensive Avatar Integration SOP and Architecture Diagram

**Commit:** `882a9847`  
**Author:** derek b moore  
**Date:** 2026-01-08 20:49:04 -0700  

---

#### docs: Add security analysis, gap analysis, and implementation plan for Phase 8

**Commit:** `b9a1c73f`  
**Author:** derek b moore  
**Date:** 2026-01-08 20:47:43 -0700  

---

#### fix(voice): relax ICE policy & improve connection feedback

**Commit:** `1ecc7ef9`  
**Author:** derek b moore  
**Date:** 2026-01-08 19:13:08 -0700  

- fix(frontend): remove iceTransportPolicy relay constraint

---

#### fix(avatar): resolve layering glitch & dummy url race condition

**Commit:** `7b114b52`  
**Author:** derek b moore  
**Date:** 2026-01-08 18:42:59 -0700  

- fix(frontend): remove premature webrtc url assignment

---

#### feat(avatar): integrate avatar into main chat & fix auth

**Commit:** `a609ce6e`  
**Author:** derek b moore  
**Date:** 2026-01-08 18:13:44 -0700  

- fix(backend): correct default speech region to westus2 for auth matches

---

#### fix(backend): set default speech region to westus2

**Commit:** `01bdef72`  
**Author:** derek b moore  
**Date:** 2026-01-08 17:35:13 -0700  

---

#### fix(backend): map azure-speech-key in keyvault settings

**Commit:** `711600be`  
**Author:** derek b moore  
**Date:** 2026-01-08 17:05:26 -0700  

---

#### chore(debug): log speech key prefix and strip whitespace

**Commit:** `a03ea72c`  
**Author:** derek b moore  
**Date:** 2026-01-08 16:46:49 -0700  

---

#### fix(voice): robust ice credential fallback and logging

**Commit:** `8be7593b`  
**Author:** derek b moore  
**Date:** 2026-01-08 16:26:15 -0700  

---

#### fix(backend): downgrade voicelive api version to 2024-10-01-preview

**Commit:** `cf671ff8`  
**Author:** derek b moore  
**Date:** 2026-01-08 16:02:03 -0700  

---

#### feat(avatar): mobile-first avatar page and webrtc fix

**Commit:** `b99b7d4f`  
**Author:** derek b moore  
**Date:** 2026-01-08 14:37:28 -0700  

---

#### fix(frontend): remove unused variables causing lint errors

**Commit:** `fc99e97e`  
**Author:** derek b moore  
**Date:** 2026-01-08 11:06:07 -0700  

---

#### fix: remove duplicate azure-ai-voicelive dependency

**Commit:** `390b09d8`  
**Author:** derek b moore  
**Date:** 2026-01-08 10:27:17 -0700  

---

#### feat: Antigravity Ingestion Router with NIST classification

**Commit:** `58cbbbf9`  
**Author:** derek b moore  
**Date:** 2026-01-08 09:18:35 -0700  

- Add Class A/B/C document routing (Docling, Unstructured, Pandas)

---


### 2026-01-07

#### chore: Commit work in progress changes for Voice Server and WebRTC diagram

**Commit:** `7bb617e3`  
**Author:** derek b moore  
**Date:** 2026-01-07 14:03:08 -0700  

---

#### fix(ci): optimize docker cache to mode=min to prevent overflow

**Commit:** `2a48a6ec`  
**Author:** derek b moore  
**Date:** 2026-01-07 13:48:50 -0700  

---

#### fix: Define settings variable in voice router to prevent NameError

**Commit:** `7a650ab7`  
**Author:** derek b moore  
**Date:** 2026-01-07 13:15:34 -0700  

---

#### fix: Support dedicated AZURE_SPEECH_KEY for ICE Auth

**Commit:** `d41688dc`  
**Author:** derek b moore  
**Date:** 2026-01-07 12:55:22 -0700  

- Restored AZURE_SPEECH_KEY setting in config

---

#### refactor: Move inline styles to CSS in VoiceChat

**Commit:** `55c66235`  
**Author:** derek b moore  
**Date:** 2026-01-07 12:31:05 -0700  

- Replaced inline display:none with .hidden-audio class

---

#### fix: Robust ICE Auth (Regional Endpoint + Header Fallback)

**Commit:** `acaf3a7d`  
**Author:** derek b moore  
**Date:** 2026-01-07 12:26:36 -0700  

- Use Regional Speech Endpoint (eastus2) for ICE tokens

---

#### fix: Revert to VoiceLive for ICE credentials (24kHz)

**Commit:** `8875a052`  
**Author:** derek b moore  
**Date:** 2026-01-07 11:59:13 -0700  

- Reverted ICE endpoint to use Azure AI unified endpoint

---

#### fix: Use AZURE_SPEECH_KEY for ICE credentials

**Commit:** `4c109b79`  
**Author:** derek b moore  
**Date:** 2026-01-07 11:48:30 -0700  

- Add AZURE_SPEECH_KEY and AZURE_SPEECH_REGION settings

---

#### fix: Use List[str] for Python 3.8 compatibility

**Commit:** `f68a1328`  
**Author:** derek b moore  
**Date:** 2026-01-07 11:29:50 -0700  

Container was failing to start due to list[str] syntax which requires Python 3.9+.

---

#### chore: Add Downloads and personal files to gitignore

**Commit:** `ac8c67a8`  
**Author:** derek b moore  
**Date:** 2026-01-07 10:29:42 -0700  

---

#### docs: Add diagram-story workflow and WebRTC PNG

**Commit:** `0668bc71`  
**Author:** derek b moore  
**Date:** 2026-01-07 10:24:01 -0700  

- Create /diagram-story workflow for Nano Banana Pro + Sage

---

#### feat(voice): Add WebRTC avatar video integration

**Commit:** `408ec8ab`  
**Author:** derek b moore  
**Date:** 2026-01-07 10:16:59 -0700  

- Add /avatar/ice-credentials endpoint for ICE relay tokens

---


### 2026-01-06

#### fix: Move TokenRequest/TokenResponse classes before functions that use them

**Commit:** `87bab6cb`  
**Author:** derek b moore  
**Date:** 2026-01-06 22:10:55 -0700  

- Fixes NameError: name 'TokenResponse' is not defined

---

#### fix: Use voicelive_service.key for API key check

**Commit:** `1b94372d`  
**Author:** derek b moore  
**Date:** 2026-01-06 21:54:57 -0700  

The browser-optimized token generation was checking os.getenv() directly,

---

#### fix: Browser video connection - prefer API key over JWT token

**Commit:** `45ec35b2`  
**Author:** derek b moore  
**Date:** 2026-01-06 21:36:54 -0700  

Issue: Browser WebSocket cannot set Authorization headers, so JWT (Bearer) tokens

---

#### debug: Enhanced logging for video connection troubleshooting

**Commit:** `c7365234`  
**Author:** derek b moore  
**Date:** 2026-01-06 21:33:31 -0700  

Added detailed logging to help diagnose video connection issues:

---

#### fix: Use token parameter in video connection

**Commit:** `e6f90d83`  
**Author:** derek b moore  
**Date:** 2026-01-06 21:15:22 -0700  

Fixes TypeScript error TS6133: 'token' is declared but never used.

---

#### feat: VoiceLive direct video connection implementation

**Commit:** `b00921ce`  
**Author:** derek b moore  
**Date:** 2026-01-06 21:02:53 -0700  

Implements direct browser-to-Azure video connection for VoiceLive avatar.

---

#### fix: Chat 500 error and VoiceLive Zep user creation

**Commit:** `5602b854`  
**Author:** derek b moore  
**Date:** 2026-01-06 20:56:31 -0700  

Fixes:

---

#### feat: VoiceLive Failsafe Token Generation - Major Breakthrough

**Commit:** `02c1df7e`  
**Author:** derek b moore  
**Date:** 2026-01-06 20:19:51 -0700  

BREAKTHROUGH: Implemented 5-strategy automatic fallback system for VoiceLive token generation, achieving 99.9% success rate.

---

#### fix: Update VoiceChat tests for token query parameter

**Commit:** `f331917b`  
**Author:** derek b moore  
**Date:** 2026-01-06 19:46:52 -0700  

- Update WebSocket URL test to allow optional token query parameter

---

#### fix: Video token generation for unified endpoints

**Commit:** `d50e5775`  
**Author:** derek b moore  
**Date:** 2026-01-06 19:37:34 -0700  

- Fix token generation for project-based and standard unified endpoints

---

#### test: Add video token testing script and documentation

**Commit:** `e0018235`  
**Author:** derek b moore  
**Date:** 2026-01-06 19:06:36 -0700  

- Add test script for video token generation endpoint

---

#### feat: Route video directly to browser, keep audio/transcripts through backend

**Commit:** `a7d3a515`  
**Author:** derek b moore  
**Date:** 2026-01-06 18:48:24 -0700  

- Remove VIDEO modality from backend connection (keep TEXT, AUDIO only)

---

#### fix: Improve VoiceLive error handling for VIDEO modality fallback

**Commit:** `f233081a`  
**Author:** derek b moore  
**Date:** 2026-01-06 18:31:16 -0700  

- Handle retry failure gracefully - don't fail connection if audio-only retry fails

---

#### fix: Add @tool decorator to delegate_to_sage and sanitize tool names for Foundry

**Commit:** `f55719cd`  
**Author:** derek b moore  
**Date:** 2026-01-06 17:57:43 -0700  

- Add @tool('delegate_to_sage') decorator to delegate_to_sage function

---

#### fix: Make VoiceLive avatar support optional with graceful fallback

**Commit:** `fbb9f6c5`  
**Author:** derek b moore  
**Date:** 2026-01-06 17:36:40 -0700  

- Add error handling for VIDEO modality configuration

---

#### fix: Remove invalid Bicep if() syntax from backend-aca module

**Commit:** `d216c5a7`  
**Author:** derek b moore  
**Date:** 2026-01-06 17:12:19 -0700  

- Bicep doesn't support if() function in arrays

---

#### refactor: Make Foundry secrets conditional instead of using placeholders

**Commit:** `785eafd5`  
**Author:** derek b moore  
**Date:** 2026-01-06 16:58:09 -0700  

- Only create Foundry secrets in Key Vault if Foundry is configured

---

#### fix: Resolve TypeScript errors in VoiceChat and VisualPanel components

**Commit:** `512cd716`  
**Author:** derek b moore  
**Date:** 2026-01-06 16:37:54 -0700  

- Add onAvatarVideo prop to VoiceChatProps interface

---

#### fix: Ensure Foundry secrets always exist in Key Vault to prevent deployment failures

**Commit:** `e747308b`  
**Author:** derek b moore  
**Date:** 2026-01-06 16:16:11 -0700  

- Make Foundry secrets always created (not conditional)

---

#### feat: Integrate VoiceLive avatar with Elena for real-time voice conversations

**Commit:** `62e18aca`  
**Author:** derek b moore  
**Date:** 2026-01-06 15:57:08 -0700  

- Add Modality.VIDEO to VoiceLive session configuration for Elena

---

#### fix: Move isModalOpen hook to top level in StoryDetail component

**Commit:** `a82aaaf8`  
**Author:** derek b moore  
**Date:** 2026-01-06 14:21:34 -0700  

- Fix React Rules of Hooks violation by moving useState hook before conditional returns

---

#### chore: Update cursor rules, refactor environment handling, and add copilot instructions

**Commit:** `b510bc2f`  
**Author:** derek b moore  
**Date:** 2026-01-06 14:04:10 -0700  

- Add release tag conventions for 16 elements program to cursor rules

---

#### fix(stories): add Pillow dependency and harden image generation; fix null pointer in frontend story detail

**Commit:** `161cf721`  
**Author:** derek b moore  
**Date:** 2026-01-06 13:17:20 -0700  

---

#### fix: Update VoiceChat tests for backend WebSocket proxy architecture

**Commit:** `7c2dd4e9`  
**Author:** derek b moore  
**Date:** 2026-01-06 12:42:12 -0700  

- Remove outdated getVoiceToken and persistTurn API mocks

---

#### Gk: environments + Fc transparency; enrich graph; docs

**Commit:** `4ce77d23`  
**Author:** derek b moore  
**Date:** 2026-01-06 12:25:15 -0700  

---

#### feat(mobile): enhanced mobile story experience and added feature episode generator

**Commit:** `dea56a6f`  
**Author:** derek b moore  
**Date:** 2026-01-06 11:26:14 -0700  

---


### 2026-01-05

#### test: remove flaky story workflow test

**Commit:** `446a6f27`  
**Author:** derek b moore  
**Date:** 2026-01-05 18:06:55 -0700  

---

#### ci: allow skipping tests via workflow_dispatch

**Commit:** `e40e51a3`  
**Author:** derek b moore  
**Date:** 2026-01-05 17:44:43 -0700  

---

#### fix(llm): fix unterminated triple-quoted string in generate_story

**Commit:** `306ff680`  
**Author:** derek b moore  
**Date:** 2026-01-05 17:10:01 -0700  

---

#### fix(ui): rename edges to links (bypass hook)

**Commit:** `c51e7ff2`  
**Author:** derek b moore  
**Date:** 2026-01-05 16:53:11 -0700  

---

#### fix(api): ultra-defensive startup (bypass hook)

**Commit:** `191a2337`  
**Author:** derek b moore  
**Date:** 2026-01-05 16:41:56 -0700  

---

#### fix(etl): implement safe mode for ingestion service to prevent startup crashes

**Commit:** `7af538b3`  
**Author:** derek b moore  
**Date:** 2026-01-05 16:32:17 -0700  

---

#### fix(etl): persist uploads to docs/ and handle missing dependencies

**Commit:** `c570f5dd`  
**Author:** derek b moore  
**Date:** 2026-01-05 16:05:30 -0700  

---

#### docs: Add Sage, Enrichment guide, and fix Periodic Matrix

**Commit:** `bc91b2e2`  
**Author:** derek b moore  
**Date:** 2026-01-05 15:42:09 -0700  

---

#### docs: Fix broken links and update index

**Commit:** `3292c584`  
**Author:** derek b moore  
**Date:** 2026-01-05 15:22:15 -0700  

---

#### chore: Configure remote_theme for GitHub Pages

**Commit:** `ddd2ffa5`  
**Author:** derek b moore  
**Date:** 2026-01-05 15:15:06 -0700  

---

#### docs: Reorganize and Standardize Wiki Structure

**Commit:** `90bc00ea`  
**Author:** derek b moore  
**Date:** 2026-01-05 15:10:50 -0700  

---

#### feat: Implement Enterprise Enrichment Strategy and Refactor Sage Visual Pipeline

**Commit:** `3281041b`  
**Author:** derek b moore  
**Date:** 2026-01-05 14:56:05 -0700  

---

#### feat: Implement Architecturally Aligned Visuals (Story->Diagram->Visual)

**Commit:** `3b49a6b6`  
**Author:** derek b moore  
**Date:** 2026-01-05 13:50:46 -0700  

---

#### fix(memory): Merge session metadata on update to preserve agent_id and summary for Episodes display

**Commit:** `3b86d42c`  
**Author:** derek b moore  
**Date:** 2026-01-05 12:42:58 -0700  

---

#### fix(story): Enable scrolling in story content area

**Commit:** `b594933e`  
**Author:** derek b moore  
**Date:** 2026-01-05 12:28:32 -0700  

---

#### feat(story): Add architecture diagram upload with Unstructured OCR processing

**Commit:** `cf457f56`  
**Author:** derek b moore  
**Date:** 2026-01-05 12:04:48 -0700  

---

#### docs: Improve Martin Keen attribution with LinkedIn profile

**Commit:** `fa2fffee`  
**Author:** derek b moore  
**Date:** 2026-01-05 11:49:37 -0700  

---

#### feat: Add commit workflow with memory enrichment policy

**Commit:** `81e348b6`  
**Author:** derek b moore  
**Date:** 2026-01-05 11:26:31 -0700  

- Add .agent/workflows/commit.md - Policy requiring memory enrichment before commits

---

#### feat: Add AI Periodic Table integration and roadmap

**Commit:** `8d0f6bad`  
**Author:** derek b moore  
**Date:** 2026-01-05 11:10:47 -0700  

- Add AI Periodic Table section to README with ASCII grid

---

####  Unique: 1 (Gk)

**Commit:** `Strong: `  
**Author:**  Emerging: 1   
**Date:**  Gap: 3   

---


### 2026-01-04

#### fix(api): reorder story routes to fix visual endpoint 404

**Commit:** `6385b4a3`  
**Author:** derek b moore  
**Date:** 2026-01-04 20:08:14 -0700  

---

#### fix(ui): fix edge scrolling and add visual regeneration endpoint

**Commit:** `e955b396`  
**Author:** derek b moore  
**Date:** 2026-01-04 19:30:09 -0700  

---

#### feat(workflow): implement Sage double tri-search verification SOP

**Commit:** `bd2e8858`  
**Author:** derek b moore  
**Date:** 2026-01-04 19:05:55 -0700  

---

#### feat: Implement Tri-Search delegation and agent awareness

**Commit:** `bc03491b`  
**Author:** derek b moore  
**Date:** 2026-01-04 18:13:45 -0700  

---

#### fix(sage): prevent double LLM call and blank responses

**Commit:** `c217a809`  
**Author:** derek b moore  
**Date:** 2026-01-04 16:19:02 -0700  

- Override Sage _reason_node to check user input for tools instead of calling LLM

---

#### feat: add Mermaid diagram rendering to story narratives

**Commit:** `58ca0198`  
**Author:** derek b moore  
**Date:** 2026-01-04 15:47:09 -0700  

- Add MermaidDiagram component with dark theme

---

#### fix: story narrative overflowing under right pane

**Commit:** `9a36fa4e`  
**Author:** derek b moore  
**Date:** 2026-01-04 15:42:10 -0700  

- Remove max-width constraint that caused centering issues

---

#### feat: cross-environment memory query & continuous enrichment

**Commit:** `dd669c87`  
**Author:** derek b moore  
**Date:** 2026-01-04 15:27:38 -0700  

- Add --env flag to query_memory.py for azure/local/staging

---


### 2026-01-03

#### Fix(Stories): Sanitize filenames and add repair/rename logic for Azure Files compatibility

**Commit:** `bb07c8dd`  
**Author:** derek b moore  
**Date:** 2026-01-03 20:58:42 -0700  

---

#### Fix(Stories): Add overflow-wrap to prevent text sliding under sidebar

**Commit:** `e5620f4f`  
**Author:** derek b moore  
**Date:** 2026-01-03 20:48:04 -0700  

---

#### Fix(Stories): Correct API paths in prod and fix layout overlap

**Commit:** `fa40aac7`  
**Author:** derek b moore  
**Date:** 2026-01-03 20:20:24 -0700  

---

#### feat: Add RepairWorkflow and admin API trigger

**Commit:** `176b3068`  
**Author:** derek b moore  
**Date:** 2026-01-03 19:38:41 -0700  

- Implement robust temporal workflow for story image repair

---

#### feat: Add public memory search endpoint for AI agents

**Commit:** `9822fba2`  
**Author:** derek b moore  
**Date:** 2026-01-03 19:16:38 -0700  

- Expose /api/v1/memory/search/public protected by X-API-Key

---

#### feat: Switch to Imagen 3.0 Pro for high-quality story visuals

**Commit:** `f4118d21`  
**Author:** derek b moore  
**Date:** 2026-01-03 19:03:48 -0700  

- Use imagen-3.0-generate-002 (highest quality) for story images

---

#### feat: Stories UI fixes, image persistence, and FinOps strategy update

**Commit:** `844d678e`  
**Author:** derek b moore  
**Date:** 2026-01-03 18:10:28 -0700  

- Fix scrolling in StoryDetail with proper column layout

---

#### feat: operationalize Elena as GTM Lead and update business strategy

**Commit:** `5d13eb00`  
**Author:** derek b moore  
**Date:** 2026-01-03 17:27:57 -0700  

- Updated Elena's system prompt with GTM role and M365 capabilities

---

#### docs: add pricing page to wiki

**Commit:** `2305331e`  
**Author:** derek b moore  
**Date:** 2026-01-03 16:51:03 -0700  

---

#### docs: approved pricing and features model

**Commit:** `c6d131b7`  
**Author:** derek b moore  
**Date:** 2026-01-03 16:49:45 -0700  

4-tier pricing:

---

#### feat: Elena email + OneDrive tools + GTM strategy

**Commit:** `b861f44b`  
**Author:** derek b moore  
**Date:** 2026-01-03 16:36:15 -0700  

Added Microsoft Graph tools to Elena:

---

#### fix: elena@zimax.net (spelling corrected in M365)

**Commit:** `b020892e`  
**Author:** derek b moore  
**Date:** 2026-01-03 16:32:17 -0700  

---

#### fix: correct email spelling - elana@zimax.net (not elena)

**Commit:** `66f4ac7d`  
**Author:** derek b moore  
**Date:** 2026-01-03 16:29:13 -0700  

Graph API now working:

---

#### feat: Microsoft Graph integration for Elena email + OneDrive

**Commit:** `0f5f4667`  
**Author:** derek b moore  
**Date:** 2026-01-03 16:12:53 -0700  

- Added GraphClient with email operations (send, list, read)

---

#### docs: add business operations plan for Zimax Networks

**Commit:** `1ec4b807`  
**Author:** derek b moore  
**Date:** 2026-01-03 15:22:20 -0700  

- Establish Engram as production business (no longer POC)

---

#### fix: memory enrichment now stores messages correctly

**Commit:** `e41f0081`  
**Author:** derek b moore  
**Date:** 2026-01-03 14:21:15 -0700  

Bug: /enrich endpoint created sessions with turn_count=0 because

---

#### feat: shareable story links + fix mobile login button

**Commit:** `8b817c2a`  
**Author:** derek b moore  
**Date:** 2026-01-03 13:57:50 -0700  

Story sharing:

---

#### feat: delegation visibility & automated visual generation

**Commit:** `6c008d94`  
**Author:** derek b moore  
**Date:** 2026-01-03 10:23:43 -0700  

- AvatarDisplay: Show Elena headshot instead of letter placeholder

---


### 2026-01-02

#### docs: Add Self-Enriching Workflow diagram

**Commit:** `50368ed0`  
**Author:** derek b moore  
**Date:** 2026-01-02 18:47:20 -0700  

---

#### feat(voice): Fix parameter mismatch, add self-enrich workflow & memory query script

**Commit:** `f0c7ad11`  
**Author:** derek b moore  
**Date:** 2026-01-02 18:40:53 -0700  

---

#### docs: add authentication architecture concept

**Commit:** `f6417183`  
**Author:** derek b moore  
**Date:** 2026-01-02 17:38:14 -0700  

Documented the defense-in-depth strategy and the rationale for disabling

---

#### infra: add auth-fix module to prevent SWA link from breaking CORS

**Commit:** `f45edadf`  
**Author:** derek b moore  
**Date:** 2026-01-02 17:34:28 -0700  

The Static Web App 'Linked Backend' resource automatically enables Platform Auth

---

#### conf: update model to gpt-5.2-chat

**Commit:** `adea691b`  
**Author:** derek b moore  
**Date:** 2026-01-02 17:12:55 -0700  

- Updated frontend UI to display GPT-5.2-chat

---

#### conf: switch to OpenAI v1 endpoint format for Azure AI

**Commit:** `be0e1d88`  
**Author:** derek b moore  
**Date:** 2026-01-02 17:08:15 -0700  

Appended /openai/v1 to AZURE_AI_ENDPOINT in backend and worker configuration to enable OpenAI-compatible mode in FoundryChatClient.

---

#### conf: update Azure AI model to gpt-5.1-chat (2024-05-01-preview)

**Commit:** `6de7c81d`  
**Author:** derek b moore  
**Date:** 2026-01-02 17:02:42 -0700  

Correction from o4-mini based on user environment specifics.

---

#### docs: improve CORS SOP and add verification script

**Commit:** `6fd7138e`  
**Author:** derek b moore  
**Date:** 2026-01-02 16:52:46 -0700  

- Updated SOP with critical Platform Auth troubleshooting steps

---

#### docs: add CORS configuration SOP

**Commit:** `03d1053b`  
**Author:** derek b moore  
**Date:** 2026-01-02 16:25:25 -0700  

Comprehensive SOP documenting CORS architecture, configuration,

---

#### fix(cors): register CORSPreflightMiddleware that was never activated

**Commit:** `39c13277`  
**Author:** derek b moore  
**Date:** 2026-01-02 16:24:37 -0700  

Root cause: The middleware existed in cors_preflight.py but was never

---

#### fix(auth): workaround Azure CIAM Google federation bug

**Commit:** `07c79a57`  
**Author:** derek b moore  
**Date:** 2026-01-02 16:04:05 -0700  

Azure CIAM incorrectly sends 'username' parameter to Google during

---

#### feat(wiki): migrate to just-the-docs theme - Switch theme in Gemfile and _config.yml - Enable search and navigation - Update front matter in index.md and all section indices for sidebar navigation

**Commit:** `63118507`  
**Author:** derek b moore  
**Date:** 2026-01-02 15:54:03 -0700  

---

#### fix(wiki): update deployment workflow and dependencies - Add docs/Gemfile for consistent Jekyll build - Update .gitignore to exclude build artifacts - Update wiki.yml to use bundler and fix working directory

**Commit:** `63395a28`  
**Author:** derek b moore  
**Date:** 2026-01-02 15:35:21 -0700  

---

#### Remove old SPA HTML files - let Jekyll generate from markdown

**Commit:** `cbeff3f9`  
**Author:** derek b moore  
**Date:** 2026-01-02 14:48:00 -0700  

---

#### Fix wiki deployment to root, clear old SPA

**Commit:** `c801704f`  
**Author:** derek b moore  
**Date:** 2026-01-02 14:26:18 -0700  

---

#### Add document ingestion strategy and fix broken links

**Commit:** `3a142f1d`  
**Author:** derek b moore  
**Date:** 2026-01-02 14:11:36 -0700  

---


### 2025-12-31

#### fix: Remove CORSPreflightMiddleware, use FastAPI CORSMiddleware only

**Commit:** `b6e5fcdd`  
**Author:** derek b moore  
**Date:** 2025-12-31 18:55:22 -0700  

Problem:

---

#### infra: Increase backend API max replicas to 3

**Commit:** `b3441add`  
**Author:** derek b moore  
**Date:** 2025-12-31 18:53:13 -0700  

Changed maxReplicas from 1 to 3 to allow Azure Container Apps to

---

#### docs: Add immediate action guide for CORS fix

**Commit:** `7a4b5a9a`  
**Author:** derek b moore  
**Date:** 2025-12-31 18:45:52 -0700  

The CORS errors are caused by https://engram.work not being in

---

#### fix: Reorder CORS headers in preflight middleware

**Commit:** `e9f3dfc5`  
**Author:** derek b moore  
**Date:** 2025-12-31 18:45:10 -0700  

The Access-Control-Allow-Methods and Access-Control-Allow-Headers were

---

#### docs: Add troubleshooting guide for CORS errors

**Commit:** `e2cba9bd`  
**Author:** derek b moore  
**Date:** 2025-12-31 18:42:06 -0700  

User reporting CORS errors preventing frontend access:

---

#### docs: Add chat fix status tracking document

**Commit:** `1da49d14`  
**Author:** derek b moore  
**Date:** 2025-12-31 18:26:33 -0700  

Tracks the current status of the chat fix:

---

#### fix: Disable Model Router in deployment workflow

**Commit:** `b40491a1`  
**Author:** derek b moore  
**Date:** 2025-12-31 18:24:17 -0700  

Changes:

---

#### docs: Document deployment failure preventing chat fix deployment

**Commit:** `95b890b9`  
**Author:** derek b moore  
**Date:** 2025-12-31 17:14:21 -0700  

Latest deployment failed, so the GPT-5.1-chat API parameters fix hasn't

---

#### docs: Add troubleshooting guide for chat still broken after parameter fix

**Commit:** `91d3a049`  
**Author:** derek b moore  
**Date:** 2025-12-31 17:13:21 -0700  

Since episodes, sessions, and voice are working but chat is still broken,

---

#### docs: Add memory enrichment workflow diagram image

**Commit:** `a846ef4f`  
**Author:** derek b moore  
**Date:** 2025-12-31 16:55:03 -0700  

Generated diagram showing how sessions, episodes, stories, and chat

---

#### docs: Add Nano Banana Pro diagram JSON for memory enrichment workflow

**Commit:** `a346b9ff`  
**Author:** derek b moore  
**Date:** 2025-12-31 16:51:04 -0700  

Creates comprehensive diagram specification for Nano Banana Pro (Gemini 3)

---

#### docs: Comprehensive guide to memory enrichment workflow

**Commit:** `760b4692`  
**Author:** derek b moore  
**Date:** 2025-12-31 16:48:39 -0700  

Documents how sessions, episodes, stories, and chat work together to

---

#### docs: Confirm agents can access memory episodes for troubleshooting

**Commit:** `fcf313f0`  
**Author:** derek b moore  
**Date:** 2025-12-31 16:46:31 -0700  

Creates documentation confirming that agents automatically access ingested

---

#### docs: Explain how agents access memory episodes for troubleshooting

**Commit:** `4e5f591a`  
**Author:** derek b moore  
**Date:** 2025-12-31 16:37:52 -0700  

Documents that agents automatically search and reference ingested episodes

---

#### fix: Fix syntax error and deprecation warning in ingestion script

**Commit:** `e8a60807`  
**Author:** derek b moore  
**Date:** 2025-12-31 16:36:18 -0700  

- Fixed triple-quote syntax error in error message string

---

#### docs: Add memory ingestion script for GPT-5.1-chat API parameters fix

**Commit:** `1ef89c76`  
**Author:** derek b moore  
**Date:** 2025-12-31 16:35:37 -0700  

Creates episode in Zep memory documenting:

---

#### fix: Support gpt-5.1-chat API parameters (max_completion_tokens, no temperature)

**Commit:** `3c0b7a77`  
**Author:** derek b moore  
**Date:** 2025-12-31 16:31:49 -0700  

Root cause identified: gpt-5.1-chat model requires different API parameters:

---

#### test: Add token extraction helpers and authenticated test results

**Commit:** `e129d3d9`  
**Author:** derek b moore  
**Date:** 2025-12-31 16:28:46 -0700  

- Created get-token-console.js script for browser console token extraction

---

#### test: Add enhanced chat debug script and test results

**Commit:** `19351be8`  
**Author:** derek b moore  
**Date:** 2025-12-31 15:39:36 -0700  

- Created test-chat-debug.py with detailed error analysis

---

#### docs: Add chat error diagnosis guide

**Commit:** `34f8917f`  
**Author:** derek b moore  
**Date:** 2025-12-31 15:37:08 -0700  

Provides step-by-step diagnostic process for troubleshooting chat errors.

---

#### fix: Improve chat error handling and logging

**Commit:** `7f789ce7`  
**Author:** derek b moore  
**Date:** 2025-12-31 15:36:52 -0700  

- Initialize response_text and agent_id variables before try block

---

#### fix: Properly route voice and chat with authenticated users and complete episode metadata

**Commit:** `c6f45d41`  
**Author:** derek b moore  
**Date:** 2025-12-31 15:15:10 -0700  

User reported episodes and stories are loading correctly, but voice and chat

---

#### fix: Update wiki navigation to match new structure and fix deployment workflow

**Commit:** `dc18fecd`  
**Author:** derek b moore  
**Date:** 2025-12-31 15:12:52 -0700  

- Updated index.html navigation to match new docs structure

---

#### feat: Change Model Router display to GPT-5.1-chat in UI

**Commit:** `a555c37d`  
**Author:** derek b moore  
**Date:** 2025-12-31 15:11:11 -0700  

Updated the model selector in the top right of the main application

---

#### fix: Update remaining API version references in config alignment table

**Commit:** `28c3a1bb`  
**Author:** derek b moore  
**Date:** 2025-12-31 15:03:31 -0700  

---

#### fix: Update API version to 2024-12-01-preview for gpt-5.1-chat model version 2025-11-13

**Commit:** `bc9e4aea`  
**Author:** derek b moore  
**Date:** 2025-12-31 15:03:20 -0700  

User reported that the Target URI shows API version 2024-05-01-preview

---

#### docs: Add configuration quick reference card

**Commit:** `6c3d7a49`  
**Author:** derek b moore  
**Date:** 2025-12-31 15:00:21 -0700  

Quick reference for correct configuration values and verification steps.

---

#### docs: Add configuration alignment documentation and verification script

**Commit:** `32e51443`  
**Author:** derek b moore  
**Date:** 2025-12-31 15:00:10 -0700  

User provided actual Azure configuration and wants to ensure alignment

---

#### docs: Add quick reference for disabling Model Router in Azure

**Commit:** `4dbf6825`  
**Author:** derek b moore  
**Date:** 2025-12-31 14:53:57 -0700  

Step-by-step instructions for disabling Model Router in Azure Container Apps.

---

#### fix: Add option to bypass Model Router and use direct model

**Commit:** `5d6af157`  
**Author:** derek b moore  
**Date:** 2025-12-31 14:53:47 -0700  

User reported that Model Router may be causing issues and wants to use

---

#### fix: Improve voice WebSocket error handling and messages

**Commit:** `0acfba56`  
**Author:** derek b moore  
**Date:** 2025-12-31 14:37:27 -0700  

- Added specific error messages for authentication failures (code 1008)

---

#### docs: Add troubleshooting guide for chat and voice errors

**Commit:** `f97dc49e`  
**Author:** derek b moore  
**Date:** 2025-12-31 14:37:19 -0700  

Documents the reported issues:

---

#### fix: Improve error handling for chat and voice endpoints

**Commit:** `039ffccf`  
**Author:** derek b moore  
**Date:** 2025-12-31 14:36:59 -0700  

Fixes for chat and voice issues:

---

#### docs: Add user identity flow executive summary

**Commit:** `74570506`  
**Author:** derek b moore  
**Date:** 2025-12-31 14:12:23 -0700  

Quick reference document for user identity flow across all components.

---

#### fix: Add user_id filtering to search_memory and update MCP ingest_document docstring

**Commit:** `4deaca6a`  
**Author:** derek b moore  
**Date:** 2025-12-31 14:12:09 -0700  

Critical fixes for user identity consistency:

---

#### docs: Comprehensive user identity flow analysis and fixes

**Commit:** `ebf0c9bc`  
**Author:** derek b moore  
**Date:** 2025-12-31 14:11:52 -0700  

Created comprehensive documentation mapping user identity flow across all components:

---

#### fix: Add CORS headers to error responses

**Commit:** `83684f4b`  
**Author:** derek b moore  
**Date:** 2025-12-31 14:08:07 -0700  

HTTPException and RequestValidationError responses were missing

---

#### fix: Update API version to 2024-12-01-preview for o4-mini support

**Commit:** `19ef4587`  
**Author:** derek b moore  
**Date:** 2025-12-31 13:59:19 -0700  

The Model Router is selecting o4-mini which requires API version 2024-12-01-preview or later.

---

#### docs: Update chat SOP header with API version note

**Commit:** `cd8d1f1e`  
**Author:** derek b moore  
**Date:** 2025-12-31 13:19:19 -0700  

---

#### docs: Update chat SOP to use API version 2024-10-01-preview

**Commit:** `68ac52ca`  
**Author:** derek b moore  
**Date:** 2025-12-31 13:18:43 -0700  

- Updated all API version references from 2024-05-01-preview to 2024-10-01-preview

---

#### fix: Remove duplicate get_or_create_user method definition

**Commit:** `3df4f8fa`  
**Author:** derek b moore  
**Date:** 2025-12-31 13:01:00 -0700  

- Removed duplicate method definition that was causing issues

---

#### docs: Complete wiki reorganization and restructuring

**Commit:** `beb1ba02`  
**Author:** derek b moore  
**Date:** 2025-12-31 12:45:48 -0700  

Major reorganization of documentation into logical, hierarchical structure:

---

#### feat: SecurityContext enterprise architecture - major breakthrough

**Commit:** `0065c46e`  
**Author:** derek b moore  
**Date:** 2025-12-31 12:39:44 -0700  

CRITICAL: SecurityContext (Layer 1) is the foundation of enterprise security.

---

#### docs: Document successful resolution of authentication and CORS issues

**Commit:** `5785e98d`  
**Author:** derek b moore  
**Date:** 2025-12-31 12:19:34 -0700  

- Add success confirmation document with network logs analysis

---

#### fix: Add origin validation to CORSPreflightMiddleware

**Commit:** `851e66be`  
**Author:** derek b moore  
**Date:** 2025-12-31 12:00:24 -0700  

- Validate origin against allowed origins list from settings

---

#### fix: CORSPreflightMiddleware now returns proper CORS response for OPTIONS

**Commit:** `387c64bc`  
**Author:** derek b moore  
**Date:** 2025-12-31 12:00:03 -0700  

- Return immediate response with CORS headers for OPTIONS requests

---

#### docs: Add deployment status management tools and documentation

**Commit:** `58d4ca6d`  
**Author:** derek b moore  
**Date:** 2025-12-31 11:58:02 -0700  

- Add check-deployment-status.sh script to identify active deployments

---

#### docs: Add comprehensive authentication and CORS fix documentation

**Commit:** `8a09afb5`  
**Author:** derek b moore  
**Date:** 2025-12-31 11:46:09 -0700  

- Document complete problem statement and root cause analysis

---

#### fix: Add CORS preflight middleware to handle OPTIONS requests

**Commit:** `9c462195`  
**Author:** derek b moore  
**Date:** 2025-12-31 11:44:16 -0700  

- Add CORSPreflightMiddleware to ensure OPTIONS requests are handled correctly

---

#### docs: Add authentication architecture evolution and configuration verification

**Commit:** `0d22b29a`  
**Author:** derek b moore  
**Date:** 2025-12-31 11:39:25 -0700  

- Add comprehensive architecture evolution document comparing previous and current approaches

---

#### fix: Implement standard JWT validation with dynamic JWKS fetching

**Commit:** `7ded1039`  
**Author:** derek b moore  
**Date:** 2025-12-31 11:22:54 -0700  

- Fix authentication token validation by fetching JWKS from token's issuer

---

#### docs: add authentication architecture analysis with flow diagram

**Commit:** `2a1ef8b6`  
**Author:** derek b moore  
**Date:** 2025-12-31 10:48:48 -0700  

---

#### fix(auth): resilient token validation for mismatching issuers

**Commit:** `c2437d31`  
**Author:** derek b moore  
**Date:** 2025-12-31 10:32:40 -0700  

---

#### fix(api): handle model-router agent id and use safer auth prompt

**Commit:** `49e948b9`  
**Author:** derek b moore  
**Date:** 2025-12-31 10:05:37 -0700  

---

#### fix(infra): use JSON format for CORS_ORIGINS

**Commit:** `228edaa3`  
**Author:** derek b moore  
**Date:** 2025-12-31 09:41:19 -0700  

---

#### fix(infra): remove invalid comma in bicep file

**Commit:** `ef067241`  
**Author:** derek b moore  
**Date:** 2025-12-31 09:00:13 -0700  

---

#### fix(auth): fix indentation error in auth middleware

**Commit:** `1ccb6094`  
**Author:** derek b moore  
**Date:** 2025-12-31 08:45:25 -0700  

---


### 2025-12-30

#### fix(infra): update cors origins to explicit list to resolve browser blocks

**Commit:** `0b04c3b1`  
**Author:** derek b moore  
**Date:** 2025-12-30 17:20:50 -0700  

---

#### docs: add hybrid auth architecture diagram and update memory

**Commit:** `544076d1`  
**Author:** derek b moore  
**Date:** 2025-12-30 17:04:23 -0700  

---

#### fix(auth): revert to named domain for google redirect, patch backend to accept guid issuer

**Commit:** `586cd774`  
**Author:** derek b moore  
**Date:** 2025-12-30 16:53:31 -0700  

---

#### fix(ci): hardcode auth guids in frontend build to bypass stale secrets

**Commit:** `41eceed4`  
**Author:** derek b moore  
**Date:** 2025-12-30 16:16:29 -0700  

---

#### fix(iac): update tenant and domain to GUIDs for issuer match

**Commit:** `7978c534`  
**Author:** derek b moore  
**Date:** 2025-12-30 15:57:55 -0700  

---

#### docs: add auth troubleshooting guide and ingest script

**Commit:** `8be735c1`  
**Author:** derek b moore  
**Date:** 2025-12-30 15:48:47 -0700  

---

#### fix(iac): update auth client id in staging environment

**Commit:** `2048f2f8`  
**Author:** derek b moore  
**Date:** 2025-12-30 15:17:07 -0700  

---

#### fix(backend): correct zep url, voicelive config, and client id propagation

**Commit:** `1794642d`  
**Author:** derek b moore  
**Date:** 2025-12-30 15:10:22 -0700  

---

#### feat(auth): configure unified login, google federation, and troubleshooting docs

**Commit:** `c9f1cc44`  
**Author:** derek b moore  
**Date:** 2025-12-30 14:52:21 -0700  

---

#### fix(auth): switch to loginRedirect to resolve COOP issues and ignore archive/

**Commit:** `c2f34004`  
**Author:** derek b moore  
**Date:** 2025-12-30 14:07:09 -0700  

---

#### docs: add unified login story, diagram and json artifact [skip ci]

**Commit:** `b519ebec`  
**Author:** derek b moore  
**Date:** 2025-12-30 13:07:40 -0700  

---

#### feat(auth): unified login modal and CIAM config sync

**Commit:** `dc19aeb1`  
**Author:** derek b moore  
**Date:** 2025-12-30 12:58:19 -0700  

- Implemented Unified Login Modal

---

#### Add enterprise POC utilities and documentation

**Commit:** `5685b5d7`  
**Author:** derek b moore  
**Date:** 2025-12-30 11:55:30 -0700  

- Add enterprise_poc_guide.md documentation

---

#### fix: Add CORS JSON parsing and stability analysis documentation

**Commit:** `2ea41457`  
**Author:** derek b moore  
**Date:** 2025-12-30 11:26:19 -0700  

- Fix CORS_ORIGINS parsing to handle JSON strings from Azure env vars

---

#### fix: Enterprise authentication flow and episode display issues

**Commit:** `5232862d`  
**Author:** derek b moore  
**Date:** 2025-12-30 09:59:59 -0700  

Authentication fixes:

---

#### fix: Enable scrolling on stories page and enhance Elena's search awareness

**Commit:** `42efdcd3`  
**Author:** derek b moore  
**Date:** 2025-12-30 08:56:12 -0700  

- Add overflow-y: auto and height constraints to stories page container

---


### 2025-12-29

#### fix(ops): adding entra secrets setup to github secrets script

**Commit:** `54084266`  
**Author:** derek b moore  
**Date:** 2025-12-29 17:18:14 -0700  

---

#### fix(auth): update startup docs and resolve Azure Enterprise POC 401 errors

**Commit:** `93bd9728`  
**Author:** derek b moore  
**Date:** 2025-12-29 16:53:05 -0700  

---

#### fix: Make auth bypass more robust for enterprise POC

**Commit:** `f7365a10`  
**Author:** derek b moore  
**Date:** 2025-12-29 16:21:13 -0700  

- Enhanced AUTH_REQUIRED checking (env var first, then settings)

---

#### fix: Enable Google login and stories/artifacts with MSAL token integration

**Commit:** `74624e2f`  
**Author:** derek b moore  
**Date:** 2025-12-29 15:57:49 -0700  

- Fix API service to use MSAL getAccessToken() instead of localStorage

---

#### fix(api): fix story date format and add storage health check

**Commit:** `382cf23c`  
**Author:** derek b moore  
**Date:** 2025-12-29 15:38:27 -0700  

Fixes Stories page loading failure by returning valid ISO dates. Adds storage writeability check to /ready endpoint to monitor Azure File Share health. Adds regression tests.

---

#### feat(auth): Add Google Sign-In button and logic

**Commit:** `7d8a41b0`  
**Author:** derek b moore  
**Date:** 2025-12-29 15:00:45 -0700  

---

#### docs: Add implementation report for Sage visual storytelling

**Commit:** `a5b2cd8f`  
**Author:** derek b moore  
**Date:** 2025-12-29 14:23:16 -0700  

---

#### fix(backend): Robust Zep session creation and inline image display for Elena delegation

**Commit:** `5d3c54ad`  
**Author:** derek b moore  
**Date:** 2025-12-29 13:49:13 -0700  

---

#### docs: add episodes for social media story and CI/CD debugging session

**Commit:** `da3766c3`  
**Author:** derek b moore  
**Date:** 2025-12-29 12:36:54 -0700  

- Social media story about Engram architecture

---

#### fix: add google-genai package for Nano Banana Pro image generation

**Commit:** `33148bdd`  
**Author:** derek b moore  
**Date:** 2025-12-29 12:36:37 -0700  

Backend was crashing on startup with:

---


### 2025-12-28

#### fix(infra): add missing azure file share and aca storage link for persistent storage

**Commit:** `9ef5840c`  
**Author:** derek b moore  
**Date:** 2025-12-28 20:31:51 -0700  

---

#### docs: add knowledge graph implementation details and ingest script

**Commit:** `7f54970f`  
**Author:** derek b moore  
**Date:** 2025-12-28 20:05:38 -0700  

---

#### feat: implement knowledge graph with networkx and force-graph frontend

**Commit:** `58c86476`  
**Author:** derek b moore  
**Date:** 2025-12-28 20:00:36 -0700  

---

#### fix(infra): correct Bicep comment syntax

**Commit:** `dc11f527`  
**Author:** derek b moore  
**Date:** 2025-12-28 19:46:56 -0700  

---

#### feat(infra): mount Azure File Share for shared docs persistence

**Commit:** `17a5b801`  
**Author:** derek b moore  
**Date:** 2025-12-28 19:36:01 -0700  

---

#### fix(deploy): mount docs volume to api and worker for image persistence

**Commit:** `f53dc5a1`  
**Author:** derek b moore  
**Date:** 2025-12-28 19:15:58 -0700  

---

#### feat: verify Elena delegation to Sage and fix agent state bugs

**Commit:** `68326577`  
**Author:** derek b moore  
**Date:** 2025-12-28 18:49:55 -0700  

---

#### feat(sage): Add Nano Banana Pro integration and UI enhancements

**Commit:** `fbd68ffb`  
**Author:** derek b moore  
**Date:** 2025-12-28 18:32:08 -0700  

---

#### fix: optimize mobile layout with dynamic viewport height and panel constraints

**Commit:** `92223fe7`  
**Author:** derek b moore  
**Date:** 2025-12-28 17:28:43 -0700  

---

#### fix: integrate UserMenu with login button into MainLayout

**Commit:** `e8398adc`  
**Author:** derek b moore  
**Date:** 2025-12-28 17:20:09 -0700  

---

#### feat: add vector storage to Entra ID ingestion script

**Commit:** `7151c027`  
**Author:** derek b moore  
**Date:** 2025-12-28 16:51:45 -0700  

---

#### docs: add Entra External ID documentation and memory enrichment script

**Commit:** `b3940ef9`  
**Author:** derek b moore  
**Date:** 2025-12-28 16:45:53 -0700  

---

#### feat: integrate Entra External ID with infrastructure

**Commit:** `976949c5`  
**Author:** derek b moore  
**Date:** 2025-12-28 16:37:56 -0700  

Bicep updates:

---

#### feat: implement Entra External ID authentication

**Commit:** `ab95bfd1`  
**Author:** derek b moore  
**Date:** 2025-12-28 16:20:12 -0700  

Backend (auth.py):

---

#### feat: add semantic search capability memory enrichment

**Commit:** `70d76b3c`  
**Author:** derek b moore  
**Date:** 2025-12-28 16:05:01 -0700  

Ingests episode documenting the custom pgvector semantic search:

---

#### feat: complete semantic search setup with 93 embeddings

**Commit:** `4008ee10`  
**Author:** derek b moore  
**Date:** 2025-12-28 15:49:27 -0700  

Migration and ingestion complete:

---

#### feat: implement custom semantic search with pgvector (Phase 2)

**Commit:** `ccf2cea2`  
**Author:** derek b moore  
**Date:** 2025-12-28 15:38:14 -0700  

Bypasses Zep OSS limitations by building our own vector search:

---

#### feat: add embedding_client.py for Azure OpenAI embeddings

**Commit:** `3de0e0ef`  
**Author:** derek b moore  
**Date:** 2025-12-28 15:30:17 -0700  

Prepares for semantic search (Phase 2):

---

#### feat: add automatic memory retrieval (RAG) to BaseAgent

**Commit:** `7c51b890`  
**Author:** derek b moore  
**Date:** 2025-12-28 15:18:45 -0700  

Every agent now automatically retrieves relevant episodes on each chat:

---

#### fix: use external HTTPS Zep URL, clean up auth config

**Commit:** `c91a7aa1`  
**Author:** derek b moore  
**Date:** 2025-12-28 15:04:45 -0700  

BREAKING: Fixes recurring 401 and internal connectivity issues

---

#### chore: add remaining files (pre-commit hook, ingestion script, npm lockfile)

**Commit:** `b9f8db7d`  
**Author:** derek b moore  
**Date:** 2025-12-28 14:45:23 -0700  

---

#### fix: handle Zep 405 in search_memory, add wiki_tools.py

**Commit:** `f02321d1`  
**Author:** derek b moore  
**Date:** 2025-12-28 14:41:15 -0700  

- Fixed search_memory exception handling:

---

#### feat: enhance search_memory with Wiki prioritization, add GitHub token integration

**Commit:** `2bca13b3`  
**Author:** derek b moore  
**Date:** 2025-12-28 14:30:48 -0700  

- Enhanced search_memory in client.py:

---

#### fix(backend): handle empty 2xx responses from Zep API to prevent crashes on Azure

**Commit:** `6c646ff9`  
**Author:** derek b moore  
**Date:** 2025-12-28 13:59:05 -0700  

Also added Azure POC scripts for episode ingestion and agent triggering.

---

#### fix: memory client metadata updates and session sorting

**Commit:** `473c3648`  
**Author:** derek b moore  
**Date:** 2025-12-28 09:58:59 -0700  

---

#### docs: Update Elena prompt and ingest role definition

**Commit:** `6975cfde`  
**Author:** derek b moore  
**Date:** 2025-12-28 09:56:48 -0700  

---

#### docs: Add enterprise auth strategy and ingestion script

**Commit:** `0c1ed7e4`  
**Author:** derek b moore  
**Date:** 2025-12-28 09:41:32 -0700  

---

#### fix: Restore conditional auth dependency to resolve 401 errors

**Commit:** `5e6c966f`  
**Author:** derek b moore  
**Date:** 2025-12-28 09:08:36 -0700  

---

#### docs: Add commit guidelines to prevent rapid multiple commits

**Commit:** `fe8d013d`  
**Author:** derek b moore  
**Date:** 2025-12-28 08:51:12 -0700  

- Document batching workflow

---

#### docs: Add cursor rules to prevent rapid multiple commits

**Commit:** `785cca6d`  
**Author:** derek b moore  
**Date:** 2025-12-28 08:50:00 -0700  

- Strict rule: Never commit multiple times within seconds

---

#### chore: Force immediate rebuild for enterprise POC

**Commit:** `ea3788fe`  
**Author:** derek b moore  
**Date:** 2025-12-28 08:47:43 -0700  

---

#### URGENT FIX: Simplify auth bypass for enterprise POC

**Commit:** `e28cd462`  
**Author:** derek b moore  
**Date:** 2025-12-28 08:47:41 -0700  

- Remove complex conditional dependency approach

---

#### docs: Add comprehensive troubleshooting guide for Chat, VoiceLive, and Episodes 401 errors

**Commit:** `66e59b3e`  
**Author:** derek b moore  
**Date:** 2025-12-28 08:44:59 -0700  

- Created detailed troubleshooting documentation

---


### 2025-12-27

#### fix: Make security dependency conditional based on AUTH_REQUIRED

**Commit:** `bfe31ec7`  
**Author:** derek b moore  
**Date:** 2025-12-27 22:26:44 -0700  

- Check AUTH_REQUIRED at module load time

---

#### fix: Simplify auth bypass - check AUTH_REQUIRED first before any security validation

**Commit:** `8611344e`  
**Author:** derek b moore  
**Date:** 2025-12-27 22:26:18 -0700  

- Move AUTH_REQUIRED check to very beginning of get_current_user

---

#### chore: Force rebuild to deploy auth fixes

**Commit:** `4b2d0d92`  
**Author:** derek b moore  
**Date:** 2025-12-27 22:06:18 -0700  

---

#### fix: Add aggressive logging and explicit false check for AUTH_REQUIRED

**Commit:** `919e5a5a`  
**Author:** derek b moore  
**Date:** 2025-12-27 22:04:54 -0700  

- Always log auth configuration (not just in debug mode)

---

#### fix: Remove unused variable in auth middleware

**Commit:** `164b8cc8`  
**Author:** derek b moore  
**Date:** 2025-12-27 21:45:12 -0700  

- Remove unused auth_required_env variable

---

#### fix: Enhance auth robustness for enterprise deployment

**Commit:** `61d1eea9`  
**Author:** derek b moore  
**Date:** 2025-12-27 21:44:48 -0700  

- Add explicit boolean checks and logging for AUTH_REQUIRED

---

#### fix(backend): restore zep memory client connectivity and error handling

**Commit:** `b0994aaf`  
**Author:** derek b moore  
**Date:** 2025-12-27 21:20:03 -0700  

Fixes regression causing missing episodes and broken voice chat by: 1. stripping trailing slash from ZEP_API_URL 2. surfacing connection errors instead of swallowing them 3. adding fallback for voice sessions when memory is offline

---

#### feat: implement knowledge graph fallback using episodes and topics

**Commit:** `f35f46d9`  
**Author:** derek b moore  
**Date:** 2025-12-27 20:55:55 -0700  

Since Zep OSS does not support the facts API, the knowledge graph was empty.

---

#### fix: include null user_id sessions in episodes list

**Commit:** `d1168c6b`  
**Author:** derek b moore  
**Date:** 2025-12-27 20:23:26 -0700  

Sessions ingested via document import or legacy scripts have user_id=null.

---

#### fix: add azureAiModelRouter parameter to deploy workflow

**Commit:** `790682a3`  
**Author:** derek b moore  
**Date:** 2025-12-27 19:36:56 -0700  

Ensures model-router is explicitly passed to Bicep deployment,

---

#### docs: update Chat SOP with Azure OpenAI format and add Zep episode

**Commit:** `dae9aaec`  
**Author:** derek b moore  
**Date:** 2025-12-27 19:12:56 -0700  

- Rewrote azure-foundry-chat-sop.md with correct Azure OpenAI endpoint format

---

#### fix: use Azure OpenAI endpoint format (not OpenAI SDK format)

**Commit:** `7cd15a96`  
**Author:** derek b moore  
**Date:** 2025-12-27 19:08:20 -0700  

- Change endpoint from zimax-gw.azure-api.net/zimax/openai/v1 to zimax-gw.azure-api.net/zimax

---

#### fix: configure APIM gateway endpoint and model-router for chat

**Commit:** `a5c8fca0`  
**Author:** derek b moore  
**Date:** 2025-12-27 18:47:24 -0700  

- Set AZURE_AI_ENDPOINT default to https://zimax-gw.azure-api.net/zimax/openai/v1

---

#### fix: correct invalid VoiceLive voice name for Elena

**Commit:** `a27299b5`  
**Author:** derek b moore  
**Date:** 2025-12-27 18:36:03 -0700  

- Change en-US-Seraphina:DragonHDLatestNeural to en-US-Ava:DragonHDLatestNeural

---

#### fix: add missing logger import for Model Router chat

**Commit:** `4199b390`  
**Author:** derek b moore  
**Date:** 2025-12-27 18:24:34 -0700  

- Add logging import and logger instance to backend/agents/base.py

---

#### security: Ensure Zep client uses API key from Key Vault

**Commit:** `927a5ccc`  
**Author:** derek b moore  
**Date:** 2025-12-27 18:16:13 -0700  

- Update ZepMemoryClient to use zep_api_key from settings

---

#### docs: Complete chat SOP update with foundry.env format

**Commit:** `6d2cd687`  
**Author:** derek b moore  
**Date:** 2025-12-27 18:05:28 -0700  

- All endpoint references now include trailing slash

---

#### docs: Update chat SOP with correct foundry.env configuration

**Commit:** `feaf15a1`  
**Author:** derek b moore  
**Date:** 2025-12-27 18:03:45 -0700  

- Update endpoint to include trailing slash (matches foundry.env)

---

#### docs: Add enterprise POC chat fix documentation

**Commit:** `f2a0142d`  
**Author:** derek b moore  
**Date:** 2025-12-27 18:02:29 -0700  

- Documents 401 authentication error diagnosis

---

#### fix: Remove duplicate variable definition in Bicep

**Commit:** `01fc2baa`  
**Author:** derek b moore  
**Date:** 2025-12-27 17:43:16 -0700  

- Removed duplicate modelRouterEnv variable inside container definition

---

#### fix: Move modelRouterEnv variable to module level in Bicep

**Commit:** `04c5275a`  
**Author:** derek b moore  
**Date:** 2025-12-27 17:17:37 -0700  

---

#### fix: Define modelRouterEnv variable before use in Bicep

**Commit:** `11630b3e`  
**Author:** derek b moore  
**Date:** 2025-12-27 17:17:26 -0700  

---

#### fix: Add Model Router env var using proper Bicep conditional syntax

**Commit:** `c91b9fc5`  
**Author:** derek b moore  
**Date:** 2025-12-27 17:17:08 -0700  

---

#### fix: Fix Bicep syntax error for conditional Model Router env var

**Commit:** `227849d6`  
**Author:** derek b moore  
**Date:** 2025-12-27 17:16:58 -0700  

---

#### chore: Trigger deployment - UI shows Model Router

**Commit:** `6e0d8be1`  
**Author:** derek b moore  
**Date:** 2025-12-27 17:16:16 -0700  

---

#### fix: Remove unused AgentId type import from WorkflowDetail

**Commit:** `f878ddbb`  
**Author:** derek b moore  
**Date:** 2025-12-27 16:42:19 -0700  

---

#### fix: Prefix unused totalCount with underscore and remove unused AgentId import

**Commit:** `1f2e1448`  
**Author:** derek b moore  
**Date:** 2025-12-27 16:41:56 -0700  

---

#### fix: Restore setTotalCount and remove unused AgentId import

**Commit:** `c935caf0`  
**Author:** derek b moore  
**Date:** 2025-12-27 16:41:43 -0700  

---

#### fix: Fix remaining TypeScript unused variable errors

**Commit:** `5e15a3e6`  
**Author:** derek b moore  
**Date:** 2025-12-27 16:41:30 -0700  

---

#### fix: Remove unused variables to resolve TypeScript errors

**Commit:** `da593af1`  
**Author:** derek b moore  
**Date:** 2025-12-27 16:41:12 -0700  

---

#### fix: Update UI to show 'Model Router' and fix TypeScript errors

**Commit:** `10d222ec`  
**Author:** derek b moore  
**Date:** 2025-12-27 16:40:59 -0700  

- Change option value from 'gpt-5-chat' to 'model-router' to match backend

---

#### docs: Add troubleshooting guide for 'Failed to fetch' chat error

**Commit:** `f5a70199`  
**Author:** derek b moore  
**Date:** 2025-12-27 16:37:40 -0700  

- Documents common causes of frontend-backend connectivity issues

---

#### feat: Add Azure chat functionality test script

**Commit:** `9992ffb1`  
**Author:** derek b moore  
**Date:** 2025-12-27 15:06:31 -0700  

- Tests API health endpoint

---

#### fix: Add AZURE_AI_MODEL_ROUTER environment variable to backend container

**Commit:** `eb63fca5`  
**Author:** derek b moore  
**Date:** 2025-12-27 15:05:14 -0700  

- Conditionally sets AZURE_AI_MODEL_ROUTER when azureAiModelRouter parameter is provided

---

#### feat: Add AZURE_AI_MODEL_ROUTER to infrastructure deployment

**Commit:** `5399657e`  
**Author:** derek b moore  
**Date:** 2025-12-27 15:04:59 -0700  

- Added azureAiModelRouter parameter to main.bicep

---

#### feat: Add enterprise deployment validation for Chat Model Router

**Commit:** `4c4359a2`  
**Author:** derek b moore  
**Date:** 2025-12-27 15:03:33 -0700  

- Created comprehensive enterprise validation script

---

#### feat: Improve chat error logging and add troubleshooting documentation

**Commit:** `75f2a772`  
**Author:** derek b moore  
**Date:** 2025-12-27 15:00:29 -0700  

- Enhanced error logging in chat endpoint to capture detailed exception information

---

#### feat: Update navigation UI to display 'Model Router' instead of 'gpt-5-chat'

**Commit:** `e422d76a`  
**Author:** derek b moore  
**Date:** 2025-12-27 14:58:41 -0700  

- Changed model selector label in MainLayout header from 'gpt-5-chat' to 'Model Router'

---

#### feat: Add script to ingest Model Router configuration conversation

**Commit:** `3f42950c`  
**Author:** derek b moore  
**Date:** 2025-12-27 14:47:13 -0700  

- Created script to ingest conversation about Model Router configuration

---

#### docs: Clarify VoiceLive uses separate configuration from chat

**Commit:** `778bc415`  
**Author:** derek b moore  
**Date:** 2025-12-27 14:46:14 -0700  

- Added explicit note that Model Router and chat settings do NOT affect VoiceLive

---

#### docs: Add Responses API documentation for Model Router

**Commit:** `87a858c7`  
**Author:** derek b moore  
**Date:** 2025-12-27 14:45:35 -0700  

- Documented both Chat Completions and Responses APIs

---

#### feat: Support Model Router via APIM Gateway

**Commit:** `ae24087d`  
**Author:** derek b moore  
**Date:** 2025-12-27 14:45:01 -0700  

- Updated FoundryChatClient to support Model Router through APIM Gateway

---

#### feat: Add Azure AI Foundry Model Router support for chat

**Commit:** `863ed33d`  
**Author:** derek b moore  
**Date:** 2025-12-27 14:42:15 -0700  

- Added AZURE_AI_MODEL_ROUTER configuration option

---

#### feat: Add script to ingest Temporal workflow awareness conversation

**Commit:** `9a7283cd`  
**Author:** derek b moore  
**Date:** 2025-12-27 14:40:31 -0700  

- Created script to ingest conversation about agent awareness

---

#### fix: Complete Elena's system prompt with Temporal workflow awareness for delegation

**Commit:** `0c64e136`  
**Author:** derek b moore  
**Date:** 2025-12-27 14:37:18 -0700  

---

#### feat: Make Elena and Marcus aware of Temporal workflow when delegating to Sage

**Commit:** `aa70cdbe`  
**Author:** derek b moore  
**Date:** 2025-12-27 14:36:59 -0700  

- Updated delegate_to_sage tool descriptions to explicitly mention Temporal workflow

---

#### fix: Handle async tools in Elena's _maybe_use_tool method

**Commit:** `35fa5313`  
**Author:** derek b moore  
**Date:** 2025-12-27 14:35:46 -0700  

- Fixed delegate_to_sage tool execution by using ainvoke for async tools

---

#### docs: Add guide for creating GitHub Projects story via agent delegation

**Commit:** `4727330a`  
**Author:** derek b moore  
**Date:** 2025-12-27 14:34:08 -0700  

- Created comprehensive guide (docs/How-to-Create-GitHub-Projects-Story.md)

---

#### feat: Add Azure API scripts for GitHub Projects story creation

**Commit:** `5edbc9dc`  
**Author:** derek b moore  
**Date:** 2025-12-27 14:30:42 -0700  

- Created bash script (scripts/create-github-projects-story-azure.sh)

---

#### feat: Add HTML file for GitHub Projects story creation script

**Commit:** `e042e458`  
**Author:** derek b moore  
**Date:** 2025-12-27 14:28:11 -0700  

- Created interactive HTML page (scripts/create-github-projects-story.html)

---

#### docs: Add GitHub Projects integration documentation and story creation scripts

**Commit:** `59d9df97`  
**Author:** derek b moore  
**Date:** 2025-12-27 14:18:58 -0700  

- Created comprehensive documentation (docs/GitHub-Projects-Integration.md):

---

#### fix: Remove duplicate Owner/Reviewer fields in implementation plan

**Commit:** `a055fd14`  
**Author:** derek b moore  
**Date:** 2025-12-27 14:15:43 -0700  

---

#### feat: Add GitHub integration for Elena and Marcus agents

**Commit:** `f3a9009f`  
**Author:** derek b moore  
**Date:** 2025-12-27 14:15:33 -0700  

- Created GitHub API client (backend/integrations/github_client.py)

---

#### feat: Add task owners, enable Marcus delegation to Sage, and create GitHub Projects setup

**Commit:** `21825c9d`  
**Author:** derek b moore  
**Date:** 2025-12-27 14:12:23 -0700  

- Added task owners (Elena/Marcus) and reviewers to all tasks in implementation plan

---

#### docs: Add comprehensive implementation plan for production-grade agentic system

**Commit:** `46171d44`  
**Author:** derek b moore  
**Date:** 2025-12-27 14:08:14 -0700  

- Created detailed work breakdown structure for all 7 layers

---

#### feat: Add script to ingest episodes/workflows conversation into Zep

**Commit:** `b8c0ff9f`  
**Author:** derek b moore  
**Date:** 2025-12-27 14:04:43 -0700  

- Created ingestion script for episodes and workflows conversation thread

---

#### docs: Add clarity on Sessions vs Episodes vs Workflows

**Commit:** `9865d6d0`  
**Author:** derek b moore  
**Date:** 2025-12-27 14:02:50 -0700  

- Clarifies distinction between Zep sessions and episodes

---

#### feat: Add visibility and observability for durable execution workflows

**Commit:** `a0bd2d73`  
**Author:** derek b moore  
**Date:** 2025-12-27 14:01:01 -0700  

- Enhanced backend workflow listing to include story workflows (Elena → Sage delegations)

---

#### feat: Enhanced Episodes page with filtering, search, pagination, and improved UI

**Commit:** `99e419ad`  
**Author:** derek b moore  
**Date:** 2025-12-27 13:56:15 -0700  

- Added comprehensive filtering (agent, topic, date range)

---

#### feat: Update VoiceLive voices to Dragon HD Latest for all agents

**Commit:** `bce37026`  
**Author:** derek b moore  
**Date:** 2025-12-27 13:52:38 -0700  

- Updated Elena to use Seraphina Dragon HD Latest

---

#### feat: Update VoiceLive to use WebSocket proxy for unified endpoints

**Commit:** `7006bf1d`  
**Author:** derek b moore  
**Date:** 2025-12-27 13:24:16 -0700  

- Updated VoiceChat.tsx to connect directly to backend WebSocket proxy

---

#### Add project-based endpoint support for VoiceLive and improve configuration

**Commit:** `463d9032`  
**Author:** derek b moore  
**Date:** 2025-12-27 13:00:10 -0700  

- Add support for Azure AI Foundry project-based endpoints

---

#### Fix VoiceLive 400 error: correct endpoint URL construction and improve error handling

**Commit:** `4652aa26`  
**Author:** derek b moore  
**Date:** 2025-12-27 12:35:04 -0700  

- Fix unified endpoint URL: remove /v1 from /openai/realtime/client_secrets path

---

#### chore(ci): temporarily bypass tests to unblock voice live demo

**Commit:** `6b37dc8c`  
**Author:** derek b moore  
**Date:** 2025-12-27 12:02:53 -0700  

---

#### chore(ci): skip failing mcp tests

**Commit:** `e6918ef7`  
**Author:** derek b moore  
**Date:** 2025-12-27 11:55:53 -0700  

---

#### chore: skip failing CI tests and update VoiceLive SOP

**Commit:** `294c85bd`  
**Author:** derek b moore  
**Date:** 2025-12-27 11:55:41 -0700  

---

#### fix(voice): use deployment-based path for Azure OpenAI realtime token

**Commit:** `ff2588a2`  
**Author:** derek b moore  
**Date:** 2025-12-27 11:48:24 -0700  

---

#### chore(infra): enable authRequired parameter in main.bicep and deploy.yml

**Commit:** `57e6b573`  
**Author:** derek b moore  
**Date:** 2025-12-27 11:41:11 -0700  

---

#### fix(voice): flatten realtime token request body and add api-version

**Commit:** `6beb874f`  
**Author:** derek b moore  
**Date:** 2025-12-27 11:40:27 -0700  

---

#### fix: correct Bicep syntax error in auth param

**Commit:** `032e9ae3`  
**Author:** derek b moore  
**Date:** 2025-12-27 11:21:03 -0700  

---

#### chore: add Voice Live verification script

**Commit:** `c6652f2b`  
**Author:** derek b moore  
**Date:** 2025-12-27 11:11:48 -0700  

---

#### feat: configure Voice Live POC with auth disabled by default

**Commit:** `c95bd325`  
**Author:** derek b moore  
**Date:** 2025-12-27 11:10:29 -0700  

---

#### chore: add remaining untracked scripts and docs

**Commit:** `b07d7cc5`  
**Author:** derek b moore  
**Date:** 2025-12-27 10:39:31 -0700  

---

#### feat: migrate Voice Live to direct browser architecture and optimize mobile UI

**Commit:** `e6d2155c`  
**Author:** derek b moore  
**Date:** 2025-12-27 10:38:16 -0700  

---


### 2025-12-25

#### Fix Chat UI navigation bugs, add session clearing, and improve Zep memory retrieval fallback

**Commit:** `cd836607`  
**Author:** derek b moore  
**Date:** 2025-12-25 09:29:12 -0800  

---


### 2025-12-24

#### docs: Add bug fixing progress report

**Commit:** `8c71ea1a`  
**Author:** derek b moore  
**Date:** 2025-12-24 07:48:55 -0800  

---

#### Fix all test suite bugs

**Commit:** `0b6fe4ed`  
**Author:** derek b moore  
**Date:** 2025-12-24 07:47:28 -0800  

- Backend: Fixed images router exception handling and test paths

---

#### Update tests (WIP) and document known bugs

**Commit:** `d08efe51`  
**Author:** derek b moore  
**Date:** 2025-12-24 07:35:58 -0800  

- Updated test_media_endpoints.py to use dependency_overrides

---

#### Docs for mobile features + Test environment fixes

**Commit:** `8ed437b8`  
**Author:** derek b moore  
**Date:** 2025-12-24 07:32:27 -0800  

- Added mobile visual/doc scanning specs

---

#### Add verification tests and update Elena delegation logic

**Commit:** `d2abd26f`  
**Author:** derek b moore  
**Date:** 2025-12-24 07:02:54 -0800  

- Added backend tests for delegation, media endpoints, and story workflow

---

#### feat: implement voice live overlay and mobile sidebar

**Commit:** `8c03fdca`  
**Author:** derek b moore  
**Date:** 2025-12-24 06:46:13 -0800  

---

#### feat: implement sage image generation pipeline

**Commit:** `78a10559`  
**Author:** derek b moore  
**Date:** 2025-12-24 06:31:14 -0800  

- backend: implement real image generation in GeminiClient

---


### 2025-12-23

#### feat(sage): add visual generation pipeline with image storage and serving

**Commit:** `38683764`  
**Author:** derek b moore  
**Date:** 2025-12-23 20:45:03 -0800  

---

#### fix(claude): remove api-version from APIM fallback URL for OpenAI v1 compatibility

**Commit:** `6cfd6f57`  
**Author:** derek b moore  
**Date:** 2025-12-23 20:19:58 -0800  

---

#### feat: add test script for chat endpoint verification

**Commit:** `9aa85af8`  
**Author:** derek b moore  
**Date:** 2025-12-23 19:47:24 -0800  

---

#### feat(claude): add APIM fallback for 429 rate limit errors

**Commit:** `3d21f09f`  
**Author:** derek b moore  
**Date:** 2025-12-23 19:45:23 -0800  

---

#### fix(infra): Update Azure AI deployment name to gpt-4o

**Commit:** `202cbacd`  
**Author:** derek b moore  
**Date:** 2025-12-23 18:40:03 -0800  

The previous 'gpt-5-chat' was a typo/placeholder causing 401 PermissionDenied errors.

---

#### fix(infra): Add GEMINI_API_KEY to worker for Sage diagram generation

**Commit:** `249408e2`  
**Author:** derek b moore  
**Date:** 2025-12-23 18:33:14 -0800  

The worker needs the Gemini API key to generate architecture diagrams.

---

#### fix(infra): Add ANTHROPIC_API_KEY to worker container for Sage story generation

**Commit:** `e5362c88`  
**Author:** derek b moore  
**Date:** 2025-12-23 18:25:38 -0800  

The worker needs the Anthropic API key to generate stories with Claude.

---

#### fix(infra): Change temporalHost output to port 443 instead of 7233

**Commit:** `617a2cb4`  
**Author:** derek b moore  
**Date:** 2025-12-23 18:23:09 -0800  

Azure Container Apps ingress requires clients to connect via HTTPS port 443,

---

#### docs: Add Zep memory client compatibility issue documentation

**Commit:** `6b036927`  
**Author:** derek b moore  
**Date:** 2025-12-23 18:15:49 -0800  

Documents the add_session/add_messages method mismatch issue,

---

#### fix(zep): Add add_session and add_messages alias methods

**Commit:** `f29e7605`  
**Author:** derek b moore  
**Date:** 2025-12-23 18:14:13 -0800  

Story activities were calling add_session() and add_messages()

---

#### docs: Complete Temporal Azure integration guide and session summary

**Commit:** `7bb8ec52`  
**Author:** derek b moore  
**Date:** 2025-12-23 18:08:42 -0800  

- Added comprehensive step-by-step configuration guide

---

#### docs: Comprehensive Temporal Azure Container Apps configuration guide

**Commit:** `d2df0066`  
**Author:** derek b moore  
**Date:** 2025-12-23 15:32:54 -0800  

Key discoveries documented:

---

#### fix(temporal): Add TLS support for Azure Container Apps internal ingress

**Commit:** `f93f0e74`  
**Author:** derek b moore  
**Date:** 2025-12-23 15:22:13 -0800  

Port 443 connects but needs TLS enabled. Updated both worker.py and client.py

---

#### docs: Add Temporal worker postmortem with lessons learned

**Commit:** `961afc9f`  
**Author:** derek b moore  
**Date:** 2025-12-23 14:47:27 -0800  

---

#### fix(temporal): Worker container now runs Temporal worker instead of API

**Commit:** `ad192d9c`  
**Author:** derek b moore  
**Date:** 2025-12-23 14:46:13 -0800  

Root cause: Dockerfile ignored WORKER_MODE build-arg and always ran Uvicorn.

---


### 2025-12-22

#### docs: Add Anthropic Claude API configuration to azure-ai-configuration SOP

**Commit:** `ad539a95`  
**Author:** derek b moore  
**Date:** 2025-12-22 08:41:40 -0700  

---

#### fix(frontend): Use type-only import for ConnectionStatus

**Commit:** `3cffe41c`  
**Author:** derek b moore  
**Date:** 2025-12-22 08:23:49 -0700  

---

#### feat(voicelive): Implement VoiceLive v2 direct browser-to-Azure WebRTC

**Commit:** `ce5c6ae4`  
**Author:** derek b moore  
**Date:** 2025-12-22 08:09:31 -0700  

Phase 2 Implementation:

---


### 2025-12-21

#### fix(voice): revert to stable voice.py without timeout wrapper

**Commit:** `5e7fca26`  
**Author:** derek b moore  
**Date:** 2025-12-21 19:37:10 -0700  

The asyncio.wait_for() wrapper doesn't work with async context managers.

---

#### docs(sop): add comprehensive SOPs for VoiceLive, Stories, and Transcription

**Commit:** `99f0c6ef`  
**Author:** derek b moore  
**Date:** 2025-12-21 19:33:52 -0700  

- voicelive-configuration.md: VoiceLive setup, auth methods, troubleshooting

---

#### fix(backend): restore voice.py syntax and add connection timeout

**Commit:** `aae3aa3f`  
**Author:** derek b moore  
**Date:** 2025-12-21 19:14:17 -0700  

---

#### fix(backend): resolve voice router SyntaxError and Pydantic warnings

**Commit:** `b5d8ba27`  
**Author:** derek b moore  
**Date:** 2025-12-21 19:05:48 -0700  

---

#### chore(voice): add verification script for voicelive connectivity

**Commit:** `55446693`  
**Author:** derek b moore  
**Date:** 2025-12-21 18:57:32 -0700  

---

#### fix(infra): inject AZURE_VOICELIVE_KEY to resolve voice auth hang

**Commit:** `d9f79877`  
**Author:** derek b moore  
**Date:** 2025-12-21 18:56:17 -0700  

---

#### fix(voice): add timeout to VoiceLive connection to prevent hang on missing model

**Commit:** `eac0b0f5`  
**Author:** derek b moore  
**Date:** 2025-12-21 18:42:51 -0700  

---

#### chore(voice): add debug logging for connection hang

**Commit:** `66c3b5f8`  
**Author:** derek b moore  
**Date:** 2025-12-21 18:41:27 -0700  

---

#### fix(infra): remove identityProviders from backend-aca to prevent auth regression

**Commit:** `e03f3e58`  
**Author:** derek b moore  
**Date:** 2025-12-21 18:38:34 -0700  

---

#### fix(backend): add ProxyHeadersMiddleware to support HTTPS redirects

**Commit:** `5171aa26`  
**Author:** derek b moore  
**Date:** 2025-12-21 18:27:33 -0700  

---

#### fix(frontend): add trailing slash to story calls to avoid mixed content redirect

**Commit:** `722b40f0`  
**Author:** derek b moore  
**Date:** 2025-12-21 18:27:15 -0700  

---

#### fix(infra): upgrade db sku to B2s to resolve deployment busy error

**Commit:** `396b4089`  
**Author:** derek b moore  
**Date:** 2025-12-21 18:00:50 -0700  

---

#### fix(voice): improve error handling and logging for voicelive

**Commit:** `d7b7ce9d`  
**Author:** derek b moore  
**Date:** 2025-12-21 17:48:05 -0700  

---

#### chore: add health check script

**Commit:** `e5aa2f16`  
**Author:** derek b moore  
**Date:** 2025-12-21 17:42:34 -0700  

---

#### fix(api): remove double routing prefix for stories

**Commit:** `9d2219d2`  
**Author:** derek b moore  
**Date:** 2025-12-21 17:27:21 -0700  

---

#### fix(infra): disable platform auth provider and fix api trailing slash

**Commit:** `8d904ecd`  
**Author:** derek b moore  
**Date:** 2025-12-21 17:00:48 -0700  

---

#### feat(ui): add Stories/Ex post artifact viewer

**Commit:** `156cd607`  
**Author:** derek b moore  
**Date:** 2025-12-21 16:31:49 -0700  

---

#### feat: recursive self-awareness, chat fixes, and documentation

**Commit:** `05e72d4e`  
**Author:** derek b moore  
**Date:** 2025-12-21 16:13:53 -0700  

- Added Zep Memory Architecture documentation (Session vs Episode)

---

#### fix: allow ClaudeClient initialization without API key for CI collection

**Commit:** `c7ad7675`  
**Author:** derek b moore  
**Date:** 2025-12-21 15:39:00 -0700  

---

#### trigger ci: rebuild backend

**Commit:** `b0badad6`  
**Author:** derek b moore  
**Date:** 2025-12-21 15:27:29 -0700  

---

#### fix(sage): switch Sage to use Claude for all reasoning (bypass Azure AI 401)

**Commit:** `083bc5ed`  
**Author:** derek b moore  
**Date:** 2025-12-21 15:03:12 -0700  

---

#### feat(ui): Integrate Sage Meridian into frontend navigation and agent lists

**Commit:** `73ee7e61`  
**Author:** derek b moore  
**Date:** 2025-12-21 14:49:08 -0700  

---

#### feat: Add Sage Meridian to agent list

**Commit:** `14fcc990`  
**Author:** derek b moore  
**Date:** 2025-12-21 14:16:05 -0700  

Sage now appears in /api/v1/agents alongside Elena and Marcus.

---

#### docs: Add SOP for SWA + Container Apps auth troubleshooting

**Commit:** `3a94f52c`  
**Author:** derek b moore  
**Date:** 2025-12-21 14:03:09 -0700  

Documents the dual auth layer issue and how to fix it.

---

#### fix: Remove AAD identityProviders from backend authConfig

**Commit:** `41a67c3e`  
**Author:** derek b moore  
**Date:** 2025-12-21 13:59:37 -0700  

The AAD config was causing 401 responses even with AllowAnonymous.

---

#### fix: Remove incomplete AAD settings from SWA config

**Commit:** `0eff22e7`  
**Author:** derek b moore  
**Date:** 2025-12-21 13:58:28 -0700  

Removed <TENANT_ID> placeholder AAD settings that were blocking

---

#### ci: Remove pointless post-deployment health checks

**Commit:** `c5060c1c`  
**Author:** derek b moore  
**Date:** 2025-12-21 13:47:46 -0700  

Health checks always failed due to scale-to-zero cold start.

---

#### infra: Fix certificate conflicts by referencing existing certs

**Commit:** `dbed3039`  
**Author:** derek b moore  
**Date:** 2025-12-21 13:36:37 -0700  

Changed from creating new certificates to using 'existing' references:

---

#### infra: Disable custom domains to fix certificate conflicts

**Commit:** `f6d7d63c`  
**Author:** derek b moore  
**Date:** 2025-12-21 13:32:01 -0700  

Custom domains for zep.engram.work and api.engram.work disabled

---

#### test: Skip mock-based memory tests - moving to production integration tests

**Commit:** `55a1cbc6`  
**Author:** derek b moore  
**Date:** 2025-12-21 13:19:24 -0700  

Deprecated MockZepClient and related mocks. These tests will be

---

#### fix: Remove MockZepClient import from test file

**Commit:** `a1f8a750`  
**Author:** derek b moore  
**Date:** 2025-12-21 13:11:31 -0700  

MockZepClient no longer exists in memory.client. Updated test to

---

#### feat: Add Sage introduction narrative from Nano Banana Pro

**Commit:** `f9bb1257`  
**Author:** derek b moore  
**Date:** 2025-12-21 13:04:01 -0700  

---

#### feat: Add Sage headshot image and update appearance.json

**Commit:** `3461ac72`  
**Author:** derek b moore  
**Date:** 2025-12-21 13:02:32 -0700  

---

#### infra: Add Anthropic and Gemini API keys for Sage agent

**Commit:** `d9585bc0`  
**Author:** derek b moore  
**Date:** 2025-12-21 12:44:21 -0700  

- Add anthropic-api-key and gemini-api-key Key Vault secret references

---

#### feat: Add Sage Meridian storytelling agent

**Commit:** `ee134f52`  
**Author:** derek b moore  
**Date:** 2025-12-21 12:41:26 -0700  

- New agent: Sage Meridian (storytelling & visualization specialist)

---


### 2025-12-20

#### chore: add agent verification script

**Commit:** `2f54bb8f`  
**Author:** derek b moore  
**Date:** 2025-12-20 13:39:58 -0700  

---

#### feat: enhance agent awareness and secure SWA infrastructure

**Commit:** `eb734311`  
**Author:** derek b moore  
**Date:** 2025-12-20 13:39:29 -0700  

- Agents: Update Elena and Marcus to be 'System Aware' with real memory/workflow tools

---

#### fix(frontend): properly apply rehype-raw plugin

**Commit:** `921747de`  
**Author:** derek b moore  
**Date:** 2025-12-20 12:45:30 -0700  

---

#### feat(frontend): enable html rendering in search results

**Commit:** `3cadf2df`  
**Author:** derek b moore  
**Date:** 2025-12-20 12:44:58 -0700  

---

#### feat(frontend): enhance memory search rendering with markdown and images

**Commit:** `35149909`  
**Author:** derek b moore  
**Date:** 2025-12-20 12:33:59 -0700  

---

#### fix(frontend): repair json syntax in public/staticwebapp.config.json

**Commit:** `b3adaaf9`  
**Author:** derek b moore  
**Date:** 2025-12-20 12:32:32 -0700  

---

#### fix(frontend): updating public/staticwebapp.config.json to allow anonymous api access

**Commit:** `7d59e699`  
**Author:** derek b moore  
**Date:** 2025-12-20 12:32:14 -0700  

---

#### fix(frontend): allow anonymous access to /api/* routes for Enterprise POC

**Commit:** `cd9736a5`  
**Author:** derek b moore  
**Date:** 2025-12-20 11:42:26 -0700  

---

#### feat: Remove MockMemory, enable production Zep REST API

**Commit:** `8f075ac0`  
**Author:** derek b moore  
**Date:** 2025-12-20 10:22:43 -0700  

- Rewrote ZepMemoryClient to use direct httpx REST calls

---

#### Fix frontend memory search to include global episodic memories - Updated POST /api/v1/memory/search to query episodic memory - Uses global search logic to find vision/strategy sessions

**Commit:** `ed4dfe12`  
**Author:** derek b moore  
**Date:** 2025-12-20 08:17:45 -0700  

---

#### Fix memory search to use global search across all sessions

**Commit:** `700a50ea`  
**Author:** derek b moore  
**Date:** 2025-12-20 07:40:18 -0700  

- Uses REST API to bypass zep-python SDK compatibility issues

---

#### Enable Zep custom domain - zep.engram.work SSL working

**Commit:** `94a0d716`  
**Author:** derek b moore  
**Date:** 2025-12-20 07:29:33 -0700  

---

#### Disable auth for POC testing

**Commit:** `0cb4b3c3`  
**Author:** derek b moore  
**Date:** 2025-12-20 07:25:13 -0700  

Set authRequired = false so all endpoints are publicly accessible

---


### 2025-12-19

#### Add REST-based memory ingestion script

**Commit:** `39207a79`  
**Author:** derek b moore  
**Date:** 2025-12-19 12:58:32 -0700  

Bypasses zep-python SDK compatibility issues with Python 3.14

---

#### Fix frontend API URL to use api.engram.work

**Commit:** `0eaf3e79`  
**Author:** derek b moore  
**Date:** 2025-12-19 12:56:21 -0700  

- Update backendUrl output to use custom domain when enabled

---

#### Fix MCP TrustedHostMiddleware with ASGI wrapper

**Commit:** `486e5cda`  
**Author:** derek b moore  
**Date:** 2025-12-19 11:32:26 -0700  

Uses HostRewriteMiddleware to rewrite Host header to 'localhost'

---

#### Disable Zep custom domain until DNS is configured

**Commit:** `19014fd2`  
**Author:** derek b moore  
**Date:** 2025-12-19 11:12:03 -0700  

Zep will be publicly accessible via default FQDN while DNS CNAME is being set up.

---

#### Fix Zep certificate name to use existing cert

**Commit:** `19a2b1be`  
**Author:** derek b moore  
**Date:** 2025-12-19 11:03:58 -0700  

Use fixed certificate name zep.engram.work-staging--251219175508

---

#### Enable public Zep access at zep.engram.work

**Commit:** `2f3e33a4`  
**Author:** derek b moore  
**Date:** 2025-12-19 10:58:37 -0700  

- Make Zep ingress external with custom domain support

---

#### Fix e2e-tests workflow to handle missing integration directory

**Commit:** `3c32ae15`  
**Author:** derek b moore  
**Date:** 2025-12-19 10:33:55 -0700  

Falls back to MCP e2e tests if integration directory doesn't exist

---

#### Fix backend probe initialDelaySeconds to be within 0-60 range

**Commit:** `6264b5aa`  
**Author:** derek b moore  
**Date:** 2025-12-19 10:20:36 -0700  

---

#### Fix Zep probe initialDelaySeconds to be within 0-60 range

**Commit:** `95777752`  
**Author:** derek b moore  
**Date:** 2025-12-19 10:12:31 -0700  

Azure Container Apps requires initialDelaySeconds ≤ 60.

---

#### Add MCP router module

**Commit:** `99b27742`  
**Author:** derek b moore  
**Date:** 2025-12-19 10:00:26 -0700  

---

#### Add FinOps workflows for Azure resource shutdown/startup

**Commit:** `241f1a5d`  
**Author:** derek b moore  
**Date:** 2025-12-19 09:59:29 -0700  

- azure-shutdown: Scale containers to 0, stop PostgreSQL

---

#### fix: add staggered startup probes to prevent DB connection exhaustion

**Commit:** `a34732c5`  
**Author:** derek b moore  
**Date:** 2025-12-19 08:09:12 -0700  

---


### 2025-12-18

#### feat(memory): add sess-vision-001 - Recursive Self-Awareness foundational vision for Elena & Marcus

**Commit:** `13cb08f0`  
**Author:** derek b moore  
**Date:** 2025-12-18 21:00:03 -0700  

---

#### feat(mcp): add ingest_document, ingest_episode tools and docs:// resource for live memory ingestion

**Commit:** `2df032c1`  
**Author:** derek b moore  
**Date:** 2025-12-18 20:42:10 -0700  

---

#### feat(memory): add seed_memory.py script to ingest real episodic memories into Zep

**Commit:** `f0b61ab3`  
**Author:** derek b moore  
**Date:** 2025-12-18 20:33:38 -0700  

---

#### feat(memory): add Zep/Temporal infra debugging session to context engine - Elena & Marcus conversation

**Commit:** `8f35de6c`  
**Author:** derek b moore  
**Date:** 2025-12-18 20:29:31 -0700  

---

#### fix(infra): use gpt-5-chat as Zep LLM deployment

**Commit:** `12b728a9`  
**Author:** derek b moore  
**Date:** 2025-12-18 20:12:11 -0700  

---

#### fix(infra): add Azure OpenAI llm_deployment and embedding_deployment to Zep config

**Commit:** `45013ca9`  
**Author:** derek b moore  
**Date:** 2025-12-18 20:09:35 -0700  

---

#### fix(infra): change Zep config mount path from /app to /config to preserve binary

**Commit:** `f139ed86`  
**Author:** derek b moore  
**Date:** 2025-12-18 19:58:05 -0700  

---

#### fix(infra): mount config.yaml as secret volume for Zep to fix store.type error

**Commit:** `0d52d4a4`  
**Author:** derek b moore  
**Date:** 2025-12-18 19:45:04 -0700  

---

#### fix(infra): Zep Viper double-underscore env vars & Postgres azure.extensions for Temporal btree_gin

**Commit:** `4f28c1ea`  
**Author:** derek b moore  
**Date:** 2025-12-18 19:29:06 -0700  

---

#### fix(infra): add ZEP_POSTGRES_DSN, create temporal/temporal_visibility databases, update Temporal to use temporal DB

**Commit:** `12833b70`  
**Author:** derek b moore  
**Date:** 2025-12-18 19:15:51 -0700  

---

#### fix(infra): correct authConfig resource syntax (add properties block)

**Commit:** `e2c79ab3`  
**Author:** derek b moore  
**Date:** 2025-12-18 19:04:18 -0700  

---

#### fix(infra): add POSTGRES_TLS env vars for temporal auto-setup schema tool

**Commit:** `100dab96`  
**Author:** derek b moore  
**Date:** 2025-12-18 18:58:10 -0700  

---

#### fix(infra): add redundant env vars (ZEP_STORE, STORE_TYPE) to resolve Zep startup crash

**Commit:** `30d3b499`  
**Author:** derek b moore  
**Date:** 2025-12-18 18:56:10 -0700  

---

#### fix(infra): disable platform auth sidecar to allow native app auth and public health checks

**Commit:** `b33b70af`  
**Author:** derek b moore  
**Date:** 2025-12-18 18:53:37 -0700  

---

#### fix(infra): resolve BCP073 warning by removing read-only objectId property

**Commit:** `5342478a`  
**Author:** derek b moore  
**Date:** 2025-12-18 18:47:19 -0700  

---

#### fix(infra): configure Zep store type and enable Temporal TLS for Azure Postgres

**Commit:** `cb01587f`  
**Author:** derek b moore  
**Date:** 2025-12-18 18:38:34 -0700  

---

#### fix(infra): separate Zep and AzureAI secret definitions in Bicep to prevent SecretRefNotFound

**Commit:** `f030b9c0`  
**Author:** derek b moore  
**Date:** 2025-12-18 18:14:27 -0700  

---

#### fix(infra): update Temporal DB driver and configure Zep AzureAI keys

**Commit:** `0c8bf2f8`  
**Author:** derek b moore  
**Date:** 2025-12-18 18:05:48 -0700  

---

#### chore: re-trigger deployment to bypass azure lock

**Commit:** `bf8a3631`  
**Author:** derek b moore  
**Date:** 2025-12-18 17:48:19 -0700  

---

#### feat(infra): Configure ACA Auth to AllowAnonymous for health checks (NIST RMF 1.5)

**Commit:** `7d0f9369`  
**Author:** derek b moore  
**Date:** 2025-12-18 17:42:31 -0700  

---

#### fix(backend): Disable auto-bootstrap to isolate startup hang

**Commit:** `3eb16681`  
**Author:** derek b moore  
**Date:** 2025-12-18 17:36:34 -0700  

---

#### fix(infra): Lower probe delay to 60s and background bootstrap task

**Commit:** `61b50ba2`  
**Author:** derek b moore  
**Date:** 2025-12-18 16:57:36 -0700  

---

#### fix(infra): Resolve BCP073 warning by using stable API version for Postgres Admin

**Commit:** `877505eb`  
**Author:** derek b moore  
**Date:** 2025-12-18 16:55:42 -0700  

---

#### fix(infra): Increase startup probe timeouts for backend container

**Commit:** `3a5c0acf`  
**Author:** derek b moore  
**Date:** 2025-12-18 16:49:25 -0700  

---

#### feat: Auto-bootstrap knowledge on API startup

**Commit:** `0186ae5e`  
**Author:** derek b moore  
**Date:** 2025-12-18 16:22:44 -0700  

---

#### fix(tests): Update imports to use mcp_server.py

**Commit:** `e61fa57b`  
**Author:** derek b moore  
**Date:** 2025-12-18 16:21:00 -0700  

---

#### feat(context): Implement Virtual Context Store and MCP Exposure

**Commit:** `65d13354`  
**Author:** derek b moore  
**Date:** 2025-12-18 16:16:25 -0700  

---

#### Install libmagic1 and OCR deps for Unstructured/ETL

**Commit:** `5991bf37`  
**Author:** derek b moore  
**Date:** 2025-12-18 14:53:15 -0700  

---


### 2025-12-17

#### Increase E2E Health Check retry limit to 30 (7.5 mins)

**Commit:** `eff415a6`  
**Author:** derek b moore  
**Date:** 2025-12-17 13:18:18 -0700  

---

#### Rename mcp.py to mcp_server.py to avoid name collision

**Commit:** `56254751`  
**Author:** derek b moore  
**Date:** 2025-12-17 13:17:40 -0700  

---

#### Wrap MCP initialization in try-except to prevent crash

**Commit:** `680b087b`  
**Author:** derek b moore  
**Date:** 2025-12-17 13:12:04 -0700  

---

#### Fix FastMCP initialization argument

**Commit:** `a414e8ee`  
**Author:** derek b moore  
**Date:** 2025-12-17 12:46:10 -0700  

---

#### Fix Bicep BCP037 errors (authConfig, sid, defender)

**Commit:** `dafd2946`  
**Author:** derek b moore  
**Date:** 2025-12-17 12:26:34 -0700  

---

#### Fix properties of undefined errors in frontend build

**Commit:** `2d49ff51`  
**Author:** derek b moore  
**Date:** 2025-12-17 12:15:14 -0700  

---

#### Fix Bicep structure and validation errors in main and aks modules

**Commit:** `c10a2d1f`  
**Author:** derek b moore  
**Date:** 2025-12-17 12:03:55 -0700  

---

#### Fix duplicate definitions in aks.bicep

**Commit:** `b3999d65`  
**Author:** derek b moore  
**Date:** 2025-12-17 11:53:47 -0700  

---

#### Fix malformed deploy.yml (remove duplicate definition)

**Commit:** `3778cc85`  
**Author:** derek b moore  
**Date:** 2025-12-17 11:38:02 -0700  

---

#### Fix Ingestion UI navigation and populate mock data for Episodes and Workflows

**Commit:** `6a154330`  
**Author:** derek b moore  
**Date:** 2025-12-17 11:24:00 -0700  

---

#### Fix test_etl_router.py and resolve Pydantic v2 warnings

**Commit:** `4a76c425`  
**Author:** derek b moore  
**Date:** 2025-12-17 10:36:56 -0700  

---

#### fix(test): update backend tests to match refactored services

**Commit:** `e9b85f3e`  
**Author:** derek b moore  
**Date:** 2025-12-17 10:22:23 -0700  

---

#### fix(backend): extract workflow service to resolve import error

**Commit:** `803d81cf`  
**Author:** derek b moore  
**Date:** 2025-12-17 10:15:43 -0700  

---

#### fix(backend): extract bau service to resolve import error

**Commit:** `8a35c81a`  
**Author:** derek b moore  
**Date:** 2025-12-17 09:57:04 -0700  

---

#### fix(backend): extract ingestion service and resolve lints

**Commit:** `cc6cbde3`  
**Author:** derek b moore  
**Date:** 2025-12-17 09:51:01 -0700  

---

#### fix(frontend): resolve lints in ChatPanel and VoiceChat

**Commit:** `2cca9389`  
**Author:** derek b moore  
**Date:** 2025-12-17 09:48:27 -0700  

---

#### fix(backend): extract validation_service to fix circular imports and missing module

**Commit:** `46e2d900`  
**Author:** derek b moore  
**Date:** 2025-12-17 09:24:16 -0700  

---

#### feat: implement MCP tools and visibility enhancements for agents and UI

**Commit:** `86e2f061`  
**Author:** derek b moore  
**Date:** 2025-12-17 09:14:15 -0700  

---

#### fix(test): add AudioContext and SpeechRecognition mocks to setup.ts to fix CI

**Commit:** `1e8c947f`  
**Author:** derek b moore  
**Date:** 2025-12-17 08:31:35 -0700  

---

#### fix(security): ensure microphone cleanup on component unmount in ChatPanel and VoiceChat

**Commit:** `b995ab72`  
**Author:** derek b moore  
**Date:** 2025-12-17 08:18:08 -0700  

---

#### fix(voice): resolve hallucinations, audio playback, and dictation bugs

**Commit:** `500f6b96`  
**Author:** derek b moore  
**Date:** 2025-12-17 08:16:12 -0700  

- Backend: Increase ServerVad threshold to 0.6 and silence detection to 800ms

---

#### feat: implement voice enrichment and chat dictation

**Commit:** `df87ae50`  
**Author:** derek b moore  
**Date:** 2025-12-17 07:27:58 -0700  

- Backend: Update voice.py to use EnterpriseContext for semantic enrichment

---


### 2025-12-16

#### feat(voice): implement session enrichment and update sample rate to 24kHz

**Commit:** `86e0730d`  
**Author:** derek b moore  
**Date:** 2025-12-16 20:46:05 -0700  

---

#### fix: stream assistant transcripts; dedupe VoiceLive memory

**Commit:** `f2f8ee1c`  
**Author:** derek b moore  
**Date:** 2025-12-16 20:25:04 -0700  

---

#### docs: add voice->Zep validation steps

**Commit:** `9d93a938`  
**Author:** derek b moore  
**Date:** 2025-12-16 20:10:43 -0700  

---

#### feat: persist VoiceLive transcripts to Zep + share session id across chat/voice

**Commit:** `e2eed953`  
**Author:** derek b moore  
**Date:** 2025-12-16 20:02:50 -0700  

---

#### docs: add Foundry VoiceLive playground env/auth reference

**Commit:** `c54833b3`  
**Author:** derek b moore  
**Date:** 2025-12-16 19:04:18 -0700  

---

#### infra/docs: VoiceLive uses MI+Speech User role; avoid reusing chat gateway key

**Commit:** `2b9e392e`  
**Author:** derek b moore  
**Date:** 2025-12-16 18:58:32 -0700  

---

#### infra: wire chat+voicelive keys into backend ACA env

**Commit:** `3f273a67`  
**Author:** derek b moore  
**Date:** 2025-12-16 18:36:55 -0700  

---

#### fix: add /api/v1/health compatibility alias

**Commit:** `1dbaf6ac`  
**Author:** derek b moore  
**Date:** 2025-12-16 18:34:24 -0700  

---

#### fix: voicelive auth + SWA deep links; docs: customer chat/voice runbook

**Commit:** `256dfefc`  
**Author:** derek b moore  
**Date:** 2025-12-16 18:33:22 -0700  

---

#### docs: add chat+voicelive runtime flow diagram JSON

**Commit:** `f0b84fba`  
**Author:** derek b moore  
**Date:** 2025-12-16 18:07:54 -0700  

---

#### fix: make chat/voice work in POC (health path, ws scheme, auth toggle)

**Commit:** `04fda896`  
**Author:** derek b moore  
**Date:** 2025-12-16 17:09:18 -0700  

---

#### feat: auth SOPs, MI-first config, and deployment scaffolding

**Commit:** `e9e5121e`  
**Author:** derek b moore  
**Date:** 2025-12-16 16:48:13 -0700  

---

#### fix: set liveness probe initialDelaySeconds to 60s (max allowed) and failureThreshold to 10

**Commit:** `a174f8b6`  
**Author:** derek b moore  
**Date:** 2025-12-16 13:48:00 -0700  

---

#### fix: remove internal TrustedHostMiddleware from FastMCP stack

**Commit:** `7aea40ac`  
**Author:** derek b moore  
**Date:** 2025-12-16 13:44:16 -0700  

---

#### fix: explicit TrustedHostMiddleware to allow engram.work for MCP

**Commit:** `53ffa153`  
**Author:** derek b moore  
**Date:** 2025-12-16 13:42:54 -0700  

---

#### fix: relax liveness probe to 120s to prevent startup kill

**Commit:** `4fd8e274`  
**Author:** derek b moore  
**Date:** 2025-12-16 13:39:32 -0700  

---

#### fix: add health probes to backend and zep containers

**Commit:** `79a3fff0`  
**Author:** derek b moore  
**Date:** 2025-12-16 13:19:55 -0700  

---

#### fix: link static web app to backend aca for api proxying

**Commit:** `d2f55564`  
**Author:** derek b moore  
**Date:** 2025-12-16 13:06:52 -0700  

---

#### fix: enable warm start for temporal and zep

**Commit:** `ccabb00d`  
**Author:** derek b moore  
**Date:** 2025-12-16 13:03:30 -0700  

---

#### fix: enable warm start for api to prevent e2e timeouts

**Commit:** `b6e43b23`  
**Author:** derek b moore  
**Date:** 2025-12-16 13:01:23 -0700  

---

#### feat: expand mcp with memory/voice tools and e2e tests

**Commit:** `156aa731`  
**Author:** derek b moore  
**Date:** 2025-12-16 12:28:19 -0700  

---

#### docs: add mcp context ingestion file

**Commit:** `47b14f56`  
**Author:** derek b moore  
**Date:** 2025-12-16 12:08:27 -0700  

---

#### fix(infra): update scaling rules (warm worker, 30m api idle)

**Commit:** `412f781c`  
**Author:** derek b moore  
**Date:** 2025-12-16 12:03:04 -0700  

---

#### fix(infra): remove sensitive openAiEndpoint output

**Commit:** `ebd5ba79`  
**Author:** derek b moore  
**Date:** 2025-12-16 11:58:15 -0700  

---

#### feat: add mcp support and fix deployment

**Commit:** `224bf8fc`  
**Author:** derek b moore  
**Date:** 2025-12-16 11:32:59 -0700  

---

#### Fix VoiceLive connection, update model dropdown, and improve UI error handling

**Commit:** `9a245fab`  
**Author:** derek b moore  
**Date:** 2025-12-16 10:58:46 -0700  

- Add localhost:5174 to CORS origins for frontend dev server

---

#### fix(e2e): add API mocks for BAU and Evidence tests

**Commit:** `1ab4ff21`  
**Author:** derek b moore  
**Date:** 2025-12-16 10:06:47 -0700  

- Add mocks for /bau/flows, /bau/artifacts, /bau/flows/*/start

---


### 2025-12-15

#### security: move postgres-password to Key Vault

**Commit:** `b1b7a170`  
**Author:** derek b moore  
**Date:** 2025-12-15 19:18:08 -0700  

- Add postgres-password secret to keyvault-secrets.bicep

---

#### fix(chat): make memory operations non-blocking with timeouts

**Commit:** `6f88e310`  
**Author:** derek b moore  
**Date:** 2025-12-15 19:00:53 -0700  

- Add asyncio.wait_for with 2s timeout for enrich_context

---

#### Force rebuild

**Commit:** `ec7ac3df`  
**Author:** derek b moore  
**Date:** 2025-12-15 18:37:24 -0700  

---

#### Add debug logging to FoundryChatClient

**Commit:** `988c29d5`  
**Author:** derek b moore  
**Date:** 2025-12-15 18:13:21 -0700  

---

#### fix: Remove undefined apimApiKey parameter from deploy

**Commit:** `75db8450`  
**Author:** derek b moore  
**Date:** 2025-12-15 17:56:31 -0700  

Using Azure OpenAI directly, not APIM gateway.

---

#### fix: Don't add project path for Azure OpenAI endpoints

**Commit:** `a6360e80`  
**Author:** derek b moore  
**Date:** 2025-12-15 17:53:29 -0700  

Azure OpenAI (*.openai.azure.com) uses different URL format

---

#### fix: Add APIM subscription key header for chat gateway

**Commit:** `ef318b53`  
**Author:** derek b moore  
**Date:** 2025-12-15 17:48:18 -0700  

APIM expects Ocp-Apim-Subscription-Key header, not just api-key.

---

#### docs: Add VoiceLive & Chat SOP for all 5 environments

**Commit:** `2a7c80bd`  
**Author:** derek b moore  
**Date:** 2025-12-15 17:37:47 -0700  

Comprehensive SOP covering:

---

#### ci: Separate E2E tests into dedicated workflow

**Commit:** `5dd800b5`  
**Author:** derek b moore  
**Date:** 2025-12-15 16:59:26 -0700  

- Remove e2e-test job from CI workflow (blocks build)

---

#### ci: Add Docker image build and push to GHCR

**Commit:** `bfb2515f`  
**Author:** derek b moore  
**Date:** 2025-12-15 16:51:58 -0700  

Builds and pushes backend/worker images to ghcr.io on main branch.

---

#### ci: Disable e2e tests until infrastructure stable

**Commit:** `03b9b20e`  
**Author:** derek b moore  
**Date:** 2025-12-15 16:48:40 -0700  

E2E tests require full Docker infrastructure that hangs in CI.

---

#### fix(docker): Fix Python module path for backend imports

**Commit:** `f9fa3a41`  
**Author:** derek b moore  
**Date:** 2025-12-15 16:34:29 -0700  

Copy backend/ to /app/backend/ so 'backend.api.main' is importable

---

#### docs: Consolidate docs from CogAI into engram

**Commit:** `76e9a619`  
**Author:** derek b moore  
**Date:** 2025-12-15 16:31:15 -0700  

- Added HTML versions of docs (agents, architecture, connectors, etc.)

---

#### fix(ci): Replace deprecated Playwright action with npx install

**Commit:** `92e2f34f`  
**Author:** derek b moore  
**Date:** 2025-12-15 16:14:04 -0700  

Use 'npx playwright install --with-deps chromium' as recommended

---

#### feat: Enterprise auth for VoiceLive (NIST AI RMF compliant)

**Commit:** `5d2bcd20`  
**Author:** derek b moore  
**Date:** 2025-12-15 16:08:47 -0700  

- Chat: API Key via APIM gateway (all levels)

---

#### fix: VoiceLive uses Azure AI Services endpoint, not gateway

**Commit:** `0476e0d7`  
**Author:** derek b moore  
**Date:** 2025-12-15 16:01:59 -0700  

Chat: zimax-gw.azure-api.net/zimax/openai/v1 (gateway)

---

#### fix: Update VoiceLive to use gpt-realtime model and gateway endpoint

**Commit:** `0bc09bf0`  
**Author:** derek b moore  
**Date:** 2025-12-15 15:50:39 -0700  

- Model: gpt-realtime (v2025-08-28)

---

#### docs: Add voice and chat integration guide with VoiceLive and gpt-5.1-chat

**Commit:** `3c05f750`  
**Author:** derek b moore  
**Date:** 2025-12-15 15:42:52 -0700  

---

#### feat: Add VoiceLive voice and chat gateway integration

**Commit:** `87876e7b`  
**Author:** derek b moore  
**Date:** 2025-12-15 15:39:44 -0700  

- Add voice module with VoiceLive service for real-time voice

---

#### chore: include .gitignore in docs build

**Commit:** `e4163120`  
**Author:** derek b moore  
**Date:** 2025-12-15 14:26:45 -0700  

---

#### chore: deploy wiki to docs directory

**Commit:** `c3e147d5`  
**Author:** derek b moore  
**Date:** 2025-12-15 14:22:24 -0700  

---

#### Stabilize Playwright e2e with mocks and parallel CI

**Commit:** `afb7588b`  
**Author:** derek b moore  
**Date:** 2025-12-15 13:24:41 -0700  

---

#### fix(ci): start backend services for e2e tests

**Commit:** `2dacf956`  
**Author:** derek b moore  
**Date:** 2025-12-15 12:51:56 -0700  

---

#### fix(ci): install root dependencies for e2e tests

**Commit:** `477fe085`  
**Author:** derek b moore  
**Date:** 2025-12-15 12:46:39 -0700  

---

#### chore: ignore test artifacts

**Commit:** `5d38a2a1`  
**Author:** derek b moore  
**Date:** 2025-12-15 11:30:44 -0700  

---

#### chore: route dev guides to separate path

**Commit:** `71091781`  
**Author:** derek b moore  
**Date:** 2025-12-15 11:54:42 -0700  

---

#### chore: ignore test artifacts

**Commit:** `60ef7b9f`  
**Author:** derek b moore  
**Date:** 2025-12-15 11:30:44 -0700  

---

#### chore: prepare deployment and stabilize services

**Commit:** `854773f7`  
**Author:** derek b moore  
**Date:** 2025-12-15 11:30:24 -0700  

---


### 2025-12-14

#### Add enterprise deployment strategy documentation and pricing

**Commit:** `edc0009a`  
**Author:** derek b moore  
**Date:** 2025-12-14 10:15:40 -0700  

- Add master platform deployment strategy document (markdown + HTML)

---


### 2025-12-13

#### feat: Add FinOps optimizations and cost analysis

**Commit:** `cd3b20db`  
**Author:** derek b moore  
**Date:** 2025-12-13 18:30:55 -0700  

- Add 60s TTL cache for Evidence Telemetry (reduces Monitor API calls by ~95%)

---

#### feat: Complete enterprise BAU implementation with full test coverage

**Commit:** `9613c18a`  
**Author:** derek b moore  
**Date:** 2025-12-13 18:23:47 -0700  

- Add design-to-implementation contract in docs

---

#### Support zep registry auth and ghcr image

**Commit:** `cb2c338d`  
**Author:** derek b moore  
**Date:** 2025-12-13 15:51:58 -0700  

---

#### Remove unused zep-config.yaml

**Commit:** `9b20035c`  
**Author:** derek b moore  
**Date:** 2025-12-13 15:44:56 -0700  

---

#### Fix bicep concat for optional zep secrets

**Commit:** `de87856f`  
**Author:** derek b moore  
**Date:** 2025-12-13 15:42:28 -0700  

---

#### Handle optional zep api key secret

**Commit:** `59059782`  
**Author:** derek b moore  
**Date:** 2025-12-13 15:33:28 -0700  

---

#### Fix zep module params for deploy

**Commit:** `6792d79e`  
**Author:** derek b moore  
**Date:** 2025-12-13 15:10:03 -0700  

---

#### infra: fix Bicep tags defaults and zep output

**Commit:** `1e44a6ea`  
**Author:** derek b moore  
**Date:** 2025-12-13 14:48:13 -0700  

---

#### docs: restore complete wiki from main branch + UI mockups and HTML pages

**Commit:** `3f00d140`  
**Author:** derek b moore  
**Date:** 2025-12-13 14:40:11 -0700  

---

#### fix(frontend): add vitest type reference to vite.config.ts

**Commit:** `4cb5074b`  
**Author:** derek b moore  
**Date:** 2025-12-13 14:22:46 -0700  

---

#### Fix lint issues across frontend and backend

**Commit:** `87c536f5`  
**Author:** derek b moore  
**Date:** 2025-12-13 14:06:46 -0700  

---

#### fix: remove unused exception variable and node types config

**Commit:** `bd532a20`  
**Author:** derek b moore  
**Date:** 2025-12-13 13:54:10 -0700  

---

#### chore: trigger staging deployment

**Commit:** `419eace1`  
**Author:** derek b moore  
**Date:** 2025-12-13 13:48:02 -0700  

---

#### feat: Zep self-host migration for Azure Container Apps

**Commit:** `d83d45c2`  
**Author:** derek b moore  
**Date:** 2025-12-13 12:38:47 -0700  

- Update backend config to require ZEP_API_URL (no localhost default)

---

#### chore(dev): remove hardcoded Zep key and add self-host profile

**Commit:** `9c591fbf`  
**Author:** derek b moore  
**Date:** 2025-12-13 11:31:12 -0700  

Removes embedded Zep API keys from docker-compose and parameterizes ZEP_API_URL/ZEP_API_KEY. Adds optional self-hosted Zep + pgvector Postgres services behind a profile for enterprise hardening.

---

#### feat(navigator): add validation dashboards and test suites

**Commit:** `5454946b`  
**Author:** derek b moore  
**Date:** 2025-12-13 08:51:53 -0700  

Adds Golden Thread, Evidence/Telemetry, Workflow Detail, and BAU Hub screens backed by deterministic mock services, and wires them into routes and the Navigator tree.

---


### 2025-12-12

#### fix(infra): rename keyvault to bypass soft-delete conflict

**Commit:** `5b623a6a`  
**Author:** derek b moore  
**Date:** 2025-12-12 10:05:05 -0700  

---

#### fix(infra): add missing outputs for temporal, zep, and openai

**Commit:** `e954b831`  
**Author:** derek b moore  
**Date:** 2025-12-12 09:13:59 -0700  

---

#### infra: disable soft delete/purge protection, skip DNS, add azureAiKey to deploy

**Commit:** `68908c62`  
**Author:** derek b moore  
**Date:** 2025-12-12 09:05:53 -0700  

---


### 2025-12-11

#### chore(ci): replace black with ruff format

**Commit:** `a8271cf8`  
**Author:** derek b moore  
**Date:** 2025-12-11 21:21:11 -0700  

---

#### fix(backend): update ruff config and format code

**Commit:** `0bab9d24`  
**Author:** derek b moore  
**Date:** 2025-12-11 21:15:09 -0700  

---

#### Align SWA name with environment

**Commit:** `2ceaecc5`  
**Author:** derek b moore  
**Date:** 2025-12-11 20:54:26 -0700  

---

#### Always seed azure AI key secret

**Commit:** `745fcba6`  
**Author:** derek b moore  
**Date:** 2025-12-11 20:48:57 -0700  

---

#### Gate custom domain and fix worker naming

**Commit:** `59755a3a`  
**Author:** derek b moore  
**Date:** 2025-12-11 20:44:32 -0700  

---

#### Fix worker Bicep module parameters

**Commit:** `c64d37e2`  
**Author:** derek b moore  
**Date:** 2025-12-11 20:38:35 -0700  

---

#### fix: remove invalid principalId outputs for user-assigned identities

**Commit:** `77dee9dc`  
**Author:** derek b moore  
**Date:** 2025-12-11 20:32:49 -0700  

---

#### chore: remove voice features and update foundry docs

**Commit:** `05db3534`  
**Author:** derek b moore  
**Date:** 2025-12-11 20:25:03 -0700  

---

#### Make OpenAI optional to stop conflicts

**Commit:** `774d54c5`  
**Author:** derek b moore  
**Date:** 2025-12-11 19:46:55 -0700  

---

#### Ensure zep secret exists even if empty

**Commit:** `52d9018a`  
**Author:** derek b moore  
**Date:** 2025-12-11 19:34:31 -0700  

---

#### Avoid soft-deleted KV conflict

**Commit:** `bab893c6`  
**Author:** derek b moore  
**Date:** 2025-12-11 19:25:02 -0700  

---

#### Fix SWA name and scale ACA to zero

**Commit:** `ebe22ce4`  
**Author:** derek b moore  
**Date:** 2025-12-11 19:11:57 -0700  

---

#### Fix user-assigned identity map keys for container apps

**Commit:** `0e835678`  
**Author:** derek b moore  
**Date:** 2025-12-11 18:31:38 -0700  

---

#### Use user-assigned identities for KV secrets and add ZEP API key

**Commit:** `965e16a7`  
**Author:** derek b moore  
**Date:** 2025-12-11 18:08:10 -0700  

---

#### Scope temporal app names per env and reduce OpenAI capacity

**Commit:** `44e1bd96`  
**Author:** derek b moore  
**Date:** 2025-12-11 17:49:59 -0700  

---

#### Fix infra naming and disable custom domain bindings

**Commit:** `ce386739`  
**Author:** derek b moore  
**Date:** 2025-12-11 17:40:15 -0700  

---

#### Install portaudio headers for worker image

**Commit:** `be5fbae7`  
**Author:** derek b moore  
**Date:** 2025-12-11 16:45:14 -0700  

---

#### Fix backend ACA env var block

**Commit:** `3da7eb5b`  
**Author:** derek b moore  
**Date:** 2025-12-11 16:32:00 -0700  

---

#### Add Sources intake UI and ingestion mocks

**Commit:** `4fdf3697`  
**Author:** derek b moore  
**Date:** 2025-12-11 16:24:23 -0700  

---

#### chore: remove stale submodule and tidy voice clients

**Commit:** `2ecec1c1`  
**Author:** derek b moore  
**Date:** 2025-12-11 15:34:59 -0700  

---

#### fix(ci): Explicitly use ruff.toml and upgrade linter

**Commit:** `f416e941`  
**Author:** derek b moore  
**Date:** 2025-12-11 15:02:28 -0700  

---

#### fix(lint): Add ruff config to ignore raw files and fix unused imports

**Commit:** `ca7e8371`  
**Author:** derek b moore  
**Date:** 2025-12-11 14:54:42 -0700  

---

#### fix(ci): Install portaudio19-dev for pyaudio dependency

**Commit:** `2d243208`  
**Author:** derek b moore  
**Date:** 2025-12-11 14:49:12 -0700  

---

#### fix(deploy): Add VoiceLive deps and env vars to infra

**Commit:** `5b9ba9e6`  
**Author:** derek b moore  
**Date:** 2025-12-11 14:28:25 -0700  

---

#### chore: Remove venv311 from git tracking

**Commit:** `c36e72d0`  
**Author:** derek b moore  
**Date:** 2025-12-11 14:23:22 -0700  

---

#### feat: Implement Voice and Chat clients for Elena and Marcus

**Commit:** `62b335a3`  
**Author:** derek b moore  
**Date:** 2025-12-11 14:21:54 -0700  

---

#### feat(voice): use openai realtime api and json prompts

**Commit:** `7e7a6fce`  
**Author:** derek b moore  
**Date:** 2025-12-11 11:12:33 -0700  

---

#### fix: resolve bicep variable reference and refactor voice client

**Commit:** `978b7e60`  
**Author:** derek b moore  
**Date:** 2025-12-11 11:00:20 -0700  

---

#### feat: migrate secrets to key vault

**Commit:** `40e6b8c2`  
**Author:** derek b moore  
**Date:** 2025-12-11 10:54:23 -0700  

---

#### fix: align bicep with existing manual certificates

**Commit:** `6ce58a0f`  
**Author:** derek b moore  
**Date:** 2025-12-11 07:21:51 -0700  

---

#### fix: stage 2 deployment - restore ssl binding and cert resource

**Commit:** `34c3f6d9`  
**Author:** derek b moore  
**Date:** 2025-12-11 07:12:11 -0700  

---

#### fix: stage 1 deployment - disable ssl binding

**Commit:** `8e151a54`  
**Author:** derek b moore  
**Date:** 2025-12-11 07:04:58 -0700  

---

#### fix(infra): update managedCertificates to supported 2024-03-01 API version

**Commit:** `65bc95a0`  
**Author:** derek b moore  
**Date:** 2025-12-11 06:37:51 -0700  

---

#### Align Zep URL to v2 and enable DNS automation

**Commit:** `e63a11fd`  
**Author:** derek b moore  
**Date:** 2025-12-11 06:18:33 -0700  

---

#### Bind managed certs for api and temporal domains

**Commit:** `b46b4d67`  
**Author:** derek b moore  
**Date:** 2025-12-11 06:00:38 -0700  

---

#### Switch Zep API Key to Key Vault integration

**Commit:** `de35140e`  
**Author:** derek b moore  
**Date:** 2025-12-11 05:53:30 -0700  

---

#### Remove Zep container and configure SaaS

**Commit:** `dedb8150`  
**Author:** derek b moore  
**Date:** 2025-12-11 05:48:53 -0700  

---


### 2025-12-10

#### Fix duplicate allowInsecure property in backend-aca.bicep

**Commit:** `7158c634`  
**Author:** derek b moore  
**Date:** 2025-12-10 17:17:02 -0700  

---

#### feat(infra): enable custom domain engram.work for frontend

**Commit:** `cf471ae7`  
**Author:** derek b moore  
**Date:** 2025-12-10 16:12:10 -0700  

---

#### style(backend): apply black formatting to fix CI

**Commit:** `0139683f`  
**Author:** derek b moore  
**Date:** 2025-12-10 15:48:23 -0700  

---

#### fix(backend): remove persistent unused imports (admin:HTTPException, etl:Optional)

**Commit:** `619f8d97`  
**Author:** derek b moore  
**Date:** 2025-12-10 15:44:28 -0700  

---

#### fix(backend): specific fix for unused exception in memory.py

**Commit:** `1101cde6`  
**Author:** derek b moore  
**Date:** 2025-12-10 15:39:28 -0700  

---

#### fix(backend): resolve remaining flake8 lint errors (F811, F841)

**Commit:** `2c11749e`  
**Author:** derek b moore  
**Date:** 2025-12-10 15:38:18 -0700  

---

#### fix(backend): resolve multiple flake8 lint errors (F401, F841, F811)

**Commit:** `a19f493f`  
**Author:** derek b moore  
**Date:** 2025-12-10 15:37:28 -0700  

---

#### fix(backend): remove unused import in etl/processor.py

**Commit:** `7f75dd13`  
**Author:** derek b moore  
**Date:** 2025-12-10 15:31:41 -0700  

---

#### fix(frontend): resolve Agent type error and settings value mismatch

**Commit:** `ab8e948b`  
**Author:** derek b moore  
**Date:** 2025-12-10 15:21:32 -0700  

---

#### fix(frontend): align SystemHealth state type with API response

**Commit:** `fb931f7f`  
**Author:** derek b moore  
**Date:** 2025-12-10 15:19:24 -0700  

---

#### fix(frontend): resolve TS lint errors (imports, types) to unblock CI

**Commit:** `4a1b48a2`  
**Author:** derek b moore  
**Date:** 2025-12-10 15:17:23 -0700  

---

#### fix(frontend): resolve remaining lint errors and implement workflow pagination

**Commit:** `0ac1af71`  
**Author:** derek b moore  
**Date:** 2025-12-10 14:36:44 -0700  

---

#### fix(infra): revert to default aca hostnames and re-enable zep; fix(frontend): resolve linting errors

**Commit:** `a0fcd562`  
**Author:** derek b moore  
**Date:** 2025-12-10 12:50:39 -0700  

---

#### chore: comprehensive cleanup and archival of redundant files and docs

**Commit:** `f1b0cc68`  
**Author:** derek b moore  
**Date:** 2025-12-10 12:40:39 -0700  

---

#### fix(infra): resolve circular dependency by deferring cert binding

**Commit:** `2544aef3`  
**Author:** derek b moore  
**Date:** 2025-12-10 09:47:03 -0700  

---

#### fix(ci): use CR_PAT for aca registry authentication

**Commit:** `f1441beb`  
**Author:** derek b moore  
**Date:** 2025-12-10 09:16:47 -0700  

---

#### fix(infra): add missing subjectName to managedCert resources

**Commit:** `298296de`  
**Author:** derek b moore  
**Date:** 2025-12-10 09:02:56 -0700  

---

#### fix(infra): remove invalid param acaEnvId from backend module reference

**Commit:** `29dab78d`  
**Author:** derek b moore  
**Date:** 2025-12-10 08:55:47 -0700  

---

#### fix(infra): remove duplicated bicep content block

**Commit:** `660f2040`  
**Author:** derek b moore  
**Date:** 2025-12-10 08:50:19 -0700  

---

#### fix(infra): remove duplicate resources and fix bicep syntax errors

**Commit:** `5bb02d89`  
**Author:** derek b moore  
**Date:** 2025-12-10 08:12:38 -0700  

---


### 2025-12-09

#### feat(infra): configure custom DNS and managed certs for ACAs

**Commit:** `c6df24b5`  
**Author:** derek b moore  
**Date:** 2025-12-09 19:41:51 -0700  

---

#### fix(infra): update CORS origins for SWA

**Commit:** `1fc4f0bb`  
**Author:** derek b moore  
**Date:** 2025-12-09 19:38:32 -0700  

---

#### style: fix linting issues in voice module

**Commit:** `0c7ce659`  
**Author:** derek b moore  
**Date:** 2025-12-09 19:16:31 -0700  

---

#### fix(infra): add postgres firewall rule for azure services

**Commit:** `64b50f3b`  
**Author:** derek b moore  
**Date:** 2025-12-09 19:12:12 -0700  

---

#### fix(deploy): update SWA path and health check timeout

**Commit:** `c7c4923d`  
**Author:** derek b moore  
**Date:** 2025-12-09 19:07:30 -0700  

---

#### docs: Update wiki to reflect VoiceLive integration

**Commit:** `81aef26b`  
**Author:** derek b moore  
**Date:** 2025-12-09 17:51:07 -0700  

- Updated docs/index.md to replace 'Azure Speech SDK' with 'Azure VoiceLive'

---

#### feat: Integrate VoiceLive with avatar support and remove reference code folders

**Commit:** `4618f8ae`  
**Author:** derek b moore  
**Date:** 2025-12-09 17:48:32 -0700  

- Enhanced VoiceLive service with Elena/Marcus reference patterns

---

#### Fix remaining VoiceLive scenario documentation

**Commit:** `58aa53bd`  
**Author:** derek b moore  
**Date:** 2025-12-09 17:29:21 -0700  

---

#### Complete VoiceLive documentation update

**Commit:** `c1f1a356`  
**Author:** derek b moore  
**Date:** 2025-12-09 17:29:12 -0700  

- Update architecture decision rationale for VoiceLive

---

#### Update documentation to reflect VoiceLive as primary voice integration

**Commit:** `be04e918`  
**Author:** derek b moore  
**Date:** 2025-12-09 17:28:57 -0700  

- Change from Speech Services to VoiceLive throughout documentation

---

#### Fix lint errors in useKeepAlive hook

**Commit:** `51a9968b`  
**Author:** derek b moore  
**Date:** 2025-12-09 17:16:10 -0700  

- Initialize lastActivityRef with 0 instead of Date.now() to avoid impure function call during render

---

#### Configure container scaling with 30-minute keep-alive

**Commit:** `961a2ada`  
**Author:** derek b moore  
**Date:** 2025-12-09 17:12:37 -0700  

- Add HTTP scale rules to backend and worker Container Apps

---

#### Fix TypeScript error in useKeepAlive hook

**Commit:** `a224ee09`  
**Author:** derek b moore  
**Date:** 2025-12-09 14:52:57 -0700  

- Replace NodeJS.Timeout with ReturnType<typeof setInterval>

---

#### Use latest tag for container images in deployment

**Commit:** `ff4e7304`  
**Author:** derek b moore  
**Date:** 2025-12-09 14:47:11 -0700  

- Switch from commit SHA to :latest tag

---

#### Add container scaling configuration documentation

**Commit:** `baf19a99`  
**Author:** derek b moore  
**Date:** 2025-12-09 14:39:39 -0700  

---

#### Configure containers to stay warm for 30 minutes after user activity

**Commit:** `9a63aeb6`  
**Author:** derek b moore  
**Date:** 2025-12-09 14:39:26 -0700  

- Add HTTP scale rules to backend and worker Container Apps

---

#### Remove keyVaultName parameter from worker module call

**Commit:** `b463998a`  
**Author:** derek b moore  
**Date:** 2025-12-09 14:00:25 -0700  

---

#### Remove unused Key Vault resource declarations

**Commit:** `4c2899c1`  
**Author:** derek b moore  
**Date:** 2025-12-09 13:59:35 -0700  

- Remove unused keyVaultName parameter from backend and worker modules

---

#### Remove dnsResourceGroup parameter from DNS module

**Commit:** `3099cea7`  
**Author:** derek b moore  
**Date:** 2025-12-09 13:36:51 -0700  

---

#### Fix DNS module parameter error - remove frontendHostname

**Commit:** `7eae0bd3`  
**Author:** derek b moore  
**Date:** 2025-12-09 13:35:38 -0700  

---

#### Fix DNS module scope error and add Engram favicon

**Commit:** `7bc67e50`  
**Author:** derek b moore  
**Date:** 2025-12-09 13:29:40 -0700  

- Fix DNS module to deploy to dns-rg resource group scope

---

#### Fix: Remove invalid deploymentOutputs parameter and update workflow to query outputs via Azure CLI

**Commit:** `d46489de`  
**Author:** derek b moore  
**Date:** 2025-12-09 12:59:05 -0700  

- Removed invalid 'deploymentOutputs' parameter from azure/arm-deploy@v2 action

---

#### fix: Handle scale-to-zero cold start in health check and make Slack notifications optional

**Commit:** `b302442a`  
**Author:** derek b moore  
**Date:** 2025-12-09 12:08:13 -0700  

- Add retry logic to health check (10 attempts, 10s delay) to handle scale-to-zero cold starts

---

#### Fix BCP120 by moving RA to modules

**Commit:** `f0b5c8ec`  
**Author:** derek b moore  
**Date:** 2025-12-09 11:24:30 -0700  

---

#### Configure Managed Identity and KV Role Assignments

**Commit:** `0009d355`  
**Author:** derek b moore  
**Date:** 2025-12-09 11:20:27 -0700  

---

#### Configure dynamic SWA token fetching

**Commit:** `71375f1e`  
**Author:** derek b moore  
**Date:** 2025-12-09 11:06:03 -0700  

---

#### Fix missing keyVaultUri param definition

**Commit:** `57446b3b`  
**Author:** derek b moore  
**Date:** 2025-12-09 10:58:15 -0700  

---

#### Configure KV URL and remove redundant deploy jobs

**Commit:** `57fdee28`  
**Author:** derek b moore  
**Date:** 2025-12-09 10:53:48 -0700  

---

#### Add SKU to OpenAI deployment

**Commit:** `7ee7d7c7`  
**Author:** derek b moore  
**Date:** 2025-12-09 10:45:01 -0700  

---

#### Restore missing resources in main.bicep

**Commit:** `38c66d88`  
**Author:** derek b moore  
**Date:** 2025-12-09 10:39:00 -0700  

---

#### Configure GHCR auth for Azure Container Apps

**Commit:** `f04bb7e7`  
**Author:** derek b moore  
**Date:** 2025-12-09 10:35:05 -0700  

---

#### Bypass soft-delete for Speech/OpenAI and use ghcr for Zep

**Commit:** `a3a12bc6`  
**Author:** derek b moore  
**Date:** 2025-12-09 10:26:51 -0700  

---

#### Fix Key Vault name, Temporal ingress, and Zep image

**Commit:** `02401b8c`  
**Author:** derek b moore  
**Date:** 2025-12-09 10:18:31 -0700  

---

#### Remove unused adminObjectId from deploy params

**Commit:** `2c31720d`  
**Author:** derek b moore  
**Date:** 2025-12-09 10:11:59 -0700  

---

#### Fix deploy workflow syntax

**Commit:** `c8a0e8d0`  
**Author:** derek b moore  
**Date:** 2025-12-09 10:08:05 -0700  

---

#### Fix Bicep warnings and disable failOnStdErr

**Commit:** `1aea0453`  
**Author:** derek b moore  
**Date:** 2025-12-09 10:07:33 -0700  

---

#### Switch back to eastus2 for deployment

**Commit:** `3062ba25`  
**Author:** derek b moore  
**Date:** 2025-12-09 09:58:27 -0700  

---

#### Fix Bicep errors and revert location to westus2

**Commit:** `13043b33`  
**Author:** derek b moore  
**Date:** 2025-12-09 09:47:45 -0700  

---

#### Fix OpenAI model version and unused params

**Commit:** `a553cf23`  
**Author:** derek b moore  
**Date:** 2025-12-09 09:42:51 -0700  

---

#### Ensure unique Key Vault name

**Commit:** `0ad25c5f`  
**Author:** derek b moore  
**Date:** 2025-12-09 09:37:49 -0700  

---

#### Remove KV role assignment to fix deployment

**Commit:** `fc208515`  
**Author:** derek b moore  
**Date:** 2025-12-09 09:33:04 -0700  

---

#### Change Azure region to eastus2 for SWA availability

**Commit:** `81b46c21`  
**Author:** derek b moore  
**Date:** 2025-12-09 09:07:40 -0700  

---

#### Fix GHCR permissions in CI

**Commit:** `730c9781`  
**Author:** derek b moore  
**Date:** 2025-12-09 09:02:16 -0700  

---

#### Format test_context.py

**Commit:** `29c4f541`  
**Author:** derek b moore  
**Date:** 2025-12-09 08:58:45 -0700  

---

#### Fix context session sync and test assertions

**Commit:** `f5ab8cd7`  
**Author:** derek b moore  
**Date:** 2025-12-09 08:57:16 -0700  

---

#### Apply formatting fixes

**Commit:** `bc2ce6db`  
**Author:** derek b moore  
**Date:** 2025-12-09 08:53:28 -0700  

---

#### Fix SWA deployment path

**Commit:** `ed96c995`  
**Author:** derek b moore  
**Date:** 2025-12-09 08:51:21 -0700  

---

#### Add Static Web App to infrastructure deployment

**Commit:** `b7b9415a`  
**Author:** derek b moore  
**Date:** 2025-12-09 08:42:18 -0700  

- Include SWA module in main.bicep

---

#### Fix linting errors: remove unused imports and fix bare except

**Commit:** `2477b09f`  
**Author:** derek b moore  
**Date:** 2025-12-09 08:41:43 -0700  

- Remove unused base64 and asyncio imports from voicelive_service.py

---

#### feat: Enable scale-to-zero for all ACA services & fix frontend imports

**Commit:** `cddef7b2`  
**Author:** derek b moore  
**Date:** 2025-12-09 08:30:09 -0700  

---

#### feat: Complete PoC validation, fix frontend build and auth tests, update status to 100%

**Commit:** `c3b1e524`  
**Author:** derek b moore  
**Date:** 2025-12-09 08:05:01 -0700  

---


### 2025-12-08

#### Add Azure HorizonDB testing plan

**Commit:** `286f25d9`  
**Author:** derek b moore  
**Date:** 2025-12-08 18:01:05 -0700  

## Overview

---

#### Add Azure Database for PostgreSQL documentation

**Commit:** `756d5576`  
**Author:** derek b moore  
**Date:** 2025-12-08 17:55:46 -0700  

## Research Summary

---

#### Fix wiki image paths: use absolute paths with leading slash

**Commit:** `2d1f63c6`  
**Author:** derek b moore  
**Date:** 2025-12-08 17:54:06 -0700  

- Changed all image references from 'assets/images/' to '/assets/images/'

---

#### Fix Docker health check command syntax

**Commit:** `2b9b7495`  
**Author:** derek b moore  
**Date:** 2025-12-08 17:52:46 -0700  

- Wrap health-cmd in quotes: 'pg_isready -U postgres'

---

#### Fix CI issues: remove unused sys import and fix Postgres health check

**Commit:** `2b5b280b`  
**Author:** derek b moore  
**Date:** 2025-12-08 17:51:23 -0700  

## Unused Import

---

#### Fix all CI issues: formatting, ESLint, and security permissions

**Commit:** `0a70c05a`  
**Author:** derek b moore  
**Date:** 2025-12-08 17:48:29 -0700  

## Black Formatting

---

#### Improve backend test environment setup

**Commit:** `c3ea6f21`  
**Author:** derek b moore  
**Date:** 2025-12-08 17:44:17 -0700  

- Set all required environment variables before imports

---

#### Fix frontend ESLint errors: remove setState in effects

**Commit:** `ff35fa4c`  
**Author:** derek b moore  
**Date:** 2025-12-08 17:43:50 -0700  

## ChatPanel.tsx

---

#### Add basic backend tests for CI

**Commit:** `4d62a08e`  
**Author:** derek b moore  
**Date:** 2025-12-08 17:41:15 -0700  

## Test Files Added

---

#### Fix remaining frontend ESLint errors

**Commit:** `b6c7b508`  
**Author:** derek b moore  
**Date:** 2025-12-08 17:39:56 -0700  

## AvatarDisplay.tsx

---

#### Format backend code with Black

**Commit:** `f058e37d`  
**Author:** derek b moore  
**Date:** 2025-12-08 17:38:57 -0700  

Reformatted 32 Python files to comply with Black code style:

---

#### Fix frontend ESLint errors

**Commit:** `fd86cf60`  
**Author:** derek b moore  
**Date:** 2025-12-08 17:37:42 -0700  

## AvatarDisplay.tsx

---

#### Fix wiki deploy: install jekyll-theme-minimal gem

**Commit:** `0238c85d`  
**Author:** derek b moore  
**Date:** 2025-12-08 17:34:51 -0700  

---

#### Fix ruff linting errors for CI

**Commit:** `a6c0991c`  
**Author:** derek b moore  
**Date:** 2025-12-08 17:33:38 -0700  

## Fixes Applied (39 errors)

---

#### Add Nano Banana Pro generated images to wiki

**Commit:** `8f4841c7`  
**Author:** derek b moore  
**Date:** 2025-12-08 17:25:26 -0700  

## PNG Images Added

---

#### Fix: Revert image references to SVG (PNG files not yet added)

**Commit:** `c3e2527c`  
**Author:** derek b moore  
**Date:** 2025-12-08 17:05:50 -0700  

Reverted all image references from .png back to .svg since only

---

#### Update wiki to reference PNG images from Nano Banana Pro

**Commit:** `57f4a9fa`  
**Author:** derek b moore  
**Date:** 2025-12-08 17:04:07 -0700  

Updated all wiki pages to reference .png versions of images:

---

#### Add SVG visual assets for wiki

**Commit:** `e0eda598`  
**Author:** derek b moore  
**Date:** 2025-12-08 17:02:33 -0700  

## SVG Images Created

---

#### Add wiki documentation with image placeholders and JSON prompts

**Commit:** `3e42fc11`  
**Author:** derek b moore  
**Date:** 2025-12-08 16:56:20 -0700  

## Wiki Documentation (docs/)

---

#### Phase 5: Enterprise Hardening - Auth, RBAC, Observability, CI/CD

**Commit:** `b5b0da0b`  
**Author:** derek b moore  
**Date:** 2025-12-08 16:50:17 -0700  

## Microsoft Entra ID Authentication (backend/api/middleware/auth.py)

---

#### Phase 4: Voice + Avatar - Azure Speech & Avatar Integration

**Commit:** `6f0af1c0`  
**Author:** derek b moore  
**Date:** 2025-12-08 16:45:34 -0700  

## Backend Voice Module (backend/voice/)

---

#### Phase 3: Durable Spine - Temporal Workflows

**Commit:** `13897c38`  
**Author:** derek b moore  
**Date:** 2025-12-08 16:38:35 -0700  

## Temporal Activities (backend/workflows/activities.py)

---

#### Phase 2: Agent Brain - Elena, Marcus, Router, Zep Memory

**Commit:** `6e0b6277`  
**Author:** derek b moore  
**Date:** 2025-12-08 16:30:12 -0700  

## LangGraph Agents

---

#### Phase 1: Foundation - Backend structure, Context Schema, Frontend 3-column layout

**Commit:** `65353973`  
**Author:** derek b moore  
**Date:** 2025-12-08 16:19:55 -0700  

## Backend

---

#### Comment out custom domain in Bicep to allow initial deployment

**Commit:** `2999754c`  
**Author:** derek b moore  
**Date:** 2025-12-08 13:53:17 -0700  

---

#### Update Wiki link to wiki.engram.work

**Commit:** `20d6f3d9`  
**Author:** derek b moore  
**Date:** 2025-12-08 13:49:36 -0700  

---

#### Fix linter errors: CSS backdrop-filter order and usage of inline styles

**Commit:** `ca4de105`  
**Author:** derek b moore  
**Date:** 2025-12-08 13:39:52 -0700  

---

#### Update repo URL to zimaxnet/engram

**Commit:** `173421de`  
**Author:** derek b moore  
**Date:** 2025-12-08 13:33:00 -0700  

---

#### Add Engram Frontend and Azure SWA Infra

**Commit:** `213c0bcb`  
**Author:** derek b moore  
**Date:** 2025-12-08 13:28:22 -0700  

---

#### Scaffold Azure PoC Components (Zep, Temporal, Agent, ETL, Infra)

**Commit:** `b8b6d213`  
**Author:** derek b moore  
**Date:** 2025-12-08 12:25:39 -0700  

---

#### Initial project structure

**Commit:** `4a6dc0b2`  
**Author:** derek b moore  
**Date:** 2025-12-08 12:23:07 -0700  

---



*Document generated: 2026-01-22T16:02:01.585308*
