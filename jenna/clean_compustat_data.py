'''File to serve as place for functions for cleaning and processing Compustat data.'''

import pandas as pd

columns = [
    'gvkey', 'datadate', 'fyearq', 'fqtr', 'fyr', 'indfmt', 'consol', 'popsrc', 'datafmt', 'tic', 
    'cusip', 'conm', 'acctstdq', 'ajexq', 'ajpq', 'curcdq', 'curncdq', 'currtrq', 'datacqtr', 
    'datafqtr', 'finalq', 'rp', 'scfq', 'srcq', 'updq', 'apdedateq', 'fdateq', 'pdateq', 'rdq', 
    'acchgq', 'acomincq', 'acoq', 'actq', 'altoq', 'ancq', 'anoq', 'aociderglq', 'aociotherq', 
    'aocipenq', 'aocisecglq', 'aol2q', 'aoq', 'apq', 'aqpl1q', 'atq', 'aul3q', 'capsq', 'ceqq', 
    'cheq', 'chq', 'cibegniq', 'cicurrq', 'ciderglq', 'cimiiq', 'ciotherq', 'cipenq', 'ciq', 
    'cisecglq', 'citotalq', 'cogsq', 'csh12q', 'cshfd12', 'cshfdq', 'cshiq', 'cshopq', 'cshoq', 
    'cshprq', 'cstkcvq', 'cstkeq', 'cstkq', 'dcomq', 'dd1q', 'diladq', 'dilavq', 'dlcq', 'dlttq', 
    'doq', 'dpactq', 'dpq', 'drcq', 'drltq', 'dvpq', 'epsf12', 'epsfi12', 'epsfiq', 'epsfxq', 
    'epspi12', 'epspiq', 'epspxq', 'epsx12', 'esopctq', 'esopnrq', 'esoprq', 'esoptq', 'fcaq', 
    'gdwlq', 'ibadjq', 'ibcomq', 'ibmiiq', 'ibq', 'icaptq', 'intanoq', 'intanq', 'invfgq', 'invoq', 
    'invrmq', 'invtq', 'invwipq', 'ivltq', 'ivstq', 'lcoq', 'lctq', 'lltq', 'lnoq', 'lol2q', 'loq', 
    'loxdrq', 'lqpl1q', 'lseq', 'ltmibq', 'ltq', 'lul3q', 'mibnq', 'mibq', 'mibtq', 'miiq', 'msaq', 
    'niq', 'nopiq', 'npq', 'oepf12', 'oeps12', 'oepsxq', 'oiadpq', 'oibdpq', 'opepsq', 'piq', 
    'pnrshoq', 'ppegtq', 'ppentq', 'prcraq', 'prshoq', 'pstknq', 'pstkq', 'pstkrq', 'rdipq', 
    'recdq', 'rectaq', 'rectoq', 'rectq', 'rectrq', 'recubq', 'req', 'reunaq', 'revtq', 'saleq', 
    'seqoq', 'seqq', 'spiq', 'stkcoq', 'teqq', 'tfvaq', 'tfvlq', 'tstknq', 'tstkq', 'txdbaq', 
    'txdbcaq', 'txdbclq', 'txdbq', 'txdiq', 'txditcq', 'txpq', 'txtq', 'txwq', 'wcapq', 'xaccq', 
    'xidoq', 'xintq', 'xiq', 'xoprq', 'xrdq', 'xsgaq', 'acchgy', 'aolochy', 'apalchy', 'aqcy', 
    'capxy', 'chechy', 'cibegniy', 'cicurry', 'cidergly', 'cimiiy', 'ciothery', 'cipeny', 
    'cisecgly', 'citotaly', 'ciy', 'cogsy', 'cshfdy', 'cshpry', 'cstkey', 'dilady', 'dilavy', 
    'dlcchy', 'dltisy', 'dltry', 'doy', 'dpcy', 'dpy', 'dvpy', 'dvy', 'epsfiy', 'epsfxy', 'epspiy', 
    'epspxy', 'esubcy', 'exrey', 'fcay', 'fiaoy', 'fincfy', 'fopoxy', 'fopoy', 'ibadjy', 'ibcomy', 
    'ibcy', 'ibmiiy', 'iby', 'intpny', 'invchy', 'ivacoy', 'ivchy', 'ivncfy', 'ivstchy', 'miiy', 
    'niy', 'nopiy', 'oancfy', 'oepsxy', 'oiadpy', 'oibdpy', 'opepsy', 'piy', 'prstkcy', 'rdipy', 
    'recchy', 'revty', 'saley', 'sivy', 'spiy', 'sppey', 'sppivy', 'sstky', 'stkcoy', 'txachy', 
    'txbcofy', 'txbcoy', 'txdcy', 'txdiy', 'txpdy', 'txty', 'txwy', 'xidocy', 'xidoy', 'xinty', 
    'xiy', 'xopry', 'xrdy', 'xsgay', 'exchg', 'cik', 'costat', 'fic', 'cshtrq', 'dvpspq', 'dvpsxq', 
    'mkvaltq', 'prccq', 'prchq', 'prclq', 'adjex', 'add1', 'addzip', 'busdesc', 'city', 'conml', 
    'ein', 'fax', 'fyrc', 'ggroup', 'gind', 'gsector', 'gsubind', 'idbflag', 'incorp', 'loc', 
    'naics', 'phone', 'prican', 'priusa', 'sic', 'spcindcd', 'spcseccd', 'spcsrc', 'state', 'stko', 
    'weburl', 'ipodate'
]

def load_csv(file_path, dtype_spec):
    """Load data from a CSV file."""
    try:
        df = pd.read_csv(file_path, dtype=dtype_spec, low_memory=False)
        return df
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def load_parquet(file_path):
    """Load data from a Parquet file."""
    try:
        df = pd.read_parquet(file_path)
        return df
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def clean_data(df):
    """Apply common preprocessing steps to the DataFrame."""
    # Convert date columns to datetime
    date_columns = ['datadate', 'apdedateq', 'fdateq', 'pdateq', 'rdq', 'adjex', 'ipodate']
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    # Drop columns with typically more than 80% nulls
    df = df[columns]
    
    # Fill missing values for numerical columns with 0
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
    df[numeric_columns] = df[numeric_columns].fillna(0) # not sure if we want to do this
    
    # Fill missing values for object columns with 'Unknown'
    object_columns = df.select_dtypes(include=['object']).columns
    df[object_columns] = df[object_columns].fillna('Unknown')
    
    return df