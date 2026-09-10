#!/usr/bin/env python3
"""
Weight Loss Reviewed — static site generator.

Run:  python3 build.py
Output: static .html files written to the repo root (served as-is by Vercel).

Content model is data-first: edit the dicts below (PROVIDERS, VERSUS, ARTICLES)
and re-run. Every provider's outbound CTA comes from AFFILIATE_LINKS — swap the
"#" placeholders for your real affiliate/tracking URLs and rebuild.
"""
import os, re, html, datetime, shutil

# --------------------------------------------------------------------------
# Site config
# --------------------------------------------------------------------------
SITE = {
    "name": "Weight Loss Reviewed",
    "domain": "https://weightlossreviewed.com",
    "tagline": "We test, score and rank online weight-loss programs.",
    "email": "hello@weightlossreviewed.com",
}
TODAY = datetime.date(2026, 9, 9)
UPDATED = TODAY.strftime("%B %Y")
YEAR = TODAY.year

# >>> REPLACE THESE with your real affiliate/tracking links, then rebuild. <<<
AFFILIATE_LINKS = {
    "embody":     "https://track.revoffers.com/aff_c?offer_id=1548&aff_id=12904",
    "ro":         "https://ro.co",  # no affiliate link supplied — homepage placeholder
    "found":      "https://track.revoffers.com/aff_c?offer_id=1162&aff_id=12905",
    "altrx":      "https://altrx.com/glp1/offer-v9?sub1=&sub2=&sub3=&sub4=&sub5=&_ef_transaction_id=&utm_source=partners&utm_campaign=id_21&utm_affiliate=21&ef=n&ef_oid=108&ef_aid=21&uid=95&oid=108&affid=21&uid=1910&oid2=5043&affid2=1952",
    "medvi":      "https://glp1.medvi.org/rx?page=multi4&uid=105&oid=5&affid=2&pub=1952&sub1=1952&uid=1946&oid2=5665&affid2=1952",
    "trimrx":     "https://trimrx.com/glp1/offer-v4-meta?catalog=winter&discount=winter140&offer_url_id=29&oid=1&affid=40&oid2=4461&affid2=1952",
    "healthrx":   "https://track.revoffers.com/aff_c?offer_id=1630&aff_id=12905&url_id=12442",
    "bmimd":      "https://track.revoffers.com/aff_c?offer_id=1332&aff_id=12904",
    "directmeds": "https://track.revoffers.com/aff_c?offer_id=1304&aff_id=12904",
    "wellmedr":   "https://track.revoffers.com/aff_c?offer_id=1593&aff_id=12905",
    "shed":       "https://track.revoffers.com/aff_c?offer_id=1516&aff_id=12904",
    "sprout":     "https://track.revoffers.com/aff_c?offer_id=1286&aff_id=12904",
}

ROOT = os.path.dirname(os.path.abspath(__file__))

def _asset_ver():
    """Fingerprint of the stylesheet, so a CSS change busts the immutable cache."""
    import hashlib
    try:
        with open(os.path.join(ROOT, "assets", "style.css"), "rb") as f:
            return hashlib.md5(f.read()).hexdigest()[:10]
    except OSError:
        return datetime.datetime.now().strftime("%Y%m%d%H%M%S")

ASSET_VER = _asset_ver()

# --------------------------------------------------------------------------
# Providers  (ranking = list order in PROVIDER_ORDER)
# scores are editorial (our rating, 0-10). price_tier is a relative indicator.
# --------------------------------------------------------------------------
PROVIDER_ORDER = ["embody", "ro", "found", "altrx", "medvi",
                  "trimrx", "healthrx", "bmimd", "directmeds", "wellmedr",
                  "shed", "sprout"]

PROVIDERS = {
    "embody": {
        "name": "Embody",
        "score": 9.4,
        "tier": "$$",
        "best_for": "Best overall",
        "highlight": "Real clinician time, meds, and lasting coaching.",
        "bullets": [
            "Video visits with real prescribing clinicians",
            "Branded + compounded GLP-1 options",
            "Coaching and tracking built in",
        ],
        "subscores": {
            "Clinical support": 9.6, "Onboarding": 9.2, "Value": 9.0,
            "Medication access": 9.5, "App & tracking": 9.4, "Transparency": 9.3,
        },
        "pros": [
            "Genuine two-way clinician access, including messaging between visits",
            "Flexible medication path if one option is out of stock or unaffordable",
            "Coaching and check-ins continue past onboarding, not just at signup",
            "Clear, itemized pricing before you commit to anything",
        ],
        "cons": [
            "Not the cheapest month-one price on the market",
            "Coaching depth is more than some people who just want a script want",
        ],
        "verdict": "Embody is our top pick because it does the boring things well: you actually talk to a clinician, the medication plan bends when supply or budget changes, and the coaching keeps showing up. It's not the rock-bottom price, but it's the program most likely to still be working for you in month six.",
        "summary": "A full-service telehealth weight-loss program built around GLP-1 medications, live clinician visits, and ongoing coaching. Embody positions itself as an end-to-end plan rather than a prescription vending machine — and in our testing that ongoing support is what separates it from cheaper competitors.",
    },
    "ro": {
        "name": "Ro",
        "score": 9.1,
        "tier": "$$$",
        "best_for": "Most established brand",
        "highlight": "Established national brand, polished logistics.",
        "bullets": [
            "Established national telehealth brand",
            "Help navigating insurance",
            "Slick app and pharmacy coordination",
        ],
        "subscores": {
            "Clinical support": 9.2, "Onboarding": 9.0, "Value": 8.4,
            "Medication access": 9.3, "App & tracking": 9.2, "Transparency": 8.8,
        },
        "pros": [
            "One of the most recognized names in direct-to-consumer telehealth",
            "Mature logistics: pharmacy coordination, refills, and reminders are smooth",
            "Support navigating branded GLP-1s and insurance where possible",
            "Large clinician network means fewer scheduling bottlenecks",
        ],
        "cons": [
            "Tends to sit at the higher end on total monthly cost",
            "Scale can make the experience feel less personal than boutique programs",
        ],
        "verdict": "Ro is the safe, established choice. If brand trust and smooth logistics matter more to you than squeezing out the lowest price, it's hard to go wrong. You pay a bit more for the polish and the name — for a lot of people that trade is worth it.",
        "summary": "Ro is a well-known national telehealth company that offers a structured weight-management program including GLP-1 medications. It leans on scale — a large clinician network, mature pharmacy logistics, and a refined app — to deliver a dependable, if pricier, experience.",
    },
    "altrx": {
        "name": "AltRx",
        "score": 8.6,
        "tier": "$",
        "best_for": "Best value",
        "highlight": "The lowest entry price and the fastest start.",
        "bullets": [
            "Lowest typical entry price",
            "Fast intake — start within days",
            "Compounded GLP-1 keeps cost down",
        ],
        "subscores": {
            "Clinical support": 8.0, "Onboarding": 9.1, "Value": 9.5,
            "Medication access": 8.6, "App & tracking": 8.2, "Transparency": 8.4,
        },
        "pros": [
            "Clearly the budget leader among the programs we tested",
            "Quick, low-friction signup and prescription review",
            "Good option if compounded semaglutide/tirzepatide fits your plan",
            "No long lock-in on most plans",
        ],
        "cons": [
            "Lighter ongoing coaching than the premium programs",
            "Support is mostly async messaging rather than scheduled visits",
        ],
        "verdict": "AltRx wins on price and speed. If you already know you want a compounded GLP-1 and don't need hand-holding, it's the most cost-effective door in. Just go in knowing the support is leaner — this is value-first, not coaching-first.",
        "summary": "AltRx is a value-focused telehealth program built around compounded GLP-1 medications and a fast, streamlined intake. It trades some of the coaching depth of premium programs for a notably lower monthly cost and quick time-to-start.",
    },
    "trimrx": {
        "name": "TrimRx",
        "score": 8.4,
        "tier": "$$",
        "best_for": "Best for tirzepatide",
        "highlight": "A program built specifically around tirzepatide.",
        "bullets": [
            "Strong tirzepatide focus",
            "Flexible dosing and titration support",
            "Reasonable mid-market pricing",
        ],
        "subscores": {
            "Clinical support": 8.4, "Onboarding": 8.5, "Value": 8.5,
            "Medication access": 8.8, "App & tracking": 8.0, "Transparency": 8.2,
        },
        "pros": [
            "Clear specialization in tirzepatide, with titration guidance",
            "Flexible plans that adjust as your dose changes",
            "Reasonable pricing that sits between budget and premium",
            "Good fit if you've decided tirzepatide is your route",
        ],
        "cons": [
            "Narrower focus means fewer options if you'd rather try semaglutide first",
            "App and tracking tools are functional but basic",
        ],
        "verdict": "TrimRx is the pick when you already want tirzepatide and want a program built around it rather than treating it as an afterthought. If you're undecided between GLP-1 options, a broader program may serve you better — but for tirzepatide specifically, TrimRx knows its lane.",
        "summary": "TrimRx is a telehealth weight-loss program that specializes in tirzepatide-based plans with flexible titration support. It's a focused option for members who have already decided tirzepatide is the route they want to take.",
    },
    "bmimd": {
        "name": "bmiMD",
        "score": 8.2,
        "tier": "$$$",
        "best_for": "Most medical-first",
        "highlight": "Physician-led care for more complex health needs.",
        "bullets": [
            "Physician-led, medical-first intake",
            "Built for complex cases",
            "Help with labs and insurance",
        ],
        "subscores": {
            "Clinical support": 9.0, "Onboarding": 7.8, "Value": 7.6,
            "Medication access": 8.6, "App & tracking": 7.8, "Transparency": 8.4,
        },
        "pros": [
            "Deeper medical oversight than most consumer-first programs",
            "Comfortable with lab work, comorbidities, and complex histories",
            "Physician involvement rather than mostly async review",
            "A sensible choice if you have health factors to manage carefully",
        ],
        "cons": [
            "Slower, more thorough onboarding — not built for instant starts",
            "Premium pricing and less of a consumer-app feel",
        ],
        "verdict": "bmiMD is the choice when the medicine matters more than the app. If you have health complexity — or you just want a physician clearly in charge — its thoroughness is reassuring. If you want fast and cheap, look elsewhere; that's not what this program is for.",
        "summary": "bmiMD takes a physician-led, medical-first approach to weight management. It's one of the most clinically thorough programs we reviewed, which makes it a strong fit for people with complex health needs — at the cost of speed and a higher price point.",
    },
    "found": {
        "name": "Found",
        "score": 9.0,
        "tier": "$$",
        "best_for": "Best for coaching",
        "highlight": "The best coaching and app in the category.",
        "bullets": [
            "Standout coaching and community",
            "GLP-1 meds where appropriate",
            "Whole-person: food, movement, sleep",
        ],
        "subscores": {
            "Clinical support": 9.0, "Onboarding": 8.8, "Value": 8.6,
            "Medication access": 8.8, "App & tracking": 9.4, "Transparency": 8.9,
        },
        "pros": [
            "The strongest coaching and behavior-change program in our lineup",
            "Polished app and an active member community",
            "Whole-person approach that looks past the injection",
            "Well-established brand with a real track record",
        ],
        "cons": [
            "The coaching-heavy model is overkill if you only want a prescription",
            "Leans toward the premium end on total cost",
        ],
        "verdict": "Found is the pick if you believe losing weight is about more than the medication. Its coaching and app are the best part of the experience, not an afterthought. If you want a program that helps you build habits — not just hand you a script — it's excellent. If you just want the script, you're paying for things you won't use.",
        "summary": "Found pairs GLP-1 medication (where appropriate) with a genuine behavior-change program — coaching, an active community, and one of the best apps we tested. It's built for people who want support changing habits, not just a prescription.",
    },
    "medvi": {
        "name": "Medvi",
        "score": 8.5,
        "tier": "$$",
        "best_for": "Best for simple GLP-1 access",
        "highlight": "Quick route to semaglutide or tirzepatide.",
        "bullets": [
            "Both semaglutide and tirzepatide",
            "Straightforward, quick intake",
            "Responsive support",
        ],
        "subscores": {
            "Clinical support": 8.4, "Onboarding": 8.8, "Value": 8.7,
            "Medication access": 8.9, "App & tracking": 8.0, "Transparency": 8.4,
        },
        "pros": [
            "Clear choice between semaglutide and tirzepatide",
            "Quick, uncomplicated onboarding",
            "Sensible mid-market pricing",
            "Support is responsive and easy to reach",
        ],
        "cons": [
            "Lighter coaching than the premium, support-led programs",
            "App and tracking tools are basic",
        ],
        "verdict": "Medvi does the fundamentals well without dressing them up. If you know what you want and value a clean, quick path to a GLP-1 over heavy coaching, it's a solid, fairly priced choice. Just don't expect the hand-holding of the top-scoring programs.",
        "summary": "Medvi is a straightforward telehealth program offering both semaglutide and tirzepatide with a quick, uncomplicated process. It's a sensible middle-ground pick for people who want efficient GLP-1 access without a lot of extras.",
    },
    "healthrx": {
        "name": "HealthRx",
        "score": 8.3,
        "tier": "$$",
        "best_for": "Best for Rx + pharmacy",
        "highlight": "Prescription-forward; pharmacy handled for you.",
        "bullets": [
            "Multiple medication options",
            "Pharmacy coordination handled for you",
            "Clear, medication-first process",
        ],
        "subscores": {
            "Clinical support": 8.3, "Onboarding": 8.4, "Value": 8.4,
            "Medication access": 8.7, "App & tracking": 7.8, "Transparency": 8.2,
        },
        "pros": [
            "Smooth pharmacy coordination and refills",
            "Several medication options rather than one lane",
            "Efficient, medication-first experience",
            "Reasonable mid-market pricing",
        ],
        "cons": [
            "Coaching and lifestyle support are minimal",
            "Tracking tools are functional but plain",
        ],
        "verdict": "HealthRx is a good fit if the medication and getting it to your door reliably are what you care about most. It's efficient and the pharmacy side is smooth. If you want coaching or a whole-person plan, a support-led program will serve you better.",
        "summary": "HealthRx is a prescription-forward telehealth program that emphasizes reliable medication access and pharmacy coordination. It's a practical choice for people who want the meds handled cleanly, with less focus on coaching.",
    },
    "directmeds": {
        "name": "DirectMeds",
        "score": 8.1,
        "tier": "$",
        "best_for": "Best for direct delivery",
        "highlight": "Budget-friendly, direct-to-door simplicity.",
        "bullets": [
            "Simple direct-to-door delivery",
            "Among the lowest entry prices",
            "Minimal friction, quick start",
        ],
        "subscores": {
            "Clinical support": 7.9, "Onboarding": 8.9, "Value": 9.0,
            "Medication access": 8.4, "App & tracking": 7.6, "Transparency": 8.0,
        },
        "pros": [
            "Very competitive pricing",
            "Fast, low-friction signup and delivery",
            "Good option if you just want the medication shipped",
            "No unnecessary extras to pay for",
        ],
        "cons": [
            "Little in the way of coaching or ongoing support",
            "Basic app and tracking",
        ],
        "verdict": "DirectMeds keeps it simple: get approved, get the medication delivered, done. For a budget-conscious, self-directed member that's exactly right. If you want support beyond the delivery, look higher up our rankings.",
        "summary": "DirectMeds is a value-focused program built around simple, direct-to-door medication delivery and a fast signup. It trades coaching and extras for a low price and minimal friction.",
    },
    "wellmedr": {
        "name": "WellMedr",
        "score": 8.0,
        "tier": "$$",
        "best_for": "Best for whole-wellness",
        "highlight": "A rounded, clinician-guided whole-wellness plan.",
        "bullets": [
            "Wellness-rounded plans beyond the meds",
            "Clinician-guided throughout",
            "Flexible options for your goals",
        ],
        "subscores": {
            "Clinical support": 8.2, "Onboarding": 8.1, "Value": 8.1,
            "Medication access": 8.2, "App & tracking": 7.9, "Transparency": 8.0,
        },
        "pros": [
            "Broader wellness focus, not medication-only",
            "Clinician guidance across the plan",
            "Flexible plans for different goals",
            "Balanced, middle-of-the-market pricing",
        ],
        "cons": [
            "Doesn't lead any single category the way top picks do",
            "App and tracking are average",
        ],
        "verdict": "WellMedr is a well-rounded generalist. It won't top any single category, but its whole-wellness angle and clinician guidance make it a dependable all-rounder for people who want a balanced plan rather than a specialist one.",
        "summary": "WellMedr takes a rounded, clinician-guided approach to weight management that considers wellness beyond the medication itself. It's a balanced all-rounder rather than a category leader.",
    },
    "shed": {
        "name": "Shed",
        "score": 7.9,
        "tier": "$$",
        "best_for": "Best for a simple start",
        "highlight": "A simple, goal-focused way to get started.",
        "bullets": [
            "Straightforward GLP-1 onboarding",
            "Goal-focused, motivating check-ins",
            "No-frills and easy to follow",
        ],
        "subscores": {
            "Clinical support": 7.8, "Onboarding": 8.4, "Value": 8.2,
            "Medication access": 8.0, "App & tracking": 7.6, "Transparency": 7.9,
        },
        "pros": [
            "Quick, uncomplicated signup",
            "A clear focus on getting you started",
            "Reasonable, middle-of-the-road pricing",
            "Good fit for first-timers who want simplicity",
        ],
        "cons": [
            "Lighter clinical and coaching depth",
            "Fewer features than the premium programs",
        ],
        "verdict": "Shed keeps things simple: a clean path to a GLP-1 without a lot of extras. If you want to get started quickly and don't need heavy coaching, it does the job. For deeper support or complex needs, look higher up our list.",
        "summary": "Shed is a straightforward telehealth weight-loss program focused on a simple, quick start with GLP-1 medication. It trades depth for ease, which makes it a reasonable pick for first-timers who value simplicity.",
    },
    "sprout": {
        "name": "Sprout",
        "score": 7.8,
        "tier": "$$",
        "best_for": "Best for a gentle start",
        "highlight": "A gentle, beginner-friendly place to begin.",
        "bullets": [
            "Beginner-friendly onboarding",
            "Lifestyle guidance alongside medication",
            "Supportive, low-pressure approach",
        ],
        "subscores": {
            "Clinical support": 7.9, "Onboarding": 8.2, "Value": 8.0,
            "Medication access": 7.9, "App & tracking": 7.7, "Transparency": 7.9,
        },
        "pros": [
            "Approachable for people new to GLP-1s",
            "Emphasis on lifestyle, not just the medication",
            "Low-pressure, supportive tone",
            "Sensible mid-market pricing",
        ],
        "cons": [
            "Not built for fast, aggressive plans",
            "Lighter on advanced clinical features",
        ],
        "verdict": "Sprout is a gentle on-ramp — a good fit if you're new to GLP-1 medications and want a supportive, lifestyle-minded start rather than a clinical-heavy program. If you want maximum medical oversight or the lowest price, other picks fit better.",
        "summary": "Sprout is a beginner-friendly telehealth weight-loss program that pairs GLP-1 medication with lifestyle guidance and a supportive, low-pressure approach. It's aimed at people easing into treatment for the first time.",
    },
}

