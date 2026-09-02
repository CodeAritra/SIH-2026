"""
Rule Checks & Regulatory Pointers for IP-SAKTI Sahayak.
Handles ABS compliance alerts, TKDL prior-art warnings, and external registry links.
"""

from typing import Dict, Any, List

EXTERNAL_REGISTRY_LINKS = [
    {
        "name": "TKDL (Traditional Knowledge Digital Library)",
        "url": "http://www.tkdl.res.in",
        "desc": "Check prior art search for traditional Indian medicinal formulations before patenting."
    },
    {
        "name": "IP India (InPASS Patent Search)",
        "url": "https://ipindiaservices.gov.in/publicsearch",
        "desc": "Search granted Indian patents and published applications."
    },
    {
        "name": "NBA India (National Biodiversity Authority)",
        "url": "http://nbaindia.org",
        "desc": "File Form III for IPR access clearance under Biological Diversity Act."
    },
    {
        "name": "GI Registry India",
        "url": "https://ipindia.gov.in/geographical-indications.htm",
        "desc": "Search registered Geographical Indications for Indian heritage herbs & goods."
    }
]

def check_abs_compliance(query: str, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Detects biological resource sourcing/export requiring NBA compliance."""
    keywords = [
        "biological resource", "biological material", "export herb", "foreign collaboration",
        "nba", "biodiversity", "sbb", "state biodiversity board", "access and benefit sharing",
        "abs", "wild herb", "cultivated species", "genetic resource"
    ]
    query_lower = query.lower()
    triggered = any(k in query_lower for k in keywords)
    
    # Also check if any retrieved chunk is from BDA or Nagoya Protocol
    if not triggered:
        for c in chunks:
            title = c["metadata"].get("source_title", "").lower()
            if "biological diversity" in title or "nagoya" in title or "cbd" in title:
                triggered = True
                break

    return {
        "triggered": triggered,
        "title": "Biological Diversity Act (ABS Compliance Alert)" if triggered else None,
        "message": (
            "Your query involves Indian biological resources. Under Section 6 of the Biological Diversity Act 2002 (amended 2023), "
            "prior approval or Form III declaration to the National Biodiversity Authority (NBA) is mandatory before patent grant."
        ) if triggered else None
    }

def check_tkdl_pointer(classification_key: str, query: str) -> Dict[str, Any]:
    """Surfaces TKDL prior art pointer when dealing with proprietary Ayurvedic patents."""
    is_proprietary = classification_key in ["proprietary", "patent_proprietary"]
    has_patent_keyword = any(k in query.lower() for k in ["patent", "prior art", "section 3(p)", "traditional knowledge"])
    
    triggered = is_proprietary or has_patent_keyword

    return {
        "triggered": triggered,
        "title": "TKDL Prior-Art Verification Required" if triggered else None,
        "message": (
            "Notice: Ayurvedic formulations based on traditional knowledge are subject to strict rejection under Section 3(p) "
            "of the Patents Act 1970. Always search the Traditional Knowledge Digital Library (TKDL) database to verify novelty "
            "and ensure non-obvious synergistic efficacy before filing a patent application."
        ) if triggered else None
    }

def get_registry_pointers(chunks: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """Returns relevant external registry links based on chunk IP types."""
    ip_types = {c["metadata"].get("ip_type") for c in chunks}
    pointers = []
    
    if "patent" in ip_types or "abs" in ip_types:
        pointers.append(EXTERNAL_REGISTRY_LINKS[0]) # TKDL
        pointers.append(EXTERNAL_REGISTRY_LINKS[1]) # IP India
    if "abs" in ip_types:
        pointers.append(EXTERNAL_REGISTRY_LINKS[2]) # NBA
    if "gi" in ip_types:
        pointers.append(EXTERNAL_REGISTRY_LINKS[3]) # GI Registry

    # Fallback to default top 2 if empty
    if not pointers:
        pointers = EXTERNAL_REGISTRY_LINKS[:2]

    return pointers
