from deepmerge import always_merger
from langdetect import detect, detect_langs

def taxonomy_reference(code, term):
    return dict(
        links=dict(
            self=f'/api/2.0/taxonomies/{code}/{term}'
        )
    )

def try_name(nlist,record, default=None):
    for name in nlist:
        try:
            return record[name]
        except:
            continue
    else:
        return default
#TODO TESTS
def schema_mapping(existing_record, doi):
    data = {}

    #itemPIDs -required
    always_merger.merge(data, {"itemPIDs": [{"scheme": "DOI", "identifier": doi}]})


    #itemCreators -required
    authors_array = try_name(nlist=['authors', 'author'], record=existing_record)
    if authors_array == None:
        always_merger.merge(data, {'itemCreators': [{"full_name": "Various authors", "nameType": "Personal"}]}) #default
    else:
        if(type(authors_array) is list):
            authors_data = []
            for author in authors_array:
                auth_data = {'nameType': 'Personal'}
                #affiliation /affiliations
                full_name = try_name(nlist=['full_name', 'name', 'fullname', 'literal', "fullName"], record=author)
                if full_name != None:
                    always_merger.merge(auth_data, {"fullName": full_name})
                    authors_data.append(auth_data)
                    continue
                given = try_name(nlist=['given', 'first', 'first_name'], record=author)
                family = try_name(nlist=['family', 'family_name', 'second_name'], record=author)
                if(given == None or family == None):
                    always_merger.merge(auth_data, {"fullName": "unknown"})
                    authors_data.append(auth_data)
                    continue
                else:
                    full_name = family + ", " + given
                    always_merger.merge(auth_data, {"fullName": full_name})
                    authors_data.append(auth_data)
                    continue

            always_merger.merge(data, {'itemCreators': authors_data})

    # document_type
    doctype = try_name(nlist=['document_type', 'type'], record=existing_record)
    if doctype == None:
        always_merger.merge(data, {'document_type': "unknown"})  # default
    else:
        always_merger.merge(data, {'document_type': doctype})

    #publication_year -required
    publication_year = try_name(nlist=['publication_year', 'issued'], record=existing_record)

    if publication_year != None and type(publication_year) is str and len(publication_year['data-part'][0]) == 4:
        always_merger.merge(data, {'itemYear': publication_year})
    elif publication_year != None and type(publication_year) is dict:
        if 'date-parts' in publication_year.keys():
            if len(str(publication_year['date-parts'][0][0])) == 4:
                always_merger.merge(data, {'itemYear': str(publication_year['date-parts'][0][0])})
            else:
                always_merger.merge(data, {'itemYear': "0"})
        else:
            always_merger.merge(data, {'itemYear': "0"})
    else:
        always_merger.merge(data, {'itemYear': "0"})

    # title - required
    title_value = try_name(nlist=['title', 'titles'], record=existing_record)
    if title_value != None:
        if type(title_value) is list:
            title_value= title_value[0]
        title =  title_value
        always_merger.merge(data, {'itemTitle': title})
    else:
        always_merger.merge(data, {'itemTitle': "unknown"}) #default

    # url
    url = try_name(nlist=['url', 'urls', 'URL', 'URLs'], record=existing_record)
    if url != None and type(url) is str:
        always_merger.merge(data, {'itemURL': url})

    # itemResourceType
    always_merger.merge(data, {'itemResourceType': taxonomy_reference('resourceType', 'article')})

    # itemRelationType
    always_merger.merge(data, {'itemRelationType': taxonomy_reference('itemRelationType', 'isReferencedBy')})

    return data
