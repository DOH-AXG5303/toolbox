import redcap
import pandas as pd

def describe_fields(project):
    """
    create a summary dataframe to describe every standard field from default API export
    
    args:
        pycap Project object
    return:
        Dataframe
        
    """  
    df_fields = project.export_field_names(format_type = "df")
    df_meta = project.export_metadata(format_type = "df")
    
    #set aside choice fields Series
    choice_fields = df_meta[df_meta["field_type"].isin(['dropdown', 'radio', 'checkbox'])]["select_choices_or_calculations"].copy()#select field type "dropdown","radio", "checkbox"
    choice_fields = choice_fields[choice_fields.notnull()] #remove possibility of NA fields

    #drop the first row, it is the index of dataframe export (unique identified: record_id, sample_id)
    df_meta = df_meta.drop(df_meta.index[0])
    df_fields = df_fields.drop(df_fields.index[0])

    #only need 2 fields from metadata export
    df_meta = df_meta[["form_name", "field_type", "text_validation_type_or_show_slider_number"]].copy()

    #combine fields from metadata and from export_field_names 
    df_fields_2 = df_fields.join(df_meta)
    
    #add field names that have type "file" (from metadata)
    files_df = df_meta[df_meta["field_type"] == "file"].copy()
    files_df['export_field_name'] = files_df.index
    df_fields_3 = pd.concat([df_fields_2, files_df])
    
    #set index to export_field_name
    df_fields_3 = df_fields_3.set_index("export_field_name")
    
    ##### add a new columns: str(dict) of possible choices for multiple choice fields####
    fields_dict = {}
    for i in choice_fields.iteritems():

        string_to_process = i[1] #the value element of the series (as opposed to index element)
        list_of_strings = string_to_process.split("|") # split the string 
        keys_values_list = [i.split(", ", 1) for i in list_of_strings]# split each list once for list of lists [key, values]
        values_dict = {t[0]:t[1] for t in keys_values_list} #dictionary of key value pairs
        fields_dict[i[0]] =  str(values_dict)

    choice_fields_series = pd.Series(fields_dict)

    complete = pd.concat([df_fields_3 ,choice_fields_series.to_frame("Choice Values")], axis = 1)
    
    ## add special case for multiple choice fields - "yesno" field type 
    yesno_dict = {"1":"Yes", "0":"No"}
    yesno_index = df_meta[df_meta["field_type"] == "yesno"].index
    yesno_series = pd.Series(str(yesno_dict), yesno_index) #create series, yes/values and index for all yesno field type
    yesno_frame = yesno_series.to_frame("Choice Values")
    
    df_joined = complete.join(yesno_frame, lsuffix='_l', rsuffix='_r')
    
    complete["Choice Values"] = df_joined["Choice Values_l"].fillna(df_joined["Choice Values_r"])
    
    return complete
