from services.website_agent import investigate_website
import os


print("=" * 60)
print("       GHOST MERCHANT")
print("       WEBSITE AGENT")
print("=" * 60)


website_path = "data/suspicious_merchant.html"

# Convert local file path into browser URL
website_url = "file://" + os.path.abspath(
    website_path
).replace("\\", "/")

result = investigate_website(
    website_url,
    "Apparel"
)


print("\n🌐 WEBSITE INVESTIGATION")
print("-" * 60)

print("Website Title:", result["title"])

print(
    "Website Risk Score:",
    result["risk_score"],
    "/100"
)

print(
    "Website Risk Level:",
    result["risk_level"]
)

print("\nEvidence")
print("-" * 60)


if result["reasons"]:

    for reason in result["reasons"]:

        print("⚠", reason)

else:

    print("✓ No major website risks detected.")


print("\nDetected Keywords:")

if result["detected_keywords"]:

    for keyword in result["detected_keywords"]:

        print("•", keyword)

else:

    print("None")


print("\nLinks Found:", result["links_found"])


print("\n" + "=" * 60)

print("Website investigation completed.")

print("=" * 60)