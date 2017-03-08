


import Field_Value_Normalizer;
import Table_Result_Handler;
import Textarea_Result_Handler;
import Public_Processor;



import re;
import pandas;
import sys;

def customized_per_doc_process_for_freddiemac(relate_info_list_for_doc, raw_xtr_result_for_doc):
	
	criteria_id_list_for_identity_info = [];
	criteria_id_df_for_identity_info = relate_info_list_for_doc[(relate_info_list_for_doc['Field_Name'] == 'Tranche') | (relate_info_list_for_doc['Field_Name'] == 'CUSIP') | (relate_info_list_for_doc['Field_Name'] == 'Group')];
	for i in range(0 ,len(criteria_id_df_for_identity_info)):
		if criteria_id_df_for_identity_info.iloc[i]['Extraction_Criteria_ID'] not in criteria_id_list_for_identity_info:
			criteria_id_list_for_identity_info.append(criteria_id_df_for_identity_info.iloc[i]['Extraction_Criteria_ID']);

	
	raw_xtr_result_for_identity = raw_xtr_result_for_doc[raw_xtr_result_for_doc['Extraction_Criteria_ID'].isin(criteria_id_list_for_identity_info)];
	element_identity_pairs_list = get_element_identity_pairs_freddiemac(raw_xtr_result_for_identity);


	for item in element_identity_pairs_list:
		print item;
	

	total_field_with_metadata_list = [];
	for i in range(0, len(relate_info_list_for_doc)):

		for element_pair in element_identity_pairs_list:
			current_row_xtr_list = Table_Result_Handler.get_a_row_fields_by_page_row_numbers(raw_xtr_result_for_doc, element_pair[1], element_pair[2]);
			current_cell_metadata = get_a_cell_metadata_freddiemac(current_row_xtr_list, element_pair, relate_info_list_for_doc.iloc[i]);
			if current_cell_metadata != []:
				total_field_with_metadata_list.append(current_cell_metadata);

	print '';
	print '';
	print 'check length!!!!!!!!!!!!!!!!!        ', len(total_field_with_metadata_list);
	print '';
	print '';


	for i in range(0, len(relate_info_list_for_doc)):			
		if relate_info_list_for_doc.iloc[i]['Field_Name'] == 'Trustee':
			for j in range(0, len(element_identity_pairs_list)):
				element_identity_pair = element_identity_pairs_list[j];
				freetext_field_with_metadata = [element_identity_pair[0]] +[relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID']] + Textarea_Result_Handler.get_freetext_metadata_by_criteria(relate_info_list_for_doc.iloc[i],raw_xtr_result_for_doc,'FHL') + ['Trustee'];
				total_field_with_metadata_list.append(freetext_field_with_metadata);

		elif relate_info_list_for_doc.iloc[i]['Field_Name'] == 'Calendar':
			for j in range(0, len(element_identity_pairs_list)):
				element_identity_pair = element_identity_pairs_list[j];
				freetext_field_with_metadata = [element_identity_pair[0]] +[relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID']] + Textarea_Result_Handler.get_freetext_metadata_by_criteria(relate_info_list_for_doc.iloc[i],raw_xtr_result_for_doc,'US') + ['Calendar'];
				total_field_with_metadata_list.append(freetext_field_with_metadata);
		elif relate_info_list_for_doc.iloc[i]['Field_Name'] == 'Clean Up Call':
			for j in range(0, len(element_identity_pairs_list)):
				element_identity_pair = element_identity_pairs_list[j];
				freetext_field_with_metadata = [element_identity_pair[0]] + [relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID']] + Textarea_Result_Handler.get_freetext_metadata_by_criteria(relate_info_list_for_doc.iloc[i],raw_xtr_result_for_doc,'1') + ['Clean Up Call'];
				total_field_with_metadata_list.append(freetext_field_with_metadata); 
		elif relate_info_list_for_doc.iloc[i]['Field_Name'] == 'Min Increment':
			for j in range(0, len(element_identity_pairs_list)):
				element_identity_pair = element_identity_pairs_list[j];
				field_value = 'N/A type Residual' if ('NPR' in element_identity_pair[7]) else '1';
				freetext_field_with_metadata = [element_identity_pair[0]] + [relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID']] + Textarea_Result_Handler.get_freetext_metadata_by_criteria(relate_info_list_for_doc.iloc[i],raw_xtr_result_for_doc,field_value) + ['Min Increment'];
				total_field_with_metadata_list.append(freetext_field_with_metadata); 
		elif relate_info_list_for_doc.iloc[i]['Field_Name'] == 'Min Purchase':
			for j in range(0, len(element_identity_pairs_list)):
				element_identity_pair = element_identity_pairs_list[j];
				field_value = '100000' if ('NTL' in element_identity_pair[-1]) or ('PO' in element_identity_pair[-1]) or ('IO' in element_identity_pair[-1]) or ('INV' in element_identity_pair[-1]) or ('NSJ' in element_identity_pair[-1])  or ('SPP' in element_identity_pair[-1]) else '1000';
				field_value = 'N/A type Residual' if 'NPR' in element_identity_pair[-1] else field_value;
				freetext_field_with_metadata = [element_identity_pair[0]] +[relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID']] + Textarea_Result_Handler.get_freetext_metadata_by_criteria(relate_info_list_for_doc.iloc[i],raw_xtr_result_for_doc,field_value) + ['Min Purchase'];
				total_field_with_metadata_list.append(freetext_field_with_metadata); 
		elif relate_info_list_for_doc.iloc[i]['Field_Name'] == 'Reset Frequency':
			for j in range(0, len(element_identity_pairs_list)):
				element_identity_pair = element_identity_pairs_list[j];
				field_value = '12.0' if not (('FIX' in element_identity_pair[-1]) or ('NPR' in element_identity_pair[-1])) else 'N/A type FIX or NPR';
				freetext_field_with_metadata = [element_identity_pair[0]] +[relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID']] + Textarea_Result_Handler.get_freetext_metadata_by_criteria(relate_info_list_for_doc.iloc[i],raw_xtr_result_for_doc,field_value) + ['Reset Frequency'];
				total_field_with_metadata_list.append(freetext_field_with_metadata); 
		
		elif relate_info_list_for_doc.iloc[i]['Extraction_Criteria_ID'] == 1083 or relate_info_list_for_doc.iloc[i]['Extraction_Criteria_ID']==23 or relate_info_list_for_doc.iloc[i]['Extraction_Criteria_ID']== 1071:
			pass;

		elif relate_info_list_for_doc.iloc[i]['Field_Name'] == 'Structuring Ranges':
			xtr_to_calcrt_config_map_id = relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID'];
			extraction_criteria_id = relate_info_list_for_doc.iloc[i]['Extraction_Criteria_ID'];
			xtr_fields_list = raw_xtr_result_for_doc[raw_xtr_result_for_doc['Extraction_Criteria_ID']==extraction_criteria_id];
			
			start_row_number = Table_Result_Handler.get_row_number_list_by_keyword(xtr_fields_list,'Initial Effective Ranges',1);

			for j in  range(0,len(element_identity_pairs_list)):
				element_identity_pair = element_identity_pairs_list[j];
				class_info = element_identity_pair[4];
				row_number = Table_Result_Handler.get_row_number_list_class_info(xtr_fields_list,class_info,1);


				freetext_field_with_metadata = [];
				if row_number==[] or 'Residual' == element_identity_pair[6] or row_number[0][1] < start_row_number[0][1]:
					freetext_field_with_metadata = [element_identity_pair[0]] +[relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID']] + Textarea_Result_Handler.get_freetext_metadata_by_criteria(relate_info_list_for_doc.iloc[i],raw_xtr_result_for_doc,'N/A') + ['Structuring Ranges'];
				else:
					row_number_info = row_number[0];
					structuring_ranges_cell = Table_Result_Handler.get_cell_field_info_by_page_row_column(xtr_fields_list, row_number_info[0], row_number_info[1],1,reverse_order=1);
					field_value = structuring_ranges_cell['Field_Value'];
					if len(re.sub(' ','',field_value)) == 0 or field_value is None:
						field_value = 'N/A, extraction error';
					freetext_field_with_metadata = [element_identity_pair[0]] + [relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID']] + [structuring_ranges_cell['Page_Number'],structuring_ranges_cell['Pos_Min_X'],structuring_ranges_cell['Pos_Min_Y'],structuring_ranges_cell['Pos_Max_X'],structuring_ranges_cell['Pos_Max_Y'],field_value,structuring_ranges_cell['Font']] + ['Structuring Ranges'];

				total_field_with_metadata_list.append(freetext_field_with_metadata);

		elif relate_info_list_for_doc.iloc[i]['Field_Name'] == 'WALs':
			raw_xtr_prepayment_table_result_for_doc = raw_xtr_result_for_doc.loc[raw_xtr_result_for_doc['Extraction_Criteria_ID'] == relate_info_list_for_doc.iloc[i]['Extraction_Criteria_ID']];
			xtr_to_calcrt_config_map_id = relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID'];
			print len(raw_xtr_prepayment_table_result_for_doc);
			current_class_row_info = [];
			for element_pair in element_identity_pairs_list:
				if element_pair[-2] == 'Residual':
					continue;
				if re.sub(r'[0-9]','',element_pair[4]) == 'R' or re.sub(r'[0-9]','',element_pair[4]) == 'RR':
					continue;	
				if 'NPR' in element_pair[-1]:
					continue;	
				class_info = element_pair[4];
				class_row_info = Table_Result_Handler.get_row_number_list_class_info_for_pricing_speed_fre(raw_xtr_prepayment_table_result_for_doc, class_info);
				
				if class_row_info != []:
					current_class_row_info = class_row_info;
					current_page_number = current_class_row_info[0];
					current_row_number = current_class_row_info[1];
					while current_row_number <= 300:
						current_row_xtr_list = Table_Result_Handler.get_a_row_fields_by_page_row_numbers(raw_xtr_prepayment_table_result_for_doc, current_page_number, current_row_number);
						number_of_percent_sign = Table_Result_Handler.get_number_of_match_regex_in_a_row(current_row_xtr_list, r'\.\d');
						if number_of_percent_sign >= 3:
							# print number_of_percent_sign, '             ==========           ', current_row_number;
							current_column_number = (number_of_percent_sign + 1)/2;
							current_cell_metadata = Table_Result_Handler.get_cell_field_info_by_page_row_column(current_row_xtr_list, current_page_number, current_row_number, current_column_number, reverse_order=1);
							pos_min_x = current_cell_metadata['Pos_Min_X'];
							pos_min_y = current_cell_metadata['Pos_Min_Y'];
							pos_max_x = current_cell_metadata['Pos_Max_X'];
							pos_max_y = current_cell_metadata['Pos_Max_Y'];
							extracted_value =current_cell_metadata['Field_Value'];
							font = current_cell_metadata['Font'];
							total_field_with_metadata_list.append([element_pair[0], xtr_to_calcrt_config_map_id, current_page_number, pos_min_x, pos_min_y, pos_max_x, pos_max_y, extracted_value, font, 'WALs']);							
							break;
						current_row_number += 1;
				else:
					class_row_info = current_class_row_info;
					if current_class_row_info == []:
						default_page_number = raw_xtr_prepayment_table_result_for_doc.iloc[0]['Page_Number'];
						freetext_field_with_metadata = [element_pair[0]] +[relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID']] + [default_page_number,0,0,0,0,'Extraction Error, Please check the original document and OID section.'] + ['Pricing Speed'];
						total_field_with_metadata_list.append(freetext_field_with_metadata);
					else:						
						print '!!!!!!!!!!!!!!!!!!!!!!! ',class_info, '                  ' ,class_row_info;
						freetext_field_with_metadata = [element_pair[0]] +[relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID']] + [class_row_info[0],0,0,0,0,'Extraction Error, Please check the original document and OID section.'] + ['WALs'];
						total_field_with_metadata_list.append(freetext_field_with_metadata);
					continue;		


			
		elif relate_info_list_for_doc.iloc[i]['Field_Name'] == 'Pricing Speed':
			raw_xtr_prepayment_table_result_for_doc = raw_xtr_result_for_doc.loc[raw_xtr_result_for_doc['Extraction_Criteria_ID'] == relate_info_list_for_doc.iloc[i]['Extraction_Criteria_ID']];
			xtr_to_calcrt_config_map_id = relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID'];
			print len(raw_xtr_prepayment_table_result_for_doc);
		
			prepayment_row_number_list = Table_Result_Handler.get_row_number_list_by_keyword(raw_xtr_prepayment_table_result_for_doc, 'Prepayment Assumption', 1);
			current_class_row_info = [];
			for element_pair in element_identity_pairs_list:
				current_page_number = 0;
				if element_pair[-2] == 'Residual':
					continue;
				if re.sub(r'[0-9]','',element_pair[4]) == 'R' or re.sub(r'[0-9]','',element_pair[4]) == 'RR':
					continue;	
				if 'NPR' in element_pair[-1]:
					continue;	
				
				class_info = element_pair[4];
				class_row_info = Table_Result_Handler.get_row_number_list_class_info_for_pricing_speed_fre(raw_xtr_prepayment_table_result_for_doc, class_info);
				
				if class_row_info != []:
					current_class_row_info = class_row_info;
					current_page_number = current_class_row_info[0];
					current_row_number = current_class_row_info[1];
					while current_row_number >= 1:
						current_row_xtr_list = Table_Result_Handler.get_a_row_fields_by_page_row_numbers(raw_xtr_prepayment_table_result_for_doc, current_page_number, current_row_number);
						number_of_percent_sign = Table_Result_Handler.get_number_of_match_regex_in_a_row(current_row_xtr_list, '%');
						if number_of_percent_sign >= 3:
							# print number_of_percent_sign, '             ==========           ', current_row_number;
							current_column_number = (number_of_percent_sign + 1)/2;
							current_cell_metadata = Table_Result_Handler.get_cell_field_info_by_page_row_column(current_row_xtr_list, current_page_number, current_row_number, current_column_number, reverse_order=1);
							pos_min_x = current_cell_metadata['Pos_Min_X'];
							pos_min_y = current_cell_metadata['Pos_Min_Y'];
							pos_max_x = current_cell_metadata['Pos_Max_X'];
							pos_max_y = current_cell_metadata['Pos_Max_Y'];
							extracted_value =current_cell_metadata['Field_Value'];
							current_row_xtr_list = Table_Result_Handler.get_a_row_fields_by_page_row_numbers(raw_xtr_prepayment_table_result_for_doc, current_page_number, current_row_number-1);
							prepay_value = Table_Result_Handler.get_cell_field_info_by_page_row_column(current_row_xtr_list, current_page_number, current_row_number-1,1)['Field_Value'];

							prepay_value = prepay_value[:re.search('Prepayment', prepay_value).start()];

							extracted_value = extracted_value + ' ' + prepay_value;

							extracted_value = Field_Value_Normalizer.remove_characters(extracted_value,[' ','\.']);
							font = current_cell_metadata['Font'];
							total_field_with_metadata_list.append([element_pair[0], xtr_to_calcrt_config_map_id, current_page_number, pos_min_x, pos_min_y, pos_max_x, pos_max_y, extracted_value, font, 'Pricing Speed']);							
							break;
						current_row_number -= 1;
				else:
					class_row_info = current_class_row_info;
					print '!!!!!!!!!!!!!!!!!!!!!!! ',class_info, '                  ' ,class_row_info;
					if current_class_row_info == []:
						default_page_number = raw_xtr_prepayment_table_result_for_doc.iloc[0]['Page_Number'];
						freetext_field_with_metadata = [element_pair[0]] +[relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID']] + [default_page_number,0,0,0,0,'Extraction Error, Please check the original document.'] + ['Pricing Speed'];
						total_field_with_metadata_list.append(freetext_field_with_metadata);
					else:	
						freetext_field_with_metadata = [element_pair[0]] +[relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID']] + [class_row_info[0],0,0,0,0,'Extraction Error, Please check the original document.'] + ['Pricing Speed'];
						total_field_with_metadata_list.append(freetext_field_with_metadata);
					continue;		


		else:
			# print relate_info_list_for_doc.iloc[i]['Field_Name'];
			for j in range(0, len(element_identity_pairs_list)):
				element_identity_pair = element_identity_pairs_list[j];
				for result_obj in Textarea_Result_Handler.get_freetext_metadata_by_criteria(relate_info_list_for_doc.iloc[i],raw_xtr_result_for_doc):
					freetext_field_with_metadata = [element_identity_pair[0]] + [relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID']] + result_obj + [relate_info_list_for_doc.iloc[i]['Field_Name']];	
					total_field_with_metadata_list.append(freetext_field_with_metadata);
		


	float_info_raw_extraction_list = raw_xtr_result_for_doc[raw_xtr_result_for_doc['Extraction_Criteria_ID']==1071];
	float_relate_info_list_for_doc = relate_info_list_for_doc[relate_info_list_for_doc['Extraction_Criteria_ID'] == 1071];
	float_info_with_metadata_list = get_float_info_for_des_inv_flt_freddie(element_identity_pairs_list, total_field_with_metadata_list, float_info_raw_extraction_list, float_relate_info_list_for_doc);
	
	total_field_with_metadata_list = total_field_with_metadata_list + float_info_with_metadata_list;





	"""
		Here we do data normalization for FreddieMac
	"""
	abbreviation_list = [];
	for item in total_field_with_metadata_list:
		if item[-1] == 'Maturity' or item[-1] == 'Closing Date' or item[-1] == 'Pricing Date':
			item[7] = Field_Value_Normalizer.get_date_digits(item[7]);
			continue;	
		if item[-1] == 'Sponsor' or item[-1] == 'Co-Sponsor':
			if abbreviation_list==[]:
				item[7] = Field_Value_Normalizer.get_sponsor_names(item[7]);
				abbreviation_list = Field_Value_Normalizer.get_mapped_abbreviation_for_sponsor(item[7],1);
				if item[-1] == 'Sponsor':
					item[7] = abbreviation_list[0][0].strip();
					stored_sponsor_string = item[7];
				else:
					abbreviation_list_for_cs = abbreviation_list[1:];
					if abbreviation_list_for_cs == []:
						item[7] = 'N/A, No Co-Sponsor/Co-Manager for this Deal Series';
					else:
						item[7] = re.sub(r' +',' ',''.join(list(zip(*abbreviation_list_for_cs)[0])));
			else:
				if item[-1] == 'Sponsor':
					item[7] = abbreviation_list[0][0].strip();
					stored_sponsor_string = item[7];
				else:
					abbreviation_list_for_cs = abbreviation_list[1:];
					if abbreviation_list_for_cs == []:
						item[7] = 'N/A, No Co-Sponsor/Co-Manager for this Deal Series';
					else:
						item[7] = re.sub(r' +',' ',''.join(list(zip(*abbreviation_list_for_cs)[0])));

			if len(re.sub(' ','',item[7])) == 0:
				item[7] = 'N/A, cannot extract Sponsor. Please check document.';


			continue;
		if item[-1] == 'Deal Size':
			item[7] = Field_Value_Normalizer.get_balance_digits(item[7]);	
			continue;
		if item[-1] == 'Descriptors':
			# print item;
			if item[2] > 2:
				item[7] = item[7] + ' EXCH';
			item[7] = Field_Value_Normalizer.get_normalized_descriptors(item[7]);		
			continue;
		if item[-1] == 'Day Count':
			item[7] = Field_Value_Normalizer.get_day_count(item[7]);
			continue;
		if item[-1] == 'Deal Series':
			item[7] = Field_Value_Normalizer.get_deal_series(item[7],'FHR');		
			continue;
		floater_index_string = '';	
		if item[-1] == 'Class Coupon':
			if '(' not in item[7] and 'N/A' not in item[7]:
				item[7] = str(round(float(item[7]),6));
			if item[7][-1] == '0' and item[7][-2] != '.':
				item[7] = item[7][:-1];
			continue;
		if item[-1] == 'Floor' or item[-1] == 'Ceiling':
			item[7] = Field_Value_Normalizer.remove_characters(item[7],['%']);
			if 'N/A' not in item[7] and '.' not in item[7]:
				item[7] = item[7]+".0";
			try:
				item[7] = str(float(item[7]));
			except:
				item[7] =item[7];
			if item[-1] == 'Ceiling':
				if 'No column' in item[7]:
					item[7] = '9999.0';
			continue;
		if item[-1] == 'Slope':
			if 'N/A' not in str(item[7]) and '.' not in str(item[7]):
				item[7] = str(item[7])+".0";
			elif item[7][-1] == '0' and item[7][-2] != '.':
				item[7] = item[7][:-1];
			continue;	

		if item[-1] == 'Floater Index':
			item[7] = Field_Value_Normalizer.get_floater_index(item[7]);
			floater_index_string = item[7];	
			continue;	
		if item[-1] == 'Floater Spread':
			if 'N/A' not in item[7]:
				flag = 0;
				if '%' in item[7]:
					flag = 1;
				item[7] = Field_Value_Normalizer.remove_subregex(item[7], r'[^0-9\.]');

				if flag == 1:
					item[7] = str(float(item[7]) * 100);
				item[3] = 50;
				item[5] = 750;
				print 'aiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii,               ',item[7];
			continue;
		if item[-1] == 'Frequency':
			item[7] = '12';	
			continue;	
		if item[-1] == 'Reset Frequency':
			item[7] = Field_Value_Normalizer.get_reset_frequency(item[7],floater_index_string);
			continue;
		if item[-1] == 'Pricing Speed':
			item[7] = Field_Value_Normalizer.get_pricing_speed(item[7]);
			if 'N/A' not in item[7]:
				item[7] = 'Please check the highlighted area and OID section of the document.';
				item[3] = 50;
				item[5] = 750;	
			continue;
		if item[-1] == 'WALs':
			if 'N/A' not in item[7]:
				item[7] = 'Please check the highlighted area and OID section of the document.';
				item[3] = 50;
				item[5] = 750;	
			continue;

		if item[-1] == 'Structuring Ranges':
			item[7] = Field_Value_Normalizer.get_structuring_ranges(item[7]);

			continue;
		if item[-1] == 'Record Date':
			item[7] = str(Field_Value_Normalizer.get_last_business_day(15));
			continue;




	# print 'part check length!!!!!!!!!!!!!         ', len([items for items in total_field_with_metadata_list if items[-1] == 'Class Coupon']);
	# for item in [items for items in total_field_with_metadata_list if items[-1] == 'Class Coupon']:
	# 	print item;
	# sys.exit();

	print '';
	print '';
	print 'check length!!!!!!!!!!!!!!!!!        ', len(total_field_with_metadata_list);
	print '';
	print '';
	return element_identity_pairs_list, total_field_with_metadata_list;


def get_a_cell_metadata_freddiemac(row_xtr_list, element_identity_pair_info, relate_info_list_for_doc_item):
	# [element_identity_pair[0],relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID'],page_number, pos_min_x, pos_min_y, pos_max_x, pos_max_y, extracted_value, font, relate_info_list_for_doc.iloc[i]['Field_Name']]
	element_identity_pair_id = element_identity_pair_info[0];
	xtr_to_calcrt_config_map_id = relate_info_list_for_doc_item['Xtr_To_Calcrt_Config_Map_ID'];
	page_number = element_identity_pair_info[1];
	pos_min_x = 0.0; 
	pos_min_y = 0.0; 
	pos_max_x = 0.0; 
	pos_max_y = 0.0; 
	extracted_value = ''; 
	font = '';
	field_name = relate_info_list_for_doc_item['Field_Name'];

	target_column_index = element_identity_pair_info[3];

	target_page_number = element_identity_pair_info[1];

	target_row_number = element_identity_pair_info[2];


	if relate_info_list_for_doc_item['Extraction_Criteria_ID'] == 23:
		if target_page_number > 3:
			return [];
		else:
			if field_name == 'Maturity':
				target_column_index = target_column_index + 1;
				while target_column_index <= len(row_xtr_list):
					current_cell_metadata = Table_Result_Handler.get_cell_field_info_by_page_row_column(row_xtr_list, target_page_number, target_row_number, target_column_index);
					if target_column_index == element_identity_pair_info[3]+1:
						pos_min_x = current_cell_metadata['Pos_Min_X'];
						pos_min_y = current_cell_metadata['Pos_Min_Y'];
						font = current_cell_metadata['Font'];
					if target_column_index == len(row_xtr_list):
						pos_max_x = current_cell_metadata['Pos_Max_X'];
						pos_max_y = current_cell_metadata['Pos_Max_Y'];
					# print extracted_value;
					extracted_value = extracted_value + current_cell_metadata['Field_Value'];
					target_column_index += 1;
				return [element_identity_pair_info[0], xtr_to_calcrt_config_map_id, page_number, pos_min_x, pos_min_y, pos_max_x, pos_max_y, extracted_value, font, field_name];
			if field_name == 'CUSIP':
				target_column_index = target_column_index;
				current_cell_metadata = Table_Result_Handler.get_cell_field_info_by_page_row_column(row_xtr_list, target_page_number, target_row_number, target_column_index);
				pos_min_x = current_cell_metadata['Pos_Min_X'];
				pos_min_y = current_cell_metadata['Pos_Min_Y'];
				pos_max_x = current_cell_metadata['Pos_Max_X'];
				pos_max_y = current_cell_metadata['Pos_Max_Y'];
				extracted_value =current_cell_metadata['Field_Value'];
				extracted_value = Field_Value_Normalizer.remove_characters(extracted_value,[' ','\.']);
				font = current_cell_metadata['Font'];
				return [element_identity_pair_info[0], xtr_to_calcrt_config_map_id, page_number, pos_min_x, pos_min_y, pos_max_x, pos_max_y, extracted_value, font, field_name];
			if field_name == 'Class Coupon':
				target_column_index = target_column_index - 2;
				current_cell_metadata = Table_Result_Handler.get_cell_field_info_by_page_row_column(row_xtr_list, target_page_number, target_row_number, target_column_index);
				pos_min_x = current_cell_metadata['Pos_Min_X'];
				pos_min_y = current_cell_metadata['Pos_Min_Y'];
				pos_max_x = current_cell_metadata['Pos_Max_X'];
				pos_max_y = current_cell_metadata['Pos_Max_Y'];
				extracted_value =current_cell_metadata['Field_Value'];
				extracted_value = Field_Value_Normalizer.remove_characters(extracted_value,[' ','\%']);

				if element_identity_pair_info[-2] == 'Residual':
					extracted_value = 'N/A';

				font = current_cell_metadata['Font'];
				return [element_identity_pair_info[0], xtr_to_calcrt_config_map_id, page_number, pos_min_x, pos_min_y, pos_max_x, pos_max_y, extracted_value, font, field_name];
			if field_name ==  'Descriptors':
				target_column_index = element_identity_pair_info[3] - 3;
				current_cell_metadata = Table_Result_Handler.get_cell_field_info_by_page_row_column(row_xtr_list, target_page_number, target_row_number, target_column_index);
				pos_min_x = current_cell_metadata['Pos_Min_X'];
				pos_min_y = current_cell_metadata['Pos_Min_Y'];
				target_column_index = element_identity_pair_info[3] - 1;
				current_cell_metadata = Table_Result_Handler.get_cell_field_info_by_page_row_column(row_xtr_list, target_page_number, target_row_number, target_column_index);
				pos_max_x = current_cell_metadata['Pos_Max_X'];
				pos_max_y = current_cell_metadata['Pos_Max_Y'];
				font = current_cell_metadata['Font'];
				extracted_value = element_identity_pair_info[7]
				return [element_identity_pair_info[0], xtr_to_calcrt_config_map_id, page_number, pos_min_x, pos_min_y, pos_max_x, pos_max_y, extracted_value, font, field_name];
			if field_name ==  'Class Balance':
				target_column_index = target_column_index - 4;
				current_cell_metadata = Table_Result_Handler.get_cell_field_info_by_page_row_column(row_xtr_list, target_page_number, target_row_number, target_column_index);
				pos_min_x = current_cell_metadata['Pos_Min_X'];
				pos_min_y = current_cell_metadata['Pos_Min_Y'];
				pos_max_x = current_cell_metadata['Pos_Max_X'];
				pos_max_y = current_cell_metadata['Pos_Max_Y'];
				extracted_value =current_cell_metadata['Field_Value'];
				extracted_value = Field_Value_Normalizer.remove_characters(extracted_value,[' ','\.','\,','\$']);	
				font = current_cell_metadata['Font'];
				return [element_identity_pair_info[0], xtr_to_calcrt_config_map_id, page_number, pos_min_x, pos_min_y, pos_max_x, pos_max_y, extracted_value, font, field_name];				
			if field_name ==  'Tranche':
				target_column_index = target_column_index - 5;
				current_cell_metadata = Table_Result_Handler.get_cell_field_info_by_page_row_column(row_xtr_list, target_page_number, target_row_number, target_column_index);
				pos_min_x = current_cell_metadata['Pos_Min_X'];
				pos_min_y = current_cell_metadata['Pos_Min_Y'];
				pos_max_x = current_cell_metadata['Pos_Max_X'];
				pos_max_y = current_cell_metadata['Pos_Max_Y'];
				extracted_value = element_identity_pair_info[4];
				font = current_cell_metadata['Font'];
				return [element_identity_pair_info[0], xtr_to_calcrt_config_map_id, page_number, pos_min_x, pos_min_y, pos_max_x, pos_max_y, extracted_value, font, field_name];

	if relate_info_list_for_doc_item['Extraction_Criteria_ID'] == 1083:
		if target_page_number <= 3:
			return [];
		else:
			if field_name == 'Maturity':
				target_column_index = target_column_index + 1;
				while target_column_index <= len(row_xtr_list):
					current_cell_metadata = Table_Result_Handler.get_cell_field_info_by_page_row_column(row_xtr_list, target_page_number, target_row_number, target_column_index);
					if target_column_index == element_identity_pair_info[3]+1:
						pos_min_x = current_cell_metadata['Pos_Min_X'];
						pos_min_y = current_cell_metadata['Pos_Min_Y'];
						font = current_cell_metadata['Font'];
					if target_column_index == len(row_xtr_list):
						pos_max_x = current_cell_metadata['Pos_Max_X'];
						pos_max_y = current_cell_metadata['Pos_Max_Y'];

					if current_cell_metadata['Field_Value'] is not None:
						extracted_value = extracted_value + current_cell_metadata['Field_Value'];
					target_column_index += 1;
				return [element_identity_pair_info[0], xtr_to_calcrt_config_map_id, page_number, pos_min_x, pos_min_y, pos_max_x, pos_max_y, extracted_value, font, field_name];
			if field_name == 'CUSIP':
				target_column_index = target_column_index;
				current_cell_metadata = Table_Result_Handler.get_cell_field_info_by_page_row_column(row_xtr_list, target_page_number, target_row_number, target_column_index);
				pos_min_x = current_cell_metadata['Pos_Min_X'];
				pos_min_y = current_cell_metadata['Pos_Min_Y'];
				pos_max_x = current_cell_metadata['Pos_Max_X'];
				pos_max_y = current_cell_metadata['Pos_Max_Y'];
				extracted_value =current_cell_metadata['Field_Value'];
				extracted_value = Field_Value_Normalizer.remove_characters(extracted_value,[' ','\.']);
				font = current_cell_metadata['Font'];
				return [element_identity_pair_info[0], xtr_to_calcrt_config_map_id, page_number, pos_min_x, pos_min_y, pos_max_x, pos_max_y, extracted_value, font, field_name];		
			if field_name == 'Class Coupon':
				target_column_index = target_column_index - 2;
				current_cell_metadata = Table_Result_Handler.get_cell_field_info_by_page_row_column(row_xtr_list, target_page_number, target_row_number, target_column_index);
				pos_min_x = current_cell_metadata['Pos_Min_X'];
				pos_min_y = current_cell_metadata['Pos_Min_Y'];
				pos_max_x = current_cell_metadata['Pos_Max_X'];
				pos_max_y = current_cell_metadata['Pos_Max_Y'];
				extracted_value =current_cell_metadata['Field_Value'];
				extracted_value = Field_Value_Normalizer.remove_characters(extracted_value,[' ','\%']);
				font = current_cell_metadata['Font'];
				return [element_identity_pair_info[0], xtr_to_calcrt_config_map_id, page_number, pos_min_x, pos_min_y, pos_max_x, pos_max_y, extracted_value, font, field_name];
			if field_name ==  'Descriptors':
				target_column_index = element_identity_pair_info[3] - 3;
				current_cell_metadata = Table_Result_Handler.get_cell_field_info_by_page_row_column(row_xtr_list, target_page_number, target_row_number, target_column_index);
				pos_min_x = current_cell_metadata['Pos_Min_X'];
				pos_min_y = current_cell_metadata['Pos_Min_Y'];
	
				target_column_index = element_identity_pair_info[3] - 1;
				current_cell_metadata = Table_Result_Handler.get_cell_field_info_by_page_row_column(row_xtr_list, target_page_number, target_row_number, target_column_index);
				pos_max_x = current_cell_metadata['Pos_Max_X'];
				pos_max_y = current_cell_metadata['Pos_Max_Y'];
				font = current_cell_metadata['Font'];
				extracted_value = element_identity_pair_info[7];
				return [element_identity_pair_info[0], xtr_to_calcrt_config_map_id, page_number, pos_min_x, pos_min_y, pos_max_x, pos_max_y, extracted_value, font, field_name];
			if field_name ==  'Class Balance':
				target_column_index = target_column_index - 5;
				current_cell_metadata = Table_Result_Handler.get_cell_field_info_by_page_row_column(row_xtr_list, target_page_number, target_row_number, target_column_index);
				pos_min_x = current_cell_metadata['Pos_Min_X'];
				pos_min_y = current_cell_metadata['Pos_Min_Y'];
				pos_max_x = current_cell_metadata['Pos_Max_X'];
				pos_max_y = current_cell_metadata['Pos_Max_Y'];
				extracted_value =current_cell_metadata['Field_Value'];
				extracted_value = Field_Value_Normalizer.remove_characters(extracted_value,[' ','\.','\,','\$']);	
				font = current_cell_metadata['Font'];
				return [element_identity_pair_info[0], xtr_to_calcrt_config_map_id, page_number, pos_min_x, pos_min_y, pos_max_x, pos_max_y, extracted_value, font, field_name];
			if field_name ==  'Tranche':
				target_column_index = target_column_index - 6;
				current_cell_metadata = Table_Result_Handler.get_cell_field_info_by_page_row_column(row_xtr_list, target_page_number, target_row_number, target_column_index);
				pos_min_x = current_cell_metadata['Pos_Min_X'];
				pos_min_y = current_cell_metadata['Pos_Min_Y'];
				pos_max_x = current_cell_metadata['Pos_Max_X'];
				pos_max_y = current_cell_metadata['Pos_Max_Y'];
				extracted_value = element_identity_pair_info[4];
				font = current_cell_metadata['Font'];
				return [element_identity_pair_info[0], xtr_to_calcrt_config_map_id, page_number, pos_min_x, pos_min_y, pos_max_x, pos_max_y, extracted_value, font, field_name];
	
	return [];
	


def get_element_identity_pairs_freddiemac(xtr_fields_list):
	tranche_location_list = [];
	grouped_rows_fields_list_by_criteria = xtr_fields_list.groupby(['Extraction_Criteria_ID']);
	cusip_position_in_each_row_list = [];
	for key, group in grouped_rows_fields_list_by_criteria:
		grouped_rows_fields_list = group.groupby(['Table_Row_Number']);
		for subkey, subgroup in grouped_rows_fields_list:
			cusip_match_location = Table_Result_Handler.get_column_number_in_row_by_regex(subgroup, r'^[0-9]{3}[0-9A-Z]{5}[0-9]{1}$');
			if cusip_match_location != []:
				cusip_position_in_each_row_list.append(cusip_match_location);

	element_identity_pairs_list = [];


	cusip_index = 1;
	for item in cusip_position_in_each_row_list:
		# print item;
		class_info = '';
		
	

		cusip_info = '';
		cusip_info = Table_Result_Handler.get_cell_field_info_by_page_row_column(xtr_fields_list,item[0],item[1],item[2])['Field_Value'];

		cusip_info = Field_Value_Normalizer.remove_characters(cusip_info,[' ','\.']);


		descriptors_info = '';
		descriptors_info = Table_Result_Handler.get_cell_field_info_by_page_row_column(xtr_fields_list,item[0],item[1],item[2]-3)['Field_Value'];
		shift_flag = 0;
		if descriptors_info is None or descriptors_info == 'I)' or descriptors_info == 'II)':
			descriptors_info = Table_Result_Handler.get_cell_field_info_by_page_row_column(xtr_fields_list,item[0],item[1],item[2]-4)['Field_Value'];
			shift_flag = 1;
		descriptors_info_2nd = Table_Result_Handler.get_cell_field_info_by_page_row_column(xtr_fields_list,item[0],item[1],item[2]-1)['Field_Value'];
		if descriptors_info_2nd is None or descriptors_info_2nd == 'I)' or descriptors_info_2nd == 'II)':
			descriptors_info_2nd = Table_Result_Handler.get_cell_field_info_by_page_row_column(xtr_fields_list,item[0],item[1],item[2]-2)['Field_Value'];	
			shift_flag = 1;
		descriptors_info = descriptors_info + '|' + descriptors_info_2nd;

		group_info = 'Residual' if 'NPR' in descriptors_info else '0';

		if shift_flag == 0:
			if item[0] < 3:
				class_info = Table_Result_Handler.get_cell_field_info_by_page_row_column(xtr_fields_list,item[0],item[1],item[2]-5)['Field_Value'];
			else:
				class_info = Table_Result_Handler.get_cell_field_info_by_page_row_column(xtr_fields_list,item[0],item[1],item[2]-6)['Field_Value'];
		else:
			if item[0] < 3:
				class_info = Table_Result_Handler.get_cell_field_info_by_page_row_column(xtr_fields_list,item[0],item[1],item[2]-6)['Field_Value'];
			else:
				class_info = Table_Result_Handler.get_cell_field_info_by_page_row_column(xtr_fields_list,item[0],item[1],item[2]-7)['Field_Value'];


		class_info = Field_Value_Normalizer.remove_characters(class_info,[' ','\.',r'\(\d\)']);	

		element_identity_pairs_list.append([cusip_index]+item+[class_info, cusip_info, group_info, descriptors_info]);
		cusip_index += 1;

	
	return element_identity_pairs_list;





def get_float_info_for_des_inv_flt_freddie(element_identity_pairs_list, total_field_with_metadata_list, float_info_raw_extraction_list, float_relate_info_list_for_doc):
	float_info_with_metadata_fix_npr = [];
	float_info_with_metadata_inv_flt = [];
	identity_pairs_list_for_inv_flt = [];
	
	
	# [47, 22, 30, 428.51499999999999, 211.214, 587.41819999999996, 220.142, 'FIX/IO| NTL(SEQ)', 'DMLJBJ+Times-Roman', 'Descriptors']
	# [index, link_id, page_number, x,y,x,y, pdf_value, font, field_name]

	identity_pairs_list_with_descriptor = Public_Processor.get_identity_pairs_with_descriptor(element_identity_pairs_list, total_field_with_metadata_list);

	for i in range(0, len(float_relate_info_list_for_doc)):
		extraction_calcrt_link_id = float_relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID'];
		field_name = float_relate_info_list_for_doc.iloc[i]['Field_Name'];
		for identity in identity_pairs_list_with_descriptor:
			descriptors_metadata = identity[2];
			descriptors = identity[1];
			if 'FIX' in descriptors or 'NPR' in descriptors:
				field_value = 'N/A, type FIX or NPR';
				info_with_metadata_obj = [identity[0]] + [extraction_calcrt_link_id] + descriptors_metadata[2:7] + [field_value,'Hardcoded',field_name];
				float_info_with_metadata_fix_npr.append(info_with_metadata_obj);
			else:
				identity_pairs_list_for_inv_flt.append((identity[0],descriptors));

	
	identity_pairs_list_for_inv_flt = list(set(identity_pairs_list_for_inv_flt));




	if identity_pairs_list_for_inv_flt !=[]:

		start_row_number = Table_Result_Handler.get_row_number_list_by_keyword(float_info_raw_extraction_list,'Class Coupon Formula');
		potential_row_number_for_class = Table_Result_Handler.get_row_number_list_by_keyword(float_info_raw_extraction_list,'LIBOR');
		row_number_for_class = [item for item in potential_row_number_for_class if item[1] > start_row_number[0][1]];


		float_info_raw_extraction_list_filtered = pandas.DataFrame();
		for row in row_number_for_class:
			float_info_raw_extraction_list_filtered = float_info_raw_extraction_list_filtered.append(float_info_raw_extraction_list[(float_info_raw_extraction_list['Page_Number']==row[0]) & (float_info_raw_extraction_list['Table_Row_Number']==row[1])]);





		identity_pairs_list_for_inv_flt_class = [];
		for identity_pair in identity_pairs_list_for_inv_flt:
			class_info = [class_item for class_item in element_identity_pairs_list if class_item[0] == identity_pair[0]][0];
			identity_pairs_list_for_inv_flt_class.append(class_info+[identity_pair[1]]);

		for identity_pair_class in identity_pairs_list_for_inv_flt_class:

			class_info = identity_pair_class[4];
			row_number = Table_Result_Handler.get_row_number_list_by_keyword(float_info_raw_extraction_list_filtered,class_info,1);

			if row_number == []:
				page_number = float_info_raw_extraction_list.iloc[0]['Page_Number'];
				field_value = 'Extraction Error, Please check the original document.';

				for i in range(0, len(float_relate_info_list_for_doc)):			
					if field_name == 'Slope':
						info_with_metadata_obj = [identity_pair_class[0],extraction_calcrt_link_id] + [page_number,0,0,0,0] + [field_value,'Hardcoded',field_name];
						float_info_with_metadata_inv_flt.append(info_with_metadata_obj);
						continue;
					if field_name == 'Floor':
						info_with_metadata_obj = [identity_pair_class[0],extraction_calcrt_link_id] + [page_number,0,0,0,0] + [field_value,'Hardcoded',field_name];
						float_info_with_metadata_inv_flt.append(info_with_metadata_obj);
						continue;
					if field_name == 'Ceiling':
						info_with_metadata_obj = [identity_pair_class[0],extraction_calcrt_link_id] + [page_number,0,0,0,0] + [field_value,'Hardcoded',field_name];
						float_info_with_metadata_inv_flt.append(info_with_metadata_obj);
						continue;
					if field_name == 'Floater Index':
						info_with_metadata_obj = [identity_pair_class[0],extraction_calcrt_link_id] + [page_number,0,0,0,0] + [field_value,interest_rate_formula_info[-1],field_name];
						float_info_with_metadata_inv_flt.append(info_with_metadata_obj);
						continue;
					if field_name == 'Floater Spread':
						info_with_metadata_obj = [identity_pair_class[0],extraction_calcrt_link_id] + [page_number,0,0,0,0] + [field_value,interest_rate_formula_info[-1],field_name];
						float_info_with_metadata_inv_flt.append(info_with_metadata_obj);
						continue;
				continue;

			interest_rate = Table_Result_Handler.get_cell_field_info_by_page_row_column(float_info_raw_extraction_list_filtered,row_number[0][0],row_number[0][1],2);
			interest_rate_formula = Table_Result_Handler.get_cell_field_info_by_page_row_column(float_info_raw_extraction_list_filtered,row_number[0][0],row_number[0][1],3);
			

			interest_rate_formula_info = [interest_rate_formula['Page_Number'],interest_rate_formula['Pos_Min_X'],interest_rate_formula['Pos_Min_Y'],interest_rate_formula['Pos_Max_X'],interest_rate_formula['Pos_Max_Y'], interest_rate_formula['Field_Value'] ,interest_rate_formula['Font']]

			interest_floor = Table_Result_Handler.get_cell_field_info_by_page_row_column(float_info_raw_extraction_list_filtered,row_number[0][0],row_number[0][1],4);
			interest_ceiling = Table_Result_Handler.get_cell_field_info_by_page_row_column(float_info_raw_extraction_list_filtered,row_number[0][0],row_number[0][1],5);

			if interest_floor is not None:
				if 'LIBOR' in interest_floor['Field_Value']:
					interest_floor = Table_Result_Handler.get_cell_field_info_by_page_row_column(float_info_raw_extraction_list_filtered,row_number[0][0],row_number[0][1],5);
					interest_ceiling = Table_Result_Handler.get_cell_field_info_by_page_row_column(float_info_raw_extraction_list_filtered,row_number[0][0],row_number[0][1],6);



			located_interest_rate = [class_coupon for class_coupon in total_field_with_metadata_list if class_coupon[-1] == 'Class Coupon' and class_coupon[0]== identity_pair_class[0]][0];
			located_interest_rate[2:9] = [interest_rate['Page_Number'],interest_rate['Pos_Min_X'],interest_rate['Pos_Min_Y'],interest_rate['Pos_Max_X'],interest_rate['Pos_Max_Y'], Field_Value_Normalizer.remove_characters(interest_rate['Field_Value'],[' ','\%']),interest_rate['Font']];


			for i in range(0, len(float_relate_info_list_for_doc)):
				extraction_calcrt_link_id = float_relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID'];
				field_name = float_relate_info_list_for_doc.iloc[i]['Field_Name'];
				descriptors_metadata = [descriptors_metadata for descriptors_metadata in total_field_with_metadata_list if descriptors_metadata[0] == identity_pair_class[0] and descriptors_metadata[-1] == 'Descriptors'][0];		
								
				if field_name == 'Slope':
					field_value = -1 if 'INV' in identity_pair_class[-1] else 1;
					info_with_metadata_obj = [identity_pair_class[0],extraction_calcrt_link_id] + descriptors_metadata[2:7] + [field_value,'Hardcoded',field_name];
					float_info_with_metadata_inv_flt.append(info_with_metadata_obj);
					continue;
				if field_name == 'Floor':
					field_value = '0';
					info_with_metadata_obj = [identity_pair_class[0],extraction_calcrt_link_id] + interest_rate_formula_info[0:5] + [field_value,'Hardcoded',field_name];
					if not interest_floor is None:
						field_value = interest_floor['Field_Value'];
						info_with_metadata_obj = [identity_pair_class[0],extraction_calcrt_link_id] + [interest_floor['Page_Number'],interest_floor['Pos_Min_X'],interest_floor['Pos_Min_Y'],interest_floor['Pos_Max_X'],interest_floor['Pos_Max_Y'], interest_floor['Field_Value'] ,interest_floor['Font']] + [field_name];
					float_info_with_metadata_inv_flt.append(info_with_metadata_obj);
					continue;
				if field_name == 'Ceiling':
					field_value = 'N/A No column for Maximum Interest Rate';
					info_with_metadata_obj = [identity_pair_class[0],extraction_calcrt_link_id] + interest_rate_formula_info[0:5] + [field_value,'Hardcoded',field_name];
					if not interest_ceiling is None:
						field_value = interest_floor['Field_Value'];
						info_with_metadata_obj = [identity_pair_class[0],extraction_calcrt_link_id] + [interest_ceiling['Page_Number'],interest_ceiling['Pos_Min_X'],interest_ceiling['Pos_Min_Y'],interest_ceiling['Pos_Max_X'],interest_ceiling['Pos_Max_Y'], interest_ceiling['Field_Value'] ,interest_ceiling['Font']] + [field_name];
					
					float_info_with_metadata_inv_flt.append(info_with_metadata_obj);
					continue;
				if field_name == 'Floater Index':
					field_value = interest_rate_formula['Field_Value'];
					info_with_metadata_obj = [identity_pair_class[0],extraction_calcrt_link_id] + interest_rate_formula_info[0:5] + [field_value,interest_rate_formula_info[-1],field_name];
					float_info_with_metadata_inv_flt.append(info_with_metadata_obj);
					continue;
				if field_name == 'Floater Spread':
					field_value = interest_rate_formula['Field_Value'];
					info_with_metadata_obj = [identity_pair_class[0],extraction_calcrt_link_id] + interest_rate_formula_info[0:5] + [field_value,interest_rate_formula_info[-1],field_name];
					float_info_with_metadata_inv_flt.append(info_with_metadata_obj);
					continue;



	float_info_with_metadata_list = float_info_with_metadata_fix_npr + float_info_with_metadata_inv_flt;
	# print len(float_info_with_metadata_list);
	return float_info_with_metadata_list;
