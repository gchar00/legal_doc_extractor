#Libraries 
import streamlit as st 
import re 

#The regex expressions were made with the help of these tools using the extracted
#text as test sample:
#https://pythex.org/    
#https://regexr.com/ explain the regex in detail 


def clean_ocr_noise(text):
    '''
    Removes extra indices, "\n", hyphenation and markers from OCR
    
    Arguments:
    - text: (Str) Text extracted from file 
    Return:
    - cleaned_text: (Str) Modified text without noise
    '''
    #Modify hyphenation like  "Ευαγ- \nγέλου" to "Ευαγγέλου"
    text = re.sub(r'(-\s*\n\s*)|(-\.*\n\s*)', '', text)
    
    #Remove page markers like "[Φύλλο  3]  ""
    text = re.sub(r'\[\s*Φύλλο\s*\d+\s*\]*.*\n', '', text)
    
    #Replace more than one consecutive newline  "\n" with just one
    text = re.sub(r'\n{2,}', '\n', text)
    
    #Replace one or more consecutive whitespace indices
    #like "Ελευθέριου   Βενιζέλου " to "Ελευθέριου Βενιζέλου" 
    text = re.sub(r'\s\s+', ' ', text)
    cleaned_text = text.strip()
    
    return cleaned_text



def extract_person_info(text, role_keywords, check_represents = False):
    """
    Extract key info for any person either seller, either buyer etc. based on 
    the role_keywords. Info about: Name, Tax_id, Id, Address is needed.
    
    Arguments:
    - text: (Str) Text to apply regex
    - role_keywords: (List of Str) Keywords that indicate role
    - check_represents: (Bool) Flag to check if the person represents someone
    Returns:
    - people: (List of Dict[Str:Str]) extracted persons with their details
    """
    
    #Regex  for parsing is written in a simple way 
    #based on keywords for each group. They are not implemented correctly 
    #with robust rules, they only demonstrate keywords.

    name_reg = r"(?:{})\s*(?:[:\s]*)(?:\w*\s*)*".format("|".join(role_keywords))
    tax_id_reg = r"ΑΦΜ\s*(\d{9})"
    id_reg = r"ΑΔΤ\s*\D+\d{4,}"
    address_reg = r"κάτοικος\s*([ά-ώ\s\d]+οδός)"
    
    names = re.findall(name_reg, text) #ex. 3 Names found
    tax_ids = re.findall(tax_id_reg, text) #ex. 2 Tax_ids found
    ids = re.findall(id_reg, text) #ex. 3 IDs found
    addresses = re.findall(address_reg, text) # ex. 2 Addresses found

    people = []
    #Create a dict profile for each person
    for i, name in enumerate(names):
        person= {
            "Name": name.strip(),
            "Tax_ID": tax_ids[i] if i < len(tax_ids) else "", #if not found --> ""
            "ID": ids[i] if i < len(ids) else "",             #if not found --> "" 
            "Address": addresses[i] if i < len(addresses) else "", #if not found--> ""
        }
        if check_represents:
            rep_reg = r"ως\s*(?:πληρεξούσιος|αντίκλητος|αντιπρόσωπος)\s+(?:του|της)\s+"
            reps = re.search(rep_reg, text)
            if reps:
                person["Represents"] = [r.strip() for r in reps] #Name of the person that represents
        people.append(person)
    return people



def extract_property_info(text):
    """
    Extract key info for a property. Info about: Address, Type, Area, Floor,
    Land registry and Building permit is needed.
    
    Arguments:
    - text: (Str) Text to apply regex
    Returns:
    - prop: (Dict[Str:Str]) extracted key info for property
    """
    #Regex  for parsing is written in a simple way 
    #based on keywords for each group. They are not implemented correctly 
    #with robust rules, they only demonstrate keywords.
    prop = {}
    #Create regex for each label info 
    keys = {
        "Address": r"(?:βρίσκεται στη|οδός)\s*[:\s]*([Α-ΩA-Zά-ώ0-9\s,]+)",
        "Type": r"(Οικόπεδο|Διαμέρισμα|Πολυκατοικία)",
        "Area": r"\s*[:]?([\d,.]+)\s*τετραγωνικών μέτρων",
        "Floor": r"(\d+[ου]*\s*ορόφου)",
        "Land registry": r"ΚΑΕΚ\s*[:\s]*([0-9]+)",
        "Building Permit": r"Άδεια Δόμησης\s*[:\s]*([0-9]+)"
    }
    for key,reg in keys.items():
        flag = re.search(reg, text)
        prop[key] = flag.group(1).strip() if flag else ""
        
    return prop


def parse_text(text):
    '''
    Parsing text to extract key info using the above helper functions
    
    Arguments:
    - text: (Str) Cleaned extracted text 
    Returns:
    - parsed_text: (Dict) Key info text extracted regarding   
    '''
    #Creating the structure for JSON file
    parsed_text = {
        "Involved_parties" : {  #Group A { [Seller1, Seller2..], [Buyer1, Buyer2..], Notary }
            "Sellers" : [], #list of sellers
            "Buyers" : [],  #list of buyers
            "Notary": {}    #notary details
            },
        "Property_details":[]   #Group B [Property1, Property2] list of properties
    }
    
    #Sellers(one or more)
    parsed_text["Involved_parties"]["Sellers"] = extract_person_info(
        text, 
        [r"(αφ'ενός):", r"ως πωλητής", r"ιδιοκτήτης"], 
        check_represents = True)
    #Buyers(one or more)
    parsed_text["Involved_parties"]["Buyers"] = extract_person_info(
        text, 
        [r"(αφ'ετέρου):", r"ως αγοραστής:", r"αγοράστρια εταιρεία"], 
        check_represents=True)
    #Notary
    notary = extract_person_info(text, 
        [r"ως συμβολαιογράφος", r"ΣΥΜΒΟΛΑΙΟΓΡΑΦΟΣ", r"παρουσιάσθηκαν σε μένα"],
        check_represents=False)
    parsed_text["Involved_parties"]["Notary"] = notary[0] if notary else {}
    #Properties
    #Find sections starts with Ακίνητο, Οικόπεδο etc. assuming each section is a property
    properties = re.split(r"(Οικόπεδο|Διαμέρισμα|Πολυκατοικία|Ακίνητο)",text)
    for prop in properties:
        parsed_text["Property_details"].append( extract_property_info(prop) )
    
    return parsed_text

