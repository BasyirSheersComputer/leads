## n8n Outreach Workflow Guide (CSV → Outlook)

This guide shows how to build two n8n workflows:
- Outreach Sender: reads your ICP CSV, sends personalized emails via Microsoft 365 (Outlook), and updates status back to CSV.
- Bounce Processor: checks mailbox for bounce messages and updates statuses.

Prerequisites
- Segment files exist with a header like: `unique_id,name,membership_number,state,category,rooms,address,phone,email,website,icp_segment,category_normalized,rooms_int`
- Files are generated in this folder (examples):
  - `Hotels_ICP_High_Value_Prospects_v2.csv`
  - `Hotels_ICP_Associate_Partners_v2.csv`
  - `Hotels_ICP_Mid_Tier_Prospects_v2.csv` (…and others)
- Close any CSVs in Excel while n8n writes to them (to prevent file locks).
- n8n has Microsoft 365 credentials configured.

---

## Workflow 1: Outreach Sender
Purpose: pick an ICP CSV, take the first 20 rows with status "New", send emails via Outlook every 15 seconds, update CSV statuses.

### Step 1: Trigger
- Add node: Manual Trigger (for on-demand) or Cron (to schedule).

### Step 2: Select ICP file
Option A: Hardcode a file with a Set node
- Add node: Set
  - Name: `Set ICP`
  - Add field `filePath` with value of one CSV, e.g. `D:\Priv\Leads\Hotels_ICP_High_Value_Prospects_v2.csv`

Option B: Choose by ICP name
- Add node: Set
  - Field: `icp` (e.g. `ICP_High_Value_Prospect`)
- Add node: Switch
  - Value to compare: `={{$json.icp}}`
  - Cases map to:
    - `ICP_High_Value_Prospect` → output sets `filePath = D:\\Priv\\Leads\\Hotels_ICP_High_Value_Prospects_v2.csv`
    - `ICP_Associate_Partner` → `...Associate_Partners_v2.csv`
    - etc.

### Step 3: Read the CSV
- Add node: Read Binary File
  - Path: `={{$json["filePath"]}}`
- Add node: Spreadsheet File
  - Operation: Read
  - Input: Binary Data → Property: `data`
  - File Format: CSV
  - Header row: true
  - Output: Items (each row as JSON)

Tip: Immediately after, add a Function to pack all rows into a single array for later merging:

```javascript
// Name: Wrap Full Rows
return [{ json: { rows: $input.all().map(i => i.json) } }];
```

### Step 4: Filter top 20 "New"
- Add node: Function
  - Code:
```javascript
const rows = $items("Wrap Full Rows")[0].json.rows;
const enriched = rows.map(r => ({
  ...r,
  status: r.status && r.status.trim() ? r.status : 'New'
}));
const newRows = enriched.filter(r => r.status === 'New').slice(0, 20);
return newRows.map(r => ({ json: r }));
```
- Add node: IF (Has Items?)
  - If no items, end the workflow.

### Step 5: Send one-by-one with delay
- Add node: Split In Batches
  - Batch size: 1
- Add node: Function (Validate + Prepare)
  - Code:
```javascript
const r = item.json;
const email = (r.email || '').trim();
const name = (r.name || '').trim();
const valid = /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email);
return [{ json: { ...r, email, name, valid } }];
```
- Add node: IF (Email valid?)
  - If false path → Set status to `Failed`, `last_result = Invalid email`, `last_contacted_at = {{$now}}` → connect to Accumulator (see Step 6).
  - If true path → Send Email.
- Add node: Microsoft 365 Outlook (Send Email)
  - To: `={{$json.email}}`
  - CC: `sugiyama-s1@almex-sta.com, matilda-a1@almex-sta.com`
  - Subject:
    - `={{`[Intro: ${$json.name}] [CID:${$json.unique_id}]`}}`
  - Body (HTML): include your template and signature; inject hotel name with `{{$json.name}}`.
    Example:
```html
<p>Dear {{$json.name}} Team,</p>
<p>[Personalized intro and value proposition...]</p>
<p>Best regards,<br/>[Your Name]<br/>[Your Title]<br/>[Your Company]</p>
```
  - Keep your signature content here; Outlook desktop signatures cannot be invoked programmatically.
- Add node: Set (Mark as Sent)
  - status: `Sent`
  - last_result: `Dispatched`
  - last_contacted_at: `={{$now}}`
  - outlook_message_id: `={{$json.messageId || ''}}`
