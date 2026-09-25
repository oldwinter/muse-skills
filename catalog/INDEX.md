# 技能索引

由 `python3 scripts/build_catalog.py` 从 `skills/` 生成。不要手改。

## 工作流与记忆

| 技能 | 是否进 prompt | manifest | eval | 说明 |
| --- | --- | --- | --- | --- |
| [forget](../skills/forget/SKILL.md) | 是 |  |  | Remove a personal fact, preference, relationship detail, topic, or prior event from Muse's active memory and stop existing copies or automations from bringing it back. Use for explicit requests such as 'forget that', 'don't remember this about me', or 'remove that from your memory'. Do not use when 'forget it' merely means cancel the current task. |
| [goals](../skills/goals/SKILL.md) | 是 |  |  | Guidance for helping users create and accomplish goals. Read it before you create a goal for the user when no goal-creation contract is in context, and whenever you help with an existing goal. A Goals-tab creation turn already carries that contract and does not need this skill. |
| [muse_db](../skills/muse_db/SKILL.md) |  |  |  | Inspect database-backed Muse records for diagnosis and cross-table tracing when purpose-built product tools do not expose the needed state. |
| [self-awareness](../skills/self-awareness/SKILL.md) |  |  |  | Ground self-referential answers in the agent's actual filesystem. Use when the user asks who the agent is, what it can do, what it knows, what it remembers, what it has built, what services are connected, or what rules it follows. |
| [skill-creator](../skills/skill-creator/SKILL.md) | 是 |  |  | Create or update a workspace skill: its description, structure, instructions, and supporting files. |
| [wide-research](../skills/wide-research/SKILL.md) |  |  |  | Use when the user needs broad parallel research across many independent inputs with a shared output schema. |

## 文档、表格与产物验收

| 技能 | 是否进 prompt | manifest | eval | 说明 |
| --- | --- | --- | --- | --- |
| [artifacts/document](../skills/artifacts/document/SKILL.md) |  |  |  | Create, read, edit, or manipulate Word documents (.docx) and Word templates (.dotx). Use whenever a build task's artifact kind is document with the default docx output, or the task mentions a Word doc, .docx, or .dotx, extracts or reorganizes content from one, inserts or replaces images, does find-and-replace in one, or works with tracked changes (redlines) or comments. Covers python-docx generation, raw OOXML editing of existing files, document structure and formatting, and render verification. Not for PDFs, spreadsheets, or Google Docs. |
| [artifacts/markdown](../skills/artifacts/markdown/SKILL.md) |  |  |  | Build or revise a plain markdown file (md) deliverable such as notes, a README, meeting minutes, documentation, or text the user will edit or paste elsewhere. Use whenever a build task's artifact kind is markdown. Covers markdown formatting conventions and read-back verification. |
| [artifacts/pdf](../skills/artifacts/pdf/SKILL.md) |  |  |  | Build, revise, or manipulate a fixed-layout PDF (report, guide, one-pager, printable document). Use whenever a build task's artifact kind is pdf, a document build's output format is pdf, or the task reads, merges, splits, crops, or fills an existing PDF, including fillable AcroForms. Covers authoring the print-CSS HTML source, rendering, the geometry and validation gates, existing-PDF manipulation and form filling, and delivery under workspace/your_files. |
| [artifacts/presentation](../skills/artifacts/presentation/SKILL.md) |  |  |  | Build or revise a slide deck (pptx by default; pdf or html on request). Use whenever a build task's artifact kind is presentation, or the user asks for a deck, slides, or a presentation. Covers per-slide HTML authoring, the StylePlan theme system, font embedding, deck assembly, render gates, and the PPTX export. |
| [artifacts/spreadsheet](../skills/artifacts/spreadsheet/SKILL.md) |  |  |  | Create, read, edit, fix, or clean spreadsheet files (.xlsx, .xlsm, .csv, .tsv). Use whenever a build task's artifact kind is spreadsheet, or the task names a spreadsheet file and wants something done to it or produced from it, including restructuring messy tabular data into a proper workbook. Covers openpyxl generation, formulas and recalculation, editing existing workbooks, and the validation gates. Not for tasks whose deliverable is a document, report, or web page that merely contains a table. |
| [artifacts/testing](../skills/artifacts/testing/SKILL.md) |  |  |  | Verify an artifact before delivering it - file deliverables (pdf, pptx, docx, xlsx, csv) and web artifacts alike. Use whenever a build is about to return a link, or a build task asks for validation, QA, or a visual check. Covers the per-kind gate scripts, render-and-look verification, and leftover-placeholder scanning. |

## 旅行、地点与预订

