STATUS_CHOICES = (
    ("Pending", "Pending"),
    ("In Review", "In Review"),
    ("Verified", "Verified"),
    ("Rejected", "Rejected"),
)


class StatusChoice:
    PENDING = "Pending"
    IN_REVIEW = "In Review"
    VERIFIED = "Verified"
    REJECTED = "Rejected"

    CHOICES = (
        (PENDING, PENDING),
        (IN_REVIEW, IN_REVIEW),
        (VERIFIED, VERIFIED),
        (REJECTED, REJECTED),
    )
