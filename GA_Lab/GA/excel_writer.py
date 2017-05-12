import xlsxwriter
import pandas as pd
import numpy as np
from itertools import product

def main():
    df1 = pd.DataFrame.from_csv('data - Copy.csv')
    df2 = pd.DataFrame.from_csv('data - deb1_4 ndim1.csv')
    df3 = pd.DataFrame.from_csv('data_2.csv')
    df4 = pd.DataFrame.from_csv('data_2 (1).csv')


    # df = pd.DataFrame.from_csv('data - Copy (2).csv')
    df = pd.concat([df1, df2, df3, df4], ignore_index=True)

    writer = pd.ExcelWriter('GA_Table.xlsx', engine='xlsxwriter')

    # df.to_excel(writer, sheet_name='Sheet1')

    n = df.N.unique()
    ndim = df.dimensions.unique()
    pm = df.p_m.unique()
    pc = df.p_c.unique()
    coding = df.coding.unique()
    mutation = df.mutation.unique()
    crossover = df.crossover.unique()
    distance_measure = df.distance_measure.unique()
    cs = df.crowding_selection.unique()
    cf = df.crowding_factor.unique()
    s = df.subpopulation_size.unique()
    functions = df.function_name.unique()

    method = df.method.unique()

    hierarchical = list(product(n, ndim, pm, pc, coding, mutation, crossover, distance_measure, cs, cf, s, method, functions))

    subdfs = []
    for (n, ndim, pm, pc, coding, mutation, crossover, distance_measure, cs, cf, s, method, function) in hierarchical:
        subdfs.append(df[df.N==n][df.dimensions==ndim][df.p_m==pm][df.p_c==pc][df.coding==coding][df.mutation==mutation][df.crossover==crossover][df.crowding_selection==cs][df.crowding_factor==cf][df.subpopulation_size==s][df.method==method][df.function_name==function])

    for subdf in subdfs:
        if not subdf.empty:
            _, name=subdf.function_name.unique()[0].split('.')
            dim = int(subdf.dimensions.unique()[0])
            
            subdf.to_excel(writer, sheet_name='{}-{}'.format(name,dim))

            # import pdb; pdb.set_trace()

            agg_params = {'NFE':['mean', 'min'],
               'NP': ['mean'],
               'PA': ['mean', 'min'],
               'PR': ['mean', lambda x: min(abs(x-1))],
               'DA': ['mean', 'min'],
               'run_time': ['mean', 'min', 'max']
              }
            agg_info = subdf.groupby(['method', 'function_name', 'dimensions', 'coding', 'crossover', 'p_c', 'p_m', 'mutation',  'crowding_selection', 'subpopulation_size', 'crowding_factor']).agg(agg_params)

            agg_info.to_excel(writer, sheet_name='{}-{}-aggregate'.format(name,dim))

    writer.save()

if __name__ == '__main__':
    main()