| 技能 | 是否进 prompt | manifest | eval | 说明 |
| --- | --- | --- | --- | --- |
| [booking](../skills/booking/SKILL.md) | 是 |  | 有 | Primary entry point for direct flight, hotel, restaurant, or event-ticket transactions and for bounded live availability checks delegated by Travel Planning. Always use before provider-specific skills or browser work when the user asks to find live availability or prices, compare bookable options, book, or continue an active booking. Do not use for trip planning itself, broad inspiration, opening hours, schedules, flight status, or other factual questions without transaction intent. |
| [duffel](../skills/duffel/SKILL.md) |  | 有 | 有 | Use Duffel to search, book, pay for, or manage flights. Use Duffel to monitor an already booked flight's fare when the user directly asks for ongoing price monitoring. |
| [flightaware](../skills/flightaware/SKILL.md) | 是 | 有 | 有 | Use for questions about a specific flight’s departure or arrival time, including “when’s my flight?” and confirmation of remembered times, plus flight status, delays, and cancellations. Verify the exact dated flight before answering; memory identifies the itinerary but does not verify its current schedule. Use FlightAware to monitor operational changes for an upcoming booked flight when the user directly asks for ongoing monitoring. |
| [opentable](../skills/opentable/SKILL.md) |  | 有 | 有 | Find restaurants on OpenTable, check availability, and make, change, or cancel reservations. Use for restaurant booking and live reservation data. |
| [places-search](../skills/places-search/SKILL.md) |  |  | 有 | Find, compare, and share details on physical places near the user or in a specified area, including restaurants, cafes, bars, hotels, parks, attractions, shops, and businesses with local services. Not for itineraries, choosing a city or region, dated events or showtimes, or directions. |
| [ticketmaster](../skills/ticketmaster/SKILL.md) |  | 有 |  | Search Ticketmaster events and seats with pricing. Returns Buy-now links to Ticketmaster checkout; it cannot complete a purchase itself. |
| [travel-planning](../skills/travel-planning/SKILL.md) | 是 |  | 有 | Use this skill when an active or proposed trip needs planning, logistics, feasibility, entry or transit checks, itinerary work, or investigation of an airport process, immigration, ground transport, a transfer, or fast-track service, even for a narrow question with no booking intent. Route a bounded flight, hotel, restaurant, event, or other item ready for live availability or booking directly to Booking. Skip this skill for a stable travel fact alone or flight status. |

## 办公、邮箱与知识库

| 技能 | 是否进 prompt | manifest | eval | 说明 |
| --- | --- | --- | --- | --- |
| [calendly](../skills/calendly/SKILL.md) |  | 有 |  | View Calendly events and event types, and manage scheduling data using the Calendly CLI. |
| [gmail](../skills/gmail/SKILL.md) | 是 | 有 | 有 | Work with the user's Gmail: search, read threads, draft, send, reply, forward, unsubscribe from mailing lists, manage labels, and open attachments. |
| [google-calendar](../skills/google-calendar/SKILL.md) | 是 | 有 | 有 | Work with the user's Google Calendar: agenda views, event details, and scheduling changes. |
| [google-contacts](../skills/google-contacts/SKILL.md) |  | 有 | 有 | Search, view, create, update, and delete the user's Google Contacts. |
| [google-docs](../skills/google-docs/SKILL.md) |  | 有 |  | Read, create, and edit the user's Google Docs. |
| [google-drive](../skills/google-drive/SKILL.md) |  | 有 | 有 | Work with the user's Google Drive: files, folders, uploads, downloads, and sharing. |
| [google-forms](../skills/google-forms/SKILL.md) |  | 有 |  | Read, create, and update the user's Google Forms, and read responses. |
| [google-sheets](../skills/google-sheets/SKILL.md) |  | 有 |  | Read, write, and manage the user's Google Sheets. |
| [google-slides](../skills/google-slides/SKILL.md) |  | 有 |  | Read, create, and edit the user's Google Slides presentations. |
| [google-tasks](../skills/google-tasks/SKILL.md) |  | 有 | 有 | Manage the user's Google Tasks: lists, task details, creation, updates, and completion. |
| [granola](../skills/granola/SKILL.md) |  | 有 |  | Search and read Granola meeting notes and transcripts through Granola's OAuth-backed MCP server. |
| [muse-mail](../skills/muse-mail/SKILL.md) | 是 |  |  | Manage Muse Mail. Use this skill for Muse Mail, mail forwarded to the mailbox, or the main agent's name plus mail. Route the user's inbox and generic sends to the user's account. Check connected accounts for broad mail questions. |
| [notion](../skills/notion/SKILL.md) |  | 有 |  | Search, read, create, and update Notion pages via the Notion MCP. |
| [outlook-calendar](../skills/outlook-calendar/SKILL.md) |  | 有 |  | View, create, update, and delete events in the user's Outlook Calendar. |
| [outlook-contacts](../skills/outlook-contacts/SKILL.md) |  | 有 |  | List, search, create, update, and delete contacts in the user's Outlook account. |
| [outlook-mail](../skills/outlook-mail/SKILL.md) |  | 有 |  | Read, search, send, reply to, and delete messages in the user's Outlook Mail. |

