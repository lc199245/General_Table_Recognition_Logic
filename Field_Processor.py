"""
	Module PDF_Processor.py
	Author @Chang Liu
	1. handle all raw contents extraction 
	2. auto-detect table contents and extract them based on the rules 
	3. auto-detect free text contents and extract them based on the rules
	4. process page by page
"""




from PDF_Database_Control import DB_Controller;

import pandas as pd;
import re;
import sys;


agency_type = '';
deal_month = '';
sorted_block_level_component_list = [];
sorted_charanno_level_component_list = [];


"""
	KEY METHOD
	method: detect_table_with_short_lines_cover_begin_only
	extract contents from tables that contain pricing speed and wals info 
	the new table extraction logic is in the following four methods, each one is responsible for a specific case:
	1. detect_table_with_short_lines_cover_begin_only
	2. detect_vertical_table_with_lines
	3. detect_table_with_lines_cover_begin_only
	4. detect_table_with_lines_cover_begin_end
	In general they share similar design, the difference between each other will be in the method comments
	the detailed steps are similar, comments about details are in method 3 and 4
"""
#####################################################################################################################
def detect_table_with_short_lines_cover_begin_only(doc_id_sent,page_number_sent,sorted_charanno_level_component_list_sent, extraction_criteria_id):
	max_x_on_page = max(zip(*sorted_charanno_level_component_list_sent)[6]);
	max_x_on_page = max_x_on_page + 1;

	min_x_on_page = min(zip(*sorted_charanno_level_component_list_sent)[4]);
	min_x_on_page = min_x_on_page - 1;

	min_y_on_page = min(zip(*sorted_charanno_level_component_list_sent)[5]);
	min_y_on_page = min_y_on_page - 1;

	max_y_on_page = max(zip(*sorted_charanno_level_component_list_sent)[7]);
	max_y_on_page = max_y_on_page + 1;


	

	cell_level_result_list = [];

	db_table_line_list = [];
	# print page_number_sent;


	x_and_y_value_block_list = [];

	horizontal_lines_list = [item for item in sorted_charanno_level_component_list_sent if ('LTLine' in item[2] or 'LTCurve' in item[2]) and item[-2] > 5 and item[-1] < 0.1 ];
	
	y_value_list = [horizontal_lines_list[0][5]];
	for i in range(1, len(horizontal_lines_list)):
		if abs(horizontal_lines_list[i][5] - y_value_list[-1]) > 5:
			y_value_list.append(horizontal_lines_list[i][5]);

	
	

	filtered_charanno_level_component_list = [item for item in sorted_charanno_level_component_list_sent if item[3] == 'LTChar' and item[5] < max(y_value_list)+20];

	current_y_value = filtered_charanno_level_component_list[0][5];
	temp_count = 1;
	
	filtered_result_y_value_list = [];

	for item in filtered_charanno_level_component_list:
		if item[5] == current_y_value:
			temp_count += 1;
			continue;
		if item[5] != current_y_value:
			if temp_count > 5:
				filtered_result_y_value_list.append(round(current_y_value,1));
				current_y_value = item[5];
				temp_count = 1;
			else:
				current_y_value = item[5];
				temp_count = 1;
			continue;

	if temp_count > 5:
		filtered_result_y_value_list.append(current_y_value);	
	
	filtered_result_y_value_list = sorted(list(set(filtered_result_y_value_list)), key=lambda x: -x);

	filtered_result_y_value_list_dup = [];

	for i in range(0, len(filtered_result_y_value_list)-1):
		if abs(filtered_result_y_value_list[i+1] - filtered_result_y_value_list[i]) > 18:
			filtered_result_y_value_list_dup.append(filtered_result_y_value_list[i]);





	y_value_list = y_value_list + filtered_result_y_value_list_dup;

	y_value_list = sorted(list(set([round(item,1) for item in y_value_list])), key=lambda x: -x);


	for item in y_value_list:
		if max_x_on_page < 680:
			db_table_line_list.append([page_number_sent, min_x_on_page * 3, 2376 - item * 3, abs(max_x_on_page - min_x_on_page) * 3, 0.02]);
		else:
			db_table_line_list.append([page_number_sent, min_x_on_page * 3, 1836 - item * 3, abs(max_x_on_page - min_x_on_page),0.02]);		
	


	
	for i in range(0, len(y_value_list)):
		part_x_value_list = [];
		part_y_value_list = [];

		if i % 3 == 0 and i+2 <= len(y_value_list) - 1:
			temp_x_value_list = [];
			temp_max_y = y_value_list[i];
			temp_min_y = y_value_list[i+2];
			temp_filtered_charanno_list = [item for item in filtered_charanno_level_component_list if item[5] >= temp_min_y and item[7] <= temp_max_y];
			
			temp_min_x = min([item[4] for item in temp_filtered_charanno_list if item[5] >= temp_min_y and item[7] <= temp_max_y]);
			temp_max_x = max([item[6] for item in temp_filtered_charanno_list if item[5] >= temp_min_y and item[7] <= temp_max_y]);

			temp_x_value = temp_min_x-1;
			part_y_value_list.append(temp_max_y);
			part_y_value_list.append(temp_min_y);
			while temp_x_value <= temp_max_x+1:
				if sum([1 for item in temp_filtered_charanno_list if item[4] <= temp_x_value and item[6] >= temp_x_value]) == 0:
					temp_x_value_list.append(temp_x_value);
				temp_x_value += 1;

			temp_x_value_list_dup = [temp_x_value_list[0]];

			for j in range(1, len(temp_x_value_list)):
				if (temp_x_value_list[j] - temp_x_value_list[j-1]) > 1:
					temp_x_value_list_dup.append(temp_x_value_list[j]);


			
			for item_x in temp_x_value_list_dup:
				part_x_value_list.append(item_x);
				if max_x_on_page < 680:
					db_table_line_list.append([page_number_sent, item_x * 3, 2376-y_value_list[i]*3 , 0.02, abs(y_value_list[i+2] - y_value_list[i]) * 3])
				else:
					db_table_line_list.append([page_number_sent, item_x * 3, 1836-y_value_list[i]*3 , 0.02, abs(y_value_list[i+2] - y_value_list[i]) * 3])	



			current_y_value = temp_filtered_charanno_list[0][5];
			temp_count = 1;
			filtered_result_y_value_list = [];
			for item in temp_filtered_charanno_list:
				# print item[0];
				if item[5] == current_y_value:
					temp_count += 1;
					continue;
				if item[5] != current_y_value:
					if temp_count > 3:
						# print '                                   ',current_y_value;
						filtered_result_y_value_list.append(round(current_y_value,1));
						current_y_value = item[5];
						temp_count = 1;
					else:
						current_y_value = item[5];
						temp_count = 1;
					continue;

			if temp_count > 5:
				filtered_result_y_value_list.append(current_y_value);

			for item in filtered_result_y_value_list:
				part_y_value_list.append(item);
				if max_x_on_page < 680:
					db_table_line_list.append([page_number_sent, temp_min_x * 3,2376 - item * 3, abs(temp_max_x - temp_min_x) * 3, 0.02]);
				else:
					db_table_line_list.append([page_number_sent, temp_min_x * 3,1836 - item * 3, abs(temp_max_x - temp_min_x) * 3, 0.02]);

			x_and_y_value_block_list.append([sorted(list(set([round(item,0) for item in part_x_value_list]))),sorted(list(set([round(item,0) for item in part_y_value_list])), key=lambda x: -x)]);
			
			part_x_value_list = [];
			part_y_value_list = [];			



	for data_pair in x_and_y_value_block_list:

		for i in range(0, len(data_pair[1])-1):



			y_value = data_pair[1][i];
			y_value_2 = data_pair[1][i+1];

			if i == 0:
				cell_string_value = ''.join([item[11] for item in filtered_charanno_level_component_list if item[5] < y_value + 3 and item[5] > y_value - 3]);
				cell_level_result_list.append([[extraction_criteria_id, item[0], cell_string_value, 100, y_value, 660, y_value + 20, item[9]]])



			row_cell_list = [];
			if abs(y_value_2 - y_value) < 5:
				continue;
			for j in range(0, len(data_pair[0])-1):
				x_value = data_pair[0][j];
				x_value_2 = data_pair[0][j+1]
				if abs(x_value_2 - x_value) < 8:
					continue;


				cell_string_value = ''.join([item[11] for item in filtered_charanno_level_component_list if item[5] < y_value_2 + 1 and item[5] > y_value_2 - 1 and item[6] < x_value_2 and item[4] > x_value ]);
				cell_string_value = re.sub(r'\t',' ', cell_string_value);
				row_cell_list.append([extraction_criteria_id, item[0], cell_string_value, x_value, y_value_2, x_value_2, y_value, item[9]]);

			cell_level_result_list.append(row_cell_list);	


	return db_table_line_list, cell_level_result_list;	





