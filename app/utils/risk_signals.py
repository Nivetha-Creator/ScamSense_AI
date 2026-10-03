import re


URGENCY_WORDS = [
    "urgent",
    "immediately",
    "act now",
    "act immediately",
    "last chance",
    "expires today",
    "within 24 hours",
    "within 48 hours",
    "limited time",
    "do it now",
    "respond immediately",
    "account will be blocked",
    "account will be suspended"
]


MONEY_WORDS = [
    "money",
    "payment",
    "pay",
    "paid",
    "cash",
    "prize",
    "reward",
    "refund",
    "lottery",
    "winner",
    "won",
    "₹",
    "rs",
    "inr",
    "rupees",
    "amount",
    "fee",
    "charge",
    "deposit",
    "transfer"
]


CREDENTIAL_WORDS = [
    "password",
    "otp",
    "pin",
    "cvv",
    "card number",
    "credit card",
    "debit card",
    "bank details",
    "account details",
    "login",
    "username",
    "verify your account",
    "verification code"
]


THREAT_WORDS = [
    "blocked",
    "suspended",
    "legal action",
    "police",
    "penalty",
    "fine",
    "arrest",
    "court",
    "case will be filed",
    "account will be closed"
]


DELIVERY_WORDS = [
    "delivery",
    "package",
    "parcel",
    "courier",
    "shipment",
    "shipping",
    "customs",
    "custom duty",
    "delivery fee",
    "delivery charge"
]


TAX_WORDS = [
    "tax",
    "tax payment",
    "customs tax",
    "customs fee",
    "gst",
    "gst payment",
    "import tax",
    "clearance fee",
    "processing fee"
]


LINK_PATTERN = r"https?://\S+|www\.\S+"


def find_matches(text, keywords):
    text_lower = text.lower()

    return [
        word
        for word in keywords
        if word.lower() in text_lower
    ]


def detect_risk_signals(text):

    urgency = find_matches(
        text,
        URGENCY_WORDS
    )

    money = find_matches(
        text,
        MONEY_WORDS
    )

    credentials = find_matches(
        text,
        CREDENTIAL_WORDS
    )

    threats = find_matches(
        text,
        THREAT_WORDS
    )

    delivery = find_matches(
        text,
        DELIVERY_WORDS
    )

    tax = find_matches(
        text,
        TAX_WORDS
    )

    links = re.findall(
        LINK_PATTERN,
        text,
        re.IGNORECASE
    )

    return {
        "urgency": urgency,
        "money_related": money,
        "credential_requests": credentials,
        "threats": threats,
        "delivery_related": delivery,
        "tax_or_fee_related": tax,
        "links": links
    }