- Add node: Wait
  - Duration: 15 seconds
- Connect Split In Batches → Next Batch until empty.

### Step 6: Accumulate updates
Goal: collect both sent and failed rows for merging back into the full dataset.
- Option A: Use Item Lists node to aggregate; or
- Option B: Use a Function to push into a single array (e.g., store in a paired branch).

Example Accumulator Function (connect both Sent and Failed paths here):
```javascript
const acc = $json.updates || [];
acc.push(item.json);
return [{ json: { updates: acc } }];
```

### Step 7: Merge with original rows
- After Split In Batches runs out (No Items Left output), merge updates into original full rows.
- Add node: Function (Merge by unique_id)
```javascript
const fullRows = $items('Wrap Full Rows')[0].json.rows;
const updatesArr = $items('Accumulator')[0].json.updates || [];
const byId = new Map(updatesArr.map(u => [u.unique_id, u]));
const merged = fullRows.map(r => byId.has(r.unique_id) ? { ...r, ...byId.get(r.unique_id) } : r);
return merged.map(r => ({ json: r }));
```

### Step 8: Write the CSV back
- Add node: Spreadsheet File (Write)
  - Operation: Write
  - File Format: CSV
  - Input: Items from Merge node
  - Header row: true
- Add node: Write Binary File
  - Path: `={{$json["filePath"]}}`

Note: If the file might be open in Excel, write to a new file name (e.g., `_v3.csv`) to avoid permission errors.

---

## Workflow 2: Bounce Processor
Purpose: detect bounces and set status to `Bounced`.

### Step 1: Trigger
- Add node: Cron (e.g., every 15 minutes) or Microsoft 365 Outlook Trigger (if available for new messages).

### Step 2: Fetch bounce emails
- Add node: Microsoft 365 Outlook (Search Emails) or IMAP Email
  - Filter for subjects like: `Undeliverable`, `Delivery has failed`, `Mail delivery failed`.
  - Time window: last 24–48 hours.

### Step 3: Extract CID and/or recipient
- Add node: Function
```javascript
const itemsOut = [];
for (const i of items) {
  const subj = i.json.subject || '';
  const match = subj.match(/CID:(HOTEL_\d{4})/);
  const uniqueId = match ? match[1] : null;
  const recipient = i.json.to && i.json.to[0] ? i.json.to[0].email : null;
  itemsOut.push({ json: { unique_id: uniqueId, recipient, bounce: true, bounce_subject: subj, received_at: i.json.date }});
}
return itemsOut;
```

### Step 4: Load target CSV
- Choose either the corresponding ICP CSV or the master merged file if you keep one.
- Add nodes: Read Binary File → Spreadsheet File (Read)

### Step 5: Merge bounce flags
- Add node: Function
```javascript
const bounces = items.map(i => i.json).filter(b => b.unique_id);
const rows = $items('Spreadsheet File')[0].json; // if needed, wrap like in Workflow 1
const map = new Map(bounces.map(b => [b.unique_id, b]));
const updated = rows.map(r => {
  if (map.has(r.unique_id)) {
    return {
      ...r,
      status: 'Bounced',
      last_result: 'Bounce',
      last_contacted_at: r.last_contacted_at || $now(),
    };
  }
  return r;
});
return updated.map(r => ({ json: r }));
```

### Step 6: Write CSV back
- Spreadsheet File (Write) → Write Binary File to the same path.

---

## Expressions and Templates
- To: `={{$json.email}}`
- CC: `sugiyama-s1@almex-sta.com, matilda-a1@almex-sta.com`
- Subject: `={{`[Intro: ${$json.name}] [CID:${$json.unique_id}]`}}`
- Body HTML: use `{{$json.name}}` wherever you would place [Hotel Name].

---

## Operational Tips
- Ensure CSVs are closed in Excel while workflows run.
- Run one ICP file per workflow execution to simplify file locking and auditing.
- Consider moving to Google Sheets or a database for multi-user concurrent safety and easier updates.
- Add a `do_not_contact` (true/false) column later and filter before sending.
- For retries: keep `Failed` rows separate from `Bounced`; you can requeue `Failed` after fixing email addresses.

---

## Optional: Master-First Approach
If you prefer a single source of truth:
1) Update a master CSV (e.g., `Hotels_ICP_Segmented_Master_v2.csv`) with statuses.
2) Periodically regenerate the per-ICP files by re-running `segment_hotels_icp.py`.




