from .models import Type, Jewel, ManufacturingTechnique

## search_jewel.py
##
## Utilities for the search bar of the jowel shop.
## Contain input validation of the search, and
## query filtering.

def int_converter(get_request, key):
    """
    Whenever a search key is avaible, tranform a string of ids in
    format "1,2,3[...]" into a python list of integer.
    """
    list_ids = get_request[key].split(",")
    try:
        list_ids = [int(id) for id in list_ids]
    except ValueError:
        return False
    get_request[key] = list_ids
    return True

def proper_search_input(get_request):
    """
    Convert ids reveiced with GET request into a python list.
    """
    if not get_request.get("technique"):
        return False
    if int_converter(get_request, "technique") is False:
        return False
    if get_request.get("types"):
        if int_converter(get_request, "types") is False:
            return False
    return True

def ids_does_exists(table, list_ids):
    """
    Check if every single ids are existing in the table.
    """
    for id in list_ids:
        try:
            table.objects.get(id=id)
        except table.DoesNotExist:
            return False
    return True

def control_search(get_request):
    """
    Control user input whenever a search is performed by the user.
    Check the type of given input and transform them in
    list of int for the request.GET object.
    Check if received ids for types and technique are existing.
    """
    #Clean up field and convert them into integer list
    if proper_search_input(get_request) is False:
        return False

    #Control ids existance for type and category
    type_ids = get_request.get("types")
    if type_ids and ids_does_exists(Type, type_ids) is False:
        return False
    category_ids = get_request.get("technique")
    if category_ids and ids_does_exists(ManufacturingTechnique, category_ids) is False:
        return False
    return True

def retrieve_searched_jewel(get_request):
    """
    Retrieve the selection of jewel according to the search filter.
    Return all jewels if not filter is available.
    """
    ids_technique = get_request.get("technique")
    ids_type = get_request.get("types")
    #Retrieve all jewel, and remove those with null Type and technique
    list_jewels = Jewel.objects.all().filter(type__isnull=False).\
            filter(technique__isnull=False)
    #Return all jewel if no filter need to be applied
    if ids_type:
        list_jewels = list_jewels.filter(type__in=ids_type)
    if ids_technique:
        list_jewels = list_jewels.filter(technique__in=ids_technique)
    return reversed(list_jewels)