SUBSCORE_ORDER = ["Clinical support", "Onboarding", "Value", "Medication access", "App & tracking", "Transparency"]

# For the head-to-head "round by round" breakdown on versus pages.
CATEGORY_FRAMES = {
    "Clinical support": "How much real clinician time, messaging and follow-up you get.",
    "Onboarding": "How quickly and painlessly you can get started.",
    "Value": "What you get for the money, judged against comparable programs.",
    "Medication access": "The range of GLP-1 options and how easily the plan adapts.",
    "App & tracking": "The quality of the day-to-day tools.",
    "Transparency": "How clearly pricing and terms are laid out up front.",
}
# Order the rounds by what matters most.
ROUND_ORDER = ["Clinical support", "Medication access", "Value", "Onboarding", "App & tracking", "Transparency"]

# --------------------------------------------------------------------------
# Versus / battle pages. Each has a unique, hand-written verdict + attribute
# grid. "winner" just controls which column gets the highlight ring.
# --------------------------------------------------------------------------
VERSUS = [
    {
        "a": "embody", "b": "ro", "winner": "embody",
        "intro": "Two of the strongest full-service programs we've tested go head to head. Embody edges it on ongoing coaching and flexibility; Ro counters with brand scale and polish. Here's how they actually differ.",
        "verdict": "Both are excellent — this is a close one. Embody takes it for most people because the coaching keeps going and the medication plan flexes when supply or budget shifts. Ro is the pick if an established national brand and frictionless logistics are what put you at ease. You won't be poorly served either way.",
        "pick_a": "You want continuous coaching and a plan that adapts month to month.",
        "pick_b": "Brand recognition and mature pharmacy logistics matter most to you.",
        "rows": [
            ("Live clinician visits", "Yes — video visits", "Yes — large network"),
            ("Ongoing coaching", "Built in, continues past onboarding", "Structured, more self-serve"),
            ("Medication flexibility", "Branded + compounded, switches easily", "Strong, brand-led"),
            ("Typical cost", "Mid ($$)", "Higher ($$$)"),
            ("Best suited to", "People who want support that lasts", "People who want an established name"),
        ],
    },
    {
        "a": "embody", "b": "altrx", "winner": "embody",
        "intro": "The premium all-rounder versus the budget champion. This one comes down to a simple question: are you paying for support, or paying as little as possible?",
        "verdict": "If money is the deciding factor, AltRx wins outright — it's cheaper and faster to start. But Embody is the better program: you get real clinician time and coaching that AltRx simply doesn't include at its price. Pay less and self-manage with AltRx, or pay more and be supported with Embody.",
        "pick_a": "You want clinician access and coaching, and will pay a bit more for it.",
        "pick_b": "You want the lowest entry price and are comfortable self-managing.",
        "rows": [
            ("Entry price", "Mid ($$)", "Lowest ($)"),
            ("Coaching depth", "High — ongoing", "Light — mostly async"),
            ("Time to start", "Fast", "Fastest"),
            ("Medication options", "Branded + compounded", "Compounded focus"),
            ("Best suited to", "Support-seekers", "Budget-first, DIY types"),
        ],
    },
    {
        "a": "embody", "b": "trimrx", "winner": "embody",
        "intro": "A broad, do-everything program against a tirzepatide specialist. The right answer depends on whether you've already picked your medication.",
        "verdict": "Embody is the better all-around program and the safer default if you're still weighing your options. But if you've specifically decided on tirzepatide, TrimRx's focus and titration support are a genuine advantage. Undecided? Start with Embody. Set on tirzepatide? TrimRx earns a look.",
        "pick_a": "You want flexibility across GLP-1 options and stronger overall support.",
        "pick_b": "You've already decided tirzepatide is your route.",
        "rows": [
            ("Medication focus", "Broad (semaglutide + tirzepatide)", "Tirzepatide specialist"),
            ("Coaching depth", "High", "Moderate"),
            ("Titration support", "Good", "Strong"),
            ("Typical cost", "Mid ($$)", "Mid ($$)"),
            ("Best suited to", "Undecided or want options", "Tirzepatide-committed"),
        ],
    },
    {
        "a": "embody", "b": "bmimd", "winner": "embody",
        "intro": "Consumer-friendly full-service versus a medical-first, physician-led model. Both are strong; they're built for different people.",
        "verdict": "For most healthy adults who want an effective, well-supported program, Embody is the smoother, better-value experience. bmiMD pulls ahead if you have health complexity — comorbidities, medication interactions, a history that needs careful oversight. Match the program to how medically complex your situation is.",
        "pick_a": "You're a straightforward case and want a great consumer experience.",
        "pick_b": "You have health complexity and want a physician clearly in charge.",
        "rows": [
            ("Model", "Consumer-first, clinician-backed", "Physician-led, medical-first"),
            ("Onboarding speed", "Fast", "Slower, thorough"),
            ("Complex cases", "Handled well", "A core strength"),
            ("Typical cost", "Mid ($$)", "Higher ($$$)"),
            ("Best suited to", "Most people", "Complex health needs"),
        ],
    },
    {
        "a": "ro", "b": "bmimd", "winner": "ro",
        "intro": "Two premium programs, two different philosophies: a polished national platform versus a physician-led medical practice. Both sit at the higher end on price.",
        "verdict": "Ro is the better pick for a smooth, scaled, brand-backed experience. bmiMD is the better pick if medical depth is the point and you'd trade some polish for a physician's close involvement. Same rough price band — the deciding factor is whether you value logistics or clinical thoroughness more.",
        "pick_a": "You want a big-brand experience with frictionless logistics.",
        "pick_b": "You want maximum medical oversight for a complex situation.",
        "rows": [
            ("Model", "National telehealth platform", "Physician-led practice"),
            ("Logistics polish", "Excellent", "Good"),
            ("Medical depth", "Strong", "Deepest"),
            ("Typical cost", "Higher ($$$)", "Higher ($$$)"),
            ("Best suited to", "Brand + convenience", "Clinical complexity"),
        ],
    },
    {
        "a": "altrx", "b": "trimrx", "winner": "altrx",
        "intro": "Two mid-market programs that both keep costs sensible. AltRx is the value generalist; TrimRx is the tirzepatide specialist. Here's the split.",
        "verdict": "AltRx wins on price and speed and is the better default if you just want an affordable GLP-1 start. TrimRx is worth the small step up if tirzepatide specifically is your plan and you want titration support built around it. Budget-first: AltRx. Tirzepatide-first: TrimRx.",
        "pick_a": "You want the lowest cost and a fast, simple start.",
        "pick_b": "You specifically want tirzepatide with titration guidance.",
        "rows": [
            ("Entry price", "Lowest ($)", "Mid ($$)"),
            ("Medication focus", "Broad, compounded", "Tirzepatide specialist"),
            ("Coaching depth", "Light", "Moderate"),
            ("Time to start", "Fastest", "Fast"),
            ("Best suited to", "Budget-first", "Tirzepatide-committed"),
        ],
    },
    {
        "a": "ro", "b": "altrx", "winner": "ro",
        "intro": "Premium brand experience versus rock-bottom pricing. This is the clearest 'you get what you pay for' matchup in our lineup.",
        "verdict": "If budget rules the decision, AltRx is dramatically cheaper and starts faster. If you want the reassurance of an established national brand with mature logistics — and can absorb the higher cost — Ro delivers that. There's no wrong answer; there's only which trade-off you'd rather make.",
        "pick_a": "You value brand trust and polished logistics over price.",
        "pick_b": "You want the lowest possible entry cost.",
        "rows": [
            ("Entry price", "Higher ($$$)", "Lowest ($)"),
            ("Brand maturity", "Established national name", "Newer, value-focused"),
            ("Coaching depth", "Structured", "Light"),
            ("Logistics polish", "Excellent", "Basic"),
            ("Best suited to", "Brand + convenience", "Budget-first"),
        ],
    },
    {
        "a": "embody", "b": "found", "winner": "embody",
        "intro": "Two support-heavy programs that both go well beyond the prescription. Embody leans on live clinician access and flexibility; Found is built around coaching and its app.",
        "verdict": "Embody edges it as the more complete package — real clinician time plus flexible medication access. But Found is arguably the best in the category at coaching and habit change, so if that's specifically what you need, it's a genuinely close call.",
        "pick_a": "You want the most complete mix of clinician access, medication flexibility and coaching.",
        "pick_b": "Behavior change and a great app matter to you more than anything else.",
    },
    {
        "a": "ro", "b": "found", "winner": "ro",
        "intro": "An established national brand versus the category's best coaching experience. Both are polished; they emphasize different things.",
        "verdict": "Ro takes it narrowly on the strength of its scale, logistics and brand trust. Found is right behind and wins outright if coaching and its app are your priority — this one comes down to whether you value infrastructure or behavior support more.",
        "pick_a": "Brand trust and smooth, proven logistics matter most.",
        "pick_b": "You want the strongest coaching and app, and will trade a little brand scale for it.",
    },
    {
        "a": "embody", "b": "medvi", "winner": "embody",
        "intro": "The most complete full-service program versus a lean, no-nonsense route to a GLP-1. Support and flexibility against speed and simplicity.",
        "verdict": "Embody is the better program for most people — more clinician time, coaching and medication flexibility. Medvi is the pick if you already know what you want and would rather skip the extras for a faster, simpler start.",
        "pick_a": "You want ongoing support and a plan that adapts over time.",
        "pick_b": "You want a quick, straightforward path to semaglutide or tirzepatide.",
    },
    {
        "a": "found", "b": "altrx", "winner": "found",
        "intro": "Coaching-first versus budget-first. Found invests in support and its app; AltRx keeps things cheap and fast.",
        "verdict": "Found is the stronger program if you value coaching and a polished experience, and it wins here. AltRx counters on price and speed — if the lowest entry cost is the deciding factor and you're happy to self-manage, it's the better fit.",
        "pick_a": "You want coaching and a great app, and will pay a bit more.",
        "pick_b": "You want the lowest entry price and a fast start.",
    },
    {
        "a": "found", "b": "medvi", "winner": "found",
        "intro": "A coaching-led program versus a simple GLP-1 access play. Both are mid-priced; the difference is how much hand-holding you get.",
        "verdict": "Found wins for anyone who wants support built in — coaching, community and a strong app. Medvi is the leaner choice for people who just want the medication handled without the extras.",
        "pick_a": "You want coaching and structure, not just a prescription.",
        "pick_b": "You want a clean, quick GLP-1 start and minimal fuss.",
    },
    {
        "a": "ro", "b": "medvi", "winner": "ro",
        "intro": "A big, established telehealth brand versus a simple, focused GLP-1 program. Trust and polish against speed and price.",
        "verdict": "Ro takes it on scale, logistics and brand reassurance. Medvi is the value-minded alternative if you don't need the brand name and want a quicker, lighter experience.",
        "pick_a": "Brand trust and mature logistics are worth a higher price to you.",
        "pick_b": "You want a simpler, faster route and care less about the brand.",
    },
    {
        "a": "altrx", "b": "medvi", "winner": "altrx",
        "intro": "Two value-minded programs, nearly neck and neck. AltRx leads on price; Medvi leans on a clean, flexible GLP-1 process.",
        "verdict": "AltRx edges it on cost and speed, making it our pick for the tightest budgets. Medvi is just behind and worth it if you want a slightly more guided choice between semaglutide and tirzepatide. Genuinely close.",
        "pick_a": "The lowest possible entry price is your priority.",
        "pick_b": "You want a clean, guided choice between semaglutide and tirzepatide.",
    },
    {
        "a": "found", "b": "trimrx", "winner": "found",
        "intro": "The category's best coaching versus a tirzepatide specialist. Broad support against focused medication expertise.",
        "verdict": "Found is the better all-round program and wins for most people. TrimRx is the smarter pick if you've specifically decided on tirzepatide and want a program built around it.",
        "pick_a": "You want strong coaching and flexibility across options.",
        "pick_b": "You've already committed to tirzepatide.",
    },
    {
        "a": "ro", "b": "trimrx", "winner": "ro",
        "intro": "An established generalist versus a tirzepatide specialist. Brand and breadth against focus.",
        "verdict": "Ro wins for most people on scale, logistics and trust. TrimRx is the better choice specifically if tirzepatide is your route and you want a program that specializes in it.",
        "pick_a": "You want a broad, established program with smooth logistics.",
        "pick_b": "Tirzepatide specifically is your plan.",
    },
    {
        "a": "embody", "b": "healthrx", "winner": "embody",
        "intro": "A full-service, coaching-led program versus a prescription-forward one that nails pharmacy logistics.",
        "verdict": "Embody is the more complete, better-supported program and our pick for most people. HealthRx is a solid, efficient choice if what you mainly want is reliable medication access with the pharmacy side handled for you.",
        "pick_a": "You want clinician time and coaching, not just the medication.",
        "pick_b": "You mainly want reliable meds and smooth pharmacy handling.",
    },
]