## 社交与消息

| 技能 | 是否进 prompt | manifest | eval | 说明 |
| --- | --- | --- | --- | --- |
| [facebook-cli](../skills/facebook-cli/SKILL.md) | 是 | 有 |  | Use when the user provides a Facebook URL or asks to read personal posts, comments, reactions, friends, timelines, profiles, stories, feeds, groups, events, or saved items, or to discover public events happening near a place, nearby, or in a local area on a date, or to create, edit, publish, or delete their own Marketplace listings. To find, browse, or buy Marketplace listings, use shopping instead. |
| [instagram](../skills/instagram/SKILL.md) | 是 | 有 |  | Answer questions about Instagram posts and reels, including links the user shares, using post context, media descriptions, and visual inspection when needed. Read profiles, followers, posts, comments, likes, stories, feed, saved content, and insights. Manage feed interests and profile details, and publish stories, reels, posts, or carousels when requested. |
| [instagram-messages](../skills/instagram-messages/SKILL.md) |  | 有 |  | Use this to interact with the user's Instagram messages. Read inboxes, threads, top recipients, filtered inbox views, DM search results, and send messages through `instagram-messages-cli`. |
| [messenger](../skills/messenger/SKILL.md) | 是 | 有 |  | Work with the user's Messenger account: read call history; read and search contacts; read, search, and summarize conversations; send, react to, unsend, or edit messages; and message Marketplace listing threads. |
| [threads](../skills/threads/SKILL.md) | 是 | 有 |  | Read and manage the user's Threads account: profile, posts, feed, saved posts, activity, insights, social graph, search, trends, and a specific post by URL or ID. Can tune feed ranking and publish posts on request. |
| [threads-messages](../skills/threads-messages/SKILL.md) |  | 有 |  | Use this to interact with the user's Threads messages: read inboxes and message threads, and send messages through `threads-messages-cli`. |

## 购物与金融数据

| 技能 | 是否进 prompt | manifest | eval | 说明 |
| --- | --- | --- | --- | --- |
| [plaid](../skills/plaid/SKILL.md) | 是 | 有 | 有 | Use to connect Plaid and read linked financial accounts: metadata, balances, transactions, recurring transactions, liabilities, and investments. |
| [printify](../skills/printify/SKILL.md) |  | 有 |  | Use Printify to browse catalog data, manage shops and products, and review or create orders. |
| [shopping](../skills/shopping/SKILL.md) | 是 |  |  | Use for any product or shopping question: find, reverse image search, shopping Instagram/Marketplace links, buy, compare, or evaluate real products with prices, images, and product page URLs, including buying or browsing Facebook Marketplace listings. Use when presenting shopping search results from any source. For shopping intent, load this skill first before any other skills. |

## 健康与健身

| 技能 | 是否进 prompt | manifest | eval | 说明 |
| --- | --- | --- | --- | --- |
| [apple-healthkit](../skills/apple-healthkit/SKILL.md) | 是 | 有 |  | The user's synced Apple Health (HealthKit) data: daily metrics (steps, distance, calories, heart rate, HRV, VO2max), sleep sessions (stages, quality, efficiency), and workouts. |
| [function-health](../skills/function-health/SKILL.md) |  | 有 |  | Retrieve lab biomarker results and clinician notes from Function Health. |
| [google-health-connect](../skills/google-health-connect/SKILL.md) | 是 | 有 |  | The user's synced Google Health Connect data from their Android device: daily metrics (steps, distance, calories, heart rate, HRV, VO2max), sleep sessions (stages, quality, efficiency), and workouts. |
| [healthex](../skills/healthex/SKILL.md) |  | 有 |  | Use to connect HealthEx and ask questions about your medications, lab results, and other health records. |
| [peloton](../skills/peloton/SKILL.md) |  | 有 |  | Connect to Peloton to browse fitness classes, check schedules, and book workouts. |
| [withings](../skills/withings/SKILL.md) |  | 有 |  | Use when linking Withings or reading Withings body measurements, activity, sleep, workout, heart, and intraday data. |

## 图像、音频与视频

