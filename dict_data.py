def import_dictionaries():
    """imports dictionaries
    
    No parameters, no returns
    
    But it does set variables equal to certain dictionaries, so here is that:
    
    int_to_title : integer to title values (ex: {0: "Another One Bites The Dust by Queen"})
    
    int_to_pathstring : integer to pathstring values (ex: {0: "another"})
    
    ¡¡Remember these variable names for use!!   """
    
    f = open("save.p", "rb")
    int_to_title = pickle.load(f)
    int_to_pathstring = pickle.load(f)
    f.close()
    
    
    