# --------------------------------------------------------------------------
# Articles (long-tail). Bodies are HTML fragments; keep them original + useful.
# --------------------------------------------------------------------------
ARTICLES = [
    {
        "slug": "glp1-weight-loss-programs-compared",
        "title": f"GLP-1 Weight-Loss Programs Compared ({YEAR}): What Actually Matters",
        "tag": "Guides",
        "date": "2026-09-09",
        "description": "Most GLP-1 telehealth programs look identical on the surface. Here are the five things that actually change your results and your bill.",
        "dek": "Every program advertises the same medications. The differences that matter are quieter — and they're the ones that decide whether you stick with it.",
        "body": """
<p>Search for a GLP-1 weight-loss program and you'll get a wall of near-identical landing pages: same medications, same stock photos, same promises. The active ingredients really are the same across most programs — so the marketing can't tell them apart, and neither can you at a glance. What actually separates a program you stick with from one you quietly cancel comes down to five things.</p>

<h2 id="support">1. How much clinician and coaching support you actually get</h2>
<p>The single biggest predictor of whether people stay on a program is support after signup. A questionnaire and an auto-approved prescription is cheap to run, so plenty of programs stop there. The ones worth paying for give you a real clinician to message, someone to adjust your dose when side effects hit, and check-ins that continue past month one. When you compare programs, look past the intake and ask what month three looks like.</p>

<h2 id="medication">2. Which medications — and how flexible the path is</h2>
<p>Programs split into branded GLP-1s (the name-brand injectables) and compounded versions prepared by pharmacies. Branded tends to cost more; compounded is usually cheaper but availability and rules shift over time. The programs that handle this best don't lock you into one lane — if supply tightens or your budget changes, they can switch you without starting over. Flexibility here quietly matters more than the sticker price.</p>

<h2 id="cost">3. The <em>total</em> cost, not the headline price</h2>
<p>"From $X/month" almost never includes everything. Read for the medication cost, the membership or visit fee, lab work if required, and what happens when your dose increases during titration. A cheap entry price attached to a plan that balloons at higher doses can end up costing more than a program that was honest up front. We score transparency separately for exactly this reason.</p>

<h2 id="titration">4. Titration and side-effect handling</h2>
<p>GLP-1 medications are started low and increased gradually. Nausea and other side effects are common early on, and how a program handles that window is a real quality signal. Can you reach someone quickly? Will they slow your titration if you're struggling? A program that treats side effects as a support problem, not an inconvenience, is one you're far more likely to stay on.</p>

<h2 id="exit">5. What happens when you want to stop</h2>
<p>Good programs plan for the off-ramp as carefully as the on-ramp. Ask whether there's a maintenance plan, guidance for tapering, and no punitive lock-in. A program confident in its results doesn't need to trap you.</p>

<div class="callout"><h3>The short version</h3><p>The medication is rarely the differentiator — support, flexibility, honest pricing, side-effect handling, and a sane exit plan are. That's exactly what our <a href="/">comparison chart</a> scores, so you can see the differences the marketing hides.</p></div>

<p class="muted"><em>This article is general information, not medical advice. GLP-1 medications are prescription drugs; whether one is right for you is a decision for you and a licensed clinician.</em></p>
""",
    },
    {
        "slug": "compounded-semaglutide-cost",
        "title": "How Much Does Compounded Semaglutide Cost Online?",
        "tag": "Costs",
        "date": "2026-09-08",
        "description": "What drives the price of compounded semaglutide through telehealth, why quotes vary so much, and how to compare offers without getting surprised.",
        "dek": "Compounded semaglutide is usually the cheaper route — but 'cheaper' hides a wide range. Here's what actually moves the number.",
        "body": """
<p>Compounded semaglutide is often marketed as the budget-friendly way onto a GLP-1, and broadly that's true — it's typically cheaper than the branded injectables. But the quotes you'll see online swing widely, and the reasons aren't always obvious from the landing page. Here's what actually drives the number so you can compare offers on equal terms.</p>

<h2 id="what">What "compounded" means</h2>
<p>Compounded medications are prepared by a pharmacy rather than sold as a mass-produced branded product. That can lower cost, but it also means quality and sourcing vary by pharmacy — so who prepares your medication matters as much as the price. A responsible program is transparent about its pharmacy partners.</p>

<h2 id="drivers">What drives the price</h2>
<ul>
  <li><strong>Your dose.</strong> Semaglutide is titrated upward over time. A low starting dose is cheaper than a maintenance dose, so an intro price may not reflect what you'll pay in a few months.</li>
  <li><strong>Membership vs. medication.</strong> Some programs split the bill into a membership fee plus medication; others bundle it. Bundled looks simpler; split can be cheaper — read both carefully.</li>
  <li><strong>Visit and lab fees.</strong> An initial consult or lab work may be extra, or may be included. This is where "from $X" quotes quietly diverge.</li>
  <li><strong>Plan length.</strong> Quarterly or longer commitments often carry a lower monthly rate than month-to-month, at the cost of flexibility.</li>
</ul>

<h2 id="compare">How to compare offers fairly</h2>
<p>Put every offer into the same shape before you judge it: total cost for a full month <em>at your expected maintenance dose</em>, including membership, visits, and shipping. A program that's cheapest at the starter dose isn't necessarily cheapest where you'll actually spend most of your time. This is exactly why our reviews score <strong>value</strong> and <strong>transparency</strong> as separate things.</p>

<div class="callout warn"><h3>A note on very low prices</h3><p>If a quote is far below everyone else, find out why before you celebrate. Ask about the pharmacy, what's included, and what happens at higher doses. Unusually cheap sometimes means something's missing.</p></div>

<p>Want the value-first option? <a href="/reviews/altrx">AltRx</a> was the budget leader in our lineup; if you'd rather trade a little cost for more support, our <a href="/">full comparison</a> lays out the differences.</p>

<p class="muted"><em>Prices change constantly and vary by provider, dose, and pharmacy. Always confirm the current total cost directly with the provider. This article is general information, not medical or pricing advice.</em></p>
""",
    },
    {
        "slug": "do-you-need-a-prescription-online",
        "title": "Do You Need a Prescription for Weight-Loss Meds Online?",
        "tag": "How it works",
        "date": "2026-09-07",
        "description": "How online weight-loss prescriptions actually work, what a legitimate telehealth evaluation looks like, and the warning signs of a service cutting corners.",
        "dek": "Yes — and that's a good thing. Here's what a real online evaluation involves, and how to tell it apart from a service that's just selling.",
        "body": """
<p>Short answer: yes. GLP-1 weight-loss medications are prescription drugs, and any legitimate program will require a prescription from a licensed clinician before you can get one. What's changed is <em>how</em> that prescription happens — increasingly through a telehealth evaluation rather than an in-person visit. Understanding what a proper evaluation looks like is the best way to spot a service that's cutting corners.</p>

<h2 id="how">How an online prescription works</h2>
<p>A legitimate telehealth flow generally looks like this: you complete a detailed medical intake, a licensed clinician reviews it (often with a video or phone visit, or a structured async review), they determine whether the medication is appropriate and safe for you, and only then is a prescription issued and sent to a pharmacy. The clinician is making a medical judgment — not rubber-stamping a purchase.</p>

<h2 id="good">What a good evaluation includes</h2>
<ul>
  <li>A thorough health history, current medications, and relevant conditions</li>
  <li>Questions about contraindications — not just "do you want to lose weight?"</li>
  <li>A real path to reach a clinician with questions or side effects</li>
  <li>Sometimes lab work, especially for more complex situations</li>
</ul>

<h2 id="flags">Warning signs to avoid</h2>
<p>Be cautious with any service that promises a prescription "guaranteed," skips a meaningful medical review, has no clear way to reach a clinician, or won't tell you who is prescribing. A prescription that requires no genuine evaluation isn't a shortcut — it's a red flag. We wrote a fuller checklist in <a href="/guides/how-to-spot-a-legit-online-clinic">how to spot a legit online clinic</a>.</p>

<div class="callout"><h3>The bottom line</h3><p>Needing a prescription is a feature, not a hurdle. The programs worth trusting treat the evaluation seriously — that's the whole point of a clinician being involved. Our <a href="/">top-rated programs</a> all use real clinical review.</p></div>

<p class="muted"><em>This is general information, not medical advice. Whether a weight-loss medication is appropriate for you is a decision for you and a licensed clinician.</em></p>
""",
    },
    {
        "slug": "tirzepatide-vs-semaglutide",
        "title": "Tirzepatide vs Semaglutide: How to Choose",
        "tag": "Medications",
        "date": "2026-09-06",
        "description": "A plain-English comparison of the two leading GLP-1 medications for weight loss — how they differ, and the practical factors that decide which is right for you.",
        "dek": "The two most-prescribed options for weight loss work in related but different ways. Here's how to think about the choice — with your clinician.",
        "body": """
<p>If you're looking at a GLP-1 program, you'll run into two names constantly: <strong>semaglutide</strong> and <strong>tirzepatide</strong>. They're related but not identical, and programs sometimes specialize in one or the other. This is a plain-English guide to the difference — but the actual decision belongs with a licensed clinician who knows your history.</p>

<h2 id="what">What they are</h2>
<p>Semaglutide is a GLP-1 receptor agonist — it mimics a gut hormone that helps regulate appetite and blood sugar. It's the active ingredient in several well-known branded weight-loss and diabetes medications. Tirzepatide acts on GLP-1 <em>and</em> a second receptor (GIP), which is why it's sometimes described as a "dual" agonist. Both are given as weekly injections and both are titrated up gradually.</p>

<h2 id="differ">How they differ in practice</h2>
<p>The headline difference is mechanism — tirzepatide's dual action versus semaglutide's single pathway. In practice, the factors that tend to decide the choice are more mundane: how your body tolerates each, side-effect profile, availability and cost of the specific product, and your clinician's judgment about your health profile. Neither is universally "better"; they're tools matched to a person.</p>

<h2 id="choose">Practical factors that decide it</h2>
<ul>
  <li><strong>Tolerability.</strong> Some people handle one better than the other. Side effects and how gently you can titrate matter a lot.</li>
  <li><strong>Availability and cost.</strong> Supply and price for a specific product shift over time and can steer the decision.</li>
  <li><strong>Your health profile.</strong> Existing conditions and medications can make one option more appropriate.</li>
  <li><strong>Program specialization.</strong> Some programs are built around one medication — <a href="/reviews/trimrx">TrimRx</a>, for instance, focuses on tirzepatide.</li>
</ul>

<div class="callout"><h3>How to actually decide</h3><p>Don't pick the molecule from an article — pick a program with a clinician who'll help you choose and adjust. If you're undecided, a broad program keeps both doors open; if you've already settled on tirzepatide, a specialist may serve you better. Our <a href="/">comparison</a> flags which is which.</p></div>

<p class="muted"><em>This article is general educational information and not medical advice. It does not compare efficacy or safety and should not be used to self-select a medication. Talk to a licensed clinician.</em></p>
""",
    },
    {
        "slug": "what-happens-when-you-stop-glp1",
        "title": "What Happens When You Stop Taking GLP-1s?",
        "tag": "Guides",
        "date": "2026-09-05",
        "description": "Why weight can return after stopping a GLP-1 medication, what a maintenance plan looks like, and why the exit strategy is part of choosing a program.",
        "dek": "Stopping is a real decision with real consequences. The best time to think about it is before you start.",
        "body": """
<p>GLP-1 medications work while you take them by helping regulate appetite. That leads to an uncomfortable but important question people often skip at signup: what happens when you stop? Planning for that is one of the more overlooked parts of choosing a program — and one of the more important.</p>

<h2 id="why">Why weight can come back</h2>
<p>Because these medications act on appetite regulation, stopping them can bring back the hunger signals they were quieting. Without a plan to maintain the habits and results you built, some or much of the lost weight can return over time. This isn't a failure of willpower — it's how the medication works. The takeaway is that stopping should be a deliberate, supported process, not a cold turn-off.</p>

<h2 id="maintenance">What a maintenance plan looks like</h2>
<ul>
  <li><strong>A lower maintenance dose</strong> rather than a hard stop, where clinically appropriate.</li>
  <li><strong>Habit and nutrition support</strong> that was built up during treatment, so it doesn't all rest on the medication.</li>
  <li><strong>Continued check-ins</strong> to catch regain early and adjust.</li>
  <li><strong>A gradual taper</strong> guided by a clinician, not an abrupt end.</li>
</ul>

<h2 id="program">Why the exit strategy is part of choosing a program</h2>
<p>Programs that invest in coaching and ongoing support — not just prescriptions — are the ones best positioned to help you maintain results or come off safely. It's one of the reasons we weight <strong>ongoing clinical support</strong> so heavily in our scores. A program that only sells you the on-ramp has no answer for the off-ramp.</p>

<div class="callout"><h3>Before you start, ask</h3><p>"What does your maintenance or tapering plan look like?" A confident, specific answer is a good sign. A vague one tells you the program is built to sell medication, not results. Our <a href="/">top picks</a> all scored well on ongoing support.</p></div>

<p class="muted"><em>General information only, not medical advice. Never start, change, or stop a prescription medication without guidance from a licensed clinician.</em></p>
""",
    },
    {
        "slug": "how-to-spot-a-legit-online-clinic",
        "title": "How to Spot a Legit Online Weight-Loss Clinic (7 Red Flags)",
        "tag": "How it works",
        "date": "2026-09-04",
        "description": "A practical checklist for telling a trustworthy telehealth weight-loss program apart from one that's just moving product.",
        "dek": "The market moved fast, and not everyone kept up on safety. Here's a seven-point check before you hand over a card.",
        "body": """
<p>Online weight-loss programs exploded in popularity, and most of the well-known ones are legitimate. But fast-growing markets attract corner-cutters, and the difference between a careful clinic and one that's just moving product isn't always obvious from a slick landing page. Run any program through this seven-point check before you sign up.</p>

<h2 id="checklist">The 7-point check</h2>
<ol>
  <li><strong>Real clinical review.</strong> There should be a genuine medical evaluation by a licensed clinician — not an instant, guaranteed prescription off a form.</li>
  <li><strong>Named, licensed prescribers.</strong> You should be able to find out who is prescribing and that they're licensed in your area.</li>
  <li><strong>A way to reach someone.</strong> Legit programs give you a clear channel to a clinician for questions and side effects. If support is a black hole, walk away.</li>
  <li><strong>Transparent pricing.</strong> The total cost — medication, membership, visits — should be clear before you pay, not revealed at checkout.</li>
  <li><strong>Honest medication information.</strong> Clear detail on whether medications are branded or compounded, and which pharmacies are used.</li>
  <li><strong>Realistic claims.</strong> Be wary of guaranteed results or dramatic promises. Responsible programs describe typical outcomes, not miracles.</li>
  <li><strong>A sane cancellation and exit policy.</strong> No punitive lock-in, and a real answer for how you taper or maintain. See <a href="/guides/what-happens-when-you-stop-glp1">what happens when you stop</a>.</li>
</ol>

<div class="callout warn"><h3>Biggest single red flag</h3><p>A "guaranteed" prescription with no meaningful medical review. A clinician's job is to decide whether a medication is safe <em>for you</em> — a program that skips that isn't offering a shortcut, it's skipping the part that keeps you safe.</p></div>

<h2 id="how">How we apply this</h2>
<p>Every program in our lineup is scored on <strong>transparency</strong> and <strong>clinical support</strong> partly against this exact checklist. It's why our rankings favor programs with real clinician involvement even when cheaper options exist. Start with our <a href="/">comparison chart</a> and you've already cleared most of these checks.</p>

<p class="muted"><em>General information only, not medical advice. When in doubt about a provider's legitimacy, consult your own clinician or your regional health authority.</em></p>
""",
    },
]