"""
	KEY METHOD
	method: detect_vertical_table_with_lines
	extract contents from tables that locate on vertical pages 

	example pdf pages:
	Available combinations or recombinations pages for Ginnie Freddie Fannie
	similar logic compares to other table detection methods
	here we find a set of short lines that share same y coordinate values, we know it's the title row, the begin of the table 

"""
################################################################################################################################
def detect_vertical_table_with_lines(doc_id_sent,page_number_sent,sorted_charanno_level_component_list_sent, extraction_criteria_id):
	db_table_line_list = [];
	max_x_on_page = max(zip(*sorted_charanno_level_component_list_sent)[6]);
	max_x_on_page = max_x_on_page + 1;

	min_x_on_page = min(zip(*sorted_charanno_level_component_list_sent)[4]);
	min_x_on_page = min_x_on_page - 1;

	min_y_on_page = min(zip(*sorted_charanno_level_component_list_sent)[5]);
	min_y_on_page = min_y_on_page - 1;

	max_y_on_page = max(zip(*sorted_charanno_level_component_list_sent)[7]);
	max_y_on_page = max_y_on_page + 1;


	horizontal_lines_list = [item for item in sorted_charanno_level_component_list_sent if (item[2] == 'LTLine' or item[2] == 'LTCurve') and item[-1] < 1 ];


	if len(horizontal_lines_list) == 0:
		return [],[];

	max_x_on_page = max(zip(*horizontal_lines_list)[6]) + 1;
	min_x_on_page = min(zip(*horizontal_lines_list)[4]) - 1;

	y_value_list = [round(item[5],1) for item in horizontal_lines_list];
	

	filtered_result_y_value_list = [];

	filtered_charanno_level_component_list = [item for item in sorted_charanno_level_component_list_sent if item[3] == 'LTChar'];

	current_y_value = filtered_charanno_level_component_list[0][5];
	temp_count = 1;
	for item in filtered_charanno_level_component_list:
		if item[5] == current_y_value:
			temp_count += 1;
			continue;
		if item[5] != current_y_value:
			if temp_count > 5:
				filtered_result_y_value_list.append(round(current_y_value,1));
				current_y_value = item[5];
				temp_count = 1;
			else:
				current_y_value = item[5];
				temp_count = 1;
			continue;

	if temp_count > 5:
		filtered_result_y_value_list.append(current_y_value);	
	



	y_value_list = sorted(list(set(y_value_list)), key=lambda x: -x);


	if len(y_value_list) < 3:
		y_value_list = y_value_list + [sorted(filtered_result_y_value_list, key=lambda x: -x)[-1]];


	y_value_list = sorted(list(set(y_value_list)), key=lambda x: -x);


	print '========================================';
	print len(sorted_charanno_level_component_list_sent);

	filtered_charanno_level_component_list = [item for item in sorted_charanno_level_component_list_sent if item[3] == 'LTChar' and item[4] > min_x_on_page and item[6] < max_x_on_page and item[5] >= y_value_list[-1] and item[7] <= y_value_list[1] ];
	print len(filtered_charanno_level_component_list);



	current_y_value = filtered_charanno_level_component_list[0][5];
	temp_count = 1;
	filtered_result_y_value_list = [];
	for item in filtered_charanno_level_component_list:
		if item[5] == current_y_value:
			temp_count += 1;
			continue;
		if item[5] != current_y_value:
			if temp_count > 3:
				filtered_result_y_value_list.append(round(current_y_value,1));
				current_y_value = item[5];
				temp_count = 1;
			else:
				current_y_value = item[5];
				temp_count = 1;
			continue;

	if temp_count > 5:
		filtered_result_y_value_list.append(current_y_value);	

	y_value_list = sorted(list(set(y_value_list + filtered_result_y_value_list)), key=lambda x: -x);

	y_value_list = y_value_list[1:];
	

	line_height = abs(y_value_list[0] - y_value_list[-1]);


	temp_x_value = min_x_on_page-1;

	result_x_value_list = [];




	current_x_value = 0;
	while temp_x_value < max_x_on_page:
		flag = 0;
		for item in filtered_charanno_level_component_list:
			if item[4] < temp_x_value and item[6] > temp_x_value:
				flag = 1;
				break;
		if flag == 0:
			result_x_value_list.append(temp_x_value);

		temp_x_value += 1;





	final_result_x_value_list = [];

	current_stack = [];


	for item in result_x_value_list:
		if current_stack == []:
			current_stack.append(item);
			continue;
		if abs(item - current_stack[-1]) <= 1:
			current_stack.append(item);
			continue;
		if abs(item - current_stack[-1]) > 1:
			final_result_x_value_list.append(current_stack[-1]);
			current_stack = [item];

	if current_stack != []:
		final_result_x_value_list.append(current_stack[0]);

	final_result_x_value_list.append(min_x_on_page);
	final_result_x_value_list.append(max_x_on_page);


	

	cell_level_result_list = [];


	final_result_x_value_list = sorted(list(set(final_result_x_value_list)));

	y_value_list = [round(item,0) for item in y_value_list];

	y_value_list = sorted(list(set(y_value_list)), key=lambda x: -x);


	for item in final_result_x_value_list:	
		if max_x_on_page < 680:
			db_table_line_list.append([page_number_sent, item * 3, 2376 - y_value_list[0] * 3 , 0.02, line_height * 3]);
		else:
			db_table_line_list.append([page_number_sent, item * 3, 1836 - y_value_list[0] * 3 , 0.02, line_height * 3]);

	for item in y_value_list:
		if max_x_on_page < 680:
			db_table_line_list.append([page_number_sent, min_x_on_page * 3, 2376 - item * 3, abs(max_x_on_page - min_x_on_page) * 3, 0.02]);
		else:
			db_table_line_list.append([page_number_sent, min_x_on_page * 3, 1836 - item * 3, abs(max_x_on_page - min_x_on_page) * 3, 0.02]);			




	for i in range(0, len(y_value_list)-1):
		y_value = y_value_list[i];
		y_value_2 = y_value_list[i+1];
		row_cell_list = [];
		for j in range(0, len(final_result_x_value_list)-1):
			x_value = final_result_x_value_list[j];
			x_value_2 = final_result_x_value_list[j+1]

			if x_value < 500 and abs(x_value_2 - x_value) < 20:
				continue;

			cell_string_value = ''.join([item[11] for item in filtered_charanno_level_component_list if round(item[5],0) <= y_value_2 + 2 and round(item[5],0) >= y_value_2-2 and item[6]<= x_value_2 and item[4] >= x_value]);
			cell_string_value = re.sub(r'\t',' ', cell_string_value);
			row_cell_list.append([extraction_criteria_id, item[0], cell_string_value, x_value, y_value_2, x_value_2, y_value, item[9]]);

		cell_level_result_list.append(row_cell_list);	


	return db_table_line_list, cell_level_result_list;





