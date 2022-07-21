import string
import random
import hashlib
import numpy as np



def padding_gen():
    """
    Generate a string of random length between 0 and 3000 characters
    to be used as padding for API calls
    
    return:
        string 
    """
    
    chars = string.ascii_uppercase + string.digits + string.ascii_lowercase
    length = random.randint(0,3000)
    
    return "".join([random.choice(chars) for i in range(length)])


def uuid_gen(text, salt = "HMAC_key"):
    """
    Generate a hash (uuid) from phone number string and HMAC key (unique passphrase)
    MD5 hash algorithm 
    
    return:
        string
    """
    textutf8 = text.encode("utf-8")
    saltutf8 = salt.encode("utf-8")
    
    hash_key = hashlib.md5(saltutf8+b":"+textutf8)
    hexa = hash_key.hexdigest()
    
    return hexa
    
    
def rename_columns(df, dic):
    """
    Rename dataframe columns to key if found in list of values in provided dictionary {"new_clm_name":["name1", "name2", "name3", etc.]}
    Args:
        df: dataframe to be modified
        dict: dictionary to map 
    """
    for key, value in dic.items():
        mask = df.columns.isin(value)
        cols_array = np.array(df.columns)
        cols_array[mask] = key 
        
        df.columns = cols_array
        
    return df
    
    
def compare_similar_dataframes(df1,df2):
    """
    Provides analysis of two dataframes that are expected to be identical.
    Args:
        df1 - Dataframe object
        df2 - Dataframe object    
    """
    #sort columns in both dataframes
    df1.columns = df1.columns.sort_values()
    df2.columns = df2.columns.sort_values()
    
    #common columns for multiple comparisons
    in_common = set(df1.columns) & set(df2.columns)
    
    #to add missmatched elements
    not_identical = []
    
    # Compare shape
    if df1.shape == df2.shape:
        print(f"The shapes of Dataframe1 and Dataframe2 are identical: {df1.shape}")
        print()
        
        if set(df1.columns) == set(df2.columns):
            print(f"The columns of Dataframe1 and Dataframe2 are identical, congrats!")
            print()
            
            #compare each set of series
            #FOR FUTURE SELF: CREATE STATEMENT TO TEST SERIES EQUALITY
            for i in df1.columns:
                try:
                    pd.testing.assert_series_equal(df1[i], df2[i], check_dtype=False)
                except:
                    print(f"NOT IDENTICAL: {i}")
                    print()
                    
                    not_identical.append(i)
                    
            return not_identical
        
        else:
            print(f"The columns of Dataframe1 and Dataframe2 are named different")
            print()
            print(f"The following columns are unique to Dataframe1: {set(df1.columns) - in_common}")
            print()
            print(f"The following columns are unique to Dataframe2: {set(df2.columns) - in_common}")
            print()

    elif df1.shape[1] != df2.shape[1]:
        print(f"The columns are not the same size. Dataframe1: {df1.shape[1]}, Dataframe2: {df2.shape[1]}")
        print()
        
        print(f"The following columns are unique to Dataframe1: {set(df1.columns) - in_common}")
        print()
        print(f"The following columns are unique to Dataframe2: {set(df2.columns) - in_common}")
        print()
    
    elif df1.shape[0] != df2.shape[0]:
        print(f"The rows are not the same size. Dataframe1: {df1.shape[0]}, Dataframe2: {df2.shape[0]}")
        print()
    
    else:
        print("something is really off about your dataframes, possibly different MultiIndex")