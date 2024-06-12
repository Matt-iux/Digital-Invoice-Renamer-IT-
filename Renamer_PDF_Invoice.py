import os
import xml.etree.ElementTree as ET
from os import listdir, path

"""
This program analyze a file .xml of a digital invoice, extract the information of specific fields like name, date and
numbers and use them to rename the invoice pdf following a fixed renaming structure 
"""


def main():
    # Assign directory path for both file type
    directory_xml = r'.\XML'
    directory_pdf = r'.\PDF'

    # Get the list of the xml name in the directory
    xml_files = [path.join(directory_xml, f) for f in listdir(directory_xml) if f.endswith('.xml')]
    # Cycle throught xml file
    for xml_file in xml_files:
        print(xml_file)
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Get the xml file basename to check in the if statement
        xml_name = os.path.basename(xml_file)
        print(xml_name)

        # Extract required element from XML
        Denomination = tree.find('FatturaElettronicaHeader/CedentePrestatore/DatiAnagrafici/Anagrafica/Denominazione')

        # Add a correction  for invoice from Name and surname origin with no denomination
        if Denomination is None:
            Denomination = tree.find('FatturaElettronicaHeader/CedentePrestatore/DatiAnagrafici/Anagrafica/Cognome')
        Date = tree.find('FatturaElettronicaBody/DatiGenerali/DatiGeneraliDocumento/Data')
        Invoice_Number = tree.find('FatturaElettronicaBody/DatiGenerali/DatiGeneraliDocumento/Numero')
        Invoice_Number_String = Invoice_Number.text
        print(Invoice_Number.text)

        # Replace / unallowed character
        dict = {'/': '-'}  # format 'substring':'replacement'
        for key, value in dict.items():
            if key in Invoice_Number.text:
                New_Invoice_Number = Invoice_Number_String.replace(key, value)
                Invoice_Number_String = New_Invoice_Number

        # Return name xml without extension (both for .xml and for .xml.xml.p7m)
        xml_no_ext = xml_name.rsplit('.', 3)[0]

        # Get the list of the xml name in the directory
        pdf_files = [path.join(directory_pdf, j) for j in listdir(directory_pdf) if j.endswith('.pdf')]

        # Cycle throught pdf file
        for pdf_file in pdf_files:
            # Get the xml file basename to check in the if
            pdf_name = os.path.basename(pdf_file)
            # Return name pdf without extension
            pdf_no_ext = pdf_name.rsplit('.', 1)[0]

            # If both names are the same, proceed to rename
            if xml_no_ext == pdf_no_ext:
                new_pdf_file_name = Denomination.text + ' FT ' + Invoice_Number_String + ' del ' + Date.text + '.pdf'
                new_xml_file_name = Denomination.text + ' FT ' + Invoice_Number_String + ' del ' + Date.text + '.xml'

                # Rename the file PDF according to the parameters
                os.rename(pdf_file, os.path.join(directory_pdf, new_pdf_file_name))
                os.rename(xml_file, os.path.join(directory_xml, new_xml_file_name))


if __name__ == "__main__":
    main()






