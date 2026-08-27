from typing import Dict, Any, List, Optional
import asyncio
import structlog
from app.core.config import settings

logger = structlog.get_logger()

class OSINTEngine:
    MODULES = {
        "domain": ["whois", "dns", "subdomain", "ssl", "wayback"],
        "ip": ["shodan", "censys", "virustotal", "abuseipdb"],
        "email": ["breach", "social", "mx", "spf"],
        "phone": ["carrier", "location", "social"],
        "person": ["social_media", "breach", "public_records"],
        "company": ["registry", "linkedin", "news", "financial"],
    }

    def __init__(self):
        self.active_modules = {}

    async def investigate(self, target: str, target_type: str, modules: Optional[List[str]] = None) -> Dict[str, Any]:
        selected = modules or self.MODULES.get(target_type, ["general"])
        logger.info("osint_investigation_start", target=target, type=target_type, modules=selected)
        tasks = [self._run_module(module, target, target_type) for module in selected]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        findings = []
        for module, result in zip(selected, results):
            if isinstance(result, Exception):
                findings.append({"module": module, "status": "error", "error": str(result)})
            else:
                findings.append({"module": module, "status": "success", "data": result})
        risk_score = self._calculate_risk(findings)
        nodes, edges = self._build_graph(target, findings)
        return {
            "target": target, "target_type": target_type, "findings": findings,
            "risk_score": risk_score,
            "risk_level": "high" if risk_score > 70 else "medium" if risk_score > 40 else "low",
            "graph_nodes": nodes, "graph_edges": edges,
            "modules_run": len(selected),
            "modules_success": sum(1 for f in findings if f["status"] == "success"),
        }

    async def _run_module(self, module: str, target: str, target_type: str) -> Dict:
        if module == "shodan" and settings.SHODAN_API_KEY:
            import shodan
            api = shodan.Shodan(settings.SHODAN_API_KEY)
            return api.host(target)
        elif module == "whois":
            import whois
            return whois.whois(target)
        elif module == "dns":
            import dns.resolver
            answers = dns.resolver.resolve(target, 'A')
            return {"a_records": [str(r) for r in answers]}
        return {"module": module, "data": "placeholder"}

    def _calculate_risk(self, findings: List[Dict]) -> float:
        score = 0
        for f in findings:
            if f["status"] != "success": continue
            data = f.get("data", {})
            if "vulns" in data: score += len(data["vulns"]) * 10
            if "ports" in data: score += len(data["ports"]) * 2
            if "breaches" in data: score += len(data["breaches"]) * 15
        return min(score, 100)

    def _build_graph(self, target: str, findings: List[Dict]) -> tuple:
        nodes = [{"id": target, "label": target, "type": "target", "color": "#ff0000"}]
        edges = []
        for f in findings:
            if f["status"] != "success": continue
            module = f["module"]
            nodes.append({"id": module, "label": module, "type": "module"})
            edges.append({"source": target, "target": module})
        return nodes, edges
