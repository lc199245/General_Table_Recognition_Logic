


import Field_Value_Normalizer;
import Table_Result_Handler;
import Textarea_Result_Handler;
import Public_Processor;



import re;
import pandas;
import sys;

def customized_per_doc_process_for_ginniemae(relate_info_list_for_doc, raw_xtr_result_for_doc):
	
	criteria_id_list_for_identity_info = [];
	criteria_id_df_for_identity_info = relate_info_list_for_doc[(relate_info_list_for_doc['Field_Name'] == 'Tranche') | (relate_info_list_for_doc['Field_Name'] == 'CUSIP') | (relate_info_list_for_doc['Field_Name'] == 'Group')];
	for i in range(0 ,len(criteria_id_df_for_identity_info)):
		if criteria_id_df_for_identity_info.iloc[i]['Extraction_Criteria_ID'] not in criteria_id_list_for_identity_info:
			criteria_id_list_for_identity_info.append(criteria_id_df_for_identity_info.iloc[i]['Extraction_Criteria_ID']);

	
	raw_xtr_result_for_identity = raw_xtr_result_for_doc[raw_xtr_result_for_doc['Extraction_Criteria_ID'].isin(criteria_id_list_for_identity_info)];
	element_identity_pairs_list = get_element_identity_pairs_ginniemae(raw_xtr_result_for_identity);




	for item in element_identity_pairs_list:
		print item;
	

	total_field_with_metadata_list = [];
	for i in range(0, len(relate_info_list_for_doc)):

		for element_pair in element_identity_pairs_list:
			# print element_pair;
			current_row_xtr_list = Table_Result_Handler.get_a_row_fields_by_page_row_numbers(raw_xtr_result_for_doc, element_pair[1], element_pair[2]);
			current_cell_metadata = get_a_cell_metadata_ginniemae(current_row_xtr_list, element_pair, relate_info_list_for_doc.iloc[i]);
			# print current_cell_metadata;
			if current_cell_metadata != []:
				total_field_with_metadata_list.append(current_cell_metadata);

	filtered_raw_xtr_list_for_pricingspeed_wals = raw_xtr_result_for_doc[raw_xtr_result_for_doc['Extraction_Criteria_ID'] == 1077];

	organized_preass_info_list = get_organized_info_list_for_pricingspeed_wals(filtered_raw_xtr_list_for_pricingspeed_wals);

	print '';
	print '';
	print 'check length!!!!!!!!!!!!!!!!!        ', len(total_field_with_metadata_list);
	print '';
	print '';

	xtr_to_calcrt_config_map_id_pricing_speed = 0;
	xtr_to_calcrt_config_map_id_wals = 0;
	# sys.exit();
	for i in range(0, len(relate_info_list_for_doc)):			
		if relate_info_list_for_doc.iloc[i]['Field_Name'] == 'Min Purchase':
			for j in range(0, len(element_identity_pairs_list)):
				element_identity_pair = element_identity_pairs_list[j];
				field_value = '100000' if ('NTL' in element_identity_pair[-1]) or ('PO' in element_identity_pair[-1]) or ('IO' in element_identity_pair[-1]) or ('INV' in element_identity_pair[-1]) or ('NSJ' in element_identity_pair[-1])  or ('SPP' in element_identity_pair[-1]) else '1000';
				field_value = 'N/A type Residual' if 'NPR' in element_identity_pair[-1] else field_value;
				freetext_field_with_metadata = [element_identity_pair[0]] +[relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID']] + Textarea_Result_Handler.get_freetext_metadata_by_criteria(relate_info_list_for_doc.iloc[i],raw_xtr_result_for_doc,field_value) + ['Min Purchase'];
				total_field_with_metadata_list.append(freetext_field_with_metadata); 

		if relate_info_list_for_doc.iloc[i]['Field_Name'] == 'Min Increment':
			for j in range(0, len(element_identity_pairs_list)):
				element_identity_pair = element_identity_pairs_list[j];
				field_value = 'N/A type Residual' if 'Residual' in element_identity_pair[6] else '1';
				freetext_field_with_metadata = [element_identity_pair[0]] + [relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID']] + Textarea_Result_Handler.get_freetext_metadata_by_criteria(relate_info_list_for_doc.iloc[i],raw_xtr_result_for_doc,field_value) + ['Min Increment'];
				total_field_with_metadata_list.append(freetext_field_with_metadata); 						
		
		if relate_info_list_for_doc.iloc[i]['Field_Name'] == 'Reset Frequency':
			for j in range(0, len(element_identity_pairs_list)):
				element_identity_pair = element_identity_pairs_list[j];
				field_value = '12.0' if not (('FIX' in element_identity_pair[-1]) or ('NPR' in element_identity_pair[-1])) else 'N/A type FIX or NPR';
				freetext_field_with_metadata = [element_identity_pair[0]] +[relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID']] + Textarea_Result_Handler.get_freetext_metadata_by_criteria(relate_info_list_for_doc.iloc[i],raw_xtr_result_for_doc,field_value) + ['Reset Frequency'];
				total_field_with_metadata_list.append(freetext_field_with_metadata); 							

		if relate_info_list_for_doc.iloc[i]['Field_Name'] == 'Calendar':			
			for j in range(0, len(element_identity_pairs_list)):
				element_identity_pair = element_identity_pairs_list[j];
				freetext_field_with_metadata = [element_identity_pair[0]] +[relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID']] + Textarea_Result_Handler.get_freetext_metadata_by_criteria(relate_info_list_for_doc.iloc[i],raw_xtr_result_for_doc,'US') + ['Calendar'];
				total_field_with_metadata_list.append(freetext_field_with_metadata);	


		if relate_info_list_for_doc.iloc[i]['Field_Name'] == 'Clean Up Call':			
			for j in range(0, len(element_identity_pairs_list)):
				element_identity_pair = element_identity_pairs_list[j];
				freetext_field_with_metadata = [element_identity_pair[0]] +[relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID']] + Textarea_Result_Handler.get_freetext_metadata_by_criteria(relate_info_list_for_doc.iloc[i],raw_xtr_result_for_doc,'1') + ['Clean Up Call'];
				total_field_with_metadata_list.append(freetext_field_with_metadata);					

		if relate_info_list_for_doc.iloc[i]['Field_Name'] == 'Record Date':
			for j in range(0, len(element_identity_pairs_list)):
				element_identity_pair = element_identity_pairs_list[j];
				freetext_field_with_metadata = [element_identity_pair[0]] +[relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID']] + Textarea_Result_Handler.get_freetext_metadata_by_criteria(relate_info_list_for_doc.iloc[i],raw_xtr_result_for_doc,'rd') + ['Record Date'];
				total_field_with_metadata_list.append(freetext_field_with_metadata);				

		if relate_info_list_for_doc.iloc[i]['Field_Name'] in ['Deal Series','Trustee','Sponsor','Co-Sponsor','Closing Date','Payment Date','Pricing Date', 'Deal Size', 'Issue Date', 'Day Count', 'Legal Matters', 'Remic Status', 'Frequency', 'First Reset Date', 'Payment Delay']:
			for j in range(0, len(element_identity_pairs_list)):
				element_identity_pair = element_identity_pairs_list[j];
				for result_obj in Textarea_Result_Handler.get_freetext_metadata_by_criteria(relate_info_list_for_doc.iloc[i],raw_xtr_result_for_doc):
					freetext_field_with_metadata = [element_identity_pair[0]] + [relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID']] + result_obj + [relate_info_list_for_doc.iloc[i]['Field_Name']];	
					total_field_with_metadata_list.append(freetext_field_with_metadata);		
		
		if relate_info_list_for_doc.iloc[i]['Field_Name'] == 'Structuring Ranges':
			filtered_raw_xtr_list = raw_xtr_result_for_doc[raw_xtr_result_for_doc['Extraction_Criteria_ID']==relate_info_list_for_doc.iloc[i]['Extraction_Criteria_ID']];	
			extraction_calcrt_link_id = relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID'];
			if len(filtered_raw_xtr_list) == 0:
				for item in element_identity_pairs_list:
					freetext_field_with_metadata = [item[0]] +[relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID']] + Textarea_Result_Handler.get_freetext_metadata_by_criteria(relate_info_list_for_doc.iloc[i],raw_xtr_result_for_doc,'N/A, no structring ranges info for this series.') + ['Structuring Ranges'];
					total_field_with_metadata_list.append(freetext_field_with_metadata); 	
			else:
				sr_row_number_list = Table_Result_Handler.get_row_number_list_by_keyword(filtered_raw_xtr_list,'through');
				
				for element_identity_pair in element_identity_pairs_list:
					flag = 0;
					for sr_row_number in sr_row_number_list:
						if element_identity_pair[4] in re.sub(r'[^A-Za-z0-9]',' ',Table_Result_Handler.get_cell_field_info_by_page_row_column(filtered_raw_xtr_list, sr_row_number[0], sr_row_number[1],1)['Field_Value']).split(' '):
							page_number = sr_row_number[0];
							pos_min_x = Table_Result_Handler.get_cell_field_info_by_page_row_column(filtered_raw_xtr_list, sr_row_number[0], sr_row_number[1],1)['Pos_Min_X'];
							pos_min_y = Table_Result_Handler.get_cell_field_info_by_page_row_column(filtered_raw_xtr_list, sr_row_number[0], sr_row_number[1],1)['Pos_Min_Y'];
							pos_max_x = Table_Result_Handler.get_cell_field_info_by_page_row_column(filtered_raw_xtr_list, sr_row_number[0], sr_row_number[1],2)['Pos_Max_X'];
							pos_max_y = Table_Result_Handler.get_cell_field_info_by_page_row_column(filtered_raw_xtr_list, sr_row_number[0], sr_row_number[1],2)['Pos_Max_Y'];
							pdf_value = sr_row_number[2];
							font = Table_Result_Handler.get_cell_field_info_by_page_row_column(filtered_raw_xtr_list, sr_row_number[0], sr_row_number[1],2)['Font'];
							field_name = 'Structuring Ranges';
							cell_field_with_metadata = [element_identity_pair[0],extraction_calcrt_link_id, page_number, pos_min_x, pos_min_y, pos_max_x, pos_max_y, pdf_value, font, field_name];
							total_field_with_metadata_list.append(cell_field_with_metadata);
							flag = 1;
							break;
					if flag == 0:
						cell_field_with_metadata = [element_identity_pair[0],extraction_calcrt_link_id, 0, 0, 0, 0, 0, 'N/A, no structring ranges info for this security.', 'Hardcoded', 'Structuring Ranges'];
						total_field_with_metadata_list.append(cell_field_with_metadata);

		if relate_info_list_for_doc.iloc[i]['Field_Name'] == 'Pricing Speed':
			xtr_to_calcrt_config_map_id_pricing_speed = relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID']; 
		if relate_info_list_for_doc.iloc[i]['Field_Name'] == 'WALs':
			xtr_to_calcrt_config_map_id_wals = relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID']; 


	


	float_info_raw_extraction_list = raw_xtr_result_for_doc[(raw_xtr_result_for_doc['Extraction_Criteria_ID']==51) | (raw_xtr_result_for_doc['Extraction_Criteria_ID']==52)];
	float_relate_info_list_for_doc = relate_info_list_for_doc[(relate_info_list_for_doc['Extraction_Criteria_ID'] == 51) | (relate_info_list_for_doc['Extraction_Criteria_ID'] == 52)];


	print 'godbless';
	print len(float_info_raw_extraction_list);
	print len(float_relate_info_list_for_doc);
	print 'godbless';

	float_info_with_metadata_list = get_float_info_for_des_inv_flt_ginnie(element_identity_pairs_list, total_field_with_metadata_list, float_info_raw_extraction_list, float_relate_info_list_for_doc);
	total_field_with_metadata_list = total_field_with_metadata_list + float_info_with_metadata_list;
	

	pricing_speed_wals_metadata_list = get_pricing_speed_wals_for_ginnie(filtered_raw_xtr_list_for_pricingspeed_wals, element_identity_pairs_list, xtr_to_calcrt_config_map_id_pricing_speed, xtr_to_calcrt_config_map_id_wals, organized_preass_info_list);

	total_field_with_metadata_list = total_field_with_metadata_list + pricing_speed_wals_metadata_list;

	"""
		Here we do data normalization for GinnieMae
	"""
	mapped_sponsor_name = '';
	mapped_cosponsor_name = '';
	mapped_trustee_name = '';


	for item in total_field_with_metadata_list:
		if isinstance(item[7],str):
			item[7] = item[7].strip();
		if item[-1] == 'Maturity':
			item[7] = Field_Value_Normalizer.get_date_digits_without_day(item[7]);
			item[7] = item[7] + '-20'
			continue;
		if item[-1] == 'Deal Size':
			item[7] = Field_Value_Normalizer.get_balance_digits(item[7]);	
			continue;
		if item[-1] == 'Descriptors':
			if item[2] > 2:
				item[7] = item[7] + ' EXCH';
			item[7] = Field_Value_Normalizer.get_normalized_descriptors(item[7]);		
			continue;
		if item[-1] == 'Class Coupon':
			item[7] = Field_Value_Normalizer.remove_characters(item[7],[' ','%']);
			if '(' not in item[7]:
				try:
					item[7] = str(round(float(item[7]),6));
				except:
					item[7] = item[7];
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

		if item[-1] == 'Sponsor':
			if mapped_sponsor_name != '':
				item[7] = mapped_sponsor_name;
			else:
				if bool(re.search('Sponsor:', item[7])):
					item[7] = item[7][re.search('Sponsor:', item[7]).end():];
					if bool(re.search('Co-Sponsor:', item[7])):
						item[7] = item[7][:re.search('Co-Sponsor:', item[7]).start()];
					item[7] = Field_Value_Normalizer.get_mapped_abbreviation_for_sponsor_gm(item[7]);
					mapped_sponsor_name = item[7];
			continue;	

		if item[-1] == 'Co-Sponsor':
			if mapped_cosponsor_name != '':
				item[7] = mapped_cosponsor_name;
			else:
				if bool(re.search('Co-Sponsor:', item[7])):
					item[7] = item[7][re.search('Co-Sponsor:', item[7]).end():];
					if bool(re.search('Trustee:', item[7])):
						item[7] = item[7][:re.search('Trustee:', item[7]).start()];
					item[7] = Field_Value_Normalizer.get_mapped_abbreviation_for_sponsor_gm(item[7]);
					mapped_cosponsor_name = item[7];
			continue;	

		if item[-1] == 'Trustee':
			if mapped_trustee_name != '':
				item[7] = mapped_trustee_name;

			if bool(re.search('Trustee:', item[7])):
				item[7] = item[7][re.search('Trustee:', item[7]).end():];
				if bool(re.search('Tax', item[7])):
					item[7] = item[7][:re.search('Tax', item[7]).start()];
				item[7] = Field_Value_Normalizer.get_mapped_abbreviation_for_trustee_gm(item[7])
			continue;
		if item[-1] == 'Day Count':
			item[7] = Field_Value_Normalizer.get_day_count(item[7]);
			continue;
		if item[-1] == 'Deal Series':
			item[7] = Field_Value_Normalizer.remove_subregex(item[7], 'Ginnie Mae REMIC Trust');
			item[7] = 'GNR ' + item[7].strip();	
			item[7] = Field_Value_Normalizer.get_deal_series(item[7]);	
			continue;
		if item[-1] == 'Floater Index':
			item[7] = Field_Value_Normalizer.get_floater_index(item[7]);
			continue;	
		if item[-1] == 'Class Balance':
			item[7] = Field_Value_Normalizer.remove_characters(item[7],[' ','\.','\,','\$']);
			continue;
		if item[-1] == 'Frequency':
			item[7] = '12';	
			continue;	
		if item[-1] == 'Reset Frequency':
			item[7] = Field_Value_Normalizer.get_reset_frequency(item[7],'');
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
		if item[-1] == 'Pricing Date' or item[-1] == 'Closing Date':
			item[7] = Field_Value_Normalizer.get_date_digits_for_gm(item[7]);
			item[7] = Field_Value_Normalizer.get_date_digits(item[7]);
			continue;
		if item[-1] == 'Payment Date' or item[-1] == 'First Reset Date':
			item[7]	= item[7][re.search('Distribution Date',item[7]).end()+1:];
			item[7] = item[7][:-13];
			continue;
		if item[-1] == 'Record Date':
			item[7] = str(Field_Value_Normalizer.get_last_business_day(20));
			continue;
		if item[-1] == 'Slope':
			if 'N/A' not in str(item[7]) and '.' not in str(item[7]):
				item[7] = str(item[7])+".0";

			elif item[7][-1] == '0' and item[7][-2] != '.':
				item[7] = item[7][:-1];
			continue;	

	for item in total_field_with_metadata_list:	
		if item[7] is None:
			item[7] = 'N/A, Extraction Error. Please check the document.';	
			continue;
		if len(re.sub(' ','',item[7])) == 0:
			item[7] = 'N/A, Extraction Error. Please check the document.';	
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


def get_a_cell_metadata_ginniemae(row_xtr_list, element_identity_pair_info, relate_info_list_for_doc_item):
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


	if relate_info_list_for_doc_item['Extraction_Criteria_ID'] == 22:
		if target_page_number > 3:
			return [];
		else:
			if field_name == 'Maturity':
				target_column_index = target_column_index + 1;
				extracted_value = '';
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
				extracted_value = element_identity_pair_info[5];
				font = current_cell_metadata['Font'];
				return [element_identity_pair_info[0], xtr_to_calcrt_config_map_id, page_number, pos_min_x, pos_min_y, pos_max_x, pos_max_y, extracted_value, font, field_name];
			if field_name == 'Class Coupon':
				target_column_index = target_column_index - 3;
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
				target_column_index = element_identity_pair_info[3] - 2;
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

	if relate_info_list_for_doc_item['Extraction_Criteria_ID'] == 25:
		if target_page_number <= 3:
			return [];
		else:
			if field_name == 'Maturity':
				target_column_index = target_column_index + 1;
				extracted_value = '';
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
				extracted_value = element_identity_pair_info[5];
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
				extracted_value = element_identity_pair_info[7];
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
	
	return [];
	


def get_element_identity_pairs_ginniemae(xtr_fields_list):
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

		if item[0] < 3:
			descriptors_info = Table_Result_Handler.get_cell_field_info_by_page_row_column(xtr_fields_list,item[0],item[1],item[2]-1)['Field_Value'];
			shift_flag = 0;

			if descriptors_info is None or descriptors_info == 'I)' or descriptors_info == 'II)':
				descriptors_info = Table_Result_Handler.get_cell_field_info_by_page_row_column(xtr_fields_list,item[0],item[1],item[2]-2)['Field_Value'];
				shift_flag = 1;
			descriptors_info_2nd = Table_Result_Handler.get_cell_field_info_by_page_row_column(xtr_fields_list,item[0],item[1],item[2]-2)['Field_Value'];
			if descriptors_info_2nd is None or descriptors_info_2nd == 'I)' or descriptors_info_2nd == 'II)':
				descriptors_info_2nd = Table_Result_Handler.get_cell_field_info_by_page_row_column(xtr_fields_list,item[0],item[1],item[2]-3)['Field_Value'];	
				shift_flag = 1;
			descriptors_info = descriptors_info + '|' + descriptors_info_2nd;
		else:
			descriptors_info = Table_Result_Handler.get_cell_field_info_by_page_row_column(xtr_fields_list,item[0],item[1],item[2]-1)['Field_Value'];
			shift_flag = 0;

			if descriptors_info is None or re.sub(' ','',descriptors_info) == 'I)' or re.sub(' ','',descriptors_info) == 'II)':
				descriptors_info = Table_Result_Handler.get_cell_field_info_by_page_row_column(xtr_fields_list,item[0],item[1],item[2]-2)['Field_Value'];
				shift_flag = 1;
			descriptors_info_2nd = Table_Result_Handler.get_cell_field_info_by_page_row_column(xtr_fields_list,item[0],item[1],item[2]-3)['Field_Value'];
			if descriptors_info_2nd is None or re.sub(' ','',descriptors_info_2nd) == 'I)' or re.sub(' ','',descriptors_info_2nd) == 'II)':
				descriptors_info_2nd = Table_Result_Handler.get_cell_field_info_by_page_row_column(xtr_fields_list,item[0],item[1],item[2]-4)['Field_Value'];	
				shift_flag = 1;
			descriptors_info = descriptors_info + '|' + descriptors_info_2nd;


		group_info = 'Residual' if 'NPR' in descriptors_info else '0';

		if shift_flag == 0:
			class_info = Table_Result_Handler.get_cell_field_info_by_page_row_column(xtr_fields_list,item[0],item[1],item[2]-5)['Field_Value'];
		else:
			class_info = Table_Result_Handler.get_cell_field_info_by_page_row_column(xtr_fields_list,item[0],item[1],item[2]-6)['Field_Value'];
	

		class_info = Field_Value_Normalizer.remove_characters(class_info,[' ','\.',r'\(\d\)']);	

		element_identity_pairs_list.append([cusip_index]+item+[class_info, cusip_info, group_info, descriptors_info]);
		cusip_index += 1;

	
	return element_identity_pairs_list;





def get_float_info_for_des_inv_flt_ginnie(element_identity_pairs_list, total_field_with_metadata_list, float_info_raw_extraction_list, float_relate_info_list_for_doc):
	float_info_with_metadata_fix_npr = [];
	float_info_with_metadata_inv_flt = [];
	identity_pairs_list_for_inv_flt = [];
	
	
	# [47, 22, 30, 428.51499999999999, 211.214, 587.41819999999996, 220.142, 'FIX/IO| NTL(SEQ)', 'DMLJBJ+Times-Roman', 'Descriptors']
	# [index, link_id, page_number, x,y,x,y, pdf_value, font, field_name]

	identity_pairs_list_with_descriptor = Public_Processor.get_identity_pairs_with_descriptor(element_identity_pairs_list, total_field_with_metadata_list);

	special_interest_rate_list = [];

	for i in range(0, len(float_relate_info_list_for_doc)):
		extraction_calcrt_link_id = float_relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID'];
		field_name = float_relate_info_list_for_doc.iloc[i]['Field_Name'];
		if field_name == 'SubRates':
			continue;

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

	# for item in identity_pairs_list_for_inv_flt:
	# 	print item;

	if identity_pairs_list_for_inv_flt !=[]:
		approximate_initial_list = float_info_raw_extraction_list[float_info_raw_extraction_list['Extraction_Criteria_ID']==52];
		print 'nimahi';
		if len(approximate_initial_list) > 0:
			for item in Table_Result_Handler.get_row_number_list_by_regex(approximate_initial_list,r'^[A-Z]{1,2}[\.]{0,}$'):
				current_row_xtr_list = Table_Result_Handler.get_a_row_fields_by_page_row_numbers(approximate_initial_list,item[0],item[1]);
				# print item, Table_Result_Handler.get_cell_field_info_by_page_row_column(current_row_xtr_list,item[0],item[1],1,reverse_order=1)['Field_Value'];
				if bool(re.search(r'[0-9]{1,}[\.]{1}[0-9]{1,}[\%]{0,1}',Table_Result_Handler.get_cell_field_info_by_page_row_column(current_row_xtr_list,item[0],item[1],1,reverse_order=1)['Field_Value'])):
					special_interest_rate_list.append([Field_Value_Normalizer.remove_characters(item[2][:3],[' ','\.']), Table_Result_Handler.get_cell_field_info_by_page_row_column(current_row_xtr_list,item[0],item[1],1,reverse_order=1)['Field_Value']])



		formula_rates_list = float_info_raw_extraction_list[float_info_raw_extraction_list['Extraction_Criteria_ID']==51];
		print 'caonima';
		if len(formula_rates_list) > 0:
			for item in Table_Result_Handler.get_row_number_list_by_regex(formula_rates_list,r'^[A-Z]{1,2}[\.]{0,}$'):
				current_row_xtr_list = Table_Result_Handler.get_a_row_fields_by_page_row_numbers(formula_rates_list,item[0],item[1]);
				special_interest_rate_list.append([Field_Value_Normalizer.remove_characters(item[2][:3],[' ','\.']), Table_Result_Handler.get_cell_field_info_by_page_row_column(current_row_xtr_list,item[0],item[1],5,reverse_order=1)['Field_Value']])

	print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~';
	print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~';

	# for item in special_interest_rate_list:
	# 	print item;

	for item in [resultitem for resultitem in total_field_with_metadata_list if resultitem[-1]=='Class Coupon' and '(' in resultitem[7]]:
		# print item[7], element_identity_pairs_list[item[0]-1][4];
		if [special_interest_rate[1] for special_interest_rate in special_interest_rate_list if element_identity_pairs_list[item[0]-1][4] == special_interest_rate[0]]!=[]: 
		 	item[7] = [special_interest_rate[1] for special_interest_rate in special_interest_rate_list if element_identity_pairs_list[item[0]-1][4] == special_interest_rate[0]][0];
		# print '^^^^^^^^^^^^^^^^^^^^^^^^^^^^',item[7];

	for i in range(0, len(float_relate_info_list_for_doc)):
		field_name = float_relate_info_list_for_doc.iloc[i]['Field_Name'];				
		extraction_calcrt_link_id = float_relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID'];
		if field_name == 'Slope':
			for identity_pair_class in identity_pairs_list_for_inv_flt:
				# print identity_pair_class;				
				field_value = -1 if 'INV' in identity_pair_class[-1] else 1;
				field_value = field_value if ('FLT' in identity_pair_class[-1]) or ('INV' in identity_pair_class[-1]) else 'N/A, not FLT or INV'; 
				descriptors_metadata = [descriptors_metadata_obj[2] for descriptors_metadata_obj in identity_pairs_list_with_descriptor if descriptors_metadata_obj[0] == identity_pair_class[0]][0];
				info_with_metadata_obj = [identity_pair_class[0],extraction_calcrt_link_id] + descriptors_metadata[2:7] + [field_value,'Hardcoded',field_name];
				float_info_with_metadata_inv_flt.append(info_with_metadata_obj);
				continue;
		if field_name == 'Floater Index':
			for identity_pair_class in identity_pairs_list_for_inv_flt:

				page_row_info = [element_identity_pair for element_identity_pair in element_identity_pairs_list if element_identity_pair[0]==identity_pair_class[0]][0];
				class_info = page_row_info[4];
				row_number = Table_Result_Handler.get_row_number_list_by_keyword(float_info_raw_extraction_list, class_info, 1);
				if 'FLT' in identity_pair_class[1] or 'INV' in identity_pair_class[1]:
					row_xtr_list = Table_Result_Handler.get_a_row_fields_by_page_row_numbers(float_info_raw_extraction_list,row_number[0][0], row_number[0][1]);
					cell_number = Table_Result_Handler.get_column_number_in_row_by_regex(row_xtr_list,'LIBOR');
					field_value = Table_Result_Handler.get_cell_field_info_by_page_row_column(row_xtr_list,row_number[0][0], row_number[0][1],cell_number[2])['Field_Value'];
					if 'LIBOR' in field_value.upper():
						if re.search('LIBOR',field_value.upper()).start() > 1 and field_value[re.search('LIBOR',field_value.upper()).start()-1]==' ':
							field_value = field_value[0:re.search('LIBOR',field_value.upper()).start()-1] + field_value[re.search('LIBOR',field_value.upper()).start():];
					
					current_result_cell_obj = Table_Result_Handler.get_cell_field_info_by_page_row_column(row_xtr_list,row_number[0][0], row_number[0][1],cell_number[2]);
					page_number = current_result_cell_obj['Page_Number'];
					pos_min_x = current_result_cell_obj['Pos_Min_X'];
					pos_min_y = current_result_cell_obj['Pos_Min_Y'];
					pos_max_x = current_result_cell_obj['Pos_Max_X'];
					pos_max_y = current_result_cell_obj['Pos_Max_Y'];
					font = current_result_cell_obj['Font'];
					cell_field_with_metadata = [identity_pair_class[0],extraction_calcrt_link_id,page_number, pos_min_x, pos_min_y, pos_max_x, pos_max_y, field_value, font, 'Floater Index'];
					float_info_with_metadata_inv_flt.append(cell_field_with_metadata);	

				else:
					field_value = 'N/A, not FLT or INV';
					descriptors_metadata = [descriptors_metadata_obj[2] for descriptors_metadata_obj in identity_pairs_list_with_descriptor if descriptors_metadata_obj[0] == identity_pair_class[0]][0];
					info_with_metadata_obj = [identity_pair_class[0],extraction_calcrt_link_id] + descriptors_metadata[2:7] + [field_value,'Hardcoded','Floater Index'];
					float_info_with_metadata_inv_flt.append(info_with_metadata_obj);

		if field_name == 'Floater Spread':
			for identity_pair_class in identity_pairs_list_for_inv_flt:
				page_row_info = [element_identity_pair for element_identity_pair in element_identity_pairs_list if element_identity_pair[0]==identity_pair_class[0]][0];
				class_info = page_row_info[4];
				row_number = Table_Result_Handler.get_row_number_list_by_keyword(float_info_raw_extraction_list, class_info, 1);

				if 'FLT' in identity_pair_class[1] or 'INV' in identity_pair_class[1]:
					row_xtr_list = Table_Result_Handler.get_a_row_fields_by_page_row_numbers(float_info_raw_extraction_list,row_number[0][0], row_number[0][1]);
					field_value = Table_Result_Handler.get_cell_field_info_by_page_row_column(row_xtr_list,row_number[0][0], row_number[0][1],2)['Field_Value'];
					current_result_cell_obj = Table_Result_Handler.get_cell_field_info_by_page_row_column(row_xtr_list,row_number[0][0], row_number[0][1],2);
					page_number = current_result_cell_obj['Page_Number'];
					pos_min_x = current_result_cell_obj['Pos_Min_X'];
					pos_min_y = current_result_cell_obj['Pos_Min_Y'];
					pos_max_x = current_result_cell_obj['Pos_Max_X'];
					pos_max_y = current_result_cell_obj['Pos_Max_Y'];
					font = current_result_cell_obj['Font'];
					cell_field_with_metadata = [identity_pair_class[0],extraction_calcrt_link_id,page_number, pos_min_x, pos_min_y, pos_max_x, pos_max_y, field_value, font, 'Floater Spread'];
					float_info_with_metadata_inv_flt.append(cell_field_with_metadata);	

				else:
					field_value = 'N/A, not FLT or INV';
					descriptors_metadata = [descriptors_metadata_obj[2] for descriptors_metadata_obj in identity_pairs_list_with_descriptor if descriptors_metadata_obj[0] == identity_pair_class[0]][0];
					info_with_metadata_obj = [identity_pair_class[0],extraction_calcrt_link_id] + descriptors_metadata[2:7] + [field_value,'Hardcoded','Floater Spread'];
					float_info_with_metadata_inv_flt.append(info_with_metadata_obj);

		if field_name == 'Floor':
			for identity_pair_class in identity_pairs_list_for_inv_flt:
				page_row_info = [element_identity_pair for element_identity_pair in element_identity_pairs_list if element_identity_pair[0]==identity_pair_class[0]][0];
				class_info = page_row_info[4];
				row_number = Table_Result_Handler.get_row_number_list_by_keyword(float_info_raw_extraction_list, class_info, 1);
				if 'FLT' in identity_pair_class[1] or 'INV' in identity_pair_class[1]:
					row_xtr_list = Table_Result_Handler.get_a_row_fields_by_page_row_numbers(float_info_raw_extraction_list,row_number[0][0], row_number[0][1]);
					field_value = Table_Result_Handler.get_cell_field_info_by_page_row_column(row_xtr_list,row_number[0][0], row_number[0][1],4, reverse_order=1)['Field_Value'];
					current_result_cell_obj = Table_Result_Handler.get_cell_field_info_by_page_row_column(row_xtr_list,row_number[0][0], row_number[0][1],4, reverse_order=1);
					page_number = current_result_cell_obj['Page_Number'];
					pos_min_x = current_result_cell_obj['Pos_Min_X'];
					pos_min_y = current_result_cell_obj['Pos_Min_Y'];
					pos_max_x = current_result_cell_obj['Pos_Max_X'];
					pos_max_y = current_result_cell_obj['Pos_Max_Y'];
					font = current_result_cell_obj['Font'];
					cell_field_with_metadata = [identity_pair_class[0],extraction_calcrt_link_id,page_number, pos_min_x, pos_min_y, pos_max_x, pos_max_y, field_value, font, 'Floor'];
					float_info_with_metadata_inv_flt.append(cell_field_with_metadata);	

				else:
					field_value = 'N/A, not FLT or INV';
					descriptors_metadata = [descriptors_metadata_obj[2] for descriptors_metadata_obj in identity_pairs_list_with_descriptor if descriptors_metadata_obj[0] == identity_pair_class[0]][0];
					info_with_metadata_obj = [identity_pair_class[0],extraction_calcrt_link_id] + descriptors_metadata[2:7] + [field_value,'Hardcoded','Floor'];
					float_info_with_metadata_inv_flt.append(info_with_metadata_obj);


		if field_name == 'Ceiling':
			for identity_pair_class in identity_pairs_list_for_inv_flt:
				page_row_info = [element_identity_pair for element_identity_pair in element_identity_pairs_list if element_identity_pair[0]==identity_pair_class[0]][0];
				class_info = page_row_info[4];
				row_number = Table_Result_Handler.get_row_number_list_by_keyword(float_info_raw_extraction_list, class_info, 1);
				if 'FLT' in identity_pair_class[1] or 'INV' in identity_pair_class[1]:
					row_xtr_list = Table_Result_Handler.get_a_row_fields_by_page_row_numbers(float_info_raw_extraction_list,row_number[0][0], row_number[0][1]);
					field_value = Table_Result_Handler.get_cell_field_info_by_page_row_column(row_xtr_list,row_number[0][0], row_number[0][1],3, reverse_order=1)['Field_Value'];
					current_result_cell_obj = Table_Result_Handler.get_cell_field_info_by_page_row_column(row_xtr_list,row_number[0][0], row_number[0][1],3, reverse_order=1);
					page_number = current_result_cell_obj['Page_Number'];
					pos_min_x = current_result_cell_obj['Pos_Min_X'];
					pos_min_y = current_result_cell_obj['Pos_Min_Y'];
					pos_max_x = current_result_cell_obj['Pos_Max_X'];
					pos_max_y = current_result_cell_obj['Pos_Max_Y'];
					font = current_result_cell_obj['Font'];
					cell_field_with_metadata = [identity_pair_class[0],extraction_calcrt_link_id,page_number, pos_min_x, pos_min_y, pos_max_x, pos_max_y, field_value, font, 'Ceiling'];
					float_info_with_metadata_inv_flt.append(cell_field_with_metadata);	

				else:
					field_value = 'N/A, not FLT or INV';
					descriptors_metadata = [descriptors_metadata_obj[2] for descriptors_metadata_obj in identity_pairs_list_with_descriptor if descriptors_metadata_obj[0] == identity_pair_class[0]][0];
					info_with_metadata_obj = [identity_pair_class[0],extraction_calcrt_link_id] + descriptors_metadata[2:7] + [field_value,'Hardcoded','Ceiling'];
					float_info_with_metadata_inv_flt.append(info_with_metadata_obj);









	float_info_with_metadata_list = float_info_with_metadata_fix_npr + float_info_with_metadata_inv_flt;

	return float_info_with_metadata_list;



def get_organized_info_list_for_pricingspeed_wals(filtered_raw_xtr_list_for_pricingspeed_wals):
	# for i in range(0, len(filtered_raw_xtr_list_for_pricingspeed_wals)):
	# 	print filtered_raw_xtr_list_for_pricingspeed_wals.iloc[i]['Field_Value'];
	prepayass_row_list = Table_Result_Handler.get_row_number_list_by_keyword(filtered_raw_xtr_list_for_pricingspeed_wals,'Prepayment',1);
	pricing_speed_row_list = Table_Result_Handler.get_row_number_list_by_keyword(filtered_raw_xtr_list_for_pricingspeed_wals,'Distribution',1);
	wals_row_list = Table_Result_Handler.get_row_number_list_by_keyword(filtered_raw_xtr_list_for_pricingspeed_wals,'Life',1);

	total_row_number_list = [prepayass_row_list, pricing_speed_row_list, wals_row_list];

	total_info_pairs_row_number_list = zip(*total_row_number_list);

	final_total_info_pairs_row_number_list = [];

	for item in total_info_pairs_row_number_list:


		target_page_row_number = [item[0][0],item[0][1]+1]
		target_class_info_xtr_row_list = Table_Result_Handler.get_a_row_fields_by_page_row_numbers(filtered_raw_xtr_list_for_pricingspeed_wals, target_page_row_number[0], target_page_row_number[1]);
		number_of_class_subtables = Table_Result_Handler.get_number_of_match_keyword_in_a_row(target_class_info_xtr_row_list, 'Class');
		class_info_with_index = [];
		record_class_index = 1;
		for class_index in range(0, len(target_class_info_xtr_row_list)):
			if target_class_info_xtr_row_list.iloc[class_index]['Field_Value'] is not None and re.sub(' ','',target_class_info_xtr_row_list.iloc[class_index]['Field_Value']) != '':
				class_list = re.sub(r' +', ' ', re.sub(',',' ',re.sub('and',' ',re.sub('Class', '', re.sub('Classes', '', target_class_info_xtr_row_list.iloc[class_index]['Field_Value']))))).split(' ');
				class_info_with_index.append([[class_name for class_name in class_list if class_name != ''], record_class_index]);
				record_class_index += 1;


		final_total_info_pairs_row_number_list.append([item, class_info_with_index]);		


	# for item in final_total_info_pairs_row_number_list:
	# 	print '-------------------------------';
	# 	for i in range(0, len(item)):
	# 		subitem = item[i];
	# 		print subitem;	
	# 	print '-------------------------------';

	return final_total_info_pairs_row_number_list;





def get_pricing_speed_wals_for_ginnie(filtered_raw_xtr_list, element_identity_pairs_list,  xtr_to_calcrt_config_map_id_pricing_speed, xtr_to_calcrt_config_map_id_wals , final_total_info_pairs_row_number_list):
	pricing_speed_wals_metadata_list = [];

	current_page_number = filtered_raw_xtr_list.iloc[0]['Page_Number'];
	for element in element_identity_pairs_list:
		flag = 0;
		if element[-2] == 'Residual':
			
			continue;

		for final_preass_info in final_total_info_pairs_row_number_list:
			for class_info in final_preass_info[1]:

				if element[4] in class_info[0]:
					try:
						# print class_info;
						prepayment_info = Table_Result_Handler.get_cell_field_info_by_page_row_column(filtered_raw_xtr_list, final_preass_info[0][0][0], final_preass_info[0][0][1],1)['Field_Value'];
						prepayment_info = prepayment_info[re.search('Prepayment',prepayment_info).start()-3:re.search('Prepayment',prepayment_info).start()];
						# print prepayment_info;

						class_info_index = class_info[1];

						pricing_speed_xtr_row_list = Table_Result_Handler.get_a_row_fields_by_page_row_numbers(filtered_raw_xtr_list, final_preass_info[0][1][0], final_preass_info[0][1][1]);
						
						current_zero_count = 0;

						pricing_speed_set_list = [];
						temp_pricing_speed_set_list = [];

						for i in range(1, len(pricing_speed_xtr_row_list)):
							cell_string = pricing_speed_xtr_row_list.iloc[i]['Field_Value'];
							if i == 1:
								current_zero_count += 1;
								temp_pricing_speed_set_list.append(pricing_speed_xtr_row_list.iloc[i]);
								continue;

							if '0%' == cell_string.strip():
								pricing_speed_set_list.append([temp_pricing_speed_set_list, current_zero_count]);
								temp_pricing_speed_set_list = [pricing_speed_xtr_row_list.iloc[i]];
								current_zero_count += 1;
							else:
								temp_pricing_speed_set_list.append(pricing_speed_xtr_row_list.iloc[i]);

						pricing_speed_set_list.append([temp_pricing_speed_set_list,current_zero_count]);		

						# print '^^^^^^^^^^^                      ',class_info_index;

						# print zip(*pricing_speed_set_list)[1];

						length = len([item[0] for item in pricing_speed_set_list if item[1] == class_info_index][0]);

						target_index = (length+1)/2;
						

						pricing_cell = [item[0] for item in pricing_speed_set_list if item[1] == class_info_index][0][target_index-1];
						
						column_number = [item[0] for item in pricing_speed_set_list if item[1] == class_info_index][0][target_index-1]['Table_Column_Number'];
						
						wals_cell = Table_Result_Handler.get_cell_field_info_by_page_row_column(filtered_raw_xtr_list, final_preass_info[0][2][0], final_preass_info[0][2][1],column_number);
		

						pricing_speed_wals_metadata_list.append([element[0], xtr_to_calcrt_config_map_id_pricing_speed, pricing_cell['Page_Number'], pricing_cell['Pos_Min_X'], pricing_cell['Pos_Min_Y'], pricing_cell['Pos_Max_X'], pricing_cell['Pos_Max_Y'], pricing_cell['Field_Value'] + ' '+ prepayment_info, pricing_cell['Font'], 'Pricing Speed']);
						pricing_speed_wals_metadata_list.append([element[0], xtr_to_calcrt_config_map_id_wals, wals_cell['Page_Number'], wals_cell['Pos_Min_X'], wals_cell['Pos_Min_Y'], wals_cell['Pos_Max_X'], wals_cell['Pos_Max_Y'], wals_cell['Field_Value'], wals_cell['Font'], 'WALs']);
						current_page_number = wals_cell['Page_Number'];
						flag = 1;
					except:
						print 'Something wrong with Pricing Speed or Wals for class ', element;
		if flag == 0:
			pricing_speed_wals_metadata_list.append([element[0], xtr_to_calcrt_config_map_id_pricing_speed, current_page_number,0,0,0,0, 'Extraction Error. Please check the document and OID section.', '', 'Pricing Speed']);
			pricing_speed_wals_metadata_list.append([element[0], xtr_to_calcrt_config_map_id_wals, current_page_number, 0,0,0,0, 'Extraction Error. Please check the document and OID section.','', 'WALs']);
								
	return pricing_speed_wals_metadata_list;
