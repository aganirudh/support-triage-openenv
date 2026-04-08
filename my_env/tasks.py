# === my_env/tasks.py ===
"""Pre-defined support tickets grouped by difficulty level.

Each level contains 3 tickets. Every ticket includes metadata fields used for
observation construction **and** an ``expected`` dict used by the grader.
"""

TASKS: dict[str, list[dict]] = {
    # ------------------------------------------------------------------
    # EASY — clear single-issue, obvious category
    # ------------------------------------------------------------------
    "easy": [
        {
            "ticket_id": "EASY-001",
            "subject": "Invoice shows wrong amount",
            "body": (
                "Hi, I just received my monthly invoice and the total is $149 "
                "instead of the $99 I was quoted when I signed up last month. "
                "Can you please correct this?"
            ),
            "tier": "free",
            "sentiment": "neutral",
            "expected": {
                "category": "billing",
                "priority": "medium",
                "response_hint": "Apologize and confirm invoice review.",
            },
        },
        {
            "ticket_id": "EASY-002",
            "subject": "Cannot log in to my account",
            "body": (
                "I keep getting an 'invalid password' error even after "
                "resetting my password twice. I need access to download my "
                "reports before end of day."
            ),
            "tier": "pro",
            "sentiment": "negative",
            "expected": {
                "category": "technical",
                "priority": "high",
                "response_hint": "Guide through password reset and escalate if needed.",
            },
        },
        {
            "ticket_id": "EASY-003",
            "subject": "How do I export data to CSV?",
            "body": (
                "I would like to export my dashboard data to a CSV file but "
                "I cannot find the option anywhere. Could you point me in the "
                "right direction?"
            ),
            "tier": "free",
            "sentiment": "positive",
            "expected": {
                "category": "general",
                "priority": "low",
                "response_hint": "Provide step-by-step export instructions.",
            },
        },
    ],
    # ------------------------------------------------------------------
    # MEDIUM — ambiguous category, mixed sentiment, judgment needed
    # ------------------------------------------------------------------
    "medium": [
        {
            "ticket_id": "MED-001",
            "subject": "App crashes and I was also overcharged",
            "body": (
                "Your mobile app has been crashing every time I open the "
                "reports page — but only on weekends. Also, I noticed my "
                "last two invoices were each $20 higher than expected. "
                "Please fix both issues."
            ),
            "tier": "pro",
            "sentiment": "frustrated",
            "expected": {
                "category": "technical",
                "priority": "high",
                "response_hint": "Acknowledge both issues; prioritize the crash, flag billing.",
            },
        },
        {
            "ticket_id": "MED-002",
            "subject": "Feature request plus a complaint",
            "body": (
                "I love the product overall but the search is painfully slow "
                "on large datasets. Also, your documentation is outdated — the "
                "API endpoint listed returns a 404. Can you update the docs "
                "and improve search performance?"
            ),
            "tier": "pro",
            "sentiment": "neutral",
            "expected": {
                "category": "technical",
                "priority": "medium",
                "response_hint": "Log feature request, acknowledge docs bug, provide workaround.",
            },
        },
        {
            "ticket_id": "MED-003",
            "subject": "Suspicious login attempt notification",
            "body": (
                "I received an email saying someone tried to log in from an "
                "IP in another country. I did not travel recently. I changed "
                "my password but I am worried my data might have been accessed. "
                "Can you check the audit logs?"
            ),
            "tier": "pro",
            "sentiment": "negative",
            "expected": {
                "category": "security",
                "priority": "high",
                "response_hint": "Confirm no breach via audit logs, recommend 2FA.",
            },
        },
    ],
    # ------------------------------------------------------------------
    # HARD — enterprise, jargon, SLA, escalation, multi-issue, frustrated
    # ------------------------------------------------------------------
    "hard": [
        {
            "ticket_id": "HARD-001",
            "subject": "SSO outage affecting 200 users since 3 AM deployment",
            "body": (
                "Our entire engineering team of 200 people has been locked "
                "out of SSO since your 3 AM deployment last night. This is a "
                "direct breach of our 99.95% uptime SLA. We need P0 "
                "escalation NOW and a root-cause analysis within 4 hours. "
                "Every hour of downtime costs us roughly $15,000 in lost "
                "productivity."
            ),
            "tier": "enterprise",
            "sentiment": "frustrated",
            "expected": {
                "category": "security",
                "priority": "critical",
                "response_hint": "Immediate P0 escalation, acknowledge SLA breach, provide ETA.",
            },
        },
        {
            "ticket_id": "HARD-002",
            "subject": "Data discrepancy in compliance audit export",
            "body": (
                "During our quarterly SOC-2 audit we discovered that the "
                "compliance export from your platform is missing 37 records "
                "from the month of February. Our auditor flagged this as a "
                "material finding. We need a corrected export ASAP and a "
                "written explanation of how the data loss occurred. If this "
                "is not resolved within 48 hours we will need to involve "
                "legal counsel."
            ),
            "tier": "enterprise",
            "sentiment": "frustrated",
            "expected": {
                "category": "technical",
                "priority": "critical",
                "response_hint": "Escalate to engineering, provide interim export, draft RCA.",
            },
        },
        {
            "ticket_id": "HARD-003",
            "subject": "Billing error compounded by API rate-limit failures",
            "body": (
                "We are on the Enterprise Unlimited plan but our API calls "
                "are being rate-limited at 100 req/s instead of the "
                "contracted 5000 req/s. This has caused three production "
                "incidents this week. On top of that, we were billed for "
                "overage charges that should not exist under our contract. "
                "I need immediate rate-limit correction, a billing credit, "
                "and an incident report for each outage."
            ),
            "tier": "enterprise",
            "sentiment": "frustrated",
            "expected": {
                "category": "escalation",
                "priority": "critical",
                "response_hint": "Escalate to engineering and billing, credit account, provide incident reports.",
            },
        },
    ],
}