from pyconcepticon.api import Concepticon 

conc = Concepticon(".")
replacements = {}
    
for concept_id, conceptset in conc.conceptsets.items():
    if conceptset.replacement_id:
        replacements[concept_id] = conceptset.replacement_id

for conceptlist_id, conceptlist in conc.conceptlists.items():  
    for concept_id, values in conceptlist.concepts.items():  
        if values.concepticon_id in replacements.keys():  
            print(f"{values.id} uses {values.concepticon_id} ({values.concepticon_gloss}) which is replaced by {replacements[values.concepticon_id]} ({conc.conceptsets[replacements[values.concepticon_id]].gloss})")
