




def get_identity_pairs_with_descriptor(element_identity_pairs_list, total_field_with_metadata_list):
	identity_pairs_list_with_descriptor = [];


	descriptor_list_with_identity_index = [item for item in total_field_with_metadata_list if item[-1] == 'Descriptors'];

	# for item in descriptor_list_with_identity_index:
	# 	print item;

	for identity in element_identity_pairs_list:
		descriptors_metadata = [descriptor_info for descriptor_info in descriptor_list_with_identity_index if descriptor_info[0] == identity[0]][0];
		descriptors = descriptors_metadata[7]
		identity_pairs_list_with_descriptor.append([identity[0],descriptors,descriptors_metadata]);
	return identity_pairs_list_with_descriptor;