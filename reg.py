import re
email_re = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
phone_re = re.compile(r'\+?\d[\d -]{8,12}\d')
address_re = re.compile(
    r'(?:(?:\d{1,5}\s+)?[\wÀ-ÿ’\'\-.,\s]+?\s+'
    r'(?:Street|St|Avenue|Ave|Boulevard|Blvd|Road|Rd|Lane|Ln|Drive|Dr|Court|Ct|Square|Sq|Loop|Trail|Trl|Parkway|Pkwy|Allee|Allée|Chemin|Via|Calle|Strasse|Straße|Rua))'
    r'[\wÀ-ÿ\s,.-]*',
    re.IGNORECASE
)

link_re = re.compile(r'href=[\'"]?([^\'" >]+)')