| 技能 | 是否进 prompt | manifest | eval | 说明 |
| --- | --- | --- | --- | --- |
| [generate_podcast](../skills/generate_podcast/SKILL.md) | 是 |  |  | Compose and deliver audio content: a podcast episode, briefing, or narrated summary, with one or more voices, as an MP3. For reading supplied text aloud verbatim, use tts. |
| [image-search](../skills/image-search/SKILL.md) | 是 |  |  | Search the web by text query for image URLs and source pages for feeds, artifacts, and visual references. Does not identify a supplied image or person. |
| [magic-moment](../skills/magic-moment/SKILL.md) |  |  |  | Make a "magic moment" video — turn a creator's talking-head recording into a vertical video preserving the source narration where their Muse story replays through artifacts and brief exchanges synced to their voiceover — bubbles, typing, emoji reactions, real widgets and pages, message sounds, closing Muse lockup finisher. Use whenever a user with talking-head or selfie footage wants it turned into a shareable clip of their Muse story — "make a magic moment", "turn this video of me into...", "add the chat over my video", "retell what Muse did for me" — even if they never say the words "magic moment". |
| [media-library](../skills/media-library/SKILL.md) | 是 |  |  | Search and inspect the user's photo library, including connected device galleries. Use for photo requests and whenever a photo could ground or personalize a response; lookups of uploaded photos are cheap, so check opportunistically and move on if nothing fits. |
| [spotify](../skills/spotify/SKILL.md) | 是 | 有 |  | Discover, search, and manage Spotify music, podcasts, and playlists, including deleting shows or episodes you created with Save to Spotify. |
| [tts](../skills/tts/SKILL.md) | 是 | 有 |  | Turn supplied text into spoken audio, single or multi-speaker. For composed audio content (a podcast, briefing, or narrated summary), use podcast. |
| [voice-design](../skills/voice-design/SKILL.md) |  |  |  | Choose or design a new speaking voice when the user asks for a new, different, custom, invented, or generated voice. |
| [voice-selector](../skills/voice-selector/SKILL.md) |  |  |  | Provides the static system voice catalog used by Jarvis. It does not define a user-facing workflow. |

## 设备、通信与网络

| 技能 | 是否进 prompt | manifest | eval | 说明 |
| --- | --- | --- | --- | --- |
| [device-data](../skills/device-data/SKILL.md) | 是 |  |  | Read cached contacts and calendar events from Muse storage. Delete Muse's local copy of either source without modifying paired devices. |
| [philips-hue](../skills/philips-hue/SKILL.md) |  | 有 |  | Control Philips Hue smart lights, rooms, scenes, and devices via the Hue Remote API v2. |
| [tailscale](../skills/tailscale/SKILL.md) |  |  |  | Set up Muse's built-in Tailscale connector, join a tailnet or Headscale network, check status, and reach private machines through the TCP tunnel proxy. Read for Tailscale, VPN, MagicDNS, network egress, exit-node, or browser routing questions and supported limits. |
| [tessie](../skills/tessie/SKILL.md) |  | 有 |  | Monitor a Tesla vehicle, inspect live state, and run explicit Tessie command endpoints. |
| [wearable-device-skills](../skills/wearable-device-skills/SKILL.md) | 是 |  |  | Use when the user asks to discover, inspect, or invoke an agentic capability dynamically published by a paired phone or wearable, including device controls, app actions, camera or media actions, and smart-home actions. |
| [wearables-comms](../skills/wearables-comms/SKILL.md) | 是 |  |  | Required for every call or text-message request originating on a wearable: resolve named recipients from synced device contacts and invoke the originating wearable, not a paired phone. |

## Muse 产品操作

| 技能 | 是否进 prompt | manifest | eval | 说明 |
| --- | --- | --- | --- | --- |
| [muse-early-access](../skills/muse-early-access/SKILL.md) | 是 |  |  | Use for questions about Muse's general early access program, requests to join it, checking or withdrawing a join request, and admission updates. |
| [muse-feedback](../skills/muse-feedback/SKILL.md) | 是 |  |  | Use for feedback and feature requests to the Muse team. Whenever your response tells the user you can't do a specific thing they wanted, or accepts them giving up on one, offer once to file feedback in that response. This covers missing integrations you can't do yourself, capabilities you lack, and tasks that keep failing at a specific point. File only on their go-ahead. Also use when asked to send, view, check, or withdraw feedback. |
| [share-ideas](../skills/share-ideas/SKILL.md) | 是 |  |  | Publish a reusable native Muse Idea with idea.share when the user explicitly asks to share or publish an Idea or asks for a muse.ai/ideas link. Never offer it unprompted. Not for pages or write-ups, sending a result to someone, social posts, or sharing an artifact. |
| [subscription-status](../skills/subscription-status/SKILL.md) | 是 |  |  | Answer questions about the user's Muse subscription, account or plan, current tier, usage, credits, remaining balance, quota, usage or rate limits, billing, reset timing, available subscription tiers, plan prices and costs, upgrades, or the subscription product catalog. |

## 别名

| 入口 | 指向 |
| --- | --- |
| `facebook` | `facebook-cli` |
| `meta-threads` | `threads` |
| `podcast` | `generate_podcast` |
| `voice-calls` | `voice-selector` |
