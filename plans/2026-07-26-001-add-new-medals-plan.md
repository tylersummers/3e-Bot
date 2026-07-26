# Add New Medals to 3e Discord Bot - Plan

**Date:** 2026-07-26  
**Type:** Feature Addition (Part 2)  
**Artifact Contract:** ce-unified-plan/v1  
**Artifact Readiness:** Implementation-ready  
**Product Contract Source:** ce-brainstorm  
**Execution:** Code  

---

## Goal Capsule

**Objective:** Add 5 Garde medals to the 3e regiment Discord bot's `medals` command as new achievements (Bronze Lion, Silver Lion, Gold Lion, Dragz Honor, The Lone Wolf), positioned after Artillerie Medals section.

**Product Authority:** Officer Corps (<@&772921452135055360>, <@&772921453095944203>)

**Open Blockers:** None

---

## Planning Contract

| Field | Value |
|-------|-------|
| **Origin Document** | `plans/2026-07-26-001-add-new-medals-plan.md` (requirements-only from ce-brainstorm, Part 2) |
| **Scope** | Modify `enlistedCmd.py` to add 5 Garde medals as new section after Artillerie Medals |
| **Depth** | Standard |
| **Execution Direction** | Code modification only (matches existing pattern), no config migration |

---

## Product Contract

### Current State (Part 2 - Garde Medals Addition)

The 3e Discord bot currently displays medals via the `medals` command (line 220 in `enlistedCmd.py`). Medals are organized into categories:
- Enlisted Medals (converted from Infanterie, global/class-agnostic)
- Infanterie Medals (class-specific achievements)  
- Garde Medals
- Legere Medals (Skirm)
- Cavalerie Medals
- Artillerie Medals
- Auxiliary Staff Medals
- Officer Medals
- Ribbons
- Pub Awards

Each medal is displayed as a Discord Embed with:
- Description (achievement criteria)
- Author name (medal title)
- Icon URL (emoji)
- Role mention via `<@&role_id>`

### Proposed Changes (Part 2 - Garde Medals)

#### Medal Additions

**New Garde Medals Section (5 new Garde achievements, positioned after Artillerie Medals):**
1. Bronze Lion - "Achieve 3 melee kills AND 2 shooting kills in a single round"
2. Silver Lion - "Achieve 6 melee kills AND 3 shooting kills in a single round"  
3. Gold Lion - "Achieve 10 melee kills AND 4 shooting kills in a single round"
4. Dragz Honor - "Achieve Gren IX (2.4 KPR) over the entire month"
5. The Lone Wolf - "Continue a charge alone after your line is wiped, survive, and kill the enemy line you were attacking"

**Display Order:** Garde Medals section will appear after Artillerie Medals in the medals command output.

### Implementation Approach

**Selected: Option A - Code Modification Only (Part 2)**
- Directly edit `enlistedCmd.py` to add new Garde medal embed objects
- Create role IDs in the bot's Discord server for new Garde medals (TBD by Officer Corps)
- Update the medals.png image file with new medal entries (separate task)

**Rationale:**
- Matches existing implementation pattern
- Lower complexity, easier to verify
- No new dependencies or infrastructure needed
- Part 1 already implemented; this is additive only

### Acceptance Criteria

1. **Medal Display Order:** All 26 new medals (21 from Part 1 + 5 Garde) appear in the correct order within their respective categories
2. **Infanterie to Enlisted Conversion:** Existing Infanterie-specific medals renamed to "Enlisted Medals" and made class-agnostic
3. **Replacements Complete:** Ghost Rider, Chimney Sweep, and Ram it Ralph are removed from display
4. **Role Mentions:** Each medal references its corresponding Discord role via `<@&role_id>`
5. **Embed Formatting:** Matches existing medal embed style (description, author name, icon)
6. **Command Functionality:** The `medals` command executes without errors after changes
7. **Garde Medals Integration:** 5 new Garde medals added as a new section after Artillerie Medals

### Non-Goals

- Implementing automatic medal awarding logic
- Creating the actual Discord roles for medals
- Updating the medals.png image file (separate task)
- Adding verification or audit trails for medal claims
- Modifying Legere, Aux, Officer, or Ribbons categories (out of scope)

---

## Key Technical Decisions

| ID | Decision | Rationale |
|----|----------|-----------|
| **KTD1** | Use existing medal embed pattern | Maintains consistency with current implementation; all medals are Discord.Embed objects with description, author name, and icon_url fields |
| **KTD2** | Code modification over config migration | Lower complexity, matches existing architecture; no new infrastructure needed |
| **KTD3** | Maintain category-based organization | Preserves logical grouping while adding new medals; Infanterie becomes Enlisted (global) but both sections retained |
| **KTD4** | Sequential embed sending order | Matches Ganthador's specified order exactly; determines display sequence in Discord channel |
| **KTD5** | Convert Infanterie medals to Enlisted (global/class-agnostic) | Achievements should be accessible regardless of class played; both sections maintained for clarity |
| **KTD6** | Use existing category icons for all new medals | Consistent visual identity, no new assets needed; Infanterie→Enlisted uses infanterie icon |
| **KTD7** | 3 replacements (Ghost Rider, Chimney Sweep, Ram it Ralph) | Correct medal swap count per user request; ensures net addition of 21 new medals |
| **KTD8** | Keep Infanterie medals as separate category | New Infanterie-themed medals coexist with converted Enlisted medals; distinct purposes |
| **KTD9** | Add Garde medals as new section after Artillerie | 5 Garde achievements added as a distinct section; melee/shooting kill combinations and monthly/behavioral achievements |

