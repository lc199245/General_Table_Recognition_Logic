import Field_Value_Normalizer;
import Table_Result_Handler;
import Textarea_Result_Handler;
import Public_Processor;



import re;
import pandas;
import sys;







def customized_per_doc_process_for_fanniemae(relate_info_list_for_doc, raw_xtr_result_for_doc):
	print '----------------------------------';
	print 'Length of related xtr results list: ',len(raw_xtr_result_for_doc);
	criteria_id_list_for_identity_info = [];
	criteria_id_df_for_identity_info = relate_info_list_for_doc[(relate_info_list_for_doc['Field_Name'] == 'Tranche') | (relate_info_list_for_doc['Field_Name'] == 'CUSIP') | (relate_info_list_for_doc['Field_Name'] == 'Group')];
	for i in range(0 ,len(criteria_id_df_for_identity_info)):
		if criteria_id_df_for_identity_info.iloc[i]['Extraction_Criteria_ID'] not in criteria_id_list_for_identity_info:
			criteria_id_list_for_identity_info.append(criteria_id_df_for_identity_info.iloc[i]['Extraction_Criteria_ID']);

	raw_xtr_result_for_identity = raw_xtr_result_for_doc[raw_xtr_result_for_doc['Extraction_Criteria_ID'].isin(criteria_id_list_for_identity_info)];
	element_identity_pairs_list = [];
	element_identity_pairs_list = get_element_identity_pairs_fanniemae(raw_xtr_result_for_identity);			
	
	for element_identity_pair in element_identity_pairs_list:
		print element_identity_pair;
	

	print '                                                     ',len(element_identity_pairs_list);
	
	total_field_with_metadata_list = [];



	for i in range(0, len(relate_info_list_for_doc)):

		for element_pair in element_identity_pairs_list:
			# print element_pair;
			current_row_xtr_list = Table_Result_Handler.get_a_row_fields_by_page_row_numbers(raw_xtr_result_for_doc, element_pair[1], element_pair[2]);
			current_cell_metadata = get_a_cell_metadata_Fanniemae(current_row_xtr_list, element_pair, relate_info_list_for_doc.iloc[i]);
			# print current_cell_metadata;
			if current_cell_metadata != []:
				total_field_with_metadata_list.append(current_cell_metadata);

	print '';
	print '';
	print 'check length!!!!!!!!!!!!!!!!!        ', len(total_field_with_metadata_list);
	print '';
	print '';

	xtr_to_calcrt_config_map_id_pricing_speed = 0;
	xtr_to_calcrt_config_map_id_wals = 0;


	for i in range(0, len(relate_info_list_for_doc)):
		if relate_info_list_for_doc.iloc[i]['Field_Name'] == 'Pricing Speed':
			xtr_to_calcrt_config_map_id_pricing_speed = relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID'];
			continue;


		if relate_info_list_for_doc.iloc[i]['Field_Name'] == 'WALs':
			xtr_to_calcrt_config_map_id_wals = relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID'];
			continue;


		if relate_info_list_for_doc.iloc[i]['Field_Name'] == 'Reset Frequency':
			for j in range(0, len(element_identity_pairs_list)):
				element_identity_pair = element_identity_pairs_list[j];
				field_value = '12.0' if not (('FIX' in element_identity_pair[-1]) or ('NPR' in element_identity_pair[-1])) else 'N/A type FIX or NPR';
				freetext_field_with_metadata = [element_identity_pair[0]] +[relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID']] + Textarea_Result_Handler.get_freetext_metadata_by_criteria(relate_info_list_for_doc.iloc[i],raw_xtr_result_for_doc,field_value) + ['Reset Frequency'];
				total_field_with_metadata_list.append(freetext_field_with_metadata); 	

		if relate_info_list_for_doc.iloc[i]['Field_Name'] == 'Calendar':
			for item in element_identity_pairs_list:
				cell_field_with_metadata = [item[0],relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID'],0, 0, 0, 0, 0, "US", "Hardcoded", relate_info_list_for_doc.iloc[i]['Field_Name']];
				total_field_with_metadata_list.append(cell_field_with_metadata);	
			continue;

		if relate_info_list_for_doc.iloc[i]['Field_Name'] == 'Clean Up Call':
			for item in element_identity_pairs_list:
				cell_field_with_metadata = [item[0],relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID'],0, 0, 0, 0, 0, "N/A", "Hardcoded", relate_info_list_for_doc.iloc[i]['Field_Name']];
				total_field_with_metadata_list.append(cell_field_with_metadata);	
			continue;
		if relate_info_list_for_doc.iloc[i]['Field_Name'] == 'Trustee':
			for item in element_identity_pairs_list:
				cell_field_with_metadata = [item[0],relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID'],0, 0, 0, 0, 0, "FNM", "Hardcoded", relate_info_list_for_doc.iloc[i]['Field_Name']];
				total_field_with_metadata_list.append(cell_field_with_metadata);	
			continue;
		if relate_info_list_for_doc.iloc[i]['Field_Name'] == 'Day Count':
			for item in element_identity_pairs_list:
				cell_field_with_metadata = [item[0],relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID'],0, 0, 0, 0, 0, "104", "Hardcoded", relate_info_list_for_doc.iloc[i]['Field_Name']];
				total_field_with_metadata_list.append(cell_field_with_metadata);	
			continue;

		if relate_info_list_for_doc.iloc[i]['Field_Name'] == 'Remic Status':
			for item in element_identity_pairs_list:
				cell_field_with_metadata = [item[0],relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID'],0, 0, 0, 0, 0, "Y", "Hardcoded", relate_info_list_for_doc.iloc[i]['Field_Name']];
				total_field_with_metadata_list.append(cell_field_with_metadata);	
			continue;

		if relate_info_list_for_doc.iloc[i]['Field_Name'] == 'Min Increment':
			for j in range(0, len(element_identity_pairs_list)):
				element_identity_pair = element_identity_pairs_list[j];
				field_value = 'N/A type Residual' if ('R' in element_identity_pair[7]) or ('RR' in element_identity_pair[7]) else '1';
				freetext_field_with_metadata = [element_identity_pair[0]] + [relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID']] + Textarea_Result_Handler.get_freetext_metadata_by_criteria(relate_info_list_for_doc.iloc[i],raw_xtr_result_for_doc,field_value) + ['Min Increment'];
				total_field_with_metadata_list.append(freetext_field_with_metadata); 
			continue;

		if relate_info_list_for_doc.iloc[i]['Field_Name'] == 'Min Purchase':
			element_identity_pairs_list_with_descriptor = Public_Processor.get_identity_pairs_with_descriptor(element_identity_pairs_list, total_field_with_metadata_list);
			for j in range(0, len(element_identity_pairs_list_with_descriptor)):
				element_identity_pair = element_identity_pairs_list_with_descriptor[j];
				field_value = '100000' if ('NTL' in element_identity_pair[1]) or ('IO' in element_identity_pair[1]) or ('INV' in element_identity_pair[1]) or ('NSJ' in element_identity_pair[1])  or ('SPP' in element_identity_pair[1]) else '1000';
				field_value = 'N/A type Residual' if 'NPR' in element_identity_pair[1] else field_value;
				freetext_field_with_metadata = [element_identity_pair[0]] +[relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID']] + Textarea_Result_Handler.get_freetext_metadata_by_criteria(relate_info_list_for_doc.iloc[i],raw_xtr_result_for_doc,field_value) + ['Min Purchase'];
				total_field_with_metadata_list.append(freetext_field_with_metadata); 
			continue;				

		if relate_info_list_for_doc.iloc[i]['Field_Name'] == 'Structuring Ranges':
			for j in range(0, len(element_identity_pairs_list)):
				element_identity_pair = element_identity_pairs_list[j];

				textarea_meta_list = Textarea_Result_Handler.get_freetext_metadata_by_criteria(relate_info_list_for_doc.iloc[i],raw_xtr_result_for_doc);

				if 'NPR' in element_identity_pair[-1]:
					freetext_field_with_metadata = [element_identity_pair[0]] + [relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID']] + [0,0,0,0,0,'N/A, type Residual.',''] + ['Structuring Ranges'];
					total_field_with_metadata_list.append(freetext_field_with_metadata); 	
				
				if textarea_meta_list == []:
					freetext_field_with_metadata = [element_identity_pair[0]] + [relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID']] + [0,0,0,0,0,'N/A, no Structuring Ranges paragraph found from this document.',''] + ['Structuring Ranges'];
					total_field_with_metadata_list.append(freetext_field_with_metadata); 
				else:
					for result_obj in textarea_meta_list:
						freetext_field_with_metadata = [element_identity_pair[0]] + [relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID']] + result_obj[:-2] + ['N/A, complex paragraph for Fannie. Please check the highlight','']  + [relate_info_list_for_doc.iloc[i]['Field_Name']];	
						total_field_with_metadata_list.append(freetext_field_with_metadata);
			continue;
		if relate_info_list_for_doc.iloc[i]['Field_Name'] == 'First Reset Date':
			for j in range(0, len(element_identity_pairs_list)):
				element_identity_pair = element_identity_pairs_list[j];

				if 'FLT' not in element_identity_pair[-1] and 'INV' not in element_identity_pair[-1]:
					freetext_field_with_metadata = [element_identity_pair[0]] + [relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID']] + [0,0,0,0,0,'N/A, Type Non-floaters','Hardcoded'] + [relate_info_list_for_doc.iloc[i]['Field_Name']];	
					total_field_with_metadata_list.append(freetext_field_with_metadata);	
					continue;


				textarea_meta_list = Textarea_Result_Handler.get_freetext_metadata_by_criteria(relate_info_list_for_doc.iloc[i],raw_xtr_result_for_doc);



				if textarea_meta_list != []:
					for result_obj in textarea_meta_list:
						freetext_field_with_metadata = [element_identity_pair[0]] + [relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID']] + result_obj + [relate_info_list_for_doc.iloc[i]['Field_Name']];	
						total_field_with_metadata_list.append(freetext_field_with_metadata);	
				else:
					freetext_field_with_metadata = [element_identity_pair[0]] + [relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID']] + [0,0,0,0,0,'N/A, no extraction result for this field. Please check the document.',''] + [relate_info_list_for_doc.iloc[i]['Field_Name']];	
					total_field_with_metadata_list.append(freetext_field_with_metadata);				
		
		if relate_info_list_for_doc.iloc[i]['Field_Name'] == 'Payment Delay':
			for j in range(0, len(element_identity_pairs_list)):
				element_identity_pair = element_identity_pairs_list[j];

				if 'FLT' in element_identity_pair[-1] or 'INV' in element_identity_pair[-1]:
					freetext_field_with_metadata = [element_identity_pair[0]] + [relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID']] + [0,0,0,0,0,'0 DAYS',''] + [relate_info_list_for_doc.iloc[i]['Field_Name']];	
					total_field_with_metadata_list.append(freetext_field_with_metadata);	
				else:
					freetext_field_with_metadata = [element_identity_pair[0]] + [relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID']] + [0,0,0,0,0,'24 DAYS',''] + [relate_info_list_for_doc.iloc[i]['Field_Name']];	
					total_field_with_metadata_list.append(freetext_field_with_metadata);
			continue;

		if relate_info_list_for_doc.iloc[i]['Field_Name'] == 'Issue Date':
			for j in range(0, len(element_identity_pairs_list)):
				element_identity_pair = element_identity_pairs_list[j];
				textarea_meta_list = Textarea_Result_Handler.get_freetext_metadata_by_criteria(relate_info_list_for_doc.iloc[i],raw_xtr_result_for_doc);


				if textarea_meta_list !=[]:
					result_obj = textarea_meta_list[0];

					result_obj[-2] = Field_Value_Normalizer.get_date_digits(result_obj[-2]);

					if 'FLT' in element_identity_pair[-1] or 'INV' in element_identity_pair[-1]:
						result_obj[-2] = result_obj[-2][:-3] + '-25';
					else:
						result_obj[-2] = result_obj[-2][:-3] + '-01';

					freetext_field_with_metadata = [element_identity_pair[0]] + [relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID']] + result_obj + [relate_info_list_for_doc.iloc[i]['Field_Name']];	
					total_field_with_metadata_list.append(freetext_field_with_metadata);	
				else:
					freetext_field_with_metadata = [element_identity_pair[0]] + [relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID']] + [0,0,0,0,0,'N/A, no extraction result for this field. Please check the document.',''] + [relate_info_list_for_doc.iloc[i]['Field_Name']];	
					total_field_with_metadata_list.append(freetext_field_with_metadata);				




		if relate_info_list_for_doc.iloc[i]['Field_Name'] in ['Payment Date','Deal Series','Sponsor','Co-Sponsor','Closing Date','Pricing Date', 'Deal Size', 'Day Count', 'Legal Matters', 'Remic Status', 'Frequency', 'Record Date']:
			for j in range(0, len(element_identity_pairs_list)):
				element_identity_pair = element_identity_pairs_list[j];
				textarea_meta_list = Textarea_Result_Handler.get_freetext_metadata_by_criteria(relate_info_list_for_doc.iloc[i],raw_xtr_result_for_doc);

				if textarea_meta_list != []:
					for result_obj in textarea_meta_list:
						freetext_field_with_metadata = [element_identity_pair[0]] + [relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID']] + result_obj + [relate_info_list_for_doc.iloc[i]['Field_Name']];	
						total_field_with_metadata_list.append(freetext_field_with_metadata);	
				else:
					freetext_field_with_metadata = [element_identity_pair[0]] + [relate_info_list_for_doc.iloc[i]['Xtr_To_Calcrt_Config_Map_ID']] + [0,0,0,0,0,'N/A, no extraction result for this field. Please check the document.',''] + [relate_info_list_for_doc.iloc[i]['Field_Name']];	
					total_field_with_metadata_list.append(freetext_field_with_metadata);						

	# sys.exit();





	float_info_raw_extraction_list = raw_xtr_result_for_doc[raw_xtr_result_for_doc['Extraction_Criteria_ID']==1107];
	float_relate_info_list_for_doc = relate_info_list_for_doc[relate_info_list_for_doc['Extraction_Criteria_ID'] == 1107];


	print 'godbless';
	print len(float_info_raw_extraction_list);
	print len(float_relate_info_list_for_doc);
	print 'godbless';

	float_info_with_metadata_list = get_float_info_for_des_inv_flt_fannie(element_identity_pairs_list, total_field_with_metadata_list, float_info_raw_extraction_list, float_relate_info_list_for_doc);
	total_field_with_metadata_list = total_field_with_metadata_list + float_info_with_metadata_list;
	

	

	##########################################################
	######### pricing speed 

	filtered_raw_xtr_list_for_pricingspeed_wals = raw_xtr_result_for_doc[raw_xtr_result_for_doc['Extraction_Criteria_ID']==1108];



	multifamily_flag = 1 if 'Multifamily' in [item[7] for item in total_field_with_metadata_list if item[-1] == 'Deal Series'][0] else 0;

	print 'multifamily flag:                   ',multifamily_flag;


	pricing_speed_wals_metadata_list =  get_pricingspeed_and_wals_for_fannie(filtered_raw_xtr_list_for_pricingspeed_wals, element_identity_pairs_list, xtr_to_calcrt_config_map_id_pricing_speed, xtr_to_calcrt_config_map_id_wals, multifamily_flag);

	##########################################################


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
			item[7] = item[7] + '-25'
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
				item[7] = Field_Value_Normalizer.get_mapped_abbreviation_for_sponsor_fm(item[7]);
				mapped_sponsor_name = item[7];
			continue;	

		if item[-1] == 'Co-Sponsor':
			if mapped_cosponsor_name != '':
				item[7] = mapped_cosponsor_name;
			else:
				item[7] = Field_Value_Normalizer.get_mapped_abbreviation_for_cosponsor_fm(item[7]);
				mapped_cosponsor_name = item[7];
			continue;	

		if item[-1] == 'Day Count':
			item[7] = Field_Value_Normalizer.get_day_count(item[7]);
			continue;
		if item[-1] == 'Deal Series':
			item[7] = Field_Value_Normalizer.remove_subregex(item[7], 'Fannie Mae REMIC Trust');
			item[7] = Field_Value_Normalizer.remove_subregex(item[7], 'Fannie Mae Multifamily REMIC Trust');
			item[7] = 'FNR ' + item[7].strip();		
			continue;
		if item[-1] == 'Floater Index':
			item[7] = Field_Value_Normalizer.get_floater_index(item[7]);
			continue;		
		if item[-1] == 'Class Balance':
			item[7] = Field_Value_Normalizer.remove_characters(item[7],[' ','\.','\,','\$']);
			item[7] = Field_Value_Normalizer.get_balance_digits(item[7]);
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
		if item[-1] == 'Closing Date':
			

			item[7] = Field_Value_Normalizer.get_date_digits(item[7]);
			
			continue;



		if item[-1] == 'Payment Date':
			item[7] = Field_Value_Normalizer.get_date_digits(item[7]);
			month = item[7][5:7];
			month = str(int(month)+1);
			month = month if len(month) == 2 else '0' + month;
			item[7] = item[7][:4] +'-'+ month + '-' + '25';
			# print item[7]; 
			continue;
		if item[-1] == 'Record Date':
			settlement_date = Field_Value_Normalizer.get_date_digits(item[7]);

			year = settlement_date[:4];
			month = settlement_date[5:7];

			item[7] = Field_Value_Normalizer.get_last_day_of_preceding_month(year,month);
			# print item[7];

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





	print '                                                       ',len(total_field_with_metadata_list);

	return element_identity_pairs_list,total_field_with_metadata_list;






def get_a_cell_metadata_Fanniemae(row_xtr_list, element_identity_pair_info, relate_info_list_for_doc_item):
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

	max_column_number = max(row_xtr_list['Table_Column_Number']);
	
	

	field_name = relate_info_list_for_doc_item['Field_Name'];

	target_column_index = element_identity_pair_info[3];

	target_page_number = element_identity_pair_info[1];

	target_row_number = element_identity_pair_info[2];


	if relate_info_list_for_doc_item['Extraction_Criteria_ID'] == 24:
		if target_page_number > 4:
			return [];
		else:
			if field_name == 'Maturity':
				target_column_index = target_column_index + 1;
				extracted_value = '';
				while target_column_index <= max_column_number:
					current_cell_metadata = Table_Result_Handler.get_cell_field_info_by_page_row_column(row_xtr_list, target_page_number, target_row_number, target_column_index);
					if target_column_index == element_identity_pair_info[3]+1:
						pos_min_x = current_cell_metadata['Pos_Min_X'];
						pos_min_y = current_cell_metadata['Pos_Min_Y'];
						font = current_cell_metadata['Font'];
					if target_column_index == max_column_number:
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
				extracted_value = element_identity_pair_info[7]
				return [element_identity_pair_info[0], xtr_to_calcrt_config_map_id, page_number, pos_min_x, pos_min_y, pos_max_x, pos_max_y, extracted_value, font, field_name];
			if field_name ==  'Class Balance':
				target_column_index = target_column_index - 4;
				current_cell_metadata = 0;
				while target_column_index > 0:
					current_cell_metadata = Table_Result_Handler.get_cell_field_info_by_page_row_column(row_xtr_list, target_page_number, target_row_number, target_column_index);
					temp_extracted_value =current_cell_metadata['Field_Value'];
					temp_extracted_value = Field_Value_Normalizer.remove_characters(temp_extracted_value,[' ','\.','\,','\$']);
					temp_extracted_value = re.sub(r'\(\d\)','', temp_extracted_value);
					temp_extracted_value = re.sub(' ','', temp_extracted_value);
					if temp_extracted_value == '':
						continue;
					else:
						break;
					target_column_index -= 1;	

				pos_min_x = current_cell_metadata['Pos_Min_X'];
				pos_min_y = current_cell_metadata['Pos_Min_Y'];
				pos_max_x = current_cell_metadata['Pos_Max_X'];
				pos_max_y = current_cell_metadata['Pos_Max_Y'];
				extracted_value =current_cell_metadata['Field_Value'];
				extracted_value = Field_Value_Normalizer.remove_characters(extracted_value,[' ','\.','\,','\$']);	
				font = current_cell_metadata['Font'];
				return [element_identity_pair_info[0], xtr_to_calcrt_config_map_id, page_number, pos_min_x, pos_min_y, pos_max_x, pos_max_y, extracted_value, font, field_name];				
			if field_name ==  'Tranche':
				target_column_index = 1;
				current_cell_metadata = Table_Result_Handler.get_cell_field_info_by_page_row_column(row_xtr_list, target_page_number, target_row_number, target_column_index);
				pos_min_x = current_cell_metadata['Pos_Min_X'];
				pos_min_y = current_cell_metadata['Pos_Min_Y'];
				pos_max_x = current_cell_metadata['Pos_Max_X'];
				pos_max_y = current_cell_metadata['Pos_Max_Y'];
				extracted_value = element_identity_pair_info[4];
				font = current_cell_metadata['Font'];
				return [element_identity_pair_info[0], xtr_to_calcrt_config_map_id, page_number, pos_min_x, pos_min_y, pos_max_x, pos_max_y, extracted_value, font, field_name];

	if relate_info_list_for_doc_item['Extraction_Criteria_ID'] == 26:
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

				if element_identity_pair_info[-2] == 'Residual':
					extracted_value = 'N/A';

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




def get_element_identity_pairs_fanniemae(xtr_fields_list):
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

	current_cusip = '';
	for item in cusip_position_in_each_row_list:
		# print item;
		class_info = '';
		
	

		cusip_info = '';
		cusip_info = Table_Result_Handler.get_cell_field_info_by_page_row_column(xtr_fields_list,item[0],item[1],item[2])['Field_Value'];


		cusip_info = Field_Value_Normalizer.remove_characters(cusip_info,[' ','\.']);


		if element_identity_pairs_list!=[] and cusip_info in zip(*element_identity_pairs_list)[5]:
			continue;

		descriptors_info = '';

		descriptors_info = Table_Result_Handler.get_cell_field_info_by_page_row_column(xtr_fields_list,item[0],item[1],item[2]-1)['Field_Value'];
		shift_flag = 0;

		if descriptors_info is None or descriptors_info == 'I)' or descriptors_info == 'II)':
			descriptors_info = Table_Result_Handler.get_cell_field_info_by_page_row_column(xtr_fields_list,item[0],item[1],item[2]-2)['Field_Value'];
			shift_flag = 1;
		
		descriptors_info_2nd = Table_Result_Handler.get_cell_field_info_by_page_row_column(xtr_fields_list,item[0],item[1],item[2]-3)['Field_Value'];
		
		if descriptors_info_2nd is None or descriptors_info_2nd == 'I)' or descriptors_info_2nd == 'II)':
			descriptors_info_2nd = Table_Result_Handler.get_cell_field_info_by_page_row_column(xtr_fields_list,item[0],item[1],item[2]-4)['Field_Value'];	
			shift_flag = 1;
		descriptors_info = descriptors_info + '|' + descriptors_info_2nd;



		group_info = 'Residual' if 'NPR' in descriptors_info else '0';

		if item[0] < 4:
			class_info = Table_Result_Handler.get_cell_field_info_by_page_row_column(xtr_fields_list,item[0],item[1],1)['Field_Value'];
		else:
			class_info = Table_Result_Handler.get_cell_field_info_by_page_row_column(xtr_fields_list,item[0],item[1],item[2]-5)['Field_Value'];

	

		class_info = Field_Value_Normalizer.remove_characters(class_info,[' ','\.',r'\(\d\)']);	

		element_identity_pairs_list.append([cusip_index]+item+[class_info, cusip_info, group_info, descriptors_info]);
		cusip_index += 1;

	
	return element_identity_pairs_list;




def get_float_info_for_des_inv_flt_fannie(element_identity_pairs_list, total_field_with_metadata_list, float_info_raw_extraction_list, float_relate_info_list_for_doc):
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

	default_page_number = 0;

	if identity_pairs_list_for_inv_flt !=[]:
		formula_rates_list = float_info_raw_extraction_list[float_info_raw_extraction_list['Extraction_Criteria_ID']==1107];
		if len(formula_rates_list) > 0:
			default_page_number = formula_rates_list.iloc[0]['Page_Number'];
			
		print 'caonima';
		if len(formula_rates_list) > 0:
			for item in Table_Result_Handler.get_row_number_list_by_regex(formula_rates_list,r'^[A-Z]{1,2}[\.]{0,}$'):
				current_row_xtr_list = Table_Result_Handler.get_a_row_fields_by_page_row_numbers(formula_rates_list,item[0],item[1]);
				special_interest_rate_list.append([Field_Value_Normalizer.remove_characters(item[2][:3],[' ','\.']), Table_Result_Handler.get_cell_field_info_by_page_row_column(current_row_xtr_list,item[0],item[1],2)['Field_Value']])

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
				# print class_info;
				row_number = Table_Result_Handler.get_row_number_list_class_info(float_info_raw_extraction_list, class_info, 1);
				
				if row_number == []:
					field_value = 'N/A, no such Class(Tranche) name found on the paragraph. Please check the document.';
					cell_field_with_metadata = [identity_pair_class[0],extraction_calcrt_link_id, default_page_number, 0, 0, 0, 0, field_value, 'Hardcoded', 'Floater Index'];
					float_info_with_metadata_inv_flt.append(cell_field_with_metadata);	
					continue;

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
				row_number = Table_Result_Handler.get_row_number_list_class_info(float_info_raw_extraction_list, class_info, 1);

				if row_number == []:
					field_value = 'N/A, no such Class(Tranche) name found on the paragraph. Please check the document.';
					cell_field_with_metadata = [identity_pair_class[0],extraction_calcrt_link_id, default_page_number, 0, 0, 0, 0, field_value, 'Hardcoded', 'Floater Spread'];
					float_info_with_metadata_inv_flt.append(cell_field_with_metadata);	
					continue;


				if 'FLT' in identity_pair_class[1] or 'INV' in identity_pair_class[1]:
					row_xtr_list = Table_Result_Handler.get_a_row_fields_by_page_row_numbers(float_info_raw_extraction_list,row_number[0][0], row_number[0][1]);
					field_value = Table_Result_Handler.get_cell_field_info_by_page_row_column(row_xtr_list,row_number[0][0], row_number[0][1],1, reverse_order=1)['Field_Value'];

					if 'basis' not in field_value:
						field_value = Table_Result_Handler.get_cell_field_info_by_page_row_column(row_xtr_list,row_number[0][0], row_number[0][1],2, reverse_order=1)['Field_Value'];


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
				row_number = Table_Result_Handler.get_row_number_list_class_info(float_info_raw_extraction_list, class_info, 1);
				if row_number == []:
					field_value = 'N/A, no such Class(Tranche) name found on the paragraph. Please check the document.';
					cell_field_with_metadata = [identity_pair_class[0],extraction_calcrt_link_id, default_page_number, 0, 0, 0, 0, field_value, 'Hardcoded', 'Floor'];
					float_info_with_metadata_inv_flt.append(cell_field_with_metadata);	
					continue;



				if 'FLT' in identity_pair_class[1] or 'INV' in identity_pair_class[1]:
					row_xtr_list = Table_Result_Handler.get_a_row_fields_by_page_row_numbers(float_info_raw_extraction_list,row_number[0][0], row_number[0][1]);
					field_value = Table_Result_Handler.get_cell_field_info_by_page_row_column(row_xtr_list,row_number[0][0], row_number[0][1],4)['Field_Value'];
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
				row_number = Table_Result_Handler.get_row_number_list_class_info(float_info_raw_extraction_list, class_info, 1);

				if row_number == []:
					field_value = 'N/A, no such Class(Tranche) name found on the paragraph. Please check the document.';
					cell_field_with_metadata = [identity_pair_class[0],extraction_calcrt_link_id, default_page_number, 0, 0, 0, 0, field_value, 'Hardcoded', 'Ceiling'];
					float_info_with_metadata_inv_flt.append(cell_field_with_metadata);	
					continue;

				if 'FLT' in identity_pair_class[1] or 'INV' in identity_pair_class[1]:
					row_xtr_list = Table_Result_Handler.get_a_row_fields_by_page_row_numbers(float_info_raw_extraction_list,row_number[0][0], row_number[0][1]);
					field_value = Table_Result_Handler.get_cell_field_info_by_page_row_column(row_xtr_list,row_number[0][0], row_number[0][1],3)['Field_Value'];
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








def get_pricingspeed_and_wals_for_fannie(filtered_raw_xtr_list_for_pricingspeed_wals, element_identity_pairs_list, xtr_to_calcrt_config_map_id_pricing_speed, xtr_to_calcrt_config_map_id_wals, multifamily_flag):

	prepayass_row_list = Table_Result_Handler.get_row_number_list_by_keyword(filtered_raw_xtr_list_for_pricingspeed_wals,'Prepayment Assumption',1);

	prepayass_pricingspeed_wals_row_list = [];
	
	pricing_speed_wals_metadata_list = [];

	for i in range(0, len(prepayass_row_list)):
		item = prepayass_row_list[i];
		prepayass_pricingspeed_wals_row_list.append(item);
		

		start_page_number = item[0];
		start_row_number = item[1];

		while start_row_number < prepayass_row_list[-1][1] + 100:
			current_row_xtr_list = Table_Result_Handler.get_a_row_fields_by_page_row_numbers(filtered_raw_xtr_list_for_pricingspeed_wals, start_page_number, start_row_number);
			number_of_match_percentsign = Table_Result_Handler.get_number_of_match_keyword_in_a_row(current_row_xtr_list, '%');
			if number_of_match_percentsign > 3:
				prepayass_pricingspeed_wals_row_list.append([start_page_number, start_row_number,'pricingspeed']);
				break;

			start_row_number += 1;




	prepayass_pricingspeed_wals_row_list.append([prepayass_pricingspeed_wals_row_list[-1][0],prepayass_pricingspeed_wals_row_list[-1][1]+50,'AssumedEnding']);

	class_range_list = [];

	current_page_number_for_class = filtered_raw_xtr_list_for_pricingspeed_wals.iloc[0]['Page_Number'];


	test_list = [];
	for identity_pair in element_identity_pairs_list:
		if identity_pair[6] == 'Residual':
			
			continue;
		
		target_class_location = Table_Result_Handler.get_row_number_list_class_info_for_pricing_speed(filtered_raw_xtr_list_for_pricingspeed_wals, identity_pair[4], prepayass_pricingspeed_wals_row_list[0][1]);
		
		current_row_number_for_wals = 0;
		current_row_number_for_pricing_speed = 0;
		current_additional_info = '';

		if target_class_location != []:
			current_page_number_for_class = target_class_location[0];
			current_row_number_for_class = target_class_location[1];

			

			################################
			#### find wals     ####
 			################################
 			current_row_number = current_row_number_for_class;
			while current_row_number < 1000:
				current_row_xtr_list = Table_Result_Handler.get_a_row_fields_by_page_row_numbers(filtered_raw_xtr_list_for_pricingspeed_wals,current_page_number_for_class,current_row_number);
				number_of_match_wals = Table_Result_Handler.get_number_of_match_regex_in_a_row(current_row_xtr_list, r'[0-9]{1,}.[0-9]{1,}');
				if number_of_match_wals > 3:
					current_row_number_for_wals = current_row_number;
					break;
				current_row_number += 1;				

			
			################################
			#### find pricing speed     ####
 			################################
 			current_row_number = current_row_number_for_class;
			while current_row_number > 1:
				current_row_xtr_list = Table_Result_Handler.get_a_row_fields_by_page_row_numbers(filtered_raw_xtr_list_for_pricingspeed_wals,current_page_number_for_class,current_row_number);
				number_of_match_wals = Table_Result_Handler.get_number_of_match_keyword_in_a_row(current_row_xtr_list, '%');
				if number_of_match_wals > 3:
					current_row_number_for_pricing_speed = current_row_number;
					break;
				current_row_number -= 1;		

			current_row_number = current_row_number_for_class;
			while current_row_number > 1:
				current_row_xtr_list = Table_Result_Handler.get_a_row_fields_by_page_row_numbers(filtered_raw_xtr_list_for_pricingspeed_wals,current_page_number_for_class,current_row_number);
				number_of_match_wals = Table_Result_Handler.get_number_of_match_keyword_in_a_row(current_row_xtr_list, 'Prepayment Assumption');
				if number_of_match_wals > 0:
					current_additional_info = Table_Result_Handler.get_cell_field_info_by_page_row_column(current_row_xtr_list,current_page_number_for_class, current_row_number,1)['Field_Value'];
					current_additional_info = current_additional_info[:3];
					break;
				current_row_number -= 1;		
			
			test_list.append([identity_pair[0],current_page_number_for_class, current_row_number_for_class, current_row_number_for_pricing_speed, current_row_number_for_wals, current_additional_info]);
		else:
			print 'class ', identity_pair,' not found!';
			test_list.append([identity_pair[0],current_page_number_for_class, current_row_number_for_class, current_row_number_for_pricing_speed, current_row_number_for_wals, current_additional_info]);




	for item in test_list:
		# print item;
		if item[3] == 0:
			pricing_speed_wals_metadata_list.append([item[0], xtr_to_calcrt_config_map_id_pricing_speed, item[1],0,0,0,0, 'Extraction error, please check the document and OID section.', 'Hardcoded', 'Pricing Speed']);
			continue;
		if item[4] == 0:
			pricing_speed_wals_metadata_list.append([item[0], xtr_to_calcrt_config_map_id_wals, item[1],0,0,0,0, 'Extraction error, please check the document and OID section.', 'Hardcoded', 'WALs']);
			continue;


		target_page_number = item[1];
		pricing_speed_row_number = item[3];
		wals_row_number = item[4];
		additional_info = item[5];

		pricing_speed_row = Table_Result_Handler.get_a_row_fields_by_page_row_numbers(filtered_raw_xtr_list_for_pricingspeed_wals,target_page_number, pricing_speed_row_number);
		target_column_index = [];
		percent_count = 0;
		percent_set_count = 0;
		for i in range(0, len(pricing_speed_row)):
			current_cell = pricing_speed_row.iloc[i];
			if '0%'	== current_cell['Field_Value'].strip():
				target_column_index.append(current_cell['Table_Column_Number']);
				percent_set_count += 1;
			if '%' in current_cell['Field_Value']:
				percent_count += 1;


		target_column_index_final = target_column_index[0] if target_column_index!=[] else 2;
		if multifamily_flag == 0:
			try:		
				target_column_index_final = target_column_index_final + (percent_count/percent_set_count + 1)/2 -1;
			except:
				target_column_index_final = 2;
		pricing_speed_cell = Table_Result_Handler.get_cell_field_info_by_page_row_column(pricing_speed_row, target_page_number, pricing_speed_row_number, target_column_index_final);

		pos_min_x = 50;
		pos_min_y = pricing_speed_cell['Pos_Min_Y'];
		pos_max_x = 750;		
		pos_max_y = pricing_speed_cell['Pos_Max_Y'];
		field_value = pricing_speed_cell['Field_Value'] + ' ' + additional_info;
		
		font = pricing_speed_cell['Font'];

		pricing_speed_wals_metadata_list.append([item[0], xtr_to_calcrt_config_map_id_pricing_speed, target_page_number, pos_min_x, pos_min_y, pos_max_x, pos_max_y, field_value, font, 'Pricing Speed']);


		wals_row = Table_Result_Handler.get_a_row_fields_by_page_row_numbers(filtered_raw_xtr_list_for_pricingspeed_wals,target_page_number, wals_row_number);
		target_column_index = 0;
		wals_count = 0;
		wals_count = 0;
		for i in range(0, len(wals_row)):
			current_cell = wals_row.iloc[i];
			if bool(re.search(r'[0-9]{1,}.[0-9]{1,}',current_cell['Field_Value'].strip())):
				target_column_index = current_cell['Table_Column_Number'];
				break;
		
		target_column_index_final = target_column_index;		
		if multifamily_flag == 0:
			try:		
				target_column_index_final = target_column_index_final + (percent_count/percent_set_count + 1)/2 -1;
			except:
				target_column_index_final = 2;

		wals_cell = Table_Result_Handler.get_cell_field_info_by_page_row_column(wals_row, target_page_number, wals_row_number, target_column_index_final);

		pos_min_x = 50;
		pos_min_y = wals_cell['Pos_Min_Y'];
		pos_max_x = 750;		
		pos_max_y = wals_cell['Pos_Max_Y'];
		field_value = wals_cell['Field_Value'];
		# print item[0], '                   ', field_value;
		
		font = wals_cell['Font'];

		pricing_speed_wals_metadata_list.append([item[0], xtr_to_calcrt_config_map_id_wals, target_page_number, pos_min_x, pos_min_y, pos_max_x, pos_max_y, field_value, font, 'WALs']);



	# sys.exit();

	return pricing_speed_wals_metadata_list;








