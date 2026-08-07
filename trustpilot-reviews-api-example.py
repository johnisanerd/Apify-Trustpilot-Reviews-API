"""
Trustpilot Reviews API: A Quick Start Example
See more at: https://apify.com/johnvc/trustpilot-reviews-api?fpr=9n7kx3
Input schema: https://apify.com/johnvc/trustpilot-reviews-api/input-schema?fpr=9n7kx3

This script shows how to call the Trustpilot Reviews API on Apify from Python and
read its structured JSON output. It keeps the run tiny so your first call stays
cheap, then prints the fields that matter for reputation monitoring.

Every row carries the review text and star rating, the separate date of experience,
the verified flag, any reply the business posted, and the company's overall rating
with its full star breakdown.

Get your free Apify API key at: https://apify.com?fpr=9n7kx3
"""

import os

from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()

# Initialize the Apify client with your API token (read from .env)
client = ApifyClient(os.getenv("APIFY_API_TOKEN"))

# Build the Actor input.
# Inputs are kept small (one company URL, maxReviewsPerCompany=3) so this first run
# is inexpensive. Billing is per review returned, and the cap is applied at the
# source, so nothing beyond the cap is collected or billed. Raise these once you
# have your own API key and know your budget.
run_input = {
    # Company review-page URLs. A bare domain such as "example.com" also works.
    # Up to 200 companies per run; add more URLs to compare a competitive set.
    "companyUrls": ["https://www.trustpilot.com/review/www.dugood.org"],
    # Your cost control: reviews returned per company, 1 to 1000.
    "maxReviewsPerCompany": 3,
    # Optional: narrow to a recent window, which is what turns a one-off pull into
    # an incremental monitoring job. Verified working values are relative windows,
    # for example "Last 30 days" or "Last 6 months". Leave the key out for all reviews.
    # "datePosted": "Last 30 days",
}

# Run the Actor and wait for it to finish
run = client.actor("johnvc/trustpilot-reviews-api").call(run_input=run_input)
if run is None:
    raise SystemExit("The Actor run did not return a result.")

# Read structured results from the run's default dataset.
# (apify-client 3.x returns a Run object; use .default_dataset_id, not run["..."])
items = list(client.dataset(run.default_dataset_id).iterate_items())
print(f"Returned {len(items)} row(s).\n")

# Show a few key fields from each row.
# Rows come in two shapes, distinguished by result_type:
#   "review" - one collected review, with its company context attached
#   "error"  - a company URL that returned nothing, with a plain-language reason
for item in items:
    result_type = item.get("result_type")

    if result_type == "review":
        print(f"[review] {item.get('companyName')} - {item.get('reviewRating')} stars")
        print(f"  Title:      {item.get('reviewTitle')}")
        print(f"  Text:       {(item.get('reviewContent') or '')[:160]}")
        print(f"  Posted:     {item.get('reviewDate')}")
        print(f"  Experience: {item.get('dateOfExperience')}")
        print(f"  Reviewer:   {item.get('reviewerName')} ({item.get('reviewerLocation')}), "
              f"{item.get('reviewerTotalReviews')} reviews total")
        print(f"  Verified:   {item.get('isVerifiedReview')} | "
              f"useful votes: {item.get('reviewUsefulCount')}")

        # A reply is the engagement signal that matters for reputation work.
        # An empty list here plus a low reviewRating is your unanswered-complaint list.
        replies = item.get("reviewReplies") or []
        print(f"  Replies:    {len(replies)}")

        # Company-level context rides along on every review row.
        print(f"  Company:    {item.get('companyOverallRating')} "
              f"({item.get('companyRatingLabel')}) across "
              f"{item.get('companyTotalReviews')} reviews | "
              f"category: {item.get('companyCategory')}")

        # Star breakdown carries both an absolute count and a percentage share per
        # level, so you can watch a rating shift before the headline number moves.
        breakdown = item.get("starBreakdown") or {}
        split = ", ".join(
            f"{level}: {vals.get('count')} ({vals.get('percent')}%)"
            for level, vals in breakdown.items()
            if isinstance(vals, dict)
        )
        print(f"  Star split: {split}")

        print(f"  Summary:    {item.get('summary')}")
        print(f"  URL:        {item.get('reviewUrl')}")

    elif result_type == "error":
        print(f"[error] {item.get('error_type')}: {item.get('error_message')}")
        print(f"  Company URL: {item.get('companyUrl')}")

    print()
