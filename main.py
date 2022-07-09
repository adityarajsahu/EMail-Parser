import email
from email import policy
from email.parser import BytesParser
import html2text
import locationtagger
import spacy

nlp = spacy.load('en_core_web_sm')

filepath = 'email-data/FW_ Mundra _ Dammam - 10,000 MT Bagged FlyAsh+++OTHERS (1).eml'

with open(filepath) as email_file:
    email_message = email.message_from_file(email_file)
  
if email_message.is_multipart():
    for part in email_message.walk():
        #print(part.is_multipart())
        #print(part.get_content_type())
        #print()
        message = str(part.get_payload(decode=True))
        plain_message = html2text.html2text(message)
        doc = nlp(plain_message)
        for ent in doc.ents:
            if ent.label_ == 'GPE':
                print(ent.text)


        """place_entity = locationtagger.find_locations(text = plain_message)
        print(len(place_entity.countries))
        print(len(place_entity.cities))"""