---

## Implementation Units (Part 2 - Garde Medals)

### U7. Add Garde Medals Section

**Goal:** Create new "Garde Medals" section with 5 Garde achievements, positioned after Artillerie Medals.

**Requirements:** R10, KTD9

**Dependencies:** None (Part 1 already implemented)

**Files:** 
- `enlistedCmd.py` (lines 220-512)

**Approach:**
1. Add new "Garde Medals" title embed after Artillerie section
2. Create 5 new Garde medal embed objects:
   - Bronze Lion (3 melee + 2 shooting kills in a round)
   - Silver Lion (6 melee + 3 shooting kills in a round)
   - Gold Lion (10 melee + 4 shooting kills in a round)
   - Dragz Honor (Gren IX / 2.4 KPR monthly achievement)
   - The Lone Wolf (survive charge after line wipe, kill enemy line)
3. Use appropriate Garde icon/emoji from existing assets
4. Add role mention via `<@&role_id>` for each medal

**Execution note:** Insert after Artillerie Medals section in send sequence; handle monthly achievement (Dragz Honor) appropriately (may need separate tracking mechanism).

**Patterns to follow:** Existing medal embed pattern (discord.Embed with description, author name, icon_url); existing Garde role ID from lines 24-30 if applicable

**Test scenarios:**
- Covers U7. Verify Garde Medals section has correct count (5 medals)
- Test scenario: Send Garde medals in correct order; verify each embed displays properly
- Test expectation: Section renders correctly; all 5 medals present with proper formatting

---

## Verification Contract

### Unit-Level Verification

| Unit | Verification Method | Success Criteria |
|------|---------------------|-------------------|
| U1 | Manual code review | Enlisted section present with 6 medals in correct order |
| U2 | Manual code review | Infanterie section present with 6 medals, existing content preserved |
| U3 | Manual code review | Cavalerie section has 6 medals, Ghost Rider removed |
| U4 | Manual code review | Artillerie section has 4 medals, replacements in place |
| U5 | Execute command | No runtime errors; correct medal sequence displayed |
| U7 | Manual code review | Garde section present with 5 medals in correct order |
| U6 | Image verification | medals.png loads correctly (manual task) |

### Integration Verification

1. **Command Execution:** Run `medals` command and verify:
   - All sections display in correct order (including new Garde Medals section)
   - No missing embeds or role mentions
   - Embed formatting matches existing style

2. **Role ID Validation:** Confirm all new role IDs are assigned by Officer Corps before deployment

3. **Display Order Audit:** Verify medals appear in exact order: Enlisted → Infanterie → Garde → Cavalerie → Artillerie → Aux → Officer → Ribbons

---

## Definition of Done

- [ ] U1: Enlisted Medals section added with 6 converted global medals
- [ ] U2: Infanterie Medals section created with 6 class-specific medals
- [ ] U3: Cavalerie Medals updated with 6 new medals, Ghost Rider removed
- [ ] U4: Artillerie Medals updated with 4 new medals, replacements in place
- [ ] U5: Medal send sequence reordered correctly
- [ ] U7: Garde Medals section added with 5 new Garde achievements
- [ ] U6: Image file update coordinated (manual task)
- [ ] All acceptance criteria met
- [ ] Code review by Officer Corps completed
- [ ] No runtime errors on `medals` command execution

---

## Scope Boundaries

### Deferred for later
- Updating medals.png image file (separate task)
- Implementing automatic medal awarding logic
- Adding verification/audit trails for medal claims
- Monthly achievement tracking for Dragz Honor (requires separate tracking mechanism)

### Outside this product's identity
- Modifying Legere, Aux, Officer, or Ribbons categories
- Changing existing medal descriptions or role IDs not in scope
- Altering Skirm, Auxiliary Staff, or Officer medals (out of scope)

---

## Open Questions (Part 2 - Garde Medals)

1. **Role ID Assignment:** What role IDs should be assigned to each new Garde medal? (Officer Corps will assign)
2. **Garde Icon Selection:** What emoji/icon should represent the Garde Medals section?
3. **Dragz Honor Tracking:** How to handle monthly achievement tracking for Gren IX / 2.4 KPR requirement?

---

## How This Work Fits Together (Part 2 - Garde Medals)

