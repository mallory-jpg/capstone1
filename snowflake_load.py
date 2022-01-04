# create DB & schema where data will be staged

# create table into which data will be loaded

# COPY INTO SOCIAL_MEDIA_DB.DBT_ANALYTICS_SCHEMA.<INPUT_TABLE>
# FROM @SOCIAL_MEDIA_DB.DBT_ANALYTICS_SCHEMA.<STAGE>
# FILE_FORMAT = (TYPE = 'JSON' STRIP_OUTER_ARRAY = TRUE);


################################################################

# define variablesSimpleList
variablesSimpleList = []

# Define an empty list to populate with variables
variablesList = []

# Loop through the members of variablesSimpleList and add them to variablesList
# This script assumes the first entry of each member of variablesSimpleList is the sourceLocation,
# and that the second entry is the destinationTable.
for [sourceLocation, destinationTable] in variablesSimpleList:
    variablesList.append(
        {
        'sourceLocation': sourceLocation,
        'destinationTable': destinationTable
        }
    )