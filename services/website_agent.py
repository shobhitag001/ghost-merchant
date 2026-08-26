from playwright.sync_api import sync_playwright


def investigate_website(url, declared_category):

    print("\n🌐 Starting website investigation...")

    try:

        # ====================================================
        # PLAYWRIGHT
        # ====================================================

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=True
            )

            page = browser.new_page()

            page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=15000
            )

            # --------------------------------------------
            # Collect website information WHILE browser
            # is still open
            # --------------------------------------------

            title = page.title()

            text = page.locator(
                "body"
            ).inner_text()

            text_lower = text.lower()

            # --------------------------------------------
            # Collect links
            # --------------------------------------------

            link_elements = page.locator("a").all()

            link_data = []

            for link in link_elements:

                try:

                    link_text = (
                        link.inner_text()
                        .strip()
                    )

                    href = link.get_attribute(
                        "href"
                    )

                    link_data.append({
                        "text": link_text,
                        "href": href
                    })

                except Exception:

                    pass

            # --------------------------------------------
            # Close browser AFTER all data collection
            # --------------------------------------------

            browser.close()


        # ====================================================
        # RISK ANALYSIS
        # ====================================================

        risk_score = 0

        reasons = []

        detected_keywords = []

        suspicious_links = []


        # ====================================================
        # 1. GAMBLING KEYWORDS
        # ====================================================

        gambling_keywords = [

            "bet",
            "betting",
            "casino",
            "aviator",
            "gambling",
            "game recharge",
            "sportsbook",
            "ipl betting",
            "betting tips"

        ]


        for keyword in gambling_keywords:

            if keyword in text_lower:

                detected_keywords.append(
                    keyword
                )


        if detected_keywords:

            risk_score += 40

            reasons.append(
                "Potential gambling-related "
                "content detected: "
                + ", ".join(
                    detected_keywords
                )
            )


        # ====================================================
        # 2. DECLARED CATEGORY CHECK
        # ====================================================

        category_keywords = {

            "apparel": [

                "shirt",
                "clothing",
                "fashion",
                "t-shirt",
                "dress",
                "jeans",
                "apparel"

            ],

            "restaurant": [

                "food",
                "restaurant",
                "menu",
                "delivery",
                "order food"

            ],

            "electronics": [

                "laptop",
                "mobile",
                "electronics",
                "computer",
                "smartphone"

            ],

            "travel": [

                "hotel",
                "flight",
                "travel",
                "holiday",
                "tour"

            ],

            "education": [

                "course",
                "education",
                "training",
                "academy",
                "learning"

            ]

        }


        expected_keywords = category_keywords.get(

            declared_category.lower(),

            []

        )


        category_match = False


        for keyword in expected_keywords:

            if keyword in text_lower:

                category_match = True

                break


        if not category_match:

            risk_score += 30

            reasons.append(

                "Website content does not strongly "
                "match the declared category: "
                + declared_category

            )


        # ====================================================
        # 3. SUSPICIOUS EXTERNAL LINKS
        # ====================================================

        suspicious_domains = [

            "t.me",
            "telegram",
            "bet",
            "casino",
            "aviator"

        ]


        for link in link_data:

            href = link["href"]

            if not href:

                continue


            href_lower = href.lower()


            for domain in suspicious_domains:

                if domain in href_lower:

                    suspicious_links.append(
                        href
                    )

                    break


        if suspicious_links:

            risk_score += 30

            reasons.append(

                "Potentially suspicious "
                "external links detected."

            )


        # ====================================================
        # 4. WEBSITE CONTENT CHECK
        # ====================================================

        if len(text.strip()) < 50:

            risk_score += 20

            reasons.append(

                "Website contains very little "
                "visible content."

            )


        # ====================================================
        # FINAL SCORE
        # ====================================================

        risk_score = min(
            risk_score,
            100
        )


        # ====================================================
        # RISK LEVEL
        # ====================================================

        if risk_score >= 80:

            risk_level = "CRITICAL"

        elif risk_score >= 60:

            risk_level = "HIGH"

        elif risk_score >= 30:

            risk_level = "MEDIUM"

        else:

            risk_level = "LOW"


        # ====================================================
        # NO RISK SIGNALS
        # ====================================================

        if not reasons:

            reasons.append(

                "Website content appears "
                "consistent with the declared "
                "business category."

            )


        # ====================================================
        # RESULT
        # ====================================================

        return {

            "title": title,

            "risk_score": risk_score,

            "risk_level": risk_level,

            "reasons": reasons,

            "detected_keywords": detected_keywords,

            "links_found": len(link_data),

            "suspicious_links": suspicious_links

        }


    # ========================================================
    # WEBSITE INVESTIGATION ERROR
    # ========================================================

    except Exception as error:

        print(
            f"⚠️ Website investigation failed: {error}"
        )


        return {

            "title": "Unable to access website",

            "risk_score": 50,

            "risk_level": "UNKNOWN",

            "reasons": [

                "Website investigation could not "
                "be completed because of a "
                "technical error.",

                f"Technical error: {error}"

            ],

            "detected_keywords": [],

            "links_found": 0,

            "suspicious_links": []

        }