



def get_freetext_metadata_by_criteria(nontable_relate_info, total_extraction_list, hardcoded_value=None):
	if hardcoded_value:
		return [0,0,0,0,0,hardcoded_value,'Hardcoded'];
	else:
		result_freetext_metadata_dfobj = total_extraction_list.loc[total_extraction_list['Extraction_Criteria_ID']==nontable_relate_info['Extraction_Criteria_ID']];
		result_freetext_metadata_list = [];
		for i in range(0, len(result_freetext_metadata_dfobj)):
			result_freetext_metadata_list.append([result_freetext_metadata_dfobj.iloc[i]['Page_Number'],result_freetext_metadata_dfobj.iloc[i]['Pos_Min_X'],result_freetext_metadata_dfobj.iloc[i]['Pos_Min_Y'],result_freetext_metadata_dfobj.iloc[i]['Pos_Max_X'],result_freetext_metadata_dfobj.iloc[i]['Pos_Max_Y'], result_freetext_metadata_dfobj.iloc[i]['Field_Value'], result_freetext_metadata_dfobj.iloc[i]['Font']]);
		return result_freetext_metadata_list;
