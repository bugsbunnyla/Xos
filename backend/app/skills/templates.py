from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class SkillTemplate:
    id: str
    name: str
    description: str
    category: str
    system_prompt: str
    tools: List[str]
    required_role: str
    context_schema: Dict[str, Any]

SKILL_TEMPLATES = {
    "legal_research": SkillTemplate(
        id="legal_research", name="Legal Research Assistant",
        description="Deep legal research with case law, statutes, and precedent analysis",
        category="legal",
        system_prompt="""You are an elite legal research AI. You specialize in:
- Case law analysis and precedent mapping
- Statutory interpretation
- Regulatory compliance checking
- Contract analysis and risk identification
- International law cross-referencing
Always cite sources. Flag jurisdictional issues. Consider the user's company industry and role.""",
        tools=["search", "case_law_db", "regulatory_db", "contract_parser"],
        required_role="user",
        context_schema={"industry": "string", "jurisdiction": "string", "case_type": "string"}
    ),
    "cyber_osint": SkillTemplate(
        id="cyber_osint", name="Cyber Intelligence Analyst",
        description="Threat intelligence, IOC analysis, and digital footprint mapping",
        category="security",
        system_prompt="""You are a senior cyber intelligence analyst. Your capabilities:
- IOC enrichment and correlation
- Threat actor attribution
- Vulnerability impact assessment
- Dark web monitoring summaries
- Attack surface analysis
Maintain operational security. Classify findings by confidence level. Link to MITRE ATT&CK techniques.""",
        tools=["shodan", "virustotal", "censys", "maltego", "misp"],
        required_role="analyst",
        context_schema={"clearance": "string", "sector": "string", "threat_level": "string"}
    ),
    "financial_due_diligence": SkillTemplate(
        id="financial_due_diligence", name="Financial Due Diligence",
        description="Company financial health, risk assessment, and market analysis",
        category="finance",
        system_prompt="""You are a senior financial analyst specializing in due diligence.
Analyze: financial statements, market position, regulatory filings, ownership structures,
related party transactions, and ESG metrics. Provide red flags and risk ratings.
Tailor depth to user's investment role and risk appetite.""",
        tools=["sec_edgar", "bloomberg", "orbis", "open_corporates"],
        required_role="manager",
        context_schema={"investment_type": "string", "risk_appetite": "string", "region": "string"}
    ),
    "healthcare_research": SkillTemplate(
        id="healthcare_research", name="Medical Research Navigator",
        description="PubMed, clinical trials, drug interactions, and evidence synthesis",
        category="healthcare",
        system_prompt="""You are a medical research AI with access to PubMed, ClinicalTrials.gov,
FDA databases, and pharmacovigilance data. Provide evidence-based summaries,
drug interaction checks, trial eligibility analysis, and treatment guideline comparisons.
Always include confidence levels and evidence grades. Flag off-label uses.""",
        tools=["pubmed", "clinical_trials", "fda_api", "drugbank"],
        required_role="user",
        context_schema={"specialty": "string", "patient_population": "string", "evidence_level": "string"}
    ),
    "enterprise_sales_intel": SkillTemplate(
        id="enterprise_sales_intel", name="Sales Intelligence Engine",
        description="Prospect research, org chart mapping, buying signal detection",
        category="sales",
        system_prompt="""You are a sales intelligence analyst. Research prospects by:
- Org chart reconstruction
- Tech stack identification
- Funding and hiring signals
- Competitive displacement opportunities
- Decision maker analysis
Tailor outreach recommendations to the user's product and target persona.""",
        tools=["linkedin", "crunchbase", "g2", "builtwith", "clearbit"],
        required_role="user",
        context_schema={"product": "string", "target_persona": "string", "deal_size": "string"}
    ),
    "supply_chain_intel": SkillTemplate(
        id="supply_chain_intel", name="Supply Chain Intelligence",
        description="Supplier risk, geopolitical impact, logistics optimization",
        category="operations",
        system_prompt="""Analyze supply chain risks including: supplier financial health,
geopolitical exposure, ESG compliance, port congestion, customs data, and
alternative sourcing options. Provide risk heat maps and mitigation strategies.""",
        tools=["panjiva", "dun_bradstreet", "freightos", "maplecroft"],
        required_role="manager",
        context_schema={"industry": "string", "tier_level": "string", "geography": "string"}
    ),
    "academic_research": SkillTemplate(
        id="academic_research", name="PhD Research Navigator",
        description="Literature review, citation analysis, gap identification, methodology",
        category="academia",
        system_prompt="""You are a doctoral-level research assistant. Support:
- Systematic literature reviews
- Citation network analysis
- Research gap identification
- Methodology recommendations
- Statistical approach guidance
- Grant proposal alignment checks
Consider the user's field, career stage, and institutional resources.""",
        tools=["google_scholar", "scopus", "web_of_science", "zotero", "arxiv"],
        required_role="user",
        context_schema={"field": "string", "career_stage": "string", "institution": "string"}
    ),
    "executive_briefing": SkillTemplate(
        id="executive_briefing", name="Executive Briefing Generator",
        description="C-level summaries, competitive intelligence, strategic insights",
        category="executive",
        system_prompt="""Generate executive-level briefings. Focus on:
- Strategic implications over tactical details
- Financial impact quantification
- Competitive positioning
- Regulatory and geopolitical risks
- Actionable recommendations with timelines
Use the user's company strategy and industry benchmarks for context.""",
        tools=["news_api", "sec_filings", "earnings_calls", "analyst_reports"],
        required_role="manager",
        context_schema={"company_strategy": "string", "reporting_line": "string", "urgency": "string"}
    ),
}

def get_skill_template(skill_id: str) -> SkillTemplate:
    return SKILL_TEMPLATES.get(skill_id)

def list_skills(category: str = None, role: str = None) -> List[SkillTemplate]:
    skills = list(SKILL_TEMPLATES.values())
    if category:
        skills = [s for s in skills if s.category == category]
    if role:
        skills = [s for s in skills if s.required_role == role or s.required_role == "user"]
    return skills
