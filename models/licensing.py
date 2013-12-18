""" Everything we need to know about wrangling licensing and attribution information.
"""
from collections import defaultdict

class Licensing():
    def __init__( self ):
        pass

    def get_formatted_licensing( self, sheets ):
        # Organize the license information for display
        licenses = defaultdict( lambda:
            defaultdict( lambda: [] )
        )

        for sheet in sheets:
            key = ( sheet.credit_name, sheet.credit_url )
            licenses[sheet.license][key].append( sheet.name )

        # Construct and display the combined license text
        license_text = ""
        for art_license in licenses:
            license_text += "The following artwork is used by permission in accordance with %s:\n" % ( art_license, )
            for key in licenses[art_license]:
                credit, url = key
                license_text += "    Artwork by %s ( %s ):\n        " % ( credit, url )
                license_text += ', '.join( licenses[art_license][( credit, url )] )
                license_text += "\n"
            license_text += "\n"

        return license_text

LICENSING = Licensing()