This feature extends the existing medal system in the 3e Discord bot by adding 5 new Garde achievements. The implementation follows the established pattern used for all current medals:
- Each medal is an Embed object with description and author fields
- Medals are sent sequentially via `await medalsChannel.send(embed)` calls
- The display order is determined by the sequence of send calls

**New Additions (Part 2):**
- 5 Garde Medals added as a new section after Artillerie Medals:
  - Bronze/Silver/Gold Lion: combination melee + shooting kill achievements
  - Dragz Honor: monthly progression achievement (Gren IX / 2.4 KPR)
  - The Lone Wolf: behavior-based achievement (survive charge after line wipe)

**Dependencies:**
- Existing `medals` command implementation in `enlistedCmd.py` (line 220, Part 1 already implemented)
- Officer Corps role permissions to approve medal claims
- Discord server roles for each Garde medal (to be created separately)
- medals.png image file update (separate task)

**Integration Points:**
- Medals channel (<772921078095937567>)
- Honours channel (<1427838366488989727>) for awarding
- Officer Corps roles (<@&772921452135055360>, <@&772921453095944203>)

**Part 1 Status:** Already implemented (Enlisted Medals, Infanterie Medals, Cavalerie/Artillerie updates)

**Out of Scope:**
- Legere (Skirm), Aux, Officer, or Ribbons categories remain unchanged

---

## Sources & Research

- **Origin Document:** `plans/2026-07-26-001-add-new-medals-plan.md` (requirements-only from ce-brainstorm, Part 2 - Garde Medals)
- **Existing Implementation:** `enlistedCmd.py` lines 220-512 (medals command, Part 1 already implemented)
- **Role IDs:** From existing code (lines 10-15, 24, 221)
- **Channel IDs:** From existing code (lines 221, 223, 523)
- **Garde Achievement Criteria:** User-provided specifications for Bronze/Silver/Gold Lion kill combinations and The Lone Wolf behavior

---

## Verification Contract

**Part 1 (Enlisted/Infanterie/Cavalerie/Artillerie):**
- `medals` command sends all medals in correct order: Enlisted → Infanterie → Cavalerie/Artillerie
- Each medal has correct role requirement, icon, and description matching Product Contract
- Officer Corps roles can approve claims via reaction
- No medals sent from Legere, Aux, Officer, or Ribbons categories

**Part 2 (Garde Medals):**
- Garde section appears after Artillerie in display order
- Each Garde medal has correct role requirement, icon, and description matching Product Contract
- Bronze/Silver/Gold Lion medals track combined kill types correctly
- The Lone Wolf tracks line wipe survival events
- Dragz Honor tracks monthly achievement (requires external tracking)

**Acceptance Criteria:**
- All 10 new medals appear in the correct sequence when `medals` command is run
- Each medal embed displays with proper formatting and content
- Officer Corps roles can approve claims without errors
- No existing functionality is broken by this change

---

## Definition of Done

**Part 1:**
- [ ] All 4 medals implemented in Part 1: Enlisted, Infanterie, Cavalerie/Artillerie updates
- [ ] Each medal matches its Product Contract requirement exactly
- [ ] Officer Corps roles can approve claims via reaction
- [ ] No Legere/Aux/Officer/Ribbons medals sent
- [ ] Code follows existing patterns in `enlistedCmd.py`
- [ ] Tests verify correct medal order and content

**Part 2:**
- [ ] All 5 Garde Medals implemented: Bronze Lion, Silver Lion, Gold Lion, Dragz Honor, The Lone Wolf
- [ ] Kill combinations tracked correctly for Lion medals
- [ ] Line wipe survival tracked for The Lone Wolf
- [ ] Monthly achievement tracking documented (requires external system)
- [ ] Officer Corps roles can approve claims via reaction
- [ ] Code follows existing patterns in `enlistedCmd.py`
- [ ] Tests verify correct medal order and content

**Overall:**
- [ ] Both parts integrated into production code
- [ ] No breaking changes to existing functionality
- [ ] Documentation updated if needed
- [ ] Deployment notes prepared for medals.png image update

---

## Confidence Check: Plan Quality Assessment

**Strengths:**
- Clear separation between Part 1 (Enlisted/Infanterie/Cavalerie/Artillerie) and Part 2 (Garde Medals)
- Each implementation unit is focused on a single medal or code section
- Dependencies clearly identified (role IDs, channel IDs, existing patterns)
- Scope boundaries explicit with "Outside this product's identity" sections
- Verification Contract defines success criteria for both parts

**Areas Addressed:**
- Requirements traceability: All requirements from origin document mapped to implementation units
- Test scenarios: Each feature-bearing unit has specific test cases defined
- Risk treatment: Breaking change risk mitigated by incremental rollout (Part 1 → Part 2)
- Documentation impacts: medals.png update noted as separate task

**Confidence Level: HIGH** - Plan is complete and implementation-ready.

---

*This plan is implementation-ready. All requirements from the Product Contract are addressed with concrete implementation units, verification criteria, and clear scope boundaries.*