"""
	KEY METHOD
	method: detect_table_with_lines_cover_begin_only
	extract contents from table that has multiple short lines to indicate the title row

	example pdf pages:
	Prepayment Assumption table for Ginnie
	for extracting pricing speed and wals for ginnie securities
"""
################################################################################################################################
def detect_table_with_lines_cover_begin_only(doc_id_sent,page_number_sent,sorted_charanno_level_component_list_sent, extraction_criteria_id):
	

	"""
		find the maximum and minimum x and y values within the page 
	"""


	max_x_on_page = max(zip(*sorted_charanno_level_component_list_sent)[6]);
	max_x_on_page = max_x_on_page + 1;

	min_x_on_page = min(zip(*sorted_charanno_level_component_list_sent)[4]);
	min_x_on_page = min_x_on_page - 1;

	min_y_on_page = min(zip(*sorted_charanno_level_component_list_sent)[5]);
	min_y_on_page = min_y_on_page - 1;

	max_y_on_page = max(zip(*sorted_charanno_level_component_list_sent)[7]);
	max_y_on_page = max_y_on_page + 1;


	

	cell_level_result_list = [];

	db_table_line_list = [];


	x_and_y_value_block_list = [];

	"""
		find all title short lines 
		after filtering the y values of these lines, we can detect the start of each table within the page
		because there might be multiple tables in a single page 
	"""

	horizontal_lines_list = [item for item in sorted_charanno_level_component_list_sent if ('LTLine' in item[2] or 'LTCurve' in item[2]) and item[-2] > 5 and item[-1] < 0.1 ];
	
	y_value_list = [horizontal_lines_list[0][5]];
	for i in range(1, len(horizontal_lines_list)):
		if abs(horizontal_lines_list[i][5] - y_value_list[-1]) > 5:
			y_value_list.append(horizontal_lines_list[i][5]);



	"""
		filter y values
		there will be multiple short lines share same y value
		we only want 1 to get the y value 
	"""

	temp_y_value = max_y_on_page;
	scan_y_value_list = [y_value_list[0]+12];
	while temp_y_value > min_y_on_page:
		flag = 0;
		for item in [item for item in sorted_charanno_level_component_list_sent if item[3] == 'LTChar']:
			if temp_y_value > item[5] and temp_y_value < item[7]:
				flag = 1;
		if flag == 0 and abs(temp_y_value - scan_y_value_list[-1]) > 20:
			scan_y_value_list.append(temp_y_value);
		temp_y_value -= 1;


	filtered_y_value_list = y_value_list;

	for i in range(0, len(y_value_list)):
		if i%3 == 2:
			for item in scan_y_value_list:
				if y_value_list[i] - item > 100:
					filtered_y_value_list.append(item);
					break;


	filtered_y_value_list = sorted(list(set(filtered_y_value_list)), key=lambda x: -x);


	for item in filtered_y_value_list:
		if max_x_on_page < 680:
			db_table_line_list.append([page_number_sent, min_x_on_page * 3, 2376 - item * 3, abs(max_x_on_page - min_x_on_page) * 3, 0.02]);
		else:
			db_table_line_list.append([page_number_sent, min_x_on_page * 3, 1836 - item * 3, abs(max_x_on_page - min_x_on_page),0.02]);		
	

	"""
		since there will be multiple tables on a page
		so we need to find the correct coordinates for each table on that page
		we do a mod operation on the y coordinates
		we find out 4 horizontal lines will cover a whole table
		so we do i % 4
		yea, this is highly depedant to the extact page 
		not perfect, but more than 95 percent of the cases, it's working
		the rest, i will provide a page number to show on front end
	"""		


	for i in range(0, len(filtered_y_value_list)):
		part_x_value_list = [];
		part_y_value_list = [];

		if i % 4 == 0 and i!= len(filtered_y_value_list)-1:
			part_y_value_list.append(filtered_y_value_list[i]);
			part_y_value_list.append(filtered_y_value_list[i+1]);
				
			temp_line_list = [horiline for horiline in horizontal_lines_list if abs(horiline[5]-filtered_y_value_list[i+1]) < 1];
			part_x_value_list = zip(*temp_line_list)[4] + zip(*temp_line_list)[6];

			x_and_y_value_block_list.append([[100,600],[filtered_y_value_list[i]+15,filtered_y_value_list[i]]]);

			x_and_y_value_block_list.append([sorted(list(set([round(item,0) for item in part_x_value_list]))),sorted(list(set([round(item,0) for item in part_y_value_list])), key=lambda x: -x)]);

			part_x_value_list = [];
			part_y_value_list = [];




		if i % 4 == 1 and i!= len(filtered_y_value_list)-1:
			temp_char_anno_list = [item for item in sorted_charanno_level_component_list_sent if item[3] == 'LTChar' and item[5] >= filtered_y_value_list[i+2] and item[7] <= filtered_y_value_list[i] ];
			if len(temp_char_anno_list) > 0:
				temp_min_x = min(zip(*temp_char_anno_list)[4]) - 1;
				temp_max_x = max(zip(*temp_char_anno_list)[6]) + 1;
				temp_x_value = temp_min_x;
				part_y_value_list.append(filtered_y_value_list[i]);
				part_y_value_list.append(filtered_y_value_list[i+2]);
				while temp_x_value < temp_max_x:
					flag = 0;
					for item in temp_char_anno_list:
						if item[4] < temp_x_value and item[6] > temp_x_value:
							flag = 1;
							break;
					if flag == 0:
						part_x_value_list.append(temp_x_value);
						if max_x_on_page < 680:
							db_table_line_list.append([page_number_sent, temp_x_value * 3, 2376-filtered_y_value_list[i]*3 , 0.02, abs(filtered_y_value_list[i+2] - filtered_y_value_list[i]) * 3])
						else:
							db_table_line_list.append([page_number_sent, temp_x_value * 3, 1836-filtered_y_value_list[i]*3 , 0.02, abs(filtered_y_value_list[i+2] - filtered_y_value_list[i]) * 3])
					temp_x_value += 1;
				
				current_y_value = temp_char_anno_list[0][5];
				temp_count = 1;
				filtered_result_y_value_list = [];
				for item in temp_char_anno_list:
					# print item[0];
					if item[5] == current_y_value:
						temp_count += 1;
						continue;
					if item[5] != current_y_value:
						if temp_count > 3:
							# print '                                   ',current_y_value;
							filtered_result_y_value_list.append(round(current_y_value,1));
							current_y_value = item[5];
							temp_count = 1;
						else:
							current_y_value = item[5];
							temp_count = 1;
						continue;

				if temp_count > 5:
					filtered_result_y_value_list.append(current_y_value);

				for item in filtered_result_y_value_list:
					part_y_value_list.append(item);
					if max_x_on_page < 680:
						db_table_line_list.append([page_number_sent, temp_min_x * 3,2376 - item * 3, abs(temp_min_x - temp_max_x) * 3, 0.02]);
					else:
						db_table_line_list.append([page_number_sent, temp_min_x * 3,1836 - item * 3, abs(temp_min_x - temp_max_x) * 3, 0.02]);
			
			x_and_y_value_block_list.append([sorted(list(set([round(item,0) for item in part_x_value_list]))),sorted(list(set([round(item,0) for item in part_y_value_list])), key=lambda x: -x)[:2]]);
			x_and_y_value_block_list.append([sorted(list(set([round(item,0) for item in part_x_value_list]))),sorted(list(set([round(item,0) for item in part_y_value_list])), key=lambda x: -x)[-3:]]);

			part_x_value_list = [];
			part_y_value_list = [];


	filtered_charanno_level_component_list = [item for item in sorted_charanno_level_component_list_sent if item[3]=='LTChar'];


	"""
		after we have lists of correct x values and y values
		we start to get text from each table cell
		we simply do a nested for loop that start from the first x value and first y value 

	"""


	for data_pair in x_and_y_value_block_list:

		for i in range(0, len(data_pair[1])-1):
			y_value = data_pair[1][i];
			y_value_2 = data_pair[1][i+1];
			row_cell_list = [];
			if abs(y_value_2 - y_value) < 5:
				continue;
			for j in range(0, len(data_pair[0])-1):
				x_value = data_pair[0][j];
				x_value_2 = data_pair[0][j+1]
				if abs(x_value_2 - x_value) < 8:
					continue;

				cell_string_value = ''.join([item[11] for item in filtered_charanno_level_component_list if item[5] < y_value and item[5] > y_value_2 - 2 and item[6]<= x_value_2+1 and item[4] >= x_value-1]);
				cell_string_value = re.sub(r'\t',' ', cell_string_value);
				cell_string_value = ''.join([char for char in cell_string_value if char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.%()0123456789, ']);
				row_cell_list.append([extraction_criteria_id, item[0], cell_string_value, x_value, y_value_2, x_value_2, y_value, item[9]]);

			cell_level_result_list.append(row_cell_list);	


	return db_table_line_list, cell_level_result_list;	





"""
	KEY METHOD
	method: detect_table_with_lines_cover_begin_end
	this method is used for extracting contents from table that have horizontal lines as header and footer
	this table recognition logic is based purely on LTChars and LTLines, no LTAnno considered

	example pdf pages:
	Page 1 table for Ginnie, Fannie and Freddie	
"""
################################################################################################################################
def detect_table_with_lines_cover_begin_end(doc_id_sent,page_number_sent,sorted_charanno_level_component_list_sent, extraction_criteria_id):

	print 'extraction_criteria_id:           ', extraction_criteria_id;
	print 'doc_id_sent:           ', doc_id_sent;

	"""
		get the maximum and minimum x values from all the characters on the page
	"""

	max_x_on_page = max(zip(*sorted_charanno_level_component_list_sent)[6]);
	min_x_on_page = min(zip(*sorted_charanno_level_component_list_sent)[4]);

	db_table_line_list = [];


	"""
		find out the lines that might be the begin and end of a table
		these lines should be horizontal lines
		also the width should be greater than 250 pixels
		this condition is used for filtertering noise lines 
	"""

	potential_lines_list = [item for item in sorted_charanno_level_component_list_sent if ('LTLine' == item[2] or 'LTCurve' == item[2]) and (item[-1] < 1) and (item[-2]) > 250];

	max_y = max(zip(*potential_lines_list)[7]);
	max_y = max_y + 1;
	min_y = min(zip(*potential_lines_list)[5]);
	min_y = min_y - 1;
	max_x = max(zip(*potential_lines_list)[6]);
	max_x = max_x + 1;
	min_x = min(zip(*potential_lines_list)[4]);
	min_x = min_x - 1;

	filtered_charanno_level_component_list = [item for item in sorted_charanno_level_component_list_sent if (item[4] > min_x) and (item[6] < max_x) and (item[5] > min_y) and (item[7] < max_y) and ('LTChar' in item[3])];



	"""
		drawing horizontal lines within a table rectangle
		by finding same x coordinates of characters 
		if there are more than 5 characters sharing same x coordinate, I conclude there is a table row
	"""

	filtered_result_y_value_list = [];
	current_y_value = filtered_charanno_level_component_list[0][5];
	temp_count = 1;
	for item in filtered_charanno_level_component_list:
		if item[5] == current_y_value:
			temp_count += 1;
			continue;
		if item[5] != current_y_value:
			if temp_count > 5:
				filtered_result_y_value_list.append(current_y_value);
				current_y_value = item[5];
				temp_count = 1;
			else:
				current_y_value = item[5];
				temp_count = 1;
			continue;

	if temp_count > 5:
		filtered_result_y_value_list.append(current_y_value);	



	final_filtered_result_y_value_list = [];
	final_filtered_result_y_value_list.append(max_y);
	for i in range(1, len(filtered_result_y_value_list)):
		if abs(filtered_result_y_value_list[i] - filtered_result_y_value_list[i-1]) < 2:
			continue;
		else:
			final_filtered_result_y_value_list.append(filtered_result_y_value_list[i]);




	
	"""
		drawing vertical lines that can correctly split columns within the table
		slightly move the vertical line pixel by pixel 
		if there is a line no character is crossing it, that means it's a correct splitting vertical lines
	"""		
	result_x_value_list = [];

	result_x_value_list.append(max_x);
	result_x_value_list.append(min_x);

	temp_x_value = min_x;

	while temp_x_value < max_x:
		flag = 0;
		for item in filtered_charanno_level_component_list:
			if temp_x_value > item[4] and temp_x_value < item[6]:
				flag = 1;
				break;
		if flag == 0 and temp_x_value - result_x_value_list[-1] > 15:
			# check_left_line = temp_x_value - 1;
			check_right_line = temp_x_value + 1;
			# left_flag = 0;
			right_flag = 0;
			# for item in filtered_charanno_level_component_list:
			# 	if check_left_line > item[4] and check_left_line < item[6]:
			# 		left_flag = 1;
			# 		break;
			
			for item in filtered_charanno_level_component_list:
				if check_right_line > item[4] and check_right_line < item[6]:
					right_flag = 1;
					break;

			if right_flag == 0:		
				result_x_value_list.append(temp_x_value);
		temp_x_value += 1;


	"""
		after we have lists of correct x values and y values
		we start to get text from each table cell
		we simply do a nested for loop that start from the first x value and first y value 

	"""

	current_x_index = 0;
	current_y_index = 0;
	cell_level_result_list = [];
	current_cell_string = '';


	result_x_value_list = sorted(list(set(result_x_value_list)));


	potential_vertical_lines_list = [round(item[4],0) for item in sorted_charanno_level_component_list_sent if (item[2] == 'LTLine' or item[2] == 'LTCurve') and item[-2] < 1 and item[-1] > 5 ]

	potential_vertical_lines_list = sorted(list(set(potential_vertical_lines_list)));

	# print '##############################################';
	# for item in potential_vertical_lines_list:
	# 	print 'vertical lines:                 ',item;
	# print '##############################################';

	if len(potential_vertical_lines_list) > 3:
		if potential_vertical_lines_list[0] > result_x_value_list[0] and potential_vertical_lines_list[-1] < result_x_value_list[-1]:
			result_x_value_list = [result_x_value_list[0]] + potential_vertical_lines_list + [result_x_value_list[-1]];


	final_filtered_result_y_value_list = sorted(list(set(final_filtered_result_y_value_list)), key=lambda x: -x);


	for item in final_filtered_result_y_value_list:
		if max_x_on_page < 680:
			db_table_line_list.append([page_number_sent, min_x * 3,2376 - item * 3, abs(max_x - min_x) * 3, 0.02]);
		else:
			db_table_line_list.append([page_number_sent, min_x * 3,1836 - item * 3, abs(max_x - min_x) * 3, 0.02]);		

	for item in result_x_value_list:
		if max_x_on_page < 680:
			db_table_line_list.append([page_number_sent, item * 3,2376 - max_y * 3, 0.02, abs(max_y - min_y) * 3]);
		else:
			db_table_line_list.append([page_number_sent, item * 3,1836 - max_y * 3, 0.02, abs(max_y - min_y) * 3]);		



	for i in range(0, len(final_filtered_result_y_value_list)-1):
		y_value = final_filtered_result_y_value_list[i];
		y_value_2 = final_filtered_result_y_value_list[i+1];
		row_cell_list = [];
		for j in range(0, len(result_x_value_list)-1):
			x_value = result_x_value_list[j];
			x_value_2 = result_x_value_list[j+1];
			"""
				if there are two vertical lines which are too close to each other
				we simply skip this column
			"""
			if abs(x_value - x_value_2) < 20 and x_value_2 < 300 and j!=0:
				continue;

			"""
				if there is nothing but dots in a table cell
				we skip this column
			"""	

			if not re.sub(' ','',re.sub('\.','',''.join([item[11] for item in filtered_charanno_level_component_list if item[5] < y_value_2 + 2 and item[5] > y_value_2-2 and item[6]<= x_value_2 and item[4] >= x_value]))) == '':
				cell_string_value = ''.join([item[11] for item in filtered_charanno_level_component_list if item[5] < y_value_2 + 2 and item[5] > y_value_2 - 2 and item[6]<= x_value_2 and item[4] >= x_value]);
				cell_string_value = re.sub(r'\t',' ', cell_string_value);
				row_cell_list.append([extraction_criteria_id, item[0], cell_string_value, x_value, y_value_2, x_value_2, y_value, item[9]]);


		cell_level_result_list.append(row_cell_list);	




	return db_table_line_list, cell_level_result_list;



	



"""
	KEY METHOD
	method: detect_table_by_anno_and_distance
	this is a method that can return all tablized contents on a pdf page given the search criteria
	E.g. 
	1. given the targeted page number (which is decided by another method), loop all the character level components on the page
	2. if the min point y value (the left bottom coordinate value) of a sequece of charaters are the same, they belong to a same row
	3. if between two characters in a same row, there is an LTAnno with text "\n". That must be a column separator;
	4. if between two characters in a same row, there is an LTAnno with text " ". That can either a normal space or a column separator.
	5. if there is an LTAnno with text " ", e.g. A" "B. we calculate the distance between A and B. If the distance is greater than the width of the LTAnno " ", we know it's a column separator.
	6. But keep in mind step 5 is not always correct. If two characters are too close, it will still take it as a normal space 

	this method has been modified after we increase our document sample set
	because it turns out some of the documents, there is no LTAnno after each column 
	so we add one more splitting decision condition here "if abs(char[6] - row_content_stack[i][4]) > char[-2] + 1:"

	this method is still being used for floating rates infomation table extraction and Pricing speed of Fannie

	also, XTR is still collecting result from this method in case the new table logic doesnt work properly for a situation

	But for now, all random files for all three agencies, there is no such case that new table extraction logic cannot handle.

"""
#############################################################################################################
def detect_table_by_anno_and_distance(sorted_charanno_level_component_list, table_extraction_list_item, page_number_list):
	print '========================== Table Extraction =============================';
	print 'Search String: ', table_extraction_list_item['Anchor_Search_String'];
	print 'Pages for this field: ', page_number_list;
	criteria_id = table_extraction_list_item['Extraction_Criteria_ID'];

	if page_number_list == []:
		print 'No pages specified for the search string: ', table_extraction_list_item['Anchor_Search_String'];
		print '';
		return;

	sorted_charanno_level_component_list = [item for item in sorted_charanno_level_component_list if item[0] in page_number_list];

	row_content_stack = [];
	table_content_list = [];
	table_content_detail_list = [];



	row_keywords = [];
	if table_extraction_list_item['Force_Data_As_Table_Row'] != None:
		row_keywords = table_extraction_list_item['Force_Data_As_Table_Row'].split(' ');
	
	number_of_columns = table_extraction_list_item['Table_Total_Columns'];
	min_number_of_columns = 0;
	if number_of_columns > 3:
		min_number_of_columns = number_of_columns - 2;
	else:
		min_number_of_columns = number_of_columns - 1;

	for j in range(0, len(sorted_charanno_level_component_list)):
		item = sorted_charanno_level_component_list[j];


		if 'LTLine' == item[2] or 'LTCurve' == item[2]:
			continue;
		if len(row_content_stack) == 0:
			row_content_stack.append(item);
			continue;
		if (len(row_content_stack) != 0) and abs(item[5] - row_content_stack[-1][5]) < 0.01 :
			row_content_stack.append(item); 
			continue;
		if (len(row_content_stack) != 0) and abs(item[5] - row_content_stack[-1][5]) > 0.01:

			result_row = '';
			result_row_detail_item = [];
			for i in range(0, len(row_content_stack)):
				char = row_content_stack[i];
				if char[11] == "%":
					if i+1 < len(row_content_stack):
						if 'LTAnno' == row_content_stack[i+1][3]:
							row_content_stack[i+1][-2] = row_content_stack[i-1][-2];
				if 'LTAnno' == char[3] and "'\\n'" != char[11]:
					char[11] = ' ';
				if i == len(row_content_stack) - 1:
					if 'LTAnno' == char[3]:
						result_row = result_row + ' ';
						char[11] = ' ';
						result_row_detail_item.append(char);
					else:
						result_row = result_row + char[11];
						result_row_detail_item.append(char);
					continue;	

				if i == 0:
					result_row = result_row + char[11];
					result_row_detail_item.append(char);
					continue;
				if i > 0:
					if 'LTAnno' == char[3] and "'\\n'" == char[11]:
						result_row = result_row + " | " ;
						char[11] = ' ';
						result_row_detail_item.append([]);
						result_row_detail_item.append(char);
						continue;
					if 'LTAnno' == char[3] and abs(row_content_stack[i+1][4] - char[6]) > char[-2]+0.0001 and not (str([tempitem for tempitem in result_row_detail_item if tempitem!=[]][-1][11]).isalpha() and str(row_content_stack[i+1][11]).isalpha()):
						result_row = result_row + " | " + char[11];
						result_row_detail_item.append([]);
						char[11] = ' ';
						result_row_detail_item.append(char);
						continue;
					if abs(row_content_stack[i+1][4] - char[6]) > char[-2] + 1:
						result_row = result_row + char[11] + " | " ;
						result_row_detail_item.append(char);
						result_row_detail_item.append([]);
					else:
						result_row = result_row + char[11];
						result_row_detail_item.append(char);


			table_content_list.append(result_row);
			table_content_detail_list.append(result_row_detail_item);
			row_content_stack = [];
			row_content_stack = [item];
			continue;
		if j == len(sorted_charanno_level_component_list) - 1:
			result_row = '';
			result_row_detail_item = [];
			row_content_stack.append(item);
			for i in range(0, len(row_content_stack)):
				char = row_content_stack[i];

				if char[11] == "%":
					if i+1 < len(row_content_stack):
						if 'LTAnno' == row_content_stack[i+1][3]:
							row_content_stack[i+1][-2] = row_content_stack[i-1][-2];

				if i == len(row_content_stack) - 1:
					if 'LTAnno' == char[3]:
						result_row = result_row + ' ';
						result_row_detail_item.append(char);
					else:
						result_row = result_row + char[11];
						result_row_detail_item.append(char);
					continue;	

				if i == 0:
					result_row = result_row + char[11];
					result_row_detail_item.append(char);
					continue;
				if i > 0:
					if 'LTAnno' == char[3] and "'\\n'" == char[11]:
						result_row = result_row + " | " ;
						char[11] = ' ';
						result_row_detail_item.append([]);
						result_row_detail_item.append(char);
						continue;
					if 'LTAnno'== char[3] and abs(row_content_stack[i+1][4] - char[6]) > char[-2]+0.0001 and not (str([tempitem for tempitem in result_row_detail_item if tempitem != []][-1][11]).isalpha() and str(row_content_stack[i+1][11]).isalpha()):
						result_row = result_row + " | " + char[11];
						result_row_detail_item.append([]);
						char[11] = ' ';
						result_row_detail_item.append(char);
						continue;
					if abs(char[6] - row_content_stack[i][4]) > char[-2] + 1:
						result_row = result_row + char[11] +" | ";
						result_row_detail_item.append(char);
						result_row_detail_item.append([]);
					else:
						print '                                                              ',char[11];
						result_row = result_row + char[11];
						result_row_detail_item.append(char);

			table_content_list.append(result_row);
			table_content_detail_list.append(result_row_detail_item);
			continue;

	

	count_rows = 1;
	cell_level_result_list = [];

	for i in range(0,len(table_content_list)):
		item = table_content_list[i];
		# print item;
		flag_contain_key_word = 0;
		cell_level_row_result = [];
		for key_word in row_keywords:
			if key_word in item:
				flag_contain_key_word = 1;
				break;

		if (flag_contain_key_word == 1) or (len(item.split("|")) >= min_number_of_columns):
			show_string = '';

			for char_item in table_content_detail_list[i]:
				if char_item == []:
					show_string = show_string + '||';
				else:
					show_string = show_string + char_item[11];
	
			# print show_string;
			cell_char_stack = [];
			for j in range(0,len(table_content_detail_list[i])):
				char_item = table_content_detail_list[i][j];
				if j==len(table_content_detail_list[i])-1:
					cell_string = '';
					cell_char_stack.append(char_item);
					for cell_char in cell_char_stack:
						cell_string = cell_string + cell_char[11];
					if cell_char_stack!=[]:
						if cell_string.strip() != '' and cell_string.strip().replace('.','').replace(' ','')!='' and cell_string.strip().replace('.','').replace('$','')!='':
							cell_object = [criteria_id, cell_string, cell_char_stack[0][0],cell_char_stack[0][4],cell_char_stack[0][5],cell_char_stack[-1][6],cell_char_stack[-1][7],cell_char_stack[0][9],cell_char_stack[0][14]];
							cell_level_row_result.append(cell_object);
							continue;


				if cell_char_stack == []:
					cell_char_stack.append(char_item);
					continue;
				if cell_char_stack != [] and char_item != []:
					cell_char_stack.append(char_item);
					continue;
				if cell_char_stack != [] and char_item == []:
					cell_string = '';
					for cell_char in cell_char_stack:
						cell_string = cell_string + cell_char[11];
					cell_object = [criteria_id, cell_string, cell_char_stack[0][0],cell_char_stack[0][4],cell_char_stack[0][5],cell_char_stack[-1][6],cell_char_stack[-1][7],cell_char_stack[0][9],cell_char_stack[0][14]];
					if cell_string.strip() != '' and cell_string.strip().replace('.','').replace(' ','')!='' and cell_string.strip().replace('.','').replace('$','')!='':
						cell_level_row_result.append(cell_object);
					cell_char_stack = [];

			cell_level_result_list.append(cell_level_row_result);
			count_rows = count_rows + 1;
	print '';
	return cell_level_result_list;






"""
	method: specify_page_number
	given the search string in table extraction criteria, this method returns a list of page numbers that contains the search string
	also we will count the number of match here, if it exceeds the maximum number of match specified in search criteria, we stop. 
"""
#############################################################################################################
def specify_page_number(sorted_block_level_component_list, extraction_list_item):
	search_string = extraction_list_item['Anchor_Search_String'];
	max_number_match = int(extraction_list_item['Max_Anchor_Searches']);
	# print max_number_match;
	page_number_list = [];
	match_count = 0;

	if 'minpagenumber' in search_string:
		min_page_number = int(search_string[re.search('minpagenumber',search_string).end()+1:]);
		print 'For anchor string ',search_string, ' the minimum page number to start with is ',min_page_number;
		sorted_block_level_component_list = [item for item in sorted_block_level_component_list if item[0] > min_page_number];	
		search_string = search_string[:re.search('minpagenumber',search_string).start()-1]

	if '&Exact&' not in search_string:
		for item in sorted_block_level_component_list:
			# print match_count;
			item[7] = item[7].replace("\\n", ' ');
			item[7] = re.sub(r' +',' ', item[7]); 
			if search_string in item[7]:
				if page_number_list == []:
					page_number_list.append(item[0]);
					match_count = match_count + 1;
					if match_count == max_number_match:
						return list(set(page_number_list));
					continue;
				if page_number_list != []:
					if item[0] - page_number_list[-1] == 1:
						page_number_list.append(item[0]);
						match_count = match_count + 1;
						if match_count == max_number_match:
							return list(set(page_number_list));
						continue;
					if item[0] - page_number_list[-1] > 1:
						return list(set(page_number_list));
	else:
		search_string = search_string.split('&')[0];
		for item in sorted_block_level_component_list:
			# print match_count;
			item[7] = item[7].rstrip();
			item[7] = re.sub(r' +',' ', item[7]); 
			if search_string == item[7]:
				if page_number_list == []:
					page_number_list.append(item[0]);
					match_count = match_count + 1;
					if match_count == max_number_match:
						return list(set(page_number_list));
					continue;
				if page_number_list != []:
					if item[0] - page_number_list[-1] == 1:
						page_number_list.append(item[0]);
						match_count = match_count + 1;
						if match_count == max_number_match:
							return list(set(page_number_list));
						continue;
					if item[0] - page_number_list[-1] > 1:
						return list(set(page_number_list));		

			

	return list(set(page_number_list));



""" KEY METHOD
	method: search_freetext_content
	loop through all the text area components and search extraction contents
	if the current text field only contains the search string but nothing else, go the the previous or next 'LTText' component 
"""
##############################################################################################################
def search_freetext_content(freetext_extraction_item, sorted_block_level_component_list_sent, page_number=None):
	search_string = freetext_extraction_item['Anchor_Search_String'];
	max_number_match = int(freetext_extraction_item['Max_Anchor_Searches']);
	start_page_number = freetext_extraction_item['Table_Total_Columns'];
	
	search_string = search_string.replace(' ','');
	current_number_match = 0;
	criteria_id = freetext_extraction_item['Extraction_Criteria_ID'];

	result_list = [];
	try:
		start_page_number = int(start_page_number);
		for i in range(0,len(sorted_block_level_component_list_sent)):
			item = sorted_block_level_component_list_sent[i];
			if search_string in item[7].replace(' ','').replace("\\n",'') and item[0] > start_page_number:		
				if page_number == None:
					target_result_item = item;
					current_number_match = current_number_match + 1;
					if len(target_result_item[7]) - len(search_string) < 4:
						target_result_item = sorted_block_level_component_list_sent[i+1];
						if 'Text' not in target_result_item[2]:
							target_result_item = sorted_block_level_component_list_sent[i-1];

					result_list.append([criteria_id]+target_result_item);
				else:
					if page_number == item[0]:
						target_result_item = item;
						current_number_match = current_number_match + 1;
						if len(target_result_item[7]) - len(search_string) < 4:
							target_result_item = sorted_block_level_component_list_sent[i+1];
							if 'Text' not in target_result_item[2]:
								target_result_item = sorted_block_level_component_list_sent[i-1];					
					result_list.append([criteria_id]+target_result_item);

			if current_number_match == max_number_match:
				return result_list;

		if result_list == []:
			print 'No match for search string: ', search_string;
			return result_list;
		else:
			return result_list;			
	except:
		for i in range(0,len(sorted_block_level_component_list_sent)):
			item = sorted_block_level_component_list_sent[i];
			if search_string in item[7].replace(' ','').replace("\\n",''):		
				if page_number == None:
					target_result_item = item;
					current_number_match = current_number_match + 1;
					if len(target_result_item[7]) - len(search_string) < 4:
						target_result_item = sorted_block_level_component_list_sent[i+1];
						if 'Text' not in target_result_item[2]:
							target_result_item = sorted_block_level_component_list_sent[i-1];

					result_list.append([criteria_id]+target_result_item);
				else:
					if page_number == item[0]:
						target_result_item = item;
						current_number_match = current_number_match + 1;
						if len(target_result_item[7]) - len(search_string) < 4:
							target_result_item = sorted_block_level_component_list_sent[i+1];
							if 'Text' not in target_result_item[2]:
								target_result_item = sorted_block_level_component_list_sent[i-1];					
					result_list.append([criteria_id]+target_result_item);

			if current_number_match == max_number_match:
				return result_list;

		if result_list == []:
			print 'No match for search string: ', search_string;
			return result_list;
		else:
			return result_list;
	


""" 
	method: get_a_row_by_anchor
	given the anchor search string, extract the row text
"""
##################################################################################################################

def get_a_row_by_anchor(single_row_critera_item, sorted_charanno_level_component_list):
	anchor_search_string = single_row_critera_item['Anchor_Search_String'];
	anchor_search_string = anchor_search_string.replace(' ','');
	max_number_match = int(single_row_critera_item['Max_Anchor_Searches']);
	row_string_stack = [];
	for item in sorted_charanno_level_component_list:
		number_match = 0;
		if row_string_stack == []:
			# print "'"+item[11]+"'";
			row_string_stack.append(item);
			continue;
		if row_string_stack != [] and abs(row_string_stack[-1][5]-item[5]) < 1:
			row_string_stack.append(item);
			continue; 

		if row_string_stack != [] and abs(row_string_stack[-1][5]- item[5]) >= 1:
			if item[3] != 'LTChar' or item[11] == u' ':
				continue;

			if item[4] <= row_string_stack[0][4] or abs(row_string_stack[-1][5]- item[5]) > row_string_stack[-1][-1]*2:
				show_string = ''.join([str(char[11]) for char in row_string_stack if char[3] == 'LTChar' and char[11] != u' ']);
					# print show_string;
				if anchor_search_string in show_string:
					number_match = number_match + 1;
					# print ''.join([str(char[11]) for char in row_string_stack]);
					if number_match == max_number_match:
						pos_min_x = 0.0;
						pos_min_y = 0.0;
						pos_max_x = 0.0;
						pos_max_y = 0.0;
						zipped_row_string_stack = zip(*row_string_stack);
						pos_min_x = min(zipped_row_string_stack[4]);
						pos_min_y = min(zipped_row_string_stack[5]);
						pos_max_x = max(zipped_row_string_stack[6]);
						pos_max_y = max(zipped_row_string_stack[7]);

						for ltanno in row_string_stack:
							if ltanno[3] == 'LTAnno':
								ltanno[11] = ' ';

						row_result_object = [1, single_row_critera_item['Extraction_Criteria_ID'], row_string_stack[0][0], ''.join([str(char[11]) for char in row_string_stack if char[3] == 'LTChar' or char[3]=='LTAnno']),str(pos_min_x),str(pos_min_y),str(pos_max_x),str(pos_max_y), row_string_stack[0][9],0,0];
						return row_result_object;
				row_string_stack = [item];
			else:
				row_string_stack.append(item);


"""
	method locate_anchor_string
	this method will return the first match of an anchor string 
	return value is a list of page number and coordinates
	if nothing match, will return an empty list 
"""
##################################################################################################################
def locate_anchor_string(anchor_string, sorted_block_level_component_list):
	for item in sorted_block_level_component_list:
		if anchor_string in item[7]:
			# print item;
			return [item[0],item[3],item[4],item[5],item[6]];
	return [];


"""
	method get_area_merged_by_begin_end
	given the begin page number and coordinates with the end page number and coordinates
	this method will return a merged extracted result 
"""
##################################################################################################################
def get_area_merged_by_begin_end(begin_anchor_location, end_anchor_location, sorted_block_level_component_list):
	page_range = range(begin_anchor_location[0], end_anchor_location[0]+1);  ## keep in mind the range(n,m) function is returning [n, n+1, ..., m-1]
	if page_range == []:
		print 'No page found between the begin and the end location.';
		return [];
	else:
		begin_page_number = page_range[0];
		end_page_number = page_range[-1];
		
		print len(sorted_block_level_component_list);

		"""
			3-step filtration (holy, now, i am more and more pythonized.)
		"""

		"""
			Step 1: filter by the page range
			if the page number of the component is within the range, we keep that component 
		"""
		filtered_pl_component_by_page_range = [item for item in sorted_block_level_component_list if item[0] in page_range];

		print len(filtered_pl_component_by_page_range);

		"""
			Step 2: filter by the begin location
			if the the component is on the begin page, then we filter the component to check whether it is BELOW the begin anchor location 
		"""
		filtered_pl_component_by_begin = [item for item in filtered_pl_component_by_page_range if (item[0] == begin_page_number and item[6] <= begin_anchor_location[4]) or (item[0] != begin_page_number)];

		print len(filtered_pl_component_by_begin);


		"""
			Step 3: filter by the end location
			if the the component is in the end page, then we filter the component to check whether it is ABOVE the end anchor location 
		"""
		filtered_pl_component_by_end = [item for item in filtered_pl_component_by_begin if (item[0] == end_page_number and item[6] >= end_anchor_location[4]) or (item[0] != end_page_number)];

		print len(filtered_pl_component_by_end);


		"""
			now we package the result 
			make it fit for raw extraction database storage
		"""

		if begin_page_number == end_page_number:
			db_raw_extraction_result_obj = [];
			field_appended_string_value = '';
			for item in filtered_pl_component_by_end:
				field_appended_string_value = field_appended_string_value + ' ' + item[7];
			db_raw_extraction_result_obj = [begin_page_number, field_appended_string_value, 50, end_anchor_location[2], 750, begin_anchor_location[4]];		## [page number, appended extraction string, minposx, minposy, maxposx, maxposy]	
			return [db_raw_extraction_result_obj];

		if begin_page_number < end_page_number:
			current_page = begin_page_number;
			current_max_y = begin_anchor_location[4];
			current_min_y = 0;
			db_raw_extraction_result_list = [];
			db_raw_extraction_result_obj = [];
			field_appended_string_value = '';

			for i in range(0, len(filtered_pl_component_by_end)):
				item = filtered_pl_component_by_end[i];
				
				if i == len(filtered_pl_component_by_end) - 1:
					field_appended_string_value = field_appended_string_value + ' ' + item[7];
					current_min_y = item[4];
					db_raw_extraction_result_obj.append(current_page);
					db_raw_extraction_result_obj.append(field_appended_string_value);
					db_raw_extraction_result_obj.append(50);
					db_raw_extraction_result_obj.append(current_min_y);
					db_raw_extraction_result_obj.append(750);
					db_raw_extraction_result_obj.append(current_max_y);
					db_raw_extraction_result_list.append(db_raw_extraction_result_obj);
					db_raw_extraction_result_obj = [];


				if item[0] == current_page:
					field_appended_string_value = field_appended_string_value + ' ' + item[7];
					current_min_y = item[4];
					continue;
				
				if item[0] != current_page:     ## we go into a new page
					db_raw_extraction_result_obj.append(current_page);
					db_raw_extraction_result_obj.append(field_appended_string_value);
					db_raw_extraction_result_obj.append(50);
					db_raw_extraction_result_obj.append(current_min_y);
					db_raw_extraction_result_obj.append(750);
					db_raw_extraction_result_obj.append(current_max_y);
					db_raw_extraction_result_list.append(db_raw_extraction_result_obj);
					db_raw_extraction_result_obj = [];
					field_appended_string_value = '';
					current_max_y = 800;
					current_page = item[0];
					continue;
				
			return db_raw_extraction_result_list;


"""
	method get_area_merged_by_begin_endofpage
	given the begin page number and coordinates 
	this method will return a merged extracted result until the end of the page 
"""
##################################################################################################################
def get_area_merged_by_begin_endofpage(begin_anchor_location, sorted_block_level_component_list):
	page_number = begin_anchor_location[0];
	filtered_pl_component_by_endofpage = [item for item in sorted_block_level_component_list if item[0] == page_number and item[4] < begin_anchor_location[2]];
	field_appended_string_value = '';
	for item in filtered_pl_component_by_endofpage:
		field_appended_string_value = field_appended_string_value + ' ' + item[7];

	return [page_number, field_appended_string_value,50,20,750,begin_anchor_location[2]];



""" 
	method: process_per_file
	for each pdf document, 
	1. we use the text area component list and character level component list as the resource
	2. based on the agency name, we query the database to find all table and freetext extraction list
	3. we call related methods to do the extraction 
"""
##################################################################################################################
def process_per_file(agency_type_sent, doc_id_sent ,sorted_block_level_component_list_sent, sorted_charanno_level_component_list_sent, extraction_criteria_list_sent):
	global sorted_block_level_component_list;
	sorted_block_level_component_list = sorted_block_level_component_list_sent;
	global sorted_charanno_level_component_list;
	sorted_charanno_level_component_list = sorted_charanno_level_component_list_sent;
	global agency_type;
	agency_type = agency_type_sent;

	"""
		right now we only have 3 different types of extraction criteria
		if later we have more, we should add them here to call the related methods
	"""

	table_extraction_list = extraction_criteria_list_sent.loc[extraction_criteria_list_sent['Extraction_Description'] == 'table_begin_str'];
	nontable_extraction_list = extraction_criteria_list_sent.loc[extraction_criteria_list_sent['Extraction_Description'] == 'nontable_begin_str'];
	key_value_extraction_list = extraction_criteria_list_sent.loc[extraction_criteria_list_sent['Extraction_Description'] == 'key_value_str'];
	nontable_extraction_with_endding_list = extraction_criteria_list_sent.loc[extraction_criteria_list_sent['Extraction_Description'] == 'nontable_begin_end_strs'];


	page_number_list_total = [];

	extracted_field_result_list_to_db = [];
	temp_extracted_field_item = [];


	"""
		for table extraction criteria
		we use detect_table_by_anno_and_distance method to get the raw extraction results 
	"""


	if not table_extraction_list.empty:

		db_table_line_list_for_doc = [];
		cell_level_result_list_table_type_1 = [];
		cell_level_result_list_table_type_2 = [];

		test_for_pricing_speed_page_number_list = [];

		test_for_vertical_page_number_list = [];

		page_number_with_criteria_id_list = [];

		test_for_prepayass_page_number_list = [];

		test_for_double_line_begin_end_page_number_list = [];

		for i in range(0, len(table_extraction_list)):
			table_extraction_list_item = table_extraction_list.iloc[i];
			page_number_list = specify_page_number(sorted_block_level_component_list, table_extraction_list_item);
			if page_number_list == []:
				print table_extraction_list_item['Anchor_Search_String'], ' table search string not found!!!!!!!!!!!!!!!!!';
				continue;

			page_number_list_total = page_number_list_total + page_number_list;
			if table_extraction_list.iloc[i]['Anchor_Search_String'] == 'Initial Percent' :
				test_for_pricing_speed_page_number_list = test_for_pricing_speed_page_number_list + page_number_list;
				page_number_with_criteria_id_list.append([page_number_list, table_extraction_list.iloc[i]['Extraction_Criteria_ID']]);
				continue;
			if table_extraction_list.iloc[i]['Anchor_Search_String'] == 'S - I -' or table_extraction_list.iloc[i]['Anchor_Search_String'] == 'Original Balances' or table_extraction_list.iloc[i]['Anchor_Search_String'] == 'Proportions(':
				print '-----------------------';
				# print table_extraction_list.iloc[i]['Anchor_Search_String'];
				print page_number_list;
				print '-----------------------';
				test_for_vertical_page_number_list = test_for_vertical_page_number_list + page_number_list;	
				page_number_with_criteria_id_list.append([page_number_list, table_extraction_list.iloc[i]['Extraction_Criteria_ID']]);	
				continue;
			if table_extraction_list.iloc[i]['Anchor_Search_String'] == 'Prepayment Assumption':
				print 'nimabi!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!';
				test_for_prepayass_page_number_list = test_for_prepayass_page_number_list + page_number_list;
				page_number_with_criteria_id_list.append([page_number_list, table_extraction_list.iloc[i]['Extraction_Criteria_ID']]);
				continue;

			if table_extraction_list.iloc[i]['Anchor_Search_String'] == 'CUSIP Number':
				page_number_with_criteria_id_list.append([page_number_list, table_extraction_list.iloc[i]['Extraction_Criteria_ID']]);
				test_for_double_line_begin_end_page_number_list = test_for_double_line_begin_end_page_number_list + page_number_list;
				continue;
				
			print table_extraction_list_item['Extraction_Criteria_ID'], '     we are here!!!!!!!!!!!!!!!';
			cell_level_result_list = detect_table_by_anno_and_distance(sorted_charanno_level_component_list, table_extraction_list_item, page_number_list);
			if cell_level_result_list != None:
				for row_number in range(0, len(cell_level_result_list)):
					if cell_level_result_list[row_number] != []:
						current_font = cell_level_result_list[row_number][0][7];
						for column_number in range(0, len(cell_level_result_list[row_number])):
							temp_extracted_field_item.append(doc_id_sent);   																				#doc_info_id
							temp_extracted_field_item.append(cell_level_result_list[row_number][column_number][0]);											#extraction_criteria_id			    
							temp_extracted_field_item.append(cell_level_result_list[row_number][column_number][2]);											#page_number
							# cell_level_result_list[row_number][column_number][1] = re.sub(r'\t',' ',cell_level_result_list[row_number][column_number][1]);
							temp_extracted_field_item.append(cell_level_result_list[row_number][column_number][1]);											#field_value
							temp_extracted_field_item.append(str(cell_level_result_list[row_number][column_number][3]));									#pos min x
							temp_extracted_field_item.append(str(cell_level_result_list[row_number][column_number][4]));									#pos min y
							temp_extracted_field_item.append(str(cell_level_result_list[row_number][column_number][5]));									#pos max x
							temp_extracted_field_item.append(str(cell_level_result_list[row_number][column_number][6]));									#pos max y
							temp_extracted_field_item.append(current_font);																					#font 
							temp_extracted_field_item.append(row_number+1);																					#row number
							temp_extracted_field_item.append(column_number+1);																				#column number
							extracted_field_result_list_to_db.append(temp_extracted_field_item);
							temp_extracted_field_item = [];


			#############################
			#############################
		table_page_number = sorted(list(set(page_number_list_total)));


		test_for_double_line_begin_end_page_number_list = sorted(list(set(test_for_double_line_begin_end_page_number_list)));
		for page_number in test_for_double_line_begin_end_page_number_list:
			# db_table_line_list_for_doc = db_table_line_list_for_doc + detect_table_by_recognizing_lines( doc_id_sent ,page_number, [item for item in sorted_charanno_level_component_list if item[0] == page_number]);
			db_result_list, cell_level_result_return = detect_table_with_lines_cover_begin_end( doc_id_sent ,page_number, [item for item in sorted_charanno_level_component_list if item[0] == page_number], [item[1] for item in page_number_with_criteria_id_list if page_number in item[0]][0]);
			cell_level_result_list_table_type_1 = cell_level_result_list_table_type_1 + cell_level_result_return;
			db_table_line_list_for_doc = db_table_line_list_for_doc + db_result_list;
		
		test_for_pricing_speed_page_number_list = sorted(list(set(test_for_pricing_speed_page_number_list)));
		for page_number in test_for_pricing_speed_page_number_list:
			db_result_list, cell_level_result_return = detect_table_with_lines_cover_begin_only( doc_id_sent ,page_number, [item for item in sorted_charanno_level_component_list if item[0] == page_number], [item[1] for item in page_number_with_criteria_id_list if page_number in item[0]][0]);
			cell_level_result_list_table_type_1 = cell_level_result_list_table_type_1 + cell_level_result_return;
			db_table_line_list_for_doc = db_table_line_list_for_doc + db_result_list;		
		


		test_for_vertical_page_number_list = sorted(list(set(test_for_vertical_page_number_list)));
		for page_number in test_for_vertical_page_number_list:
			db_result_list, cell_level_result_return = detect_vertical_table_with_lines( doc_id_sent ,page_number, [item for item in sorted_charanno_level_component_list if item[0] == page_number],[item[1] for item in page_number_with_criteria_id_list if page_number in item[0]][0]);
			db_table_line_list_for_doc = db_table_line_list_for_doc + db_result_list;
			cell_level_result_list_table_type_1 = cell_level_result_list_table_type_1 + cell_level_result_return;


		test_for_prepayass_page_number_list = sorted(list(set(test_for_prepayass_page_number_list)));
		for page_number in test_for_prepayass_page_number_list:
			db_result_list, cell_level_result_return = detect_table_with_short_lines_cover_begin_only( doc_id_sent ,page_number, [item for item in sorted_charanno_level_component_list if item[0] == page_number],[item[1] for item in page_number_with_criteria_id_list if page_number in item[0]][0]);
			db_table_line_list_for_doc = db_table_line_list_for_doc + db_result_list;
			cell_level_result_list_table_type_1 = cell_level_result_list_table_type_1 + cell_level_result_return;


		DB_Controller.insert_table_line(doc_id_sent, db_table_line_list_for_doc);
		#######################
		#######################

		if cell_level_result_list_table_type_1 != None:
			for row_number in range(0, len(cell_level_result_list_table_type_1)):
				if cell_level_result_list_table_type_1[row_number] != []:
					
					for column_number in range(0, len(cell_level_result_list_table_type_1[row_number])):
						temp_extracted_field_item.append(doc_id_sent);   																			#doc_info_id
						temp_extracted_field_item = temp_extracted_field_item + cell_level_result_list_table_type_1[row_number][column_number];
						temp_extracted_field_item.append(row_number+1);																				#row number
						temp_extracted_field_item.append(column_number+1);																			#column number
						extracted_field_result_list_to_db.append(temp_extracted_field_item);
						temp_extracted_field_item = [];	



		

		# sys.exit();		
	"""
		for nontable extraction criteria
		we use search_freetext_content method to get the raw extraction results 
		this method is directly using the segmantation by PDFMiner
		which is not always the perfect solution
		we can check the result and see whether we should use key_value_str criteria or this one
	"""


	if not nontable_extraction_list.empty:
		for i in range(0, len(nontable_extraction_list)):
			nontable_extraction_item = nontable_extraction_list.iloc[i];
			nontable_result = search_freetext_content(nontable_extraction_item, sorted_block_level_component_list);
			for i in range(0, len(nontable_result)):
				item = nontable_result[i];
				temp_extracted_field_item.append(doc_id_sent);   								#doc_info_id
				temp_extracted_field_item.append(item[0]);										#extraction_criteria_id			    
				temp_extracted_field_item.append(item[1]);										#page_number
				temp_extracted_field_item.append(item[8]);										#field_value
				temp_extracted_field_item.append(str(item[4]));										#pos min x
				temp_extracted_field_item.append(str(item[5]));										#pos min y
				temp_extracted_field_item.append(str(item[6]));										#pos max x
				temp_extracted_field_item.append(str(item[7]));										#pos max y
				temp_extracted_field_item.append(item[10]);										#font 
				temp_extracted_field_item.append(0);											#row number
				temp_extracted_field_item.append(0);											#column number
				extracted_field_result_list_to_db.append(temp_extracted_field_item);		


				page_number_list_total.append(item[1]);
				temp_extracted_field_item = [];

	"""
		for key value extraction criteria
		we use get_a_row_by_anchor method to get the raw extraction results 
		the result is the row with that key value string 
	"""

	if not key_value_extraction_list.empty:
		for i in range(0, len(key_value_extraction_list)):
			temp_row_result_obj = get_a_row_by_anchor(key_value_extraction_list.iloc[i], sorted_charanno_level_component_list);
			if temp_row_result_obj:
				temp_row_result_obj[0] = doc_id_sent;
				extracted_field_result_list_to_db.append(temp_row_result_obj);
				page_number_list_total.append(temp_row_result_obj[2]);
			else:
				print " No key value found for:", key_value_extraction_list.iloc[i]['Anchor_Search_String']," please check the csv files to see whether the key value string exists or not.";



	if not nontable_extraction_with_endding_list.empty:

		for i in range(0,len(nontable_extraction_with_endding_list)):
			print '--------------------------------------------------------------------------';
			extracted_area_result_list = [];		
			nontable_begin_end_creitem = nontable_extraction_with_endding_list.iloc[i];
			anchor_search_string = nontable_begin_end_creitem['Anchor_Search_String'];
			begin_anchor_string = anchor_search_string.split('|')[0];
			end_anchor_string = anchor_search_string.split('|')[1];

			if '/' not in end_anchor_string:
				if end_anchor_string == 'endofpage':
					begin_anchor_location = locate_anchor_string(begin_anchor_string,sorted_block_level_component_list);
					if begin_anchor_location != []:
						extracted_area_result_list.append(get_area_merged_by_begin_endofpage(begin_anchor_location,sorted_block_level_component_list));
				else:
					begin_anchor_location = locate_anchor_string(begin_anchor_string,sorted_block_level_component_list);
					end_anchor_location = locate_anchor_string(end_anchor_string,sorted_block_level_component_list);
					if begin_anchor_location == []:
						print 'Location not found for anchor string:',begin_anchor_string;
						break;

					if end_anchor_location == []:
						print 'Location not found for anchor string:',end_anchor_string;
						break;

					while end_anchor_location[0] < begin_anchor_location[0]:
						end_anchor_location = locate_anchor_string(end_anchor_string,[item for item in sorted_block_level_component_list if item[0] > end_anchor_location[0]]);


					print 'Location for',begin_anchor_string, ' is', begin_anchor_location;
					print 'Location for',end_anchor_string, ' is', end_anchor_location;

					extracted_area_result_list = extracted_area_result_list + get_area_merged_by_begin_end(begin_anchor_location, end_anchor_location, sorted_block_level_component_list);

				for item in extracted_area_result_list:
					temp_item = [doc_id_sent] + [nontable_begin_end_creitem['Extraction_Criteria_ID']] + [item[0]] + [item[1]] + [str(item[2])] + [str(item[3])] + [str(item[4])] + [str(item[5])] + ['Multiple Fonts'] + [0] + [0];
					# print temp_item;
					page_number_list_total.append(temp_item[2]);
					extracted_field_result_list_to_db.append(temp_item);	

			else:
				end_anchor_string_one = end_anchor_string.split('/')[0];
				end_anchor_string_two = end_anchor_string.split('/')[1];

				begin_anchor_location = locate_anchor_string(begin_anchor_string,sorted_block_level_component_list);
				end_anchor_location = locate_anchor_string(end_anchor_string_one,sorted_block_level_component_list);
				if end_anchor_location == []:
					end_anchor_location = locate_anchor_string(end_anchor_string_two,sorted_block_level_component_list);

				if begin_anchor_location == []:
					print 'Location not found for anchor string:',begin_anchor_string;
					break;
				if end_anchor_location == []:
					print 'Location not found for anchor string:',end_anchor_string;
					break;
				
				print 'Location for',begin_anchor_string, ' is', begin_anchor_location;
				print 'Location for',end_anchor_string, ' is', end_anchor_location;

				extracted_area_result_list = extracted_area_result_list + get_area_merged_by_begin_end(begin_anchor_location, end_anchor_location, sorted_block_level_component_list);

				for item in extracted_area_result_list:
					temp_item = [doc_id_sent] + [nontable_begin_end_creitem['Extraction_Criteria_ID']] + [item[0]] + [item[1]] + [str(item[2])] + [str(item[3])] + [str(item[4])] + [str(item[5])] + ['Multiple Fonts'] + [0] + [0];
					# print temp_item;
					page_number_list_total.append(temp_item[2]);

					extracted_field_result_list_to_db.append(temp_item);						




	print 'The length of raw extration result for this document:',len(extracted_field_result_list_to_db);




	DB_Controller.bulk_insert_merge_extracted_fields(extracted_field_result_list_to_db);

	page_number_list_total = list(sorted(set(page_number_list_total)));
	return page_number_list_total;


		






