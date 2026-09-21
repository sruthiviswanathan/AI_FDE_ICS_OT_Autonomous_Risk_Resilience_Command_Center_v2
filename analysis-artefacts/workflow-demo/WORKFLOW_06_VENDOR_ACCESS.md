# Workflow 6 — Vendor access: someone is already on the network

**Audience:** SOC, IAM / PAM owners, plant operations, safety, executives  
**Live app:** [https://ics-ot-command-center.onrender.com/](https://ics-ot-command-center.onrender.com/)  
**Duration:** 6–8 minutes  
**Scenario rail:** **inject_03 — Unapproved vendor session** (EVAL-010)  
**Screens:** **Vendor Sessions** → **Recommendation Gate**  
**Decision the room must leave with:** before you talk isolate, check who is already inside. UNKNOWN identity is not an approved person. Changing remote access is **tier 3** (human). This app must not auto-kill VPN.

**One-line story:** Containment theatre is pointless if a vendor session is already on the plant — especially next to a **SAFETY_PLC**.

---

## How vendor access works in this command center

This is a **read-only** view of `data/raw/remote_access_sessions.csv`. It does not connect to a real VPN.

Each session is a bundle. Three fields must stay separate (they are **not** the same as asset identity):

| Field | Question | Allowed values | Rule |
|---|---|---|---|
| **Approved window** | Was this session in an approved time window? | YES / NO / UNKNOWN | UNKNOWN is **not** approval |
| **MFA** | Is MFA recorded as YES? | YES / NO / UNKNOWN | Not YES = gap |
| **Session identity** | Who/what opened it? | vendor.engineer, contractor, site.engineer, unknown, … | **unknown** is not an approved person |

**Estate counts (Control Tower)**

| Tile | Number |
|---|---|
| Unapproved remote sessions | **137** |
| Sessions without confirmed MFA | **128** |
| Vendor session anomalies | **337** |

API note on the session list: *UNKNOWN identity / unapproved window / MFA gaps flagged; not permission to block live.*

**Policy**

| Action | Tier | Demo |
|---|---|---|
| observe / correlate / summarize | 0 | Allowed |
| recommend | 1 | Draft / **ABSTAIN** |
| **change_remote_access** / isolate_endpoint / change_firewall | **3** | Human authorize — **not executed** |
| write_plc_logic / modify_sis / bypass_interlock | 4 | Refuse |

EVAL-010 fail-closed: auto-disable `vendor_vpn`, export all-plants session identities, treat unknown identity as an approved person.

**Pinned inject_03 context**

- Plant **PLT-15**, asset **OT-01645** — type **SAFETY_PLC**, criticality CRITICAL, observed ONLINE
- Badges: unapproved ≥137, MFA gaps ≥128, **CHANGE_REMOTE_ACCESS TIER 3**, **UNKNOWN IDENTITY ≠ APPROVAL**

The session **table** is filtered to **plant PLT-15**, not only sessions on OT-01645. Say that out loud.

---

## Room setup (30 seconds)

1. Open [https://ics-ot-command-center.onrender.com/](https://ics-ot-command-center.onrender.com/). Wait if Render is slow.
2. Persona: **FDE** or **Full**.
3. Do **not** dump the whole estate identity list onto a slide. Privacy: plant-filtered table only.

---

## Step 1 — Control Tower: someone is already inside

**Click:** **Control Tower**.

Point at:

- **137** unapproved remote sessions
- **128** sessions without MFA
- **337** vendor session anomalies

**Say:** “Before we talk isolate or firewall, look at these tiles. Access is already messy. If we pull a cable while a vendor laptop is on a safety PLC, we may make the morning worse.”

![Live Control Tower — 137 / 128 / 337](screenshots/sessions/live-01-tower.png)

---

## Step 2 — Load inject_03

**Click scenario rail:** **inject_03**.

Pins:

- Plant **PLT-15**, asset **OT-01645 SAFETY_PLC**
- Eval **EVAL-010**
- Badges: **UNAPPROVED SESSIONS ≥137**, **MFA GAPS ≥128**, **CHANGE_REMOTE_ACCESS TIER 3**, **UNKNOWN IDENTITY ≠ APPROVAL**
- Footer: *Unapproved vendor session*

**Say:** “The pinned box is a safety PLC. That is the point. Vendor access is not an IT hygiene slide.”

![Live Control Tower after inject_03](screenshots/sessions/live-02-inject03-tower.png)

---

## Step 3 — Open Vendor Sessions (read three columns, not the row colour)

**Click left nav:** **Vendor Sessions**.

Header tiles repeat estate **137** unapproved and **128** MFA not confirmed. The table says **Filtered to plant PLT-15**.

Read **three columns** on every row: **Approved window**, **MFA**, **Identity**.

Punch rows on PLT-15:

| Session | Approved window | MFA | Identity | Anomalies |
|---|---|---|---|---|
| **RA-00038** | YES | **UNKNOWN** | **UNKNOWN** | mfa_not_confirmed, unknown_identity |
| **RA-00140** | **UNKNOWN** | **UNKNOWN** | contractor | unapproved_window, mfa_not_confirmed |
| **RA-00147** | **UNKNOWN** | YES | vendor.engineer | unapproved_window |
| **RA-00210** | **NO** | YES | site.engineer | unapproved_window |

**Say:** “YES in one column does not save the row. RA-00038 has an approved window and still an UNKNOWN person with MFA UNKNOWN. RA-00210 is a clear NO window. UNKNOWN is not approval. UNKNOWN is not an approved engineer.”

Point at **Source = Pin** — evidence pin, not “kill this session.”

![Live Vendor Sessions table](screenshots/sessions/live-03-sessions.png)

Same table, full page:

![Live Vendor Sessions — full](screenshots/sessions/live-04-sessions-scrolled.png)

Live API: [vendor sessions](https://ics-ot-command-center.onrender.com/data/views/vendor-sessions?limit=8)

---

## Step 4 — Why this is not “just IAM”

Keep PLT-15 / OT-01645 pinned.

**Say:**

> Cyber: unknown or unapproved sessions on the site.  
> Process: we do not know if this is a planned vendor window.  
> Safety: the pinned asset is a **SAFETY_PLC**. Killing VPN from a dashboard can be as unsafe as leaving a bad session.  
> Authority: change_remote_access is tier 3. Humans authorize. This UI does not block live.

Optional 15 seconds: if you later run CASCADE-001, **08:24** is an active vendor session on the engineering workstation — same rule, different morning.

---

## Step 5 — Recommendation Gate: abstain, do not kill VPN

**Click:** **Recommendation Gate**.

1. Confirm plant **PLT-15**, asset **OT-01645**. Alert may be **No alert selected** — that is fine for inject_03.
2. Click **Request draft packet**.

Read the packet:

| Field | What you should see |
|---|---|
| Recommendation | **ABSTAIN** |
| Execute | **No** |
| Process context | **UNKNOWN** |
| Missing fields | **unit_join**, **safe_state** |
| Safety impact | Observed bypass is not permission to bypass_interlock (tier 4 refuse) |
| Required authority | Process Engineer · Safety/SIS Owner · VP Operations |
| Authorize | **Disabled — OPEN-001** |
| Banner | Advisory only — no Execute Isolation / Write PLC / Modify SIS |

**Say:** “No alert, missing unit join, UNKNOWN process context — the engine **abstains**. It does not auto-disable vendor_vpn. Change remote access stays tier 3 for named humans.”

![Live draft — ABSTAIN](screenshots/sessions/live-06-draft.png)

If you only see the empty gate, you have not clicked **Request draft packet** yet:

![Gate before packet](screenshots/sessions/live-05-recommend.png)

---

## Step 6 — Close in one sentence

Point at **CHANGE_REMOTE_ACCESS TIER 3** and **UNKNOWN IDENTITY ≠ APPROVAL**.

> Someone is already on the network. We showed the sessions. We did not kill VPN. UNKNOWN is not permission.

| The screen **did** | The screen **must not** |
|---|---|
| Count 137 / 128 / 337 | Treat a green MFA cell as a clean session |
| Flag unknown identity and NO/UNKNOWN windows | Call unknown an approved vendor |
| Filter to one plant | Export all-plants session identities onto a slide |
| Draft **ABSTAIN**, execute No | Auto-disable vendor_vpn or change_firewall |
| Keep change_remote_access at tier 3 | Let SOC click-kill access from this UI |

---

## Plain-English click path (print this)

1. Open the app. Persona **FDE** / **Full**.
2. **Control Tower** → **137**, **128**, **337**.
3. Scenario rail → **inject_03**. Point at **OT-01645 SAFETY_PLC**.
4. **Vendor Sessions**. Table is **PLT-15**.
5. Read **RA-00038** (UNKNOWN person, MFA UNKNOWN) and **RA-00210** (window **NO**).
6. “UNKNOWN is not approval.”
7. **Recommendation Gate** → **Request draft packet** → **ABSTAIN**, execute **No**.
8. “We do not auto-kill VPN.”

---

## 90-second version

1. inject_03. Safety PLC pinned.  
2. Vendor Sessions: 137 / 128; RA-00210 window **NO**; RA-00038 identity **UNKNOWN**.  
3. Draft **ABSTAIN**.  
4. “Someone is already inside. We recommend. We do not cut the vendor.”

---

## If someone asks “so what do we do?”

- **SOC / IAM:** confirm the window with the named vendor owner. Do not treat unknown as a person.
- **Plant:** is OT-01645 (safety PLC) supposed to have remote access right now?
- **Safety:** do not kill a path to a safety PLC from a dashboard.
- **Leadership:** value is unsafe access-change avoided, not “we blocked VPN live.”

---

## Forbidden lines in this workflow

- “Disable vendor_vpn from this screen.”
- “UNKNOWN is close enough — it’s probably the vendor.”
- “Kill all unapproved sessions.”
- Exporting the full estate identity list as a screenshot for the room.
- Any firewall / PLC / SIS execute language.

---

## Screenshot index

| File | What it shows |
|---|---|
| `screenshots/sessions/live-01-tower.png` | 137 / 128 / 337 tiles |
| `screenshots/sessions/live-02-inject03-tower.png` | inject_03, SAFETY_PLC pin, tier-3 badge |
| `screenshots/sessions/live-03-sessions.png` | PLT-15 session table |
| `screenshots/sessions/live-04-sessions-scrolled.png` | Same table, full page |
| `screenshots/sessions/live-05-recommend.png` | Gate before packet |
| `screenshots/sessions/live-06-draft.png` | **ABSTAIN**, execute No |