# --------------------------------------------------------------------------
# Rendering helpers
# --------------------------------------------------------------------------
def cta(slug, label=None, cls="btn btn-primary btn-sm btn-block"):
    p = PROVIDERS[slug]
    label = label or f"Check {p['name']}"
    url = AFFILIATE_LINKS.get(slug, "#")
    rel = ' rel="sponsored nofollow" target="_blank"' if url != "#" else ""
    return f'<a class="{cls}" href="{html.escape(url, quote=True)}"{rel}>{label} →</a>'

def stars(score):
    filled = round(score / 2)  # 0-10 -> 0-5
    return "★" * filled + "☆" * (5 - filled)

# Provider logos: drop a file named <slug>.<ext> into assets/logos/ and it is
# picked up automatically. Falls back to the text name if no logo is present.
LOGO_EXTS = ["svg", "png", "webp", "jpg", "jpeg"]

def logo_src(slug):
    for ext in LOGO_EXTS:
        rel = f"assets/logos/{slug}.{ext}"
        if os.path.exists(os.path.join(ROOT, rel)):
            return "/" + rel
    return None

def logo_img(slug, cls="plogo"):
    src = logo_src(slug)
    if not src:
        return ""
    name = PROVIDERS[slug]["name"]
    return f'<img class="{cls}" src="{src}" alt="{name} logo" loading="lazy">'

TIER_MEANING = {"$": "Budget", "$$": "Mid-range", "$$$": "Premium"}

def review_url(slug):  return f"/reviews/{slug}"
def versus_url(v):     return f"/{v['a']}-vs-{v['b']}"
def article_url(a):    return f"/guides/{a['slug']}"

NAV = [
    ("Compare", "/"),
    ("Reviews", "/reviews"),
    ("Comparisons", "/comparisons"),
    ("Articles", "/guides"),
    ("How We Rank", "/methodology"),
]

# Inline icons (Heroicons-style, stroke=currentColor) — keeps everything crisp
# and theme-colored without external requests.
_IC = {
    "check": '<path d="M4.5 12.75l6 6 9-13.5" stroke-width="2"/>',
    "check-c": '<circle cx="12" cy="12" r="9" stroke-width="2"/><path d="M8.5 12.5l2.5 2.5 4.5-5" stroke-width="2"/>',
    "shield": '<path d="M12 3l7 3v5c0 4.5-3 7.6-7 9-4-1.4-7-4.5-7-9V6l7-3z" stroke-width="1.8"/><path d="M9 12l2 2 4-4" stroke-width="1.8"/>',
    "lock": '<rect x="5" y="11" width="14" height="9" rx="2" stroke-width="1.8"/><path d="M8 11V8a4 4 0 018 0v3" stroke-width="1.8"/>',
    "scale": '<path d="M12 4v16M7 20h10M6 8h12M6 8l-3 6a3 3 0 006 0L6 8zm12 0l-3 6a3 3 0 006 0l-3-6z" stroke-width="1.7"/>',
    "clipboard": '<rect x="5" y="5" width="14" height="16" rx="2" stroke-width="1.8"/><path d="M9 5V4a1 1 0 011-1h4a1 1 0 011 1v1M9 11h6M9 15h4" stroke-width="1.8"/>',
    "dollar": '<circle cx="12" cy="12" r="9" stroke-width="1.8"/><path d="M12 7v10M14.5 9.3C14 8.5 13 8 12 8c-1.4 0-2.5.8-2.5 2s1.1 1.8 2.5 2 2.5.8 2.5 2-1.1 2-2.5 2c-1 0-2-.5-2.5-1.3" stroke-width="1.6"/>',
    "user-check": '<circle cx="9" cy="8" r="3.2" stroke-width="1.8"/><path d="M3.5 20a5.5 5.5 0 0111 0M16 12l2 2 4-4" stroke-width="1.8"/>',
    "heart": '<path d="M12 20s-7-4.4-9.2-8.5C1.3 8.6 2.7 5.5 6 5.5c2 0 3.2 1.2 4 2.4.8-1.2 2-2.4 4-2.4 3.3 0 4.7 3.1 3.2 6C19 15.6 12 20 12 20z" stroke-width="1.7"/>',
    "spark": '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8L12 3z" stroke-width="1.6"/>',
    "chart": '<path d="M4 20V10M10 20V4M16 20v-7M4 20h16" stroke-width="1.9"/>',
    "badge": '<path d="M12 3l2.1 1.5 2.6-.2 1 2.4 2.2 1.4-.6 2.5.6 2.5-2.2 1.4-1 2.4-2.6-.2L12 21l-2.1-1.5-2.6.2-1-2.4L4.1 16l.6-2.5L4.1 11l2.2-1.4 1-2.4 2.6.2L12 3z" stroke-width="1.5"/><path d="M9 12l2 2 4-4" stroke-width="1.7"/>',
    "pill": '<rect x="3.5" y="8.5" width="17" height="7" rx="3.5" stroke-width="1.8"/><path d="M12 8.5v7" stroke-width="1.8"/>',
    "clock": '<circle cx="12" cy="12" r="9" stroke-width="1.8"/><path d="M12 7v5l3 2" stroke-width="1.8"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6" stroke-width="2"/>',
}

def icon(name, cls="", size=24):
    body = _IC.get(name, "")
    c = f' class="{cls}"' if cls else ""
    return (f'<svg{c} viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" '
            f'stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{body}</svg>')

def score_word(score):
    if score >= 9.5: return "Exceptional"
    if score >= 9.0: return "Excellent"
    if score >= 8.5: return "Great"
    if score >= 8.0: return "Very good"
    return "Good"

def sentence1(s):
    return re.split(r'(?<=[.!?])\s+', s.strip())[0]

# "Alternatives to X" money pages — built for the most-searched brands.
ALT_TARGETS = ["ro", "found", "embody", "medvi", "altrx"]

def alt_url(slug):
    return f"/{slug}-alternatives"

def header(active=""):
    def link(name, href):
        cur = ' aria-current="page"' if href == active else ""
        return f'<a href="{href}"{cur}>{name}</a>'
    links = "".join(link(name, href) for name, href in NAV)
    return f"""<header class="site-header"><div class="wrap">
  <a class="brand" href="/"><span class="brand-name">Weight&nbsp;Loss&nbsp;<em>Reviewed</em></span><span class="brand-tag">Compare the best GLP-1 weight-loss programs</span></a>
  <button class="nav-toggle" aria-label="Menu" onclick="document.getElementById('nav').classList.toggle('open')">☰</button>
  <nav class="nav" id="nav">{links}</nav>
</div></header>"""

