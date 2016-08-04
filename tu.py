import pandas
import os
import matplotlib.pyplot as plt
import sys
from bs4 import BeautifulSoup

# CHANGE ME
FILES_TO_PROCESS = 10000

# Init arrays for collecting scatter plot data
things_of_interest = ['rent roll','appraisal','payment history']
rrs = []
apps = []
phs = []
error_count = 0
file_count = 0

# If row contains name set the Flag to True
def match_name( name, cell_str, flag ):
	# Don't check contains in cell if flag is already true
	if flag:
		return True
	else:
		if name in cell_str:
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
		if file.endswith(".html") or file.endswith(".htm"):
			loc = os.path.join(root, file)
			# Show progress
			sys.stdout.write('|')
			sys.stdout.flush()

			with open(loc) as f:
				
					file_count += 1
					# extract tables from html 
					bs_tables = BeautifulSoup(f.read(), "lxml").findAll('table')
					for bs_table in bs_tables:
						try:
							bs_table_string = str(bs_table).lower()
							
							if any(x in bs_table_string for x in things_of_interest):
								# load html table as a DataFrame 
								df = pandas.read_html(bs_table_string)

								for table in df:
									try:
										# Init flags to detect table type
										rr_flag = False
										app_flag = False
										ph_flag = False

										for index, row in table.iterrows():
											try:
												for cell in row:
													cell_str = str(cell)
													rr_flag = match_name('rent roll', cell_str, rr_flag)
													app_flag = match_name('appraisal', cell_str, app_flag)
													ph_flag = match_name('payment history', cell_str, ph_flag)

												if rr_flag and app_flag and ph_flag:
													break
											except (ValueError):
												pass

										# Append to the correct scatter plot data
										if rr_flag:		
											rrs.append(table.shape)
										if app_flag:		
											apps.append(table.shape)
										if ph_flag:		
											phs.append(table.shape)
									except (ValueError):
										pass
						except (ValueError):
							error_count += 1

# Create plot arrays
rr_x_val = [x[1] for x in rrs]
rr_y_val = [x[0] for x in rrs]

app_x_val = [x[1] for x in apps]
app_y_val = [x[0] for x in apps]

ph_x_val = [x[1] for x in phs]
ph_y_val = [x[0] for x in phs]

print('X')
print("Files: {a:5d} , Errors : {b:5d}".format(a=file_count, b=error_count))

fig = plt.figure(figsize=(32,10))

# Scatter plot 
ax0 = fig.add_subplot(331)
ax0.scatter(rr_x_val, rr_y_val, s=10, c='b', marker="s", label='Rent Roll')
ax0.set_title('Rent Roll - Shapes')
ax0.set_xlabel('Rows')
ax0.set_ylabel('Columns')

ax1 = fig.add_subplot(332)
ax1.scatter(app_x_val, app_y_val, s=10, c='r', marker="o", label='Appraisal')
ax1.set_title('Appraisal - Shapes')
ax1.set_xlabel('Rows')
ax1.set_ylabel('Columns')

ax2 = fig.add_subplot(333)
ax2.scatter(ph_x_val, ph_y_val, s=10, c='r', marker="o", label='Payment History')
ax2.set_title('Payment History - Shapes')
ax2.set_xlabel('Rows')
ax2.set_ylabel('Columns')

# Histograms
ax3 = fig.add_subplot(334)
ax3.hist(rr_y_val)
ax3.set_title("Rent Roll - Columns")

ax4 = fig.add_subplot(335)
ax4.hist(app_y_val)
ax4.set_title("Appraisal - Columns")

ax5 = fig.add_subplot(336)
ax5.hist(ph_y_val)
ax5.set_title("Payment History - Columns")

ax6 = fig.add_subplot(337)
ax6.hist(rr_x_val)
ax6.set_title("Rent Roll - Rows")

ax7 = fig.add_subplot(338)
ax7.hist(app_x_val)
ax7.set_title("Appraisal - Rows")

ax8 = fig.add_subplot(339)
ax8.hist(ph_x_val)
ax8.set_title("Payment History - Rows")

# Save and Show plot
plt.savefig('tu.png')
plt.show()
