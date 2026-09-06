"""
Seed Corpus Generator for IP-SAKTI Sahayak.
Generates comprehensive legal/regulatory seed documents tagged across 3 core axes:
1. Jurisdiction (india | international)
2. IP Type (patent | gi | trademark | copyright | design | trade_secret | plant_variety | abs | drug_regulatory)
3. Formulation Category (classical | proprietary | new_drug | phytopharma | ayurveda_aahar | cosmetic | all)
"""

import os
import json

CORPUS_DIR = os.path.join(os.path.dirname(__file__), "..", "corpus")

SEED_DOCUMENTS = [
    {
        "id": "patents_act_1970",
        "title": "Patents Act, 1970 (India)",
        "jurisdiction": "india",
        "ip_type": "patent",
        "formulation_category": "classical, proprietary",
        "filename": "patents_act_1970.txt",
        "content": """
Section 3(p): Inventions Not Patentable - Traditional Knowledge
An invention which in effect, is traditional knowledge or which is an aggregation or duplication of known properties of traditionally known component or components is not patentable. For Ayurvedic formulations, combining known medicinal plants (e.g. Ashwagandha and Turmeric) without synergistic non-obvious technical effect is barred under Section 3(p).

Section 3(e): Mere Admixture Not Patentable vs Synergistic Combinations
A substance obtained by a mere admixture resulting only in the aggregation of the properties of the components thereof or a process for producing such substance is not patentable. To overcome Section 3(e) for polyherbal combinations (e.g. Ashwagandha, Turmeric, Pippali), the applicant must furnish comparative experimental data demonstrating a statistically significant synergistic effect (Combination Index CI < 1.0) rather than a simple additive effect.

Section 3(d): Enhanced Efficacy and Novel Extraction Processes
The mere discovery of a new form of a known substance which does not result in the enhancement of the known efficacy of that substance, or the mere discovery of any new property or new use for a known substance or of the mere use of a known process, machine or apparatus unless such known process results in a new product or employs at least one new reactant is not an invention. However, a novel extraction method (e.g. supercritical CO2 extraction, targeted fraction isolation) that results in enhanced therapeutic efficacy, superior bioavailability, or an unexpected bioactive profile for Ayurvedic botanicals may be patentable as a novel process invention.

Section 3(j): Non-Patentability of Plants and Animals
Plants and animals in whole or any part thereof including seeds, varieties and species and essentially biological processes for production or propagation of plants and animals are not inventions. However, isolated microorganisms or purified active phytochemical compounds with novel technical processes may be patentable if novel and inventive.

Section 6: Application for Patents and Biological Material Disclosure
Where an invention described in a patent specification uses biological material sourced from India, the applicant is required to disclose the source and geographical origin of the biological material used in the specification.

Section 10(4): Complete Specification and Deposit of Biological Material
If the applicant mentions biological material in the specification which is not easily available to the public, the material must be deposited at an International Depository Authority (IDA) under the Budapest Treaty on or before the date of filing in India.
"""
    },
    {
        "id": "patents_rules_2024",
        "title": "Patents (Amendment) Rules, 2024 (India)",
        "jurisdiction": "india",
        "ip_type": "patent",
        "formulation_category": "proprietary, phytopharma",
        "filename": "patents_rules_2024.txt",
        "content": """
Section 13: Time Limit for Submitting NBA Approval
Under the Patents (Amendment) Rules 2024, the applicant using Indian biological resources must submit permission/clearance from the National Biodiversity Authority (NBA) prior to the grant of the patent (Form 18A / Rule 55). Failure to submit NBA clearance before final grant order will lead to rejection.

Section 55: Pre-Grant Opposition Procedure
Any person may file pre-grant opposition under Section 25(1) citing Section 3(p) prior art or non-disclosure of biological source. Traditional Knowledge Digital Library (TKDL) references are officially accepted by examiners to issue pre-grant rejections.
"""
    },
    {
        "id": "bda_2002_amended_2023",
        "title": "Biological Diversity Act, 2002 (Amended 2023) (India)",
        "jurisdiction": "india",
        "ip_type": "abs",
        "formulation_category": "all",
        "filename": "bda_2002_amended_2023.txt",
        "content": """
Section 3: Access to Biological Resources by Non-Citizens and Foreign Entities
No person who is not a citizen of India, or a body corporate registered outside India, or having foreign participation in share capital or management, shall access any biological resource occurring in India or associated traditional knowledge for research, commercial utilization, or bio-survey without prior approval of the National Biodiversity Authority (NBA).

Section 4: Transfer of Results of Research
No person shall transfer the results of any research relating to any biological resources occurring in or obtained from India to any foreign entity without prior approval of the NBA.

Section 6: Application for Intellectual Property Rights (IPR)
(1) No person shall apply for any IP right in India or outside India for any invention based on any research or information on a biological resource obtained from India without obtaining prior approval of the NBA before grant of patent.
(2) Under the 2023 Amendment, registered Ayush practitioners, cultivated bio-resource users, and domestic codifiers are exempted from benefit-sharing obligations for domestic commercial use, but IPR filings still require NBA declaration.

Section 7: Prior Intimation to State Biodiversity Board (SBB)
Indian citizens and Indian MSMEs accessing biological resources for commercial utilization must give prior intimation to the concerned State Biodiversity Board (SBB) in prescribed form, unless using cultivated medicinal plants registered under Ministry of Ayush / State Agriculture boards.

Section 40: Exemptions for Normally Traded Commodities
Central Government may declare biological resources normally traded as commodities (NTAC) exempt from provisions of the Act when used strictly as commodities, but not when used as research inputs for patentable IP.
"""
    },
    {
        "id": "bd_rules_2024",
        "title": "Biological Diversity (Amendment) Rules, 2024 (India)",
        "jurisdiction": "india",
        "ip_type": "abs",
        "formulation_category": "all",
        "filename": "bd_rules_2024.txt",
        "content": """
Section 14: Digital ABS Clearance Portal
Applications for NBA approval for IPR (Form III) and Commercial Utilization (Form I) must be filed electronically through the ABS e-portal. Benefit sharing ranges from 0.1% to 0.5% of annual gross ex-factory sale price for commercial entities.

Section 18: Simplified Clearance for Cultivated Species
Where biological resources are derived from registered cultivated lands (verified via Ayush e-Aushadhi / Agriculture portal certificates), benefit-sharing fees are waived, though IPR registration notification to NBA remains mandatory.
"""
    },
    {
        "id": "nba_abs_handbook",
        "title": "NBA ABS Procedural Handbook & Guidelines (India)",
        "jurisdiction": "india",
        "ip_type": "abs",
        "formulation_category": "all",
        "filename": "nba_abs_handbook.txt",
        "content": """
Section 1: Approval Process for Form III IPR Applications
Any Indian applicant filing for patent on biological resources must submit Form III to National Biodiversity Authority. Approval timing is synchronized with Patent Office Form 18A examination. Benefit-sharing tiers are assigned based on ex-factory sales: 0.1% for turnover up to Rs 1 Crore, scaling up to 0.5% above Rs 5 Crore.

Section 2: Foreign Entity Access Restrictions under Section 3
Entities with foreign shareholding exceeding 0% must execute Mutually Agreed Terms (MAT) and Prior Informed Consent (PIC) with NBA prior to accessing biological materials or submitting global PCT patent applications.
"""
    },
    {
        "id": "tkdl_info_tkrc",
        "title": "TKDL Framework & TKRC Structure (India)",
        "jurisdiction": "india",
        "ip_type": "patent",
        "formulation_category": "classical, proprietary",
        "filename": "tkdl_info_tkrc.txt",
        "content": """
Section 1: Traditional Knowledge Resource Classification (TKRC) Structure
The TKDL database categorizes over 450,000 formulation formulations from Ayurveda, Unani, Siddha, and Yoga into 5,000 subgroup codes under International Patent Classification (IPC) section A61K 36/00.

Section 2: Prior Art Citations in International Patent Offices
Major patent offices (USPTO, EPO, JPO, IPO) access TKDL non-disclosure agreements to issue 3(p) prior-art rejections. Formulation innovators must verify TKRC entries prior to drafting claims on botanical extracts.
"""
    },
    {
        "id": "gi_act_1999",
        "title": "Geographical Indications of Goods Act, 1999 (India)",
        "jurisdiction": "india",
        "ip_type": "gi",
        "formulation_category": "classical, proprietary",
        "filename": "gi_act_1999.txt",
        "content": """
Section 2(e): Definition of Geographical Indication
An indication which identifies agricultural, natural, or manufactured goods (including Ayurvedic herbs and formulations like Navara Rice, Kashmir Saffron, or Kangra Tea) originating in a definite territory, where a given quality, reputation, or characteristic is essentially attributable to its geographical origin.

Section 9: Prohibition of Registration of Certain GIs
A geographical indication shall not be registered if it is generic, contrary to law, scandalous, or likely to deceive consumers regarding geographic origin.

Section 20: Rights Conferred by Registration
Registration gives the producer organization the exclusive right to use the GI in relation to the goods and seek legal injunction against unauthorized misuse, false geographic origin claims, or unfair competition.

Section 22: Infringement of Registered Geographical Indication
Using a registered GI tag on Ayurvedic products not originating from the designated region constitutes passing off and criminal infringement under Section 103 of the GI Act.
"""
    },
    {
        "id": "trademarks_act_1999",
        "title": "Trade Marks Act, 1999 (India)",
        "jurisdiction": "india",
        "ip_type": "trademark",
        "formulation_category": "all",
        "filename": "trademarks_act_1999.txt",
        "content": """
Section 9: Absolute Grounds for Refusal of Trademark
Trademarks which consist exclusively of marks or indications designating the plant species, classical Ayurvedic ingredient names (e.g., 'Triphala', 'Chyawanprash', 'Tulsi'), or generic botanical descriptions cannot be registered as exclusive trademarks for medicinal products.

Section 11: Relative Grounds for Refusal
A trademark shall not be registered if it is confusingly similar or identical to an earlier registered trademark for medicinal and pharmaceutical products (Class 5 and Class 3).

Section 29: Infringement of Registered Trademarks
Unauthorized commercial use of a mark identical or deceptive to a registered brand for health and wellness products constitutes infringement, subject to statutory damages and injunctions.
"""
    },
    {
        "id": "drugs_cosmetics_act_1940",
        "title": "Drugs and Cosmetics Act, 1940 & Rules 1945 (India)",
        "jurisdiction": "india",
        "ip_type": "drug_regulatory",
        "formulation_category": "classical, proprietary, phytopharma, cosmetic",
        "filename": "drugs_cosmetics_act_1940.txt",
        "content": """
Section 3(a): Definition of Ayurvedic, Siddha or Unani (ASU) Drug
Includes all medicines intended for internal or external use for or in the diagnosis, treatment, mitigation or prevention of disease or disorder in human beings or animals, manufactured exclusively in accordance with the formulae described in the authoritative books of Ayurvedic System specified in the First Schedule.

Section 33EEB: Patent or Proprietary Medicine Requirements
For ASU drugs, a 'patent or proprietary medicine' means a formulation containing ingredients specified in Ayurvedic authoritative books but processed in a non-classical dosage form or ratio. Requires manufacturing license from State Licensing Authority (Ayush) and safety/efficacy validation under Rule 158B.

Section 33N: Ayurvedic Pharmacopoeia Committee (APC) Standards
All raw botanical ingredients and finished Ayurvedic products must comply with official quality standards specified in the Ayurvedic Pharmacopoeia of India (API).

Schedule T: Good Manufacturing Practices (GMP)
Mandates factory hygiene, raw material testing, batch manufacturing records, and quality control lab compliance for all licensed Ayush manufacturing units.
"""
    },
    {
        "id": "drugs_magic_remedies_1954",
        "title": "Drugs and Magic Remedies (Objectionable Advertisements) Act, 1954 (India)",
        "jurisdiction": "india",
        "ip_type": "drug_regulatory",
        "formulation_category": "classical, proprietary, ayurveda_aahar",
        "filename": "drugs_magic_remedies_1954.txt",
        "content": """
Section 3: Prohibition of Advertisement of Certain Drugs
No person shall take part in the publication of any advertisement referring to any drug (including Ayurvedic drugs) in terms which suggest or calculated to lead to the use of that drug for the diagnosis, cure, mitigation, treatment or prevention of any disease or condition specified in the Schedule (e.g. Diabetes, Cancer, Infertility, Paralysis, Obesity).

Section 4: Prohibition of Misleading Advertisements
Prohibits advertisements that directly or indirectly give false impressions regarding the true character or efficacy of an Ayurvedic medicine or claim magical/miraculous healing powers.
"""
    },
    {
        "id": "fssai_ayurveda_aahar_2022",
        "title": "FSSAI Ayurveda-Aahar Regulations, 2022/2024 (India)",
        "jurisdiction": "india",
        "ip_type": "drug_regulatory",
        "formulation_category": "ayurveda_aahar",
        "filename": "fssai_ayurveda_aahar_2022.txt",
        "content": """
Regulation 3: Definition of Ayurveda Aahar
Ayurveda Aahar means food prepared in accordance with the recipes, ingredients, and processes described in the authoritative books of Ayurveda listed under Schedule A of FSSAI regulations. It excludes therapeutic drugs defined under the Drugs and Cosmetics Act.

Regulation 4: Labeling and Non-Curative Claims
Ayurveda Aahar packaging must prominently display the official 'Ayurveda Aahar' logo. Labels MUST NOT claim to treat, cure, or prevent any human disease or medical condition. Only disease-risk-reduction or general wellness claims permitted by FSSAI expert committee are allowed.

Schedule I & II: Permitted Botanical Ingredients
Only ingredients listed in authoritative Ayurvedic texts or approved FSSAI positive lists can be incorporated into Ayurveda Aahar food supplements. Synthetic vitamins or therapeutic synthetic compounds are strictly prohibited.
"""
    },
    {
        "id": "trips_agreement",
        "title": "TRIPS Agreement (WIPO/WTO) (International)",
        "jurisdiction": "international",
        "ip_type": "patent",
        "formulation_category": "all",
        "filename": "trips_agreement.txt",
        "content": """
Article 27: Patentable Subject Matter
Patents shall be available for any inventions, whether products or processes, in all fields of technology, provided that they are new, involve an inventive step and are capable of industrial application. Member states may exclude diagnostic, therapeutic and surgical methods for treatment of humans.

Article 22: Protection of Geographical Indications
Members shall provide legal means to prevent designation or presentation of a good that indicates or suggests that the good originates in a geographical area other than the true place of origin in a manner which misleads the public.

Article 39: Protection of Undisclosed Information (Trade Secrets)
Natural and legal persons shall have the possibility of preventing information lawfully within their control (e.g. proprietary herbal extraction ratios or trade secret processing methods) from being disclosed to, acquired by, or used by others without consent in a manner contrary to honest commercial practices.
"""
    },
    {
        "id": "cbd_convention",
        "title": "Convention on Biological Diversity (CBD) (International)",
        "jurisdiction": "international",
        "ip_type": "abs",
        "formulation_category": "all",
        "filename": "cbd_convention.txt",
        "content": """
Article 8(j): Traditional Knowledge, Innovations and Practices
Each Contracting Party shall, as far as possible and as appropriate, respect, preserve and maintain knowledge, innovations and practices of indigenous and local communities embodying traditional lifestyles relevant for the conservation and sustainable use of biological diversity and promote their wider application with approval of holders of such knowledge.

Article 15: Access to Genetic Resources
Recognizes sovereign rights of States over their natural resources. Authority to determine access to genetic resources rests with national governments and is subject to national legislation, based on Prior Informed Consent (PIC) and Mutually Agreed Terms (MAT).
"""
    },
    {
        "id": "nagoya_protocol",
        "title": "Nagoya Protocol on Access and Benefit-Sharing (International)",
        "jurisdiction": "international",
        "ip_type": "abs",
        "formulation_category": "all",
        "filename": "nagoya_protocol.txt",
        "content": """
Article 5: Fair and Equitable Benefit-Sharing
Benefits arising from the utilization of genetic resources as well as subsequent applications and commercialization shall be shared in a fair and equitable way with the Party providing such resources. Benefits may be monetary (royalties) or non-monetary (technology transfer, capacity building).

Article 6: Access to Genetic Resources
Access to genetic resources for commercial or research utilization requires Prior Informed Consent (PIC) of the provider country unless otherwise determined by that Party.

Article 17: Monitoring the Utilization of Resources (Checkpoints)
Parties must designate checkpoints (such as IP offices, research funding agencies, or regulatory authorities) to monitor compliance and verify that applicants have obtained PIC and MAT before granted IP or market approval.
"""
    },
    {
        "id": "wipo_grtk_treaty_2024",
        "title": "WIPO Treaty on Intellectual Property, Genetic Resources and Associated Traditional Knowledge (2024) (International)",
        "jurisdiction": "international",
        "ip_type": "patent",
        "formulation_category": "classical, proprietary",
        "filename": "wipo_grtk_treaty_2024.txt",
        "content": """
Article 3: Mandatory Patent Disclosure Requirement
Where an invention in a patent application is materially/directly based on genetic resources, each Contracting Party shall require applicants to disclose the country of origin or source of the genetic resources. Where the invention is directly based on traditional knowledge associated with genetic resources, applicants must disclose the indigenous community or source providing the TK.

Article 4: Information Systems and Database Safeguards
Contracting Parties may establish digital databases of genetic resources and traditional knowledge (such as India's TKDL) to assist patent offices in conducting prior art searches and preventing erroneous patent grants.
"""
    },
    {
        "id": "pct_treaty",
        "title": "Patent Cooperation Treaty (PCT) (International)",
        "jurisdiction": "international",
        "ip_type": "patent",
        "formulation_category": "proprietary, phytopharma, new_drug",
        "filename": "pct_treaty.txt",
        "content": """
Article 3: The International Application
Filing a single PCT international application has the effect of a regular national application in all designated PCT member states. Useful for Ayurvedic startups seeking patent protection in multiple global jurisdictions.

Article 15: The International Search
Each PCT application is subjected to an International Search Report (ISR) and Written Opinion by an International Searching Authority (ISA) to evaluate novelty and inventive step prior to entering national phases (typically at 30 or 31 months).
"""
    },
    {
        "id": "budapest_treaty",
        "title": "Budapest Treaty on Microorganism Deposit (International)",
        "jurisdiction": "international",
        "ip_type": "patent",
        "formulation_category": "phytopharma, new_drug",
        "filename": "budapest_treaty.txt",
        "content": """
Article 3: Recognition of Deposit of Microorganisms
For patent procedures involving microbial strains, probiotic Ayurvedic fermentations, or bio-catalytic processes, a deposit of the microorganism made with one International Depository Authority (IDA) (e.g. MTCC Chandigarh in India) shall be recognized by all contracting states.
"""
    }
]

def generate_seed_corpus():
    os.makedirs(CORPUS_DIR, exist_ok=True)
    manifest = []
    
    for doc in SEED_DOCUMENTS:
        file_path = os.path.join(CORPUS_DIR, doc["filename"])
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"# {doc['title']}\n")
            f.write(f"Jurisdiction: {doc['jurisdiction']}\n")
            f.write(f"IP Type: {doc['ip_type']}\n")
            f.write(f"Formulation Category: {doc['formulation_category']}\n\n")
            f.write(doc["content"].strip())
            f.write("\n")
        
        manifest.append({
            "id": doc["id"],
            "title": doc["title"],
            "jurisdiction": doc["jurisdiction"],
            "ip_type": doc["ip_type"],
            "formulation_category": doc["formulation_category"],
            "filename": doc["filename"],
            "is_real_text": True
        })
        print(f"Generated seed document: {doc['filename']}")
        
    manifest_path = os.path.join(CORPUS_DIR, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
        
    print(f"Successfully generated {len(SEED_DOCUMENTS)} seed documents in {CORPUS_DIR}")

if __name__ == "__main__":
    generate_seed_corpus()