def footer():
    review_links = "".join(f'<a href="{review_url(s)}">{PROVIDERS[s]["name"]} review</a>' for s in PROVIDER_ORDER)
    guide_links = "".join(f'<a href="{article_url(a)}">{a["title"].split(":")[0].split("(")[0].strip()}</a>' for a in ARTICLES[:4])
    return f"""<footer class="site-footer"><div class="wrap">
  <div class="foot-grid">
    <div>
      <a class="brand" href="/"><span class="brand-name">Weight&nbsp;Loss&nbsp;<em>Reviewed</em></span><span class="brand-tag">Compare the best GLP-1 weight-loss programs</span></a>
      <p>Independent, editorial scoring of online weight-loss programs. We rank what we'd actually recommend to a friend — and we tell you exactly how we score.</p>
      <p><a href="/methodology">Our scoring methodology →</a></p>
      <div class="foot-badges">
        <span>{icon('shield', size=16)} Independent</span>
        <span>{icon('lock', size=16)} Secure &amp; private</span>
        <span>{icon('user-check', size=16)} Clinician-informed</span>
      </div>
    </div>
    <div><h4>Reviews</h4>{review_links}</div>
    <div><h4>Popular guides</h4>{guide_links}<a href="/guides">All guides →</a></div>
  </div>
  <div class="foot-disclaim">
    <p><strong>Advertising disclosure:</strong> Weight Loss Reviewed is reader-supported. When you sign up through links on our site we may earn a commission, at no extra cost to you. This never changes our scores or rankings — see our <a href="/disclosure">full disclosure</a> and <a href="/methodology">methodology</a>.</p>
    <p><strong>Medical disclaimer:</strong> Nothing on this site is medical advice. GLP-1 and other weight-loss medications are prescription drugs; decisions about them belong to you and a licensed clinician. Content is for general information only.</p>
    <p>© {YEAR} Weight Loss Reviewed. All rights reserved.</p>
  </div>
</div></footer>"""

def base_page(title, description, path, body, active="", jsonld="", article_meta=None):
    canonical = SITE["domain"] + (path if path != "/" else "/")
    og_type = "article" if article_meta else "website"
    blocks = jsonld if isinstance(jsonld, (list, tuple)) else ([jsonld] if jsonld else [])
    ld = "".join(f'<script type="application/ld+json">{b}</script>' for b in blocks if b)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:site_name" content="{SITE['name']}">
<meta name="twitter:card" content="summary_large_image">
<meta name="robots" content="index,follow,max-image-preview:large">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Lora:ital,wght@0,400;0,500;0,600;0,700;1,400;1,600&display=swap">
<link rel="stylesheet" href="/assets/style.css?v={ASSET_VER}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%230d9488'/%3E%3Ctext x='16' y='22' font-size='15' font-family='Arial' font-weight='bold' fill='white' text-anchor='middle'%3EWR%3C/text%3E%3C/svg%3E">
{ld}
</head>
<body>
{header(active)}
{body}
{footer()}
</body>
</html>"""

def crumbs(items):
    parts = []
    for i, (name, href) in enumerate(items):
        if href and i < len(items) - 1:
            parts.append(f'<a href="{href}">{name}</a>')
        else:
            parts.append(f'<span>{name}</span>')
    return '<div class="wrap"><nav class="crumbs">' + ' › '.join(parts) + '</nav></div>'

# --------------------------------------------------------------------------
# JSON-LD builders
# --------------------------------------------------------------------------
def ld_org():
    return ('{"@context":"https://schema.org","@type":"Organization","name":"%s",'
            '"url":"%s","description":"Editorial reviews and rankings of online weight-loss programs."}'
            % (SITE["name"], SITE["domain"]))

def ld_website():
    # Helps Google/social show the site name as "Weight Loss Reviewed".
    return ('{"@context":"https://schema.org","@type":"WebSite","name":"%s",'
            '"alternateName":"weightlossreviewed.com","url":"%s"}'
            % (SITE["name"], SITE["domain"]))

def ld_product(p, slug):
    return ('{"@context":"https://schema.org","@type":"Product","name":"%s",'
            '"description":"%s","review":{"@type":"Review","reviewRating":'
            '{"@type":"Rating","ratingValue":"%s","bestRating":"10"},'
            '"author":{"@type":"Organization","name":"%s"}}}'
            % (p["name"], p["summary"].replace('"', "'"), p["score"], SITE["name"]))

def ld_article(a):
    return ('{"@context":"https://schema.org","@type":"Article","headline":"%s",'
            '"description":"%s","datePublished":"%s","dateModified":"%s",'
            '"author":{"@type":"Organization","name":"%s"},'
            '"publisher":{"@type":"Organization","name":"%s"}}'
            % (a["title"].replace('"', "'"), a["description"].replace('"', "'"),
               a["date"], a["date"], SITE["name"], SITE["name"]))

# Homepage FAQ — also emitted as FAQPage structured data.
FAQ = [
    ("How do online weight-loss programs work?",
     "You complete a medical intake online, a licensed clinician reviews it (often over a video or structured visit) to decide whether a medication such as a GLP-1 is appropriate and safe for you, and if so a prescription is sent to a pharmacy and delivered to your door. The better programs add coaching and ongoing check-ins on top of the prescription."),
    ("Who qualifies for a GLP-1 weight-loss medication?",
     "Eligibility is a clinical decision, but these medications are generally considered for adults with a higher body-mass index, or a slightly lower BMI alongside a weight-related condition. A licensed clinician weighs your full health history, current medications and any contraindications. No legitimate program can promise a prescription before that review."),
    ("How much do these programs cost?",
     "It varies widely by provider, medication (branded vs compounded), and your dose. Rather than publish prices that go stale within weeks, we show a relative tier ($–$$$) and link you to each provider's current offer. When comparing, always look at the total monthly cost at your expected maintenance dose — not just the intro price."),
    ("Is it safe to get weight-loss medication online?",
     "It can be, when there is a genuine clinical evaluation by a licensed prescriber, clear medication and pharmacy information, and a real way to reach someone about side effects. Be wary of any service that ‘guarantees’ a prescription with no meaningful review. Every program we rank is scored partly on exactly these safety signals."),
    ("Semaglutide or tirzepatide — which is better?",
     "Neither is universally better; they work in related but different ways, and the right choice depends on your tolerance, health profile, availability and your clinician's judgment. Some programs specialize in one. If you're undecided, a broad program keeps both options open."),
    ("Will I regain weight if I stop?",
     "Because these medications work on appetite regulation, stopping without a plan can bring hunger — and weight — back. That's why we weight ongoing coaching and maintenance support heavily: the programs that help you build habits and taper carefully give you the best shot at keeping results."),
    ("Can I use insurance for an online program?",
     "Sometimes. Coverage for GLP-1 medications varies a lot by plan and by whether the drug is branded or compounded. Some programs help you check and navigate insurance; many members pay out of pocket, which is part of why compounded options are popular. Check current coverage with the provider and your insurer."),
    ("How is this different from seeing my own doctor?",
     "The medicine and the need for a prescription are the same — the difference is convenience and structure. Online programs handle the visit, prescription, pharmacy and follow-up in one place, often with coaching built in. If you have a complex medical history, a provider with deeper clinical oversight (or your own physician) may be the better route."),
]

def ld_faq():
    items = ",".join(
        '{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}}'
        % (q.replace('"', "'"), a.replace('"', "'"))
        for q, a in FAQ
    )
    return '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[%s]}' % items

def ld_faq_custom(pairs):
    items = ",".join(
        '{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}}'
        % (q.replace('"', "'"), re.sub("<[^>]+>", "", ans).replace('"', "'"))
        for q, ans in pairs)
    return '{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[%s]}' % items

# --------------------------------------------------------------------------
# Page: Home (comparison chart)
# --------------------------------------------------------------------------
def provider_card(slug, i):
    p = PROVIDERS[slug]
    top = " top" if i == 1 else ""
    ribbon = f'<div class="ribbon">{icon("badge", size=15)} Editor\'s Choice</div>' if i == 1 else ""
    logo = logo_img(slug) or f'<span style="font-weight:800;color:var(--ink)">{p["name"]}</span>'
    lis = [f'<li class="offer">{icon("spark", size=16)}{p["highlight"]}</li>']
    lis += [f'<li>{icon("check", size=16)}{b}</li>' for b in p["bullets"]]
    bullets = "".join(lis)
    return f"""<article class="rowcard{top}" id="{slug}">
  {ribbon}
  <div class="rank">{i}</div>
  <div class="logo-cell">{logo}</div>
  <div class="cell cell-main">
    <div class="provider-name"><a href="{review_url(slug)}">{p['name']}</a> <span class="best-tag">{p['best_for']}</span></div>
    <div class="trust-inline"><span class="verified">{icon('check-c', size=15)} Independently reviewed</span>
      <span class="sep">•</span> <a href="{review_url(slug)}">Read our full review</a></div>
    <ul class="bullets">{bullets}</ul>
  </div>
  <div class="aside-cell">
    <div class="score-badge"><div class="score-num">{p['score']}<span>/10</span></div><div class="score-word">{score_word(p['score'])}</div></div>
    <div class="stars-row">{stars(p['score'])}</div>
    {cta(slug, label='View Plans', cls='btn btn-primary btn-sm btn-block')}
    <a class="btn btn-ghost btn-sm btn-block" href="{review_url(slug)}">Read review</a>
  </div>
</article>"""

def sidebar():
    mini = "".join(
        f'<li><span class="mr-num">{i}</span><a class="mr-name" href="{review_url(s)}">{PROVIDERS[s]["name"]}</a>'
        f'<span class="mr-score">{PROVIDERS[s]["score"]}</span></li>'
        for i, s in enumerate(PROVIDER_ORDER[:5], 1))
    return f"""<aside class="sidebar">
  <div class="widget widget-pad">
    <h4>Top rated</h4>
    <ul class="mini-rank">{mini}</ul>
  </div>
  <div class="widget widget-pad">
    <h4>Why trust us</h4>
    <ul class="trust-list">
      <li>{icon('shield')}<span><b>Independent</b>Commissions never change a score.</span></li>
      <li>{icon('user-check')}<span><b>Clinician-informed</b>Scored on real clinical support.</span></li>
      <li>{icon('scale')}<span><b>Transparent</b><a href="/methodology">See how we rank</a>.</span></li>
    </ul>
  </div>
  <div class="widget widget-pad widget-note">
    <p>Reader-supported. We may earn a commission from some links, at no cost to you — it never affects our rankings. <a href="/disclosure">Full disclosure</a>.</p>
  </div>
</aside>"""

def render_home():
    cards = "\n".join(provider_card(s, i) for i, s in enumerate(PROVIDER_ORDER, 1))
    vs_cards = "".join(
        f'<a class="post-card" href="{versus_url(v)}"><div class="thumb"></div><div class="pc-body">'
        f'<span class="tag">Comparison</span><h3>{PROVIDERS[v["a"]]["name"]} vs {PROVIDERS[v["b"]]["name"]}</h3>'
        f'<p>Scores {PROVIDERS[v["a"]]["score"]} vs {PROVIDERS[v["b"]]["score"]} — see who wins and why.</p>'
        f'<span class="read">Compare →</span></div></a>'
        for v in VERSUS[:3]
    )
    guide_cards = "".join(
        f'<a class="post-card" href="{article_url(a)}"><div class="thumb"></div><div class="pc-body">'
        f'<span class="tag">{a["tag"]}</span><h3>{a["title"]}</h3><p>{a["description"]}</p>'
        f'<span class="read">Read article →</span></div></a>'
        for a in ARTICLES[:3]
    )
    faq_html = "".join(
        f'<details><summary>{q}</summary><div class="faq-a"><p>{a}</p></div></details>'
        for q, a in FAQ
    )
    vs_links = "".join(
        f'<li><a href="{versus_url(v)}">{PROVIDERS[v["a"]]["name"]} vs {PROVIDERS[v["b"]]["name"]}</a></li>'
        for v in VERSUS[:5])
    article_links = "".join(
        f'<li><a href="{article_url(a)}">{a["title"]}</a></li>' for a in ARTICLES[:5])

    # full comparison table (all providers)
    trows = ""
    for i, slug in enumerate(PROVIDER_ORDER, 1):
        p = PROVIDERS[slug]
        cls = ' class="row-top"' if i == 1 else ''
        trows += (
            f'<tr{cls}><td class="rk">{i}</td>'
            f'<td class="attr"><a href="{review_url(slug)}">{p["name"]}</a></td>'
            f'<td>{p["best_for"]}</td>'
            f'<td class="hl">{p["highlight"]}</td>'
            f'<td class="pr" title="{TIER_MEANING[p["tier"]]}">{p["tier"]}</td>'
            f'<td class="sc"><strong>{p["score"]}</strong> <span class="muted">{score_word(p["score"])}</span></td>'
            f'<td>{cta(slug, label="View", cls="btn btn-primary btn-sm")}</td></tr>'
        )
    comparison_table = (
        '<table class="cmp cmp-full"><thead><tr>'
        '<th>#</th><th>Program</th><th>Best for</th><th>Highlight</th>'
        '<th>Price</th><th>Editor score</th><th></th></tr></thead>'
        f'<tbody>{trows}</tbody></table>'
    )

    body = f"""
