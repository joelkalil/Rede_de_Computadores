import pandas as pd

dt1 = pd.read_csv('data/pv_10kw.csv')

dt2 = pd.read_csv('data/profiles.csv.data')

# List to convert in pandas after processing
new_dt1 = []

#
new_dt2 = dt2.copy()

# Suport variable
count = 0
mean_val = 0

# Initial value
new_dt1.append({
    'Date': dt1['Date'][0],
    'P # [W]': dt1['P # [W]'][0]
})

# Looping
for i in range(1, dt1['Date'].size-1):
    mean_val += dt1['P # [W]'][i]
    count += 1

    if count == 15:
        new_dt1.append({
            'Date': dt1['Date'][i],
            'P # [W]': mean_val/15
        })
        count = 0
        mean_val = 0

# Converting list of jsons to pandas
new_dt1 = pd.json_normalize(data=new_dt1)
print(new_dt1)

# Exporting the new dataframe
new_dt1.to_csv('data/new_pv_10kw.csv', index=False)

# Sum the dt1 and dt2 to 0~30 indexs
for i in range(0,30):
    new_dt2[str(i)] = new_dt2[str(i)] + new_dt1['P # [W]']

print(new_dt2)

# Exporting the new dataframe
new_dt2.to_csv('data/new_profiles.csv.data', index=False)