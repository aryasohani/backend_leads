DECISION_KEYWORDS = ["ceo","founder","co-founder","cto","cxo","chief","head of","vp","vice president","director"]
INFLUENCER_KEYWORDS = ["manager","lead","senior","principal","architect","growth","product"]

def role_score(role: str) -> (int, str):
    r = role.lower()
    for kw in DECISION_KEYWORDS:
        if kw in r:
            return 20, "Role indicates decision maker"
    for kw in INFLUENCER_KEYWORDS:
        if kw in r:
            return 10, "Role indicates influencer"
    return 0, "Role not relevant"

def industry_score(lead_industry: str, offer_use_cases: list) -> (int, str):
    li = lead_industry.lower()
    for icp in offer_use_cases:
        icp_l = icp.lower()
        if li == icp_l:
            return 20, f"Exact industry/ICP match: {icp}"
    for icp in offer_use_cases:
        if icp.lower() in li or li in icp.lower():
            return 10, f"Adjacent industry match with: {icp}"
    return 0, "Industry not matched"

def completeness_score(lead: dict) -> (int, str):
    required = ["name","role","company","industry","location"]
    for k in required:
        if not lead.get(k):
            return 0, f"Missing field {k}"
    return 10, "All required fields present"

def compute_rule_score(lead:dict, offer:dict) -> (int, list):
    rs, reasons = 0, []
    s, r = role_score(lead.get("role",""))
    rs += s; reasons.append(r)
    s, r = industry_score(lead.get("industry",""), offer.get("ideal_use_cases",[]))
    rs += s; reasons.append(r)
    s, r = completeness_score(lead)
    rs += s; reasons.append(r)
    if rs > 50: rs = 50
    return rs, reasons