<section class="hero hero-home"><div class="wrap">
  <span class="hero-flag"><span class="dot"></span> Updated {UPDATED} · Independently reviewed</span>
  <h1>The best online weight-loss programs</h1>
  <p class="lede">We score every GLP-1 program the same way — so you can compare the top online providers and find your fit in minutes.</p>
</div></section>

<div class="layout">
  <main class="main-col">
    <div class="chart-head"><h2>Top {len(PROVIDER_ORDER)} programs, ranked</h2><span class="muted" style="font-size:.9rem">Editor-scored · {UPDATED}</span></div>
    <div class="disclosure-note">{icon('badge', size=16)} <span>We may earn a commission when you sign up through our links — at no cost to you, and with no effect on our scores. <a href="/disclosure">How this works</a>.</span></div>
    <div class="chart">{cards}</div>
    <p class="muted" style="font-size:.85rem;margin-top:16px">Scores are our independent editorial rating out of 10. Price tiers ($–$$$) are relative indicators — always confirm current pricing with the provider.</p>
  </main>
  {sidebar()}
</div>

<section class="section"><div class="wrap">
  <h2 style="margin-top:0">Compare all {len(PROVIDER_ORDER)} programs</h2>
  <p class="muted" style="margin-bottom:18px">How every program scores side by side. Sorted by our editorial rating.</p>
  <div class="table-scroll">{comparison_table}</div>

  <div class="content-grid">
    <div>
      <h3>How to choose a weight-loss program</h3>
      <p>Most programs prescribe the same handful of GLP-1 medications, so the drug itself rarely sets them apart. What differs is the care around it — four things decide whether a program works for you:</p>
      <ul class="ticks">
        <li><b>Clinician access</b> — real visits and follow-up, not just an intake form.</li>
        <li><b>Medication options</b> — branded and compounded, with room to switch.</li>
        <li><b>Total cost</b> — what you pay at your maintenance dose, not just to start.</li>
        <li><b>Transparency</b> — pricing and terms clear before you commit.</li>
      </ul>
    </div>
    <div>
      <h3>Who can use these programs</h3>
      <p>GLP-1 medications are prescription treatments, so eligibility is decided by a licensed clinician — not a checklist. In practice they're usually considered for adults with a higher BMI, or a lower BMI alongside a weight-related condition. The clinician reviews your history, current medications and anything that would make the medication unsafe before prescribing.</p>
      <p class="note"><strong>This is information, not medical advice.</strong> Whether a medication is right for you is a decision for you and your clinician. GLP-1 drugs carry real risks and aren't right for everyone.</p>
    </div>
    <div>
      <h3>What it costs</h3>
      <p>Pricing changes often and depends on the provider, the medication and your dose, so each review uses a simple $–$$$ tier instead of a number that goes stale. When you compare, look at the total monthly cost at your maintenance dose — including membership and shipping — not just the introductory price. Our <a href="/guides/compounded-semaglutide-cost">guide to compounded semaglutide costs</a> breaks it down.</p>
    </div>
    <div>
      <h3>How we rank programs</h3>
      <p>Every program is scored out of 10 across the same six factors — clinician support, medication access, value, transparency, onboarding and the app — with support and access weighted most. We're reader-supported and may earn a commission, but it never changes a score. <a href="/methodology">Read the full methodology</a>.</p>
    </div>
  </div>

  <h2 id="faq">Frequently asked questions</h2>
  <div class="faq faq-grid">{faq_html}</div>
</div></section>

<section class="section section-soft"><div class="wrap">
  <div class="two-col-lists">
    <div>
      <h3>Compare programs</h3>
      <ul class="link-list">{vs_links}</ul>
      <a class="more" href="/comparisons">All comparisons →</a>
    </div>
    <div>
      <h3>Articles</h3>
      <ul class="link-list">{article_links}</ul>
      <a class="more" href="/guides">All articles →</a>
    </div>
  </div>
</div></section>
"""
    return base_page(
        f"Best Online Weight-Loss Programs ({YEAR}) — Ranked &amp; Scored | {SITE['name']}",
        f"We independently scored {len(PROVIDER_ORDER)} online weight-loss programs on clinician support, medication access, value and transparency. Compare the ranked chart.",
        "/", body, active="/", jsonld=[ld_website(), ld_org(), ld_faq()])

# --------------------------------------------------------------------------
# Page: Provider review
# --------------------------------------------------------------------------
def render_review(slug):
    p = PROVIDERS[slug]
    rank = PROVIDER_ORDER.index(slug) + 1
    pros = "".join(f"<li>{x}</li>" for x in p["pros"])
    cons = "".join(f"<li>{x}</li>" for x in p["cons"])
    sc_rows = ""
    for k in SUBSCORE_ORDER:
        v = p["subscores"][k]
        sc_rows += f'<div class="row"><span>{k}</span><span class="snum">{v}</span><span class="bar"><i style="width:{v*10}%"></i></span></div>'
    sc_rows += f'<div class="row"><span>Overall</span><span class="snum">{p["score"]}</span><span class="bar"><i style="width:{p["score"]*10}%"></i></span></div>'

    # related versus pages featuring this provider
    related = [v for v in VERSUS if slug in (v["a"], v["b"])][:3]
    rel_cards = "".join(
        f'<a class="post-card" href="{versus_url(v)}"><div class="thumb"></div><div class="pc-body">'
        f'<h3>{PROVIDERS[v["a"]]["name"]} vs {PROVIDERS[v["b"]]["name"]}</h3>'
        f'<span class="read">Compare →</span></div></a>' for v in related)

    body = f"""
{crumbs([("Home","/"),("Reviews","/reviews"),(p["name"]+" Review", "")])}
<section class="hero"><div class="wrap narrow">
  <span class="hero-flag"><span class="dot"></span> Ranked #{rank} of {len(PROVIDER_ORDER)} · {p['best_for']}</span>
  {f'<div><span class="hero-logo"><img src="{logo_src(slug)}" alt="{p["name"]} logo"></span></div>' if logo_src(slug) else ''}
  <h1>{p['name']} Review ({YEAR})</h1>
  <div class="meta-line"><span class="chip-score">{p['score']}<span style="font-weight:600">/10</span></span>
    <span class="stars">{stars(p['score'])}</span>
    <span class="tag">{score_word(p['score'])}</span>
    <span class="tag">{p['tier']} · {TIER_MEANING[p['tier']]}</span>
    <span>Updated {UPDATED}</span></div>
  <p class="lede">{p['summary']}</p>
  <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:8px">{cta(slug, label=f"View {p['name']} plans", cls='btn btn-primary')}
    <a class="btn btn-ghost" href="#scorecard">Jump to scorecard</a></div>
</div></section>

<div class="wrap narrow article-body" style="padding-top:26px">
  <div class="disclosure-note">{icon('badge', size=16)} <span>We may earn a commission if you sign up through our links — at no cost to you, and with no effect on this score. <a href="/disclosure">Details</a>.</span></div>

  <div class="callout"><h3>{icon('badge')} Our verdict</h3><p>{p['verdict']}</p>
    <p style="margin-bottom:0">{cta(slug, label=f"View {p['name']} plans", cls='btn btn-primary btn-sm')}</p></div>

  <h2 id="scorecard">Scorecard</h2>
  <div class="scorecard">{sc_rows}</div>

  <h2>Pros &amp; cons</h2>
  <div class="proscons">
    <div class="box pros"><h4>{icon('check-c', size=20)} What we liked</h4><ul class="pros">{pros}</ul></div>
    <div class="box cons"><h4>What to weigh</h4><ul class="cons">{cons}</ul></div>
  </div>

  <h2>Who it's for</h2>
  <p>{p['name']} is our pick for <strong>{p['best_for'].lower()}</strong>. {p['highlight']}</p>
  <p>As with any GLP-1 program, whether it's right for you depends on your health profile and goals — and ultimately on a conversation with a licensed clinician. Use our score as a starting point, not a prescription.</p>

  <div class="cta-strip">
    <h2>Ready to look at {p['name']}?</h2>
    <p>Check current plans and pricing directly with the provider.</p>
    {cta(slug, label=f"Visit {p['name']}", cls='btn btn-primary')}
  </div>
</div>

<section class="section section-alt"><div class="wrap">
  <h2 style="margin-top:0">{p['name']} compared</h2>
  <div class="post-grid">{rel_cards}</div>
</div></section>
"""
    return base_page(
        f"{p['name']} Review ({YEAR}): Is It Worth It? Score {p['score']}/10 | {SITE['name']}",
        f"Our {p['name']} review — scored {p['score']}/10. {p['summary'][:110]}",
        review_url(slug), body, active="/reviews", jsonld=ld_product(p, slug))

# --------------------------------------------------------------------------
# Page: Versus / battle
# --------------------------------------------------------------------------
def render_versus(v):
    a, b = PROVIDERS[v["a"]], PROVIDERS[v["b"]]
    An, Bn = a["name"], b["name"]
    win_a = " win" if v["winner"] == v["a"] else ""
    win_b = " win" if v["winner"] == v["b"] else ""
    winner = PROVIDERS[v["winner"]]["name"]
    flag_a = f'<div class="win-flag">{icon("badge", size=13)} Winner</div>' if v["winner"] == v["a"] else ""
    flag_b = f'<div class="win-flag">{icon("badge", size=13)} Winner</div>' if v["winner"] == v["b"] else ""

    def first_sentence(s):
        return re.split(r'(?<=[.!?])\s+', s.strip())[0]

    def human_list(items):
        items = [i.lower() for i in items]
        if len(items) == 1: return items[0]
        if len(items) == 2: return f"{items[0]} and {items[1]}"
        return ", ".join(items[:-1]) + f", and {items[-1]}"

    # specs table — use hand-written rows if present, else auto from sub-scores
    def qual(x):
        return ("Extensive" if x >= 9.2 else "Strong" if x >= 8.7 else "Solid" if x >= 8.2
                else "Good" if x >= 7.8 else "Basic")
    rows = v.get("rows")
    if not rows:
        rows = [
            ("Clinician support", qual(a["subscores"]["Clinical support"]), qual(b["subscores"]["Clinical support"])),
            ("Medication access", qual(a["subscores"]["Medication access"]), qual(b["subscores"]["Medication access"])),
            ("Ease of starting", qual(a["subscores"]["Onboarding"]), qual(b["subscores"]["Onboarding"])),
            ("Value for money", qual(a["subscores"]["Value"]), qual(b["subscores"]["Value"])),
            ("Typical price", f"{a['tier']} · {TIER_MEANING[a['tier']]}", f"{b['tier']} · {TIER_MEANING[b['tier']]}"),
        ]
    trows = ""
    trows += f'<tr><td class="attr">Editor rating</td><td><strong>{a["score"]}/10</strong> · {score_word(a["score"])}</td><td><strong>{b["score"]}/10</strong> · {score_word(b["score"])}</td></tr>'
    trows += f'<tr><td class="attr">Best for</td><td>{a["best_for"]}</td><td>{b["best_for"]}</td></tr>'
    for attr, va, vb in rows:
        trows += f'<tr><td class="attr">{attr}</td><td>{va}</td><td>{vb}</td></tr>'

    # round-by-round breakdown, driven by the sub-scores
    rounds_html = ""; wins_a = wins_b = 0
    for cat in ROUND_ORDER:
        sa, sb = a["subscores"][cat], b["subscores"][cat]
        diff = round(sa - sb, 1)
        if abs(diff) < 0.15:
            win_name = None; sent = f"{An} and {Bn} are evenly matched."
        elif diff > 0:
            wins_a += 1; win_name = An
            deg = "clearly ahead" if diff >= 0.6 else ("a step ahead" if diff >= 0.3 else "just ahead")
            sent = f"{An} scores {sa} to {sb} — {deg}."
        else:
            wins_b += 1; win_name = Bn
            deg = "clearly ahead" if -diff >= 0.6 else ("a step ahead" if -diff >= 0.3 else "just ahead")
            sent = f"{Bn} scores {sb} to {sa} — {deg}."
        win_tag = (f'<span class="win">Winner: {win_name}</span>' if win_name
                   else '<span class="win" style="color:var(--muted);background:var(--surface-2)">Even</span>')
        rounds_html += (f'<div class="vs-round"><h3>{cat}</h3>'
                        f'<p>{CATEGORY_FRAMES[cat]} {sent}</p>'
                        f'<div class="rd-scores">{An} <b>{sa}</b> · {Bn} <b>{sb}</b>{win_tag}</div></div>')
    even = 6 - wins_a - wins_b
    tally = f"{An} takes {wins_a}, {Bn} takes {wins_b}" + (f", with {even} even" if even else "") + "."

    # where they differ / agree
    gaps = sorted(((c, a["subscores"][c], b["subscores"][c]) for c in ROUND_ORDER),
                  key=lambda x: abs(x[1] - x[2]), reverse=True)
    big = [(c, sa, sb) for c, sa, sb in gaps if abs(sa - sb) >= 0.3][:2]
    if big:
        parts = []
        for c, sa, sb in big:
            w = An if sa > sb else Bn
            parts.append(f"<strong>{c.lower()}</strong>, where {w} leads {max(sa,sb)} to {min(sa,sb)}")
        differ = "The clearest daylight between them shows up in " + " and ".join(parts) + ". "
    else:
        differ = "No single category blows the other away — the gaps are incremental rather than dramatic. "
    differ += f"Zoom out and the split is simple: {An} is our pick for {a['best_for'].lower()}, while {Bn} earns {Bn}'s place as {b['best_for'].lower()}."
    close = [c for c, sa, sb in gaps if abs(sa - sb) <= 0.2]
    similar = (f"On {human_list(close)}, there's little to separate them — both land within a couple of tenths, so those categories won't decide your choice."
               if close else "")

    # pricing
    ta, tb = a["tier"], b["tier"]
    if ta == tb:
        pricing = f"{An} and {Bn} both sit in the {TIER_MEANING[ta].lower()} range ({ta}), so price isn't the deciding factor between them."
        cheaper_note = "Neither is dramatically cheaper than the other"
    else:
        if len(ta) < len(tb):
            pricing = f"{An} is the more budget-friendly of the two ({ta}, {TIER_MEANING[ta].lower()}), while {Bn} sits higher ({tb}, {TIER_MEANING[tb].lower()})."
            cheaper_note = f"{An} is the cheaper option"
        else:
            pricing = f"{Bn} is the more budget-friendly of the two ({tb}, {TIER_MEANING[tb].lower()}), while {An} sits higher ({ta}, {TIER_MEANING[ta].lower()})."
            cheaper_note = f"{Bn} is the cheaper option"

    # matchup FAQ
    if v["winner"] == v["a"]:
        wname, lname, ws, ls, wcount, loser_pick = An, Bn, a["score"], b["score"], wins_a, v["pick_b"]
    else:
        wname, lname, ws, ls, wcount, loser_pick = Bn, An, b["score"], a["score"], wins_b, v["pick_a"]
    lp = loser_pick[0].lower() + loser_pick[1:]
    med_better = An if a["subscores"]["Medication access"] >= b["subscores"]["Medication access"] else Bn
    clin_better = An if a["subscores"]["Clinical support"] >= b["subscores"]["Clinical support"] else Bn
    app_better = An if a["subscores"]["App & tracking"] >= b["subscores"]["App & tracking"] else Bn
    vfaq = [
        (f"Is {An} better than {Bn}?",
         f"In our scoring, {wname} comes out ahead — {ws}/10 to {ls}/10, winning {wcount} of the six categories we rate. That makes it our pick for most people. {lname} is still the better choice if {lp}"),
        (f"Which is cheaper, {An} or {Bn}?",
         f"{cheaper_note}. {pricing} Whichever you lean toward, compare the total cost at your maintenance dose — not just the introductory price."),
        (f"Do {An} and {Bn} prescribe the same medications?",
         f"Both work from the same GLP-1 toolkit — semaglutide and/or tirzepatide, branded or compounded depending on the plan. On medication access and flexibility, {med_better} scores a little higher in our review. Availability of any specific product shifts over time, so confirm current options with each provider."),
        (f"Which has better clinician support, {An} or {Bn}?",
         f"{clin_better} edges ahead on clinical support in our scoring — that's the depth of real clinician time and follow-up you get. Both include a genuine medical review; the difference is how much ongoing access comes with it."),
        (f"Are {An} and {Bn} legit?",
         f"Both meet the bar we score for: a real evaluation by a licensed clinician before any prescription, clear medication information, and a way to reach someone with questions. Neither should issue a GLP-1 without a proper review."),
        (f"Which has the better app, {An} or {Bn}?",
         f"{app_better} has the edge on day-to-day tools and tracking in our scoring. If living in an app and logging progress matters to you, that's worth weighing; if you mostly want the medication handled, it matters less."),
        (f"Can I switch between {An} and {Bn}?",
         f"Generally, yes. Neither program locks you into a long contract, so if you start with one and it isn't the right fit you can move to the other. Just never stop or change a GLP-1 medication without talking to your clinician first."),
    ]
    vfaq_html = "".join(f'<details><summary>{q}</summary><div class="faq-a"><p>{ans}</p></div></details>' for q, ans in vfaq)

    intro = (f"<strong>{An} and {Bn} prescribe the same GLP-1 medications — so what really separates them is the care around the prescription.</strong> "
             f"{An} is our pick for {a['best_for'].lower()}; {Bn}, for {b['best_for'].lower()}. Here's how they stack up, category by category.")
    # bold the actual verdict (first sentence), keep the rest lighter
    vparts = re.split(r'(?<=[.!?])\s+', v['verdict'].strip(), maxsplit=1)
    verdict_html = f"<strong>{vparts[0]}</strong>" + (f" {vparts[1]}" if len(vparts) > 1 else "")
    # sticky mobile CTA bar — winner on the left, more prominent
    w_slug = v["winner"]; l_slug = v["b"] if w_slug == v["a"] else v["a"]
    def visit_btn(slug, cls):
        url = AFFILIATE_LINKS.get(slug, "#")
        rel = ' rel="sponsored nofollow" target="_blank"' if url != "#" else ""
        return f'<a class="{cls}" href="{html.escape(url, quote=True)}"{rel}>Visit {PROVIDERS[slug]["name"]}</a>'
    sticky = (f'<div class="vs-sticky">{visit_btn(w_slug, "vs-sticky-btn win")}'
              f'{visit_btn(l_slug, "vs-sticky-btn")}</div><div class="vs-sticky-spacer"></div>')

    def mast_logo(slug):
        src = logo_src(slug)
        inner = (f'<img src="{src}" alt="{PROVIDERS[slug]["name"]} logo">' if src
                 else f'<span>{PROVIDERS[slug]["name"]}</span>')
        return f'<div class="vs-mast-logo">{inner}</div>'

    body = f"""
