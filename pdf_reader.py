import camelot

pdf = "./Dummy_Shift_Schedule_July_2026.pdf"

table = camelot.read_pdf(pdf, flavor="lattice", pages="all")

df = table[0].df

print(df)
