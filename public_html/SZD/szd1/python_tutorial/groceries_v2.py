import pandas as pd
import sys

def main():

    #load data
    filename = sys.argv[1]
    df = pd.read_csv(filename, sep = '\t') 
    
    #df stands for dataframe, 'sep' stands for separator of our values (tabulator in this case).

    #calculate the final price of our grocery list
    sum = df['mnozstvi'] * df['cena_za_jednotku'] 
    
    #this is a elementwise product of two arrays, no looping is required
    
    sum = sum.sum() 
    
    #note: sum is dataframe variable, we need to change it from dataframe to a number. 
    #The sum, max, etc. methods are also implemented

    #printing the grocery list and the total cost
    print(df['polozka'].tolist(), sum) 
    
    #the tolist() function converts dataframe to python array


#this if statement is executed when the script is directly executed. When it is called inside a different script, it will not execute.
if __name__ == "__main__":
    main()