<section class="vs-hero"><div class="wrap">
  {crumbs([("Home","/"),("Comparisons","/comparisons"),(f'{An} vs {Bn}', "")])}
  <span class="flag">{icon('scale', size=15)} Head-to-head comparison · Updated {UPDATED}</span>
  <h1>{An} vs {Bn}</h1>
  <p class="lede">{v['intro']}</p>
</div></section>

<div class="wrap wide article-body" style="padding-top:36px">
  <p style="font-size:1.1rem;margin-bottom:1.4em">{intro}</p>

  <div class="callout"><h3>Bottom line: {winner} wins</h3><p>{verdict_html}</p>
    <p style="margin:16px 0 0">{cta(v['winner'], label=f"View {winner} plans", cls='btn btn-primary btn-sm')}</p></div>

  <h2>Round by round</h2>
  <p>We scored both programs on the six things that actually decide a weight-loss plan. {tally} Here's how each category shook out.</p>
  <div class="vs-rounds">{rounds_html}</div>

  <h2>Where they differ most</h2>
  <p>{differ}</p>
  {f'<p>{similar}</p>' if similar else ''}

  <h2>Pricing: {An} vs {Bn}</h2>
  <p>{pricing} Remember that prices move constantly and depend on your dose, so treat the tiers as a guide and confirm the current number with each provider. The figure that matters is the total monthly cost once you reach your maintenance dose — a cheap starter price can climb. We unpack this in <a href="/guides/compounded-semaglutide-cost">how much compounded semaglutide costs</a>.</p>

  <h2>The specs, side by side</h2>
  <div class="table-scroll"><table class="cmp">
    <thead><tr><th>&nbsp;</th><th>{An}</th><th>{Bn}</th></tr></thead>
    <tbody>{trows}</tbody>
  </table></div>

  <h2>Which should you pick?</h2>
  <div class="proscons">
    <div class="box pros"><h4>Choose {An} if…</h4><p style="margin:0 0 14px;color:var(--ink-soft)">{v['pick_a']}</p>
      {cta(v['a'], label=f"View {An} plans", cls='btn btn-primary btn-sm')}</div>
    <div class="box pros"><h4>Choose {Bn} if…</h4><p style="margin:0 0 14px;color:var(--ink-soft)">{v['pick_b']}</p>
      {cta(v['b'], label=f"View {Bn} plans", cls='btn btn-primary btn-sm')}</div>
  </div>

  <h2>Common questions</h2>
  <div class="faq">{vfaq_html}</div>

  <div class="cta-strip">
    <h2>Our pick: {winner}</h2>
    <p>{winner} came out ahead across our scoring. Check its current plans and offer directly with the provider.</p>
    {cta(v['winner'], label=f"View {winner} plans", cls='btn btn-primary btn-lg')}
  </div>

  <p class="muted" style="font-size:.88rem">Both programs are scored with the same independent <a href="/methodology">methodology</a>. We may earn a commission from either provider — it changes nothing about the scores or the verdict. Pricing tiers are relative; confirm current prices with each provider. Nothing here is medical advice.</p>
</div>
{sticky}
"""
    ttl = f"{An} vs {Bn} ({YEAR}): Which Is Better? | {SITE['name']}"
    desc = f"{An} vs {Bn} compared across six categories — clinician support, medications, cost, onboarding and more — with a clear verdict on which wins."
    return base_page(ttl, desc, versus_url(v), body, active="/comparisons", jsonld=ld_faq_custom(vfaq))

# --------------------------------------------------------------------------
# Page: Alternatives to <brand>
# --------------------------------------------------------------------------
def render_alternatives(target):
    t = PROVIDERS[target]
    Tn = t["name"]
    alts = [s for s in PROVIDER_ORDER if s != target][:6]

    items = ""
    for i, slug in enumerate(alts, 1):
        p = PROVIDERS[slug]
        # is there a direct comparison page for this pair?
        vpair = next((vv for vv in VERSUS if {vv["a"], vv["b"]} == {target, slug}), None)
        vlink = f' · <a href="{versus_url(vpair)}">{Tn} vs {p["name"]}</a>' if vpair else ""
        why = f"{p['highlight']} We score it {p['score']}/10 — our pick for {p['best_for'].lower()}."
        items += f"""<div class="alt-item">
  <div class="alt-rank">{i}</div>
  <div class="alt-main">
    <div class="alt-name"><a href="{review_url(slug)}">{p['name']}</a> <span class="best-tag">{p['best_for']}</span></div>
    <p>{why}</p>
    <div class="alt-links"><a href="{review_url(slug)}">Read review</a>{vlink}</div>
  </div>
  <div class="alt-side">
    <div class="score-num">{p['score']}<span>/10</span></div>
    <div class="score-word">{score_word(p['score'])}</div>
    {cta(slug, label='View Plans', cls='btn btn-primary btn-sm btn-block')}
  </div>
</div>"""

    top = alts[0]
    body = f"""
<section class="hero"><div class="wrap narrow">
  {crumbs([("Home","/"),("Comparisons","/comparisons"),(f'{Tn} alternatives', "")])}
  <span class="hero-flag"><span class="dot"></span> {len(alts)} alternatives · Updated {UPDATED}</span>
  <h1>The best {Tn} alternatives</h1>
  <p class="lede">{Tn} is a strong program — {sentence1(t['summary']).rstrip('.')} — but it isn't the right fit for everyone. Here are the {Tn} alternatives we rate most highly, scored on the same <a href="/methodology">methodology</a>.</p>
</div></section>

<div class="wrap wide article-body" style="padding-top:32px">
  <p>Maybe you want a lower price, more coaching, a different medication, or simply a second opinion before you commit. Whatever the reason, these programs are the closest {Tn} competitors worth your time — ranked by our editorial score. Still weighing {Tn} itself? Read our <a href="{review_url(target)}">full {Tn} review</a>.</p>

  <div class="alt-list">{items}</div>

  <div class="callout"><h3>{icon('badge')} Our top {Tn} alternative: {PROVIDERS[top]['name']}</h3>
    <p>{PROVIDERS[top]['summary']}</p>
    <p style="margin:14px 0 0">{cta(top, label=f"View {PROVIDERS[top]['name']} plans", cls='btn btn-primary btn-sm')}</p></div>

  <p class="muted" style="font-size:.88rem">Rankings are our independent editorial scores, built on the same <a href="/methodology">methodology</a>. We may earn a commission from links here — it never affects our scoring. Pricing tiers are relative; confirm current prices with each provider. Nothing here is medical advice.</p>
</div>
"""
    ttl = f"{len(alts)} Best {Tn} Alternatives ({YEAR}) — Compared &amp; Ranked | {SITE['name']}"
    desc = f"Looking for a {Tn} alternative? We ranked the {len(alts)} best competitors on clinician support, medication access, value and transparency."
    return base_page(ttl, desc, alt_url(target), body, active="/comparisons", jsonld=ld_org())

# --------------------------------------------------------------------------
# Page: Article
# --------------------------------------------------------------------------
def render_article(a):
    # build a simple TOC from h2 ids
    heads = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', a["body"])
    toc = ""
    if len(heads) >= 3:
        items = "".join(f'<li><a href="#{hid}">{re.sub("<.*?>","",txt)}</a></li>' for hid, txt in heads)
        toc = f'<div class="toc"><strong>In this guide</strong><ol>{items}</ol></div>'
    d = datetime.datetime.strptime(a["date"], "%Y-%m-%d").strftime("%B %-d, %Y")
    body = f"""
{crumbs([("Home","/"),("Guides","/guides"),(a["title"][:40]+("…" if len(a["title"])>40 else ""), "")])}
<div class="wrap narrow">
  <div style="padding-top:22px">
    <span class="tag">{a['tag']}</span>
    <h1 style="margin-top:14px">{a['title']}</h1>
    <div class="meta-line"><span>By the {SITE['name']} team</span><span>·</span><span>{d}</span></div>
    <p class="lede">{a['dek']}</p>
  </div>
  {toc}
  <div class="article-body">{a['body']}</div>

  <div class="cta-strip">
    <h2>Compare the top-rated programs</h2>
    <p>See how the leading online weight-loss programs score head to head.</p>
    <a class="btn btn-primary" href="/">See the rankings →</a>
  </div>
</div>
"""
    return base_page(f"{a['title']} | {SITE['name']}", a["description"],
                     article_url(a), body, active="/guides",
                     jsonld=ld_article(a), article_meta=True)

# --------------------------------------------------------------------------
# Index pages
# --------------------------------------------------------------------------
def render_reviews_index():
    cards = ""
    for i, slug in enumerate(PROVIDER_ORDER, 1):
        p = PROVIDERS[slug]
        cards += f"""<a class="post-card" href="{review_url(slug)}"><div class="thumb"></div><div class="pc-body">
  <span class="tag">#{i} · {p['best_for']}</span>
  <h3>{p['name']} <span style="color:var(--muted);font-weight:700">— {p['score']}/10</span></h3>
  <p>{p['highlight']}</p><span class="read">Read review →</span></div></a>"""
    body = f"""
<section class="hero"><div class="wrap">
  {crumbs([("Home","/"),("Reviews","")])}
  <span class="hero-flag">{len(PROVIDER_ORDER)} in-depth, independent reviews</span>
  <h1>Online weight-loss program reviews</h1>
  <p class="lede">Independently scored reviews of each program — the good, the trade-offs, and who it's really for.</p>
</div></section>
<section class="section"><div class="wrap"><div class="post-grid">{cards}</div></div></section>
"""
    return base_page(f"Online Weight-Loss Program Reviews ({YEAR}) | {SITE['name']}",
                     "In-depth, independently scored reviews of the top online weight-loss programs, including pros, cons and who each is best for.",
                     "/reviews", body, active="/reviews", jsonld=ld_org())

def render_versus_index():
    cards = ""
    for v in VERSUS:
        a, b = PROVIDERS[v["a"]], PROVIDERS[v["b"]]
        cards += f"""<a class="post-card" href="{versus_url(v)}"><div class="thumb"></div><div class="pc-body">
  <h3>{a['name']} vs {b['name']}</h3>
  <p>{a['name']} ({a['score']}) vs {b['name']} ({b['score']}). {v['intro'][:90]}…</p>
  <span class="read">See the verdict →</span></div></a>"""
    alt_cards = "".join(
        f'<a class="post-card" href="{alt_url(s)}"><div class="thumb"></div><div class="pc-body">'
        f'<span class="tag">Alternatives</span><h3>{PROVIDERS[s]["name"]} alternatives</h3>'
        f'<p>The best {PROVIDERS[s]["name"]} competitors, ranked and compared.</p>'
        f'<span class="read">See alternatives →</span></div></a>'
        for s in ALT_TARGETS)
    body = f"""
<section class="hero"><div class="wrap">
  {crumbs([("Home","/"),("Comparisons","")])}
  <span class="hero-flag">{len(VERSUS)} head-to-head matchups</span>
  <h1>Weight-loss program comparisons</h1>
  <p class="lede">Deciding between two programs? Each comparison breaks the matchup down to a clear, honest verdict.</p>
</div></section>
<section class="section"><div class="wrap"><div class="post-grid">{cards}</div></div></section>
<section class="section section-soft"><div class="wrap">
  <h2 style="margin-top:0">Looking for alternatives?</h2>
  <p class="lead">Shopping away from a specific brand? These round up the best competitors, ranked.</p>
  <div class="post-grid">{alt_cards}</div>
</div></section>
"""
    return base_page(f"Weight-Loss Program Comparisons: Head-to-Head ({YEAR}) | {SITE['name']}",
                     "Side-by-side comparisons of the top online weight-loss programs — scores, pricing tiers and a clear verdict on each matchup.",
                     "/comparisons", body, active="/comparisons", jsonld=ld_org())

def render_guides_index():
    cards = ""
    for a in ARTICLES:
        cards += f"""<a class="post-card" href="{article_url(a)}"><div class="thumb"></div><div class="pc-body">
  <span class="tag">{a['tag']}</span><h3>{a['title']}</h3><p>{a['description']}</p>
  <span class="read">Read article →</span></div></a>"""
    body = f"""
<section class="hero"><div class="wrap">
  {crumbs([("Home","/"),("Articles","")])}
  <span class="hero-flag">{len(ARTICLES)} articles &amp; guides</span>
  <h1>Weight-loss articles &amp; guides</h1>
  <p class="lede">Plain-English answers to the questions people actually ask before choosing a GLP-1 program.</p>
</div></section>
<section class="section"><div class="wrap"><div class="post-grid">{cards}</div></div></section>
"""
    return base_page(f"Weight-Loss Guides & Answers ({YEAR}) | {SITE['name']}",
                     "Clear, practical guides on GLP-1 programs, costs, prescriptions and how to choose a legitimate online weight-loss clinic.",
                     "/guides", body, active="/guides", jsonld=ld_org())

# --------------------------------------------------------------------------
# Static pages
# --------------------------------------------------------------------------
def render_methodology():
    weights = [
        ("Clinical support", "Do you get real clinician access and coaching that lasts beyond signup?"),
        ("Medication access", "Range of GLP-1 options and how easily the plan adapts to supply and budget."),
        ("Value", "Total cost for what you get — judged against comparable programs, not in a vacuum."),
        ("Transparency", "Is pricing and medication information clear before you pay?"),
        ("Onboarding", "How fast and painless it is to get started, without cutting clinical corners."),
        ("App & tracking", "Quality of the tools you use day to day."),
    ]
    rows = "".join(f'<tr><td class="attr">{n}</td><td>{d}</td></tr>' for n, d in weights)
    body = f"""
<section class="hero"><div class="wrap narrow">
  {crumbs([("Home","/"),("How We Rank","")])}
  <span class="hero-flag">Editorial standards</span>
  <h1>How we score weight-loss programs</h1>
  <p class="lede">Our rankings are opinions, but they're not arbitrary. Here's exactly what we measure and how we keep it honest.</p>
</div></section>
<div class="wrap narrow article-body" style="padding-top:26px">
  <h2 style="margin-top:0">What we score</h2>
  <p>Every program gets an overall score out of 10, built from six sub-scores. We weight support and access most heavily, because they're what actually determine whether a program works for real people over time.</p>
  <div class="table-scroll"><table class="cmp"><thead><tr><th>Factor</th><th>What it captures</th></tr></thead><tbody>{rows}</tbody></table></div>

  <h2>How we keep it independent</h2>
  <p>We're reader-supported: when you sign up through our links we may earn a commission. That funds the site, but it does not buy a better score or a higher ranking. Commissions do not factor into our scoring at all — a program we earn nothing from can outrank one we do, and sometimes does.</p>

  <h2>About pricing tiers</h2>
  <p>Because prices and promotions change constantly — and vary by dose and pharmacy — we show a relative tier ($, $$, $$$) rather than a fixed number that would be out of date within weeks. For current pricing, always check the provider directly through the "check offer" links.</p>

  <h2>What we don't do</h2>
  <ul>
    <li>We don't give medical advice or compare the clinical efficacy of medications.</li>
    <li>We don't publish fabricated prices or invent facts about a provider.</li>
    <li>We don't let a commission change a score. Ever.</li>
  </ul>

  <div class="callout"><h3>Spotted something wrong?</h3><p>Programs change. If a detail is out of date or we've got something wrong, tell us at <a href="mailto:{SITE['email']}">{SITE['email']}</a> and we'll review it.</p></div>
</div>
"""
    return base_page(f"How We Score Weight-Loss Programs — Methodology | {SITE['name']}",
                     "Our editorial methodology: the six factors we score, how we weight them, and how we stay independent from the commissions that fund the site.",
                     "/methodology", body, active="/methodology", jsonld=ld_org())

def render_about():
    body = f"""
<section class="hero"><div class="wrap narrow">
  {crumbs([("Home","/"),("About","")])}
  <span class="hero-flag">About us</span>
  <h1>Why Weight Loss Reviewed exists</h1>
  <p class="lede">Choosing an online weight-loss program is confusing on purpose. We cut through it.</p>
</div></section>
<div class="wrap narrow article-body" style="padding-top:26px">
  <p>The online weight-loss market exploded, and the marketing got very good at making every program look identical and every promise look guaranteed. It's genuinely hard to tell a careful, clinician-led program from one that's just moving product.</p>
  <p>Weight Loss Reviewed is our attempt to fix that. We score programs on the things that actually matter — real clinical support, medication access, honest pricing and transparency — and we publish <a href="/methodology">exactly how we do it</a>. Our goal is simple: recommend what we'd tell a friend to use.</p>
  <h2>How we make money</h2>
  <p>We're reader-supported. When you sign up through our links, we may earn a commission at no extra cost to you. That never changes our scores or rankings — read our <a href="/disclosure">full disclosure</a> for the details.</p>
  <h2>A note on medical advice</h2>
  <p>We're a review site, not a clinic. Nothing here is medical advice, and we never compare the clinical efficacy of medications. Whether a weight-loss medication is right for you is a decision for you and a licensed clinician.</p>
  <p>Questions or corrections? Reach us at <a href="mailto:{SITE['email']}">{SITE['email']}</a>.</p>
</div>
"""
    return base_page(f"About {SITE['name']}",
                     "Weight Loss Reviewed scores online weight-loss programs independently, on the factors that actually decide results. Here's who we are and how we work.",
                     "/about", body, jsonld=ld_org())

def render_disclosure():
    body = f"""
{crumbs([("Home","/"),("Disclosure","")])}
<div class="wrap narrow article-body" style="padding-top:26px">
  <h1>Advertising &amp; medical disclosure</h1>
  <p class="muted">Last updated {UPDATED}</p>

  <h2>Advertising / affiliate disclosure</h2>
  <p>{SITE['name']} is reader-supported. Some links on this site are affiliate or sponsored links, which means we may earn a commission if you sign up or make a purchase through them — at no additional cost to you. These commissions help fund the site.</p>
  <p>Earning a commission never influences our editorial scores, rankings, or verdicts. We score programs using a consistent <a href="/methodology">methodology</a>, and a program we earn no commission from can and does outrank one we do. Sponsored or affiliate links are marked with <code>rel="sponsored nofollow"</code> where applicable.</p>

  <h2>Medical disclaimer</h2>
  <p>The content on {SITE['name']} is provided for general informational and educational purposes only and is <strong>not medical advice</strong>. It is not a substitute for professional medical advice, diagnosis, or treatment. GLP-1 and other weight-loss medications are prescription drugs that carry risks and are not appropriate for everyone.</p>
  <p>Always seek the advice of a licensed physician or qualified health provider with any questions about a medical condition or medication. Never disregard professional medical advice or delay seeking it because of something you read here. We do not compare the clinical efficacy or safety of medications.</p>

  <h2>Accuracy</h2>
  <p>We work to keep information current, but programs, prices and offers change frequently. Always confirm current details — especially pricing — directly with the provider before making a decision. Spotted an error? Email <a href="mailto:{SITE['email']}">{SITE['email']}</a>.</p>
</div>
"""
    return base_page(f"Advertising & Medical Disclosure | {SITE['name']}",
                     "Weight Loss Reviewed's advertising, affiliate and medical disclosures, and how commissions relate (and don't) to our editorial scores.",
                     "/disclosure", body, jsonld=ld_org())

def render_404():
    body = f"""<div class="wrap narrow" style="padding:80px 20px;text-align:center">
  <span class="eyebrow-2">Error 404</span>
  <h1 style="margin-top:8px">Page not found</h1>
  <p class="lead">That page moved or never existed. Try the <a href="/">rankings</a>, our <a href="/reviews">reviews</a>, or the <a href="/guides">articles</a>.</p>
  <p><a class="btn btn-primary" href="/">Back to the rankings {icon('arrow', size=16)}</a></p>
</div>"""
    return base_page(f"Page not found | {SITE['name']}", "Page not found.", "/404", body)

# --------------------------------------------------------------------------
# sitemap + robots
# --------------------------------------------------------------------------
def build_sitemap(urls):
    items = ""
    for u in urls:
        items += f'  <url><loc>{SITE["domain"]}{u}</loc><lastmod>{TODAY.isoformat()}</lastmod></url>\n'
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + items + '</urlset>\n')

def robots():
    return (f"User-agent: *\nAllow: /\n\nSitemap: {SITE['domain']}/sitemap.xml\n")

# --------------------------------------------------------------------------
# Writer + main
# --------------------------------------------------------------------------
def write(path, content):
    full = os.path.join(ROOT, path.lstrip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    return "/" + path.lstrip("/")

def main():
    written = []
    # home
    written.append((write("index.html", render_home()), "/"))
    # reviews
    written.append((write("reviews/index.html", render_reviews_index()), "/reviews"))
    for slug in PROVIDER_ORDER:
        written.append((write(f"reviews/{slug}.html", render_review(slug)), review_url(slug)))
    # versus
    written.append((write("comparisons.html", render_versus_index()), "/comparisons"))
    for v in VERSUS:
        written.append((write(f"{v['a']}-vs-{v['b']}.html", render_versus(v)), versus_url(v)))
    for tslug in ALT_TARGETS:
        written.append((write(f"{tslug}-alternatives.html", render_alternatives(tslug)), alt_url(tslug)))
    # guides
    written.append((write("guides/index.html", render_guides_index()), "/guides"))
    for a in ARTICLES:
        written.append((write(f"guides/{a['slug']}.html", render_article(a)), article_url(a)))
    # static
    written.append((write("methodology.html", render_methodology()), "/methodology"))
    written.append((write("about.html", render_about()), "/about"))
    written.append((write("disclosure.html", render_disclosure()), "/disclosure"))
    write("404.html", render_404())
    # sitemap + robots
    urls = [u for _, u in written]
    write("sitemap.xml", build_sitemap(urls))
    write("robots.txt", robots())
    print(f"Built {len(written)} pages + sitemap + robots.")
    for _, u in written:
        print("  ", u)

if __name__ == "__main__":
    main()

