import pandas
import os
import matplotlib.pyplot as plt
import sys
from bs4 import BeautifulSoup

# CHANGE ME
FILES_TO_PROCESS = 10000

# Init arrays for collecting scatter plot data
thing_of_interest = sys.argv[1]
print('Finding: ')
print(thing_of_interest)
shapes = []
error_count = 0
file_count = 0

# If row contains name set the Flag to True
def match_name( name, row_str, flag ):
	# Don't check contains in row if flag is already true
	if flag:
		return True
	else:
		if name in row_str:
			return True
		else:
			return False 

# Walk the FS (For testing use: /Users/debajyotiroy/Ingest/test)
for root, dirs, files in os.walk("/Users/debajyotiroy/Ingest/Staging"):
	if file_count >= FILES_TO_PROCESS:
		break

	for file in files:
		if file_count >= FILES_TO_PROCESS:
			break
		# For a html file
		if file.endswith(".html"):
			loc = os.path.join(root, file)
			# Show progress
			sys.stdout.write('|')
			sys.stdout.flush()

			with open(loc) as f:
				try:
					file_count += 1
					# extract tables from html 
					bs_tables = BeautifulSoup(f.read(), "lxml").findAll('table')
					for bs_table in bs_tables:
						bs_table_string = str(bs_table)
						if thing_of_interest in bs_table_string:
							# load html table as a DataFrame 
							df = pandas.read_html(bs_table_string)
							for table in df:

								# Init flags to detect table type
								shape_flag = False

								for index, row in table.iterrows():
									row_str = row.to_string().lower()

									shape_flag = match_name(thing_of_interest, row_str, shape_flag)

									if shape_flag:
										break

								# Append to the correct scatter plot data
								if shape_flag:		
									shapes.append(table.shape)
				except (ValueError):
					error_count += 1
					pass

# Create plot arrays
x_val = [x[0] for x in shapes]
y_val = [x[1] for x in shapes]

print('X')
print("Files: {a:5d} , Errors : {b:5d}".format(a=file_count, b=error_count))

fig = plt.figure(figsize=(32,10))

# Scatter plot 
ax0 = fig.add_subplot(131)
ax0.scatter(x_val, y_val, s=10, c='b', marker="s", label=thing_of_interest)
ax0.set_title(thing_of_interest+' - Shapes')
ax0.set_xlabel('Rows')
ax0.set_ylabel('Columns')

# Histograms
ax1 = fig.add_subplot(132)
ax1.hist(y_val)
ax1.set_title(thing_of_interest+' - Columns')

ax2 = fig.add_subplot(133)
ax2.hist(x_val)
ax2.set_title(thing_of_interest+' - Rows')

# Save and Show plot
plt.savefig('tu_'+thing_of_interest+'.png')
plt.show()