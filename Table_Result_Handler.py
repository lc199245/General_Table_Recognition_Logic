import re;


def get_row_number_list_by_keyword(table_extraction_list, keyword, fix_column_number=None):
	result_row_list = [];
	for i in range(0, len(table_extraction_list)):
		column_number = table_extraction_list.iloc[i]['Table_Column_Number'];
		if table_extraction_list.iloc[i]['Field_Value']:
			if keyword in table_extraction_list.iloc[i]['Field_Value'] and (column_number==fix_column_number or fix_column_number==None):
				result_row_list.append(tuple([table_extraction_list.iloc[i]['Page_Number'], table_extraction_list.iloc[i]['Table_Row_Number'], table_extraction_list.iloc[i]['Field_Value']]));
	return sorted(list(set(result_row_list)));


def get_row_number_list_by_regex(table_extraction_list, regex, fix_column_number=None):
	result_row_list = [];
	for i in range(0, len(table_extraction_list)):
		field_value = table_extraction_list.iloc[i]['Field_Value'];
		column_number = table_extraction_list.iloc[i]['Table_Column_Number'];
		if field_value == None:
			continue;
		if bool(re.search(regex, re.sub(' ','',field_value))) and (fix_column_number==column_number or fix_column_number==None):
			result_row_list.append(tuple([table_extraction_list.iloc[i]['Page_Number'], table_extraction_list.iloc[i]['Table_Row_Number'], table_extraction_list.iloc[i]['Field_Value']]));

	return sorted(list(set(result_row_list)));



def get_column_number_in_row_by_regex(row_extraction_list, regex):
	for i in range(len(row_extraction_list)-1,-1,-1):
		field_value = row_extraction_list.iloc[i]['Field_Value'];

		if field_value == None:
			continue;

		if bool(re.search(regex, re.sub(' ','',field_value))):
			# print re.sub(' ','',field_value); 
			return [row_extraction_list.iloc[i]['Page_Number'], row_extraction_list.iloc[i]['Table_Row_Number'],row_extraction_list.iloc[i]['Table_Column_Number']];
	return [];

def get_column_number_in_row_by_string(row_extraction_list, match_string):
	for i in range(0,len(row_extraction_list)):
		field_value = row_extraction_list.iloc[i]['Field_Value'];
		if match_string in field_value:
			return [row_extraction_list.iloc[i]['Page_Number'], row_extraction_list.iloc[i]['Table_Row_Number'],row_extraction_list.iloc[i]['Table_Column_Number']];
	return [];

def get_cell_field_info_by_page_row_column(table_extraction_list, page_number, row_number, column_number, reverse_order = None):
	target_row = table_extraction_list.loc[(table_extraction_list['Page_Number'] == page_number) & (table_extraction_list['Table_Row_Number'] == row_number)];
	if reverse_order:
		current_column_number = 0;
		for i in range(len(target_row)-1,-1,-1):
			current_column_number +=1;
			if current_column_number == column_number:
				return target_row.iloc[i];
	else:
		current_column_number = 0;
		for i in range(0,len(target_row)):
			current_column_number +=1;
			if current_column_number == column_number:
				return target_row.iloc[i];


def get_a_row_fields_by_page_row_numbers(table_extraction_list, page_number, row_number):
	return table_extraction_list.loc[(table_extraction_list['Page_Number'] == page_number) & (table_extraction_list['Table_Row_Number'] == row_number )];


def get_number_of_match_keyword_in_a_row(row_extraction_list, keyword):
	count = 0;
	for i in range(0, len(row_extraction_list)):
		if row_extraction_list.iloc[i]['Field_Value'] is None:
			continue;

		if keyword in row_extraction_list.iloc[i]['Field_Value']:
			count +=1 ;
	return count;


def get_number_of_match_regex_in_a_row(row_extraction_list, regex):
	count = 0;
	for i in range(0, len(row_extraction_list)):
		if row_extraction_list.iloc[i]['Field_Value'] is None:
			continue;
		if bool(re.search(regex,re.sub(' ','',row_extraction_list.iloc[i]['Field_Value']))):
			count +=1 ;
	return count;


def get_row_number_list_class_info(table_extraction_list, keyword, fix_column_number=None):
	result_row_list = [];
	for i in range(0, len(table_extraction_list)):
		column_number = table_extraction_list.iloc[i]['Table_Column_Number'];

		if keyword in re.sub(r'[^A-Za-z]',' ',table_extraction_list.iloc[i]['Field_Value']).split(' ') and (column_number==fix_column_number or fix_column_number==None):
			nimabi = re.sub(r'[^A-Za-z]',' ',table_extraction_list.iloc[i]['Field_Value']).split(' ');
			flag = 0;
			for word in nimabi:
				if bool(re.search(r'[A-Z]{0,}[a-z]{1,}',word)):
					flag = 1;
			if flag == 0:
				result_row_list.append(tuple([table_extraction_list.iloc[i]['Page_Number'], table_extraction_list.iloc[i]['Table_Row_Number'], table_extraction_list.iloc[i]['Field_Value']]));
	return sorted(list(set(result_row_list)));


def get_row_number_list_class_info_for_pricing_speed(table_extraction_list, class_info, min_row_number=1):

	result_row_list = [];
	for i in range(0, len(table_extraction_list)):
		current_cell_string = table_extraction_list.iloc[i]['Field_Value'];
		if current_cell_string == None:
			continue;

		current_cell_string =re.sub(r' +',' ',re.sub('\.','',re.sub(',',' ', re.sub('and',' ',current_cell_string))));

		if re.search(r'[a-z]', current_cell_string):
			continue;

		current_cell_string_list = current_cell_string.split(' ');
		if class_info in current_cell_string_list and table_extraction_list.iloc[i]['Table_Row_Number'] >= min_row_number:
			return [table_extraction_list.iloc[i]['Page_Number'], table_extraction_list.iloc[i]['Table_Row_Number'], table_extraction_list.iloc[i]['Field_Value']];


	return [];


def get_row_number_list_class_info_for_pricing_speed_fre(table_extraction_list, class_info, min_row_number=1):

	result_row_list = [];
	for i in range(0, len(table_extraction_list)):
		current_cell_string = table_extraction_list.iloc[i]['Field_Value'];
		if current_cell_string == None:
			continue;

		current_cell_string =re.sub(r' +',' ',re.sub('\.','',re.sub(',',' ', re.sub('and',' ',current_cell_string))));

		current_cell_string_list = current_cell_string.split(' ');
		if class_info in current_cell_string_list and table_extraction_list.iloc[i]['Table_Row_Number'] >= min_row_number:
			return [table_extraction_list.iloc[i]['Page_Number'], table_extraction_list.iloc[i]['Table_Row_Number'], table_extraction_list.iloc[i]['Field_Value']];

	print 'heheheheeheheheheh,       ',class_info;
	return [];