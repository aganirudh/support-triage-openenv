# === my_env/tasks.py ===
"""Pre-defined support tickets grouped by difficulty level.

Each level contains 5 tickets. Every ticket includes metadata fields used for
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
            "body": "Hi, I just received my monthly invoice and the total is $149 instead of the $99 I was quoted. Can you please correct this?",
            "tier": "free",
            "sentiment": "neutral",
            "expected": {
                "category": "billing",
                "priority": "medium",
                "escalate": False,
                "response_hint": "Apologize and confirm invoice review for correct amount.",
            },
        },
        {
            "ticket_id": "EASY-002",
            "subject": "Cannot log in to my account",
            "body": "I keep getting an 'invalid password' error even after resetting my password twice. I need access for reports.",
            "tier": "pro",
            "sentiment": "negative",
            "expected": {
                "category": "technical",
                "priority": "high",
                "escalate": True,
                "response_hint": "Guide through reset and escalate to tech support.",
            },
        },
        {
            "ticket_id": "EASY-003",
            "subject": "How do I export data to CSV?",
            "body": "I would like to export my dashboard data to a CSV file but I cannot find the option anywhere.",
            "tier": "free",
            "sentiment": "positive",
            "expected": {
                "category": "general",
                "priority": "low",
                "escalate": False,
                "response_hint": "Provide step-by-step export instructions for CSV.",
            },
        },
        {
            "ticket_id": "EASY-004",
            "subject": "Update my credit card",
            "body": "My card expired and I need to update my billing info so my subscription doesn't get cancelled.",
            "tier": "pro",
            "sentiment": "neutral",
            "expected": {
                "category": "billing",
                "priority": "medium",
                "escalate": False,
                "response_hint": "Point to the billing settings page for card update.",
            },
        },
        {
            "ticket_id": "EASY-005",
            "subject": "Delete my account",
            "body": "I no longer need this service. Please delete my account and all associated data.",
            "tier": "free",
            "sentiment": "neutral",
            "expected": {
                "category": "general",
                "priority": "low",
                "escalate": False,
                "response_hint": "Explain account deletion process and confirm request.",
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
            "body": "Your mobile app has been crashing every time I open the reports page. Also, I noticed my last two invoices were higher.",
            "tier": "pro",
            "sentiment": "frustrated",
            "expected": {
                "category": "technical",
                "priority": "high",
                "escalate": True,
                "response_hint": "Acknowledge crashes and billing discrepancy. Escalate to engineering.",
            },
        },
        {
            "ticket_id": "MED-002",
            "subject": "Feature request plus a complaint",
            "body": "I love the product but search is slow. Also, your documentation API endpoint listed returns a 404.",
            "tier": "pro",
            "sentiment": "neutral",
            "expected": {
                "category": "technical",
                "priority": "medium",
                "escalate": False,
                "response_hint": "Log feature request for search and acknowledge documentation bug.",
            },
        },
        {
            "ticket_id": "MED-003",
            "subject": "Suspicious login attempt",
            "body": "I received an email saying someone tried to log in from another country. I changed my password but I am worried.",
            "tier": "pro",
            "sentiment": "negative",
            "expected": {
                "category": "security",
                "priority": "high",
                "escalate": True,
                "response_hint": "Review audit logs and confirm security status. Suggest 2FA.",
            },
        },
        {
            "ticket_id": "MED-004",
            "subject": "API performance issues on production",
            "body": "We are getting intermittent 503 errors on the /v1/search endpoint. It happens about 5% of the time.",
            "tier": "enterprise",
            "sentiment": "negative",
            "expected": {
                "category": "technical",
                "priority": "high",
                "escalate": True,
                "response_hint": "Acknowledge 503 errors and escalate to site reliability engineering.",
            },
        },
        {
            "ticket_id": "MED-005",
            "subject": "Request for bulk discount on 50 seats",
            "body": "We are looking to expand our team from 10 to 60 users. Can we get a bulk discount for the next year?",
            "tier": "pro",
            "sentiment": "positive",
            "expected": {
                "category": "billing",
                "priority": "medium",
                "escalate": True,
                "response_hint": "Escalate to sales for discount negotiation and seat expansion.",
            },
        },
    ],
    # ------------------------------------------------------------------
    # HARD — enterprise, jargon, SLA, escalation, multi-issue, frustrated
    # ------------------------------------------------------------------
    "hard": [
        {
            "ticket_id": "HARD-001",
            "subject": "SSO outage affecting 200 users",
            "body": "Our entire engineering team is locked out of SSO since your 3 AM deployment. This is an SLA breach. We need P0 escalation.",
            "tier": "enterprise",
            "sentiment": "frustrated",
            "expected": {
                "category": "security",
                "priority": "critical",
                "escalate": True,
                "response_hint": "Immediate P0 escalation for SSO outage and SLA breach acknowledgment.",
            },
        },
        {
            "ticket_id": "HARD-002",
            "subject": "Data discrepancy in compliance audit",
            "body": "During our quarterly SOC-2 audit we found missing records. We need a corrected export within 48 hours or legal action.",
            "tier": "enterprise",
            "sentiment": "frustrated",
            "expected": {
                "category": "technical",
                "priority": "critical",
                "escalate": True,
                "response_hint": "Urgent escalation for compliance data loss. Provide corrected export timeline.",
            },
        },
        {
            "ticket_id": "HARD-003",
            "subject": "Billing error compounded by rate-limits",
            "body": "We are rate-limited at 100 req/s instead of 5000. Also, we were billed for overage charges in error.",
            "tier": "enterprise",
            "sentiment": "frustrated",
            "expected": {
                "category": "escalation",
                "priority": "critical",
                "escalate": True,
                "response_hint": "Escalate to engineering for rate-limit fix and billing for credits.",
            },
        },
        {
            "ticket_id": "HARD-004",
            "subject": "GDPR Right to Be Forgotten request for 500+ users",
            "body": "We need to process a bulk GDPR deletion for 524 user accounts. This must be completed and documented within 30 days.",
            "tier": "enterprise",
            "sentiment": "neutral",
            "expected": {
                "category": "security",
                "priority": "high",
                "escalate": True,
                "response_hint": "Escalate to legal and compliance team for bulk GDPR processing.",
            },
        },
        {
            "ticket_id": "HARD-005",
            "subject": "Zero-day vulnerability disclosure",
            "body": "I found a way to bypass your authentication using a crafted JWT. Attaching proof of concept. Requesting bug bounty info.",
            "tier": "free",
            "sentiment": "neutral",
            "expected": {
                "category": "security",
                "priority": "critical",
                "escalate": True,
                "response_hint": "Immediate escalation to security engineering for zero-day triage.",
            },
        },
    ],
}