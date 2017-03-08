"""
	Module PDF_Page_Extractor.py
	Author @Chang Liu
	1. Use IO to load a pdf file
	2. Scan the pages and find out the potential end
	3. Use pyPDF2 to rotate vertical pages;
	4. Store the visulizable csv file and the pickle file for a quick reloading
	5. Provide detection logic for a new pdf or an existing pdf 
	6. The pdf process methods will be called here
"""


from pdfminer.pdfdocument import *;
from pdfminer.pdfpage import *;
from pdfminer.pdfparser import *;
from pdfminer.pdfinterp import *;
from pdfminer.pdfdevice import *;
from pdfminer.converter import *;
from pdfminer.layout import *;
import sys;
import PyPDF2;
import glob;
import time;
import stopit;
import functools;
import multiprocessing;
import gc;
import traceback;





from PDF_Database_Control import DB_Controller;
import Field_Processor;
import CSV_Generator;



reload(sys);
sys.setdefaultencoding('utf-8');




pdf_directory = "";
pdf_file_name_list = [];

"""
	method: check_file_name
	get agency name and deal month from the pdf document name

"""
######################################################################################
def check_file_name(pdf_file_name):
	pdf_file_name_list = pdf_file_name.split('_');
	agency_type = pdf_file_name_list[0];
	deal_month = pdf_file_name_list[1];
	print 'agency_type:  ', agency_type;
	print 'deal_month: ', deal_month[:-4];
	return agency_type,deal_month;





"""
	method set_pdf_directory
	set the directory of all pdf documents 	
"""
############################################################################################
def set_pdf_directory_cl(set_pdf_directory):
	global pdf_directory;
	pdf_directory = set_pdf_directory;
	print pdf_directory;
	get_file_list_on_given_directory_cl();



"""
	method get_file_list_on_given_directory
	get all pdf documents from the given directory	
"""
############################################################################################
def get_file_list_on_given_directory_cl():
	global pdf_directory;
	file_list = glob.glob(pdf_directory);
	file_name_list = [];
	for item in file_list:
		file_name_list.append(item);
	global pdf_file_name_list;
	pdf_file_name_list = file_name_list;
	return file_name_list;




"""
	method set_pdf_directory
	set the directory of all pdf documents 	
"""
############################################################################################
def set_pdf_directory(set_pdf_directory):
	global pdf_directory;
	pdf_directory = set_pdf_directory;
	print pdf_directory;
	"""
		here we query the db to see the file we extracted
		if the file has already been extracted, we won't extract for a second time, we will skip this document 
	"""
	extracted_file_list_df = DB_Controller.get_all_extracted_document();
	extracted_file_list = [];
	for i in range(0, len(extracted_file_list_df)):
		extracted_file_list.append(extracted_file_list_df.iloc[i]['PDF_File_Name']);

	get_file_list_on_given_directory(extracted_file_list);



"""
	method get_file_list_on_given_directory
	get all pdf documents from the given directory	
"""
############################################################################################
def get_file_list_on_given_directory(extracted_file_list):
	global pdf_directory;
	file_list = glob.glob(pdf_directory);
	file_name_list = [];
	for item in file_list:
		file_name_list.append(item);
	global pdf_file_name_list;
	pdf_file_name_list = file_name_list;

	temp_pdf_file_name_list = [];
	for item in pdf_file_name_list:
		exist_flag = 0;
		for check_file in extracted_file_list:
			if check_file[:-4] in item.split("\\")[-1]:
				exist_flag = 1;
				break;
		if exist_flag == 0:
			temp_pdf_file_name_list.append(item);
		else:
			print "File ",item,"has been extracted.";
			print "The result is already in the databse. We skip this file.";
	print len(temp_pdf_file_name_list);

	pdf_file_name_list = temp_pdf_file_name_list;
	return file_name_list;




"""
	PDFMiner extraction routine
	method process_pdf_file
	create pdf_document object for a pdf document 
	the reason I separated this method is because on version 1, we might have to recreate a pdf document object
	but in Version 2, the design has been optimized, this method will only be called once for each document 
"""
############################################################################################
def process_pdf_file(pdf_file_name):
	pdf_file = open(pdf_file_name,'rb');
	pdf_parser = PDFParser(pdf_file);   # this is a pdf parser object 

	pdf_document = PDFDocument(pdf_parser);           # this is a pdf document object
											  # can have a second parameter, as password
											  # if the document doesn't have password, then just ignore it

	if not pdf_document.is_extractable:
		raise PDFTextExtractionNotAllowed;    # test whether the pdf allows text extraction	

	return pdf_document;


"""
	PDFMiner extraction routine
	method get_allobjs_page
	given a layout object of a page
	this method returns all text area components ("LTText") of that page (subsequently, each text area will contain a list of character level components ("LTChar" and "LTAnno"))
"""
############################################################################################
def get_allobjs_page(page_layout):
	obj_list = list(page_layout._objs);
	return obj_list;


vertical_pagenum_list = [];
horizontal_pagenum_list = [];


"""
	PDFMiner extraction routine
	KET METHOD 
	method get_doc_component_list
	given a pdf document object, this method will do a page by page analysis
	1. Follow the PDFMiner Class Relationship, implement child classes and interfaces for extraction 
	2. Analyze page by page, for each page process we set a time out to be 1 second (usually a horizontal common page processed within 1 seconds)
	3. If processing time for a page exceeds 1 second (can be easily more than several minutes if it is a vertical page with portrait page page orientation), we specify it to be 'Vertical' and rotate in the later steps 
	4. If processing time for a page is less than 1 second, we analyze the first character, calculate its upright matrix, if the character is 'Vertical', we specify the page to be vertical 
	5. Process until we reach the endding string specified for this agency or we reach the end of the document 
	6. We have a interpret result list containing all page layout information 
"""
######################################################################################

def get_doc_component_list(pdf_document, end_string=None, page_num_list=None, rotated_file_flag=None):
	
	pdf_resmg = PDFResourceManager();		  # create a resource manager object

	pdf_laparams = LAParams();    # this is the default layout 
	pdf_device_la = PDFPageAggregator(pdf_resmg, laparams = pdf_laparams);
	pdf_interpreter_la = PDFPageInterpreter(pdf_resmg, pdf_device_la);
	
	interpret_result_list = [];


	number_of_complex_pages = 0;

	if page_num_list == None:       ### if no page number list specified, then we do for all pages
		for pageid, page in enumerate(PDFPage.create_pages(pdf_document)): 
			sstart_time = time.time();
			with stopit.ThreadingTimeout(1) as to_ctx_mrg:
				assert to_ctx_mrg.state == to_ctx_mrg.EXECUTING
				pdf_interpreter_la.process_page(page);             							 
				page_layout = pdf_device_la.get_result();
				first_char_obj = get_allobjs_page(page_layout)[0];
				if 'Vertical' == analyze_LTTextBoxHorizontal(first_char_obj,'split')[0][-1]:
					# print analyze_LTTextBoxHorizontal(first_char_obj,'split')[0]; 
					vertical_pagenum_list.append(pageid+1);
				else:
					horizontal_pagenum_list.append(pageid+1);
					interpret_result_list.append(get_allobjs_page(page_layout));


			if to_ctx_mrg.state == to_ctx_mrg.EXECUTED:
				eend_time = time.time();
				print 'Page number: ', (pageid+1),'The processing time is:', eend_time - sstart_time;
				sstart_time = time.time();
			elif to_ctx_mrg.state == to_ctx_mrg.TIMED_OUT:
				print '---------------------------------------------------------------------';
				print 'Page ', pageid+1, ' is too complex to analyze. The interpreting time exceeds 1 seconds. We skip this page.'; 
				vertical_pagenum_list.append(pageid+1);
				if rotated_file_flag == 1:
					print 'WARNING: There is a page in rotated document which is still too complex to analyze. Page',pageid + 1;
				print '---------------------------------------------------------------------';
			else:
				'''do nothing''';
			last_component_of_page = [item for item in get_allobjs_page(page_layout) if isinstance(item, LTText)][-1];
			if end_string!=None:   
				if isinstance(last_component_of_page, LTText) :
					if str(last_component_of_page.get_text())[0:2]==end_string:    # this is very fragile
						print "Number of complex pages: ", number_of_complex_pages;
						print "Endding signal: ",str(last_component_of_page.get_text()), pageid + 1;
						return interpret_result_list;
		return interpret_result_list;

	for pageid, page in enumerate(PDFPage.create_pages(pdf_document)):   ################ here we might specify the page number if needed
		if (pageid+1) in page_num_list:									 ################ The page number in the database starts from 1 while the numerator starts from 0
			pstart_time = time.time();
			pdf_interpreter_la.process_page(page);
			page_layout = pdf_device_la.get_result();
			interpret_result_list.append(get_allobjs_page(page_layout));     	
			pend_time = time.time();
			print 'Page ', pageid+1, ' |Process time: ', (pend_time - pstart_time)/60.0;
			if (pageid+1) == page_num_list[-1]:
				break; 
	return interpret_result_list;

######################################################################################








"""
	method: sort_component_by_pos
	the original extracted component list from pdfminer is ordered by component type 
	here we provide a custimized sorting method to re-organized the extracted component list
	the sorting is based on position
	option 1: from top left to bottom right, row by row, text area block level
	option 2: from top left to bottom right, row by row, character and annotation level 
"""
######################################################################################
def sort_component_by_pos(component_list, sort_option):     							
	if sort_option == 1:    
		sorted_component_list = sorted(component_list, key = lambda x: (x[0],-(x[6]),(x[3])));										    
	if sort_option == 2:
		sorted_component_list = sorted(component_list, key = lambda x: (x[0],-(x[5]),(x[4])));
	if sort_option == 3:
		sorted_component_list = sorted(component_list, key = lambda x: (x[0],(x[3]),(x[4])));
	if sort_option == 4:
		sorted_component_list = sorted(component_list, key = lambda x: (x[0],(x[5]),(x[4])));
	if sort_option == 5:
		sorted_component_list = sorted(component_list, key = lambda x: (x[0],(x[4])));

	return sorted_component_list;										
######################################################################################



"""
	method decode_a_page_level_component
	the first hand extraction list from PDFMiner is in a OOP way, which is an object containing multiple attributes
	since we are not using OOP in our solution, I designed this method to get all attributes out and reorgnize them into multi-dimensional pure python list
	so each text area will be represented by an item in a list 

	in version 2 you can see here, i modified this method to make it more robust.
	in version 1 we are splitting the string and get each value we want 
	but that is not robust because some attributes might contain spaces that mess up the whole thing 
	in version 2, im using object attributes getter to get each value
	this is better and robust 
"""
###################################################################################################
def decode_a_page_level_component(pl_component,page_num, component_index):
	component_info = [];
	component_info.append(page_num+1);
	component_info.append(component_index+1);

	lt_name = pl_component.__class__.__name__;      # get the lt type
	component_info.append(lt_name);

	position_box = pl_component.bbox;          # get the postion box 
	component_info.append(position_box[0]);
	component_info.append(position_box[1]);
	component_info.append(position_box[2]);
	component_info.append(position_box[3]);


	# print '                               ',type(pl_component);
	if isinstance(pl_component, LTText):
		# print type(pl_component);
		area_text = ''.join([char for char in pl_component.get_text() if ord(char)<=128]) ;        # get the text    
		### remove non-utf-8 characters for the ui to render

		area_text = area_text.replace("\n",' ');
		area_text = re.sub(r'	',' ', area_text);

		component_info.append(area_text)
		char_anno_list = pl_component._objs;   

		if not isinstance(char_anno_list[0], LTChar):
			rotation_matrix = char_anno_list[0]._objs[0].matrix;     # get the rotation matrix (text direction matrix) for a character in this text area
			font_name = char_anno_list[0]._objs[0].fontname;         # get the font name
			adv = char_anno_list[0]._objs[0].adv;                    # get the adv value
			font_size = char_anno_list[0]._objs[0].size;             # get the font size
			is_upright = char_anno_list[0]._objs[0].upright;         # get the boolean value for is upright
		else:
			rotation_matrix = char_anno_list[0].matrix;     # get the rotation matrix (text direction matrix) for a character in this text area
			font_name = char_anno_list[0].fontname;         # get the font name
			adv = char_anno_list[0].adv;                    # get the adv value
			font_size = char_anno_list[0].size;             # get the font size
			is_upright = char_anno_list[0].upright;         # get the boolean value for is upright

		component_info.append(str(rotation_matrix));
		component_info.append(font_name);
		component_info.append(adv);
		component_info.append(font_size);
		component_info.append(is_upright);

		if rotation_matrix[0]-0 > 0.1 and rotation_matrix[3]-0 > 0.1:
			component_info.append('Horizontal');
		if rotation_matrix[1]-0 > 0.1 and rotation_matrix[2]-0 < -0.1:
			component_info.append('Vertical');	


	else:
		component_info = component_info + [''];


	# print component_info;
	# print '==================================================';
	return component_info;			

"""
	method calc_width_and_height
	based on the min point max point coordinates, we calculate out the witdh and height for each block on a page 
"""
###################################################################################################
def calc_width_and_height(component, type):
	
	if type == 'block_level_component':
		return [component[5] - component[3], component[6] - component[4]];
	if type == 'charanno_level_component':
		return [component[6] - component[4], component[7] - component[5]];





"""
	method decode_page_instance_of_doc
	once we have the interpret page result list from get_doc_component_list, we use this method to process the objects list 
	this method will call decode_a_page_level_component to decode a page object from PDFMiner 

"""
###################################################################################################
def decode_page_instance_of_doc(initial_page_list,option):
	pl_component_list = [];
	corrected_page_number_list = [];
	if option == 'horizontal':
		global horizontal_pagenum_list;
		print horizontal_pagenum_list;
		corrected_page_number_list = horizontal_pagenum_list;
	if option == 'vertical':
		global vertical_pagenum_list;
		print vertical_pagenum_list;
		corrected_page_number_list = vertical_pagenum_list;

	for i in range(0, len(initial_page_list)):
		for j in range(0,len(initial_page_list[i])):
			component_detail_list = decode_a_page_level_component(initial_page_list[i][j],corrected_page_number_list[i]-1,j);
			component_detail_list = component_detail_list;
			pl_component_list.append(component_detail_list);

	sorted_block_level_component_list = sort_component_by_pos(pl_component_list,1);


	for i in range(0,len(sorted_block_level_component_list)):
		if 'Text' not in sorted_block_level_component_list[i][2]:    											# indicating it is not a LTChar
			sorted_block_level_component_list[i] = sorted_block_level_component_list[i]  + ['','','','','',''];
			sorted_block_level_component_list[i]  = sorted_block_level_component_list[i]  + calc_width_and_height(sorted_block_level_component_list[i] ,'block_level_component');
		else:
			sorted_block_level_component_list[i]  = sorted_block_level_component_list[i]  + calc_width_and_height(sorted_block_level_component_list[i] ,'block_level_component');


	return sorted_block_level_component_list;	

""" 
	methods split_analyze_LTTextLineHorizontal split_string_detail_process analyze_LTTextBoxHorizontal
	these three methods are dealing with the layout class structure of PDFMiner 
	I'm decoding from the top to the bottom, hard to explain in details, please take a look at the Class Relationship UML I drew about PDFMiner 
	just include these three methods when you need to extract pdf document to a pure multi-dimensional list 
	because basically, I am just converting attributes (of a class instance) to variables and objects to items in lists  

	in version 2 this method also has been optimized
	samething with the method decode_a_block_level_component
"""

#################################################################################
def split_analyze_LTTextLineHorizontal(LTTextLineHorizontal_obj):
	detailed_info_list = LTTextLineHorizontal_obj._objs;
	split_detailed_info_list = [];
	for item in detailed_info_list:
		if ('Anno' not in str(item)):
			temp_split_detail_obj = [];
			lt_name = item.__class__.__name__;
			temp_split_detail_obj.append(lt_name);

			position_box = item.bbox;
			temp_split_detail_obj.append(position_box[0]);
			temp_split_detail_obj.append(position_box[1]);
			temp_split_detail_obj.append(position_box[2]);
			temp_split_detail_obj.append(position_box[3]);

			rotation_matrix = item.matrix;
			temp_split_detail_obj.append(str(item.matrix));

			font_name = item.fontname;
			temp_split_detail_obj.append(font_name);

			adv = item.adv;
			temp_split_detail_obj.append(adv);

			character = item.get_text();
			temp_split_detail_obj.append(character);

			font_size = item.size;
			temp_split_detail_obj.append(font_size);

			is_upright = item.upright;
			temp_split_detail_obj.append(is_upright);

			if rotation_matrix[0]-0 > 0.1 and rotation_matrix[3]-0 > 0.1:
				temp_split_detail_obj.append('Horizontal');
			if rotation_matrix[1]-0 > 0.1 and rotation_matrix[2]-0 < -0.1 :
				temp_split_detail_obj.append('Vertical');	
			split_detailed_info_list.append(temp_split_detail_obj);
		else:
			split_detailed_info_list.append(item);
	return split_detailed_info_list;
######################################################################################

def analyze_LTTextBoxHorizontal(LTTextBoxHorizontal_obj, option):
	detailed_info_list = [];
	temp_info_list = LTTextBoxHorizontal_obj._objs;
	if option == 'raw':
		for item in temp_info_list:
			detailed_info_list = detailed_info_list + raw_analyze_LTTextLineHorizontal(item);
	if option == 'split':
		for item in temp_info_list:
			detailed_info_list = detailed_info_list + split_analyze_LTTextLineHorizontal(item);		

	return detailed_info_list;

######################################################################################
def split_string_detail_process(initial_page_list, page_num, option):
	split_component_list = [];
	i = 0;
	if option == 'horizontal':
		i = horizontal_pagenum_list.index(page_num);
	if option == 'vertical':
		i = vertical_pagenum_list.index(page_num);

	for j in range(0,len(initial_page_list[i])):
		process_flag = 0;
		if (process_flag == 0) and ('LTTextBoxHorizontal' in str(type(initial_page_list[i][j]))):
			process_flag = 1;
			temp_detailed_component_list = analyze_LTTextBoxHorizontal(initial_page_list[i][j],'split');
			for item in temp_detailed_component_list:
				detailed_object = [];
				detailed_object.append(page_num);
				detailed_object.append(j+1);
				detailed_object.append(str(initial_page_list[i][j]).split(' ',1)[0][1:]);
				if not isinstance(item,LTAnno):
					detailed_object = detailed_object + item;
				else:
					detailed_object.append(str(item).split(' ',1)[0][1:]);
					detailed_object = detailed_object + [split_component_list[-1][4],split_component_list[-1][5],split_component_list[-1][6],split_component_list[-1][7],'','',''];
					detailed_object.append(str(item).split(' ',1)[1][:-1]);
				split_component_list.append(detailed_object);
		if process_flag == 0:
			detailed_object = [];
			detailed_object.append(page_num);
			detailed_object.append(j+1);
			temp_raw_info_list = str(initial_page_list[i][j]).split(' ',2);
			detailed_object.append(temp_raw_info_list[0][1:]);
			detailed_object.append('');
			detailed_object.append(float(temp_raw_info_list[1].split(',',3)[0]));
			detailed_object.append(float(temp_raw_info_list[1].split(',',3)[1]));
			detailed_object.append(float(temp_raw_info_list[1].split(',',3)[2]));
			detailed_object.append(float(temp_raw_info_list[1].split(',',3)[3][:-1]));	
			split_component_list.append(detailed_object);											
	sorted_split_component_list = sort_component_by_pos(split_component_list,2);



	for i in range(0,len(sorted_split_component_list)):
		if sorted_split_component_list[i][3] == 'LTAnno':    											# indicating it is not a LTChar
			sorted_split_component_list[i] = sorted_split_component_list[i] + ['','',''];
			sorted_split_component_list[i] = sorted_split_component_list[i] + calc_width_and_height(sorted_split_component_list[i],'charanno_level_component');
		elif sorted_split_component_list[i][3] == 'LTChar':
			sorted_split_component_list[i] = sorted_split_component_list[i] + calc_width_and_height(sorted_split_component_list[i],'charanno_level_component');
		else:
			sorted_split_component_list[i] = sorted_split_component_list[i] + ['','','','','','',''];
			sorted_split_component_list[i] = sorted_split_component_list[i] + calc_width_and_height(sorted_split_component_list[i],'charanno_level_component');

	return sorted_split_component_list;

######################################################################################
######################################################################################
######################################################################################



"""
	copy-and-paste for preventing cross module import  
"""
######################################################################################
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



"""
	KEY METHOD 
	method rotate_vertical_pages_and_merge
	this method is reponsible for rotating all vertical pages (those portrait-oriented pages with vertical text directions)
	1. we rotate all these pages and merge them using PyPDF2
	2. we store the temporary rotated pdf document
	3. we redo the PDFMiner processing for this temporary pdf document
	4. return the rotated extraction list and append it to the former extracted list 
	5. the temporary pdf document will be deleted once the process is finished 
"""
######################################################################################
def rotate_vertical_pages_and_merge(pdf_file_name, vertical_pagenum_list):
	pdf_in = open(pdf_file_name, 'rb')
	pdf_reader = PyPDF2.PdfFileReader(pdf_in)
	pdf_writer = PyPDF2.PdfFileWriter()
	 
	for pagenum in vertical_pagenum_list:
	    page = pdf_reader.getPage(pagenum-1);
	    page.rotateClockwise(90);
	    pdf_writer.addPage(page);
	 
	pdf_out = open('rotated.pdf', 'wb');
	pdf_writer.write(pdf_out);
	pdf_out.close();
	pdf_in.close();
	rotated_document = process_pdf_file('rotated.pdf');
	vertical_page_list = get_doc_component_list(rotated_document,rotated_file_flag=1);
	return vertical_page_list;




"""
	KEY METHOD 
	method pdf_process_main
	1. this is the main function for PDF_Loader, the PDF_Engine will call this method to start the extraction logic 
	2. for each pdf document, first we will check whether we have already processed it or not
	3. if so, we will have middle csvs generated for the document and we directly load the csv files instead of using PDFMiner to process the document. This will save us a lot of time when do debugging.
	4. if no csvs found for this document, we follow the PDFMinber routine to do the extraction and save the extracted list into csvs files 
	5. once we have the component list, we call Field_Processor module here to do the search and specific extraction with rules
"""
######################################################################################
def pdf_page_extraction_main():
	page_extraction_result_with_criteria = [];
	for item in pdf_file_name_list:
		print '';
		print '';
		print '------------------------------------------------------------------------------';
		print item;
		try:
			sorted_block_level_component_list = [];
			sorted_charanno_level_component_list = [];
			doc_component_instance_list = [];
			csv_file_name = CSV_Generator.get_csv_path(item);
			pdf_name = CSV_Generator.get_pdf_name(item);
			agency_type, deal_month = check_file_name(pdf_name);
			extraction_criteria_list = DB_Controller.get_extraction_criteria_list(agency_type);

			endding_criteria_list = extraction_criteria_list.loc[extraction_criteria_list['Extraction_Description'] == 'doc_end_str'];    # get the ending string of a document


			"""
				the following statement is to get all the criteria that require to do a character analysis of the page 
				these criteria need a characters analysis about certain pdf pages
				for now, it's 'key_value_str' and 'table_begin_str'
			"""
			criteria_requrie_character_analysis = extraction_criteria_list.loc[(extraction_criteria_list['Extraction_Description'] == 'key_value_str') | (extraction_criteria_list['Extraction_Description'] == 'table_begin_str')] ;
			print "Number of criteria that require characters analysis of pages:",len(criteria_requrie_character_analysis);
		

			global vertical_pagenum_list;
			global horizontal_pagenum_list;
			doc_id = 0;

			print 'Extracting file ' ,pdf_name;
			pdf_document = process_pdf_file(item);
			print 'Success!', item;
			end_string = None;
			if not endding_criteria_list.empty:
				end_string = endding_criteria_list.iloc[-1]['Anchor_Search_String'];

			doc_component_instance_list = get_doc_component_list(pdf_document,end_string);
			
			sorted_block_level_component_list = decode_page_instance_of_doc(doc_component_instance_list,'horizontal');
			
			
			############################################################
			doc_component_instance_list_rotated = rotate_vertical_pages_and_merge(item,vertical_pagenum_list);
			############################################################
			sorted_block_level_component_list = sorted_block_level_component_list + decode_page_instance_of_doc(doc_component_instance_list_rotated, 'vertical');
			sorted_block_level_component_list = sort_component_by_pos(sorted_block_level_component_list, 1);

			page_number_list = [];
			for i in range(0, len(criteria_requrie_character_analysis)):
				page_number = specify_page_number(sorted_block_level_component_list, criteria_requrie_character_analysis.iloc[i]);
				page_number_list = page_number_list + page_number;

			page_number_list = list(set(page_number_list));

			for page_num in page_number_list:
				if page_num in vertical_pagenum_list:
					temp_sorted_charanno_level_component_list = split_string_detail_process(doc_component_instance_list_rotated,page_num, 'vertical');
					temp_sorted_charanno_level_component_list = sort_component_by_pos(temp_sorted_charanno_level_component_list,2);
					sorted_charanno_level_component_list = sorted_charanno_level_component_list + temp_sorted_charanno_level_component_list;
				if page_num in horizontal_pagenum_list:
					temp_sorted_charanno_level_component_list = split_string_detail_process(doc_component_instance_list,page_num, 'horizontal');
					temp_sorted_charanno_level_component_list = sort_component_by_pos(temp_sorted_charanno_level_component_list,2);
					sorted_charanno_level_component_list = sorted_charanno_level_component_list + temp_sorted_charanno_level_component_list;
			sorted_charanno_level_component_list = sort_component_by_pos(sorted_charanno_level_component_list,2);




			print 'Number of pages we processed: ',len(doc_component_instance_list), type(doc_component_instance_list);
			title_list = ['Page_Num','Component_Index','Component_Type','Coor_Min_X','Coor_Min_Y','Coor_Max_X',\
			'Coor_Max_Y','Text','Matrix', 'Font', 'Adv(wid*fsize*scal)','FontSize(pt)','Upright(Bool)','Text_Direction','Box_Width','Box_Height']
			CSV_Generator.generate_mid_csv(item,sorted_block_level_component_list,title_list);

			title_list = ['Page_Num','Component_Index','Parent_Component_Type','Component_Type','Coor_Min_X','Coor_Min_Y','Coor_Max_X',\
			'Coor_Max_Y','Matrix', 'Font', 'Adv(wid*fsize*scal)','Text','FontSize(pt)','Upright(Bool)','Text_Direction','Box_Width','Box_Height']

			CSV_Generator.generate_mid_csv(item,sorted_charanno_level_component_list,title_list, pdf_name[:-4]+'_LTTextBoxes_Details');
			doc_id = DB_Controller.insert_or_update_doc_info(pdf_name, agency_type);


			print 'Length of pl component list: ',len(sorted_block_level_component_list);
			print 'Vertical Page Number List: ',vertical_pagenum_list;
			print 'Horizontal Page Number List: ', horizontal_pagenum_list;
			print '------------------------------------------------------------------------------';
			print '';
			print '';
			page_extraction_result_with_criteria.append([agency_type, doc_id, sorted_block_level_component_list, sorted_charanno_level_component_list, vertical_pagenum_list, horizontal_pagenum_list, item, extraction_criteria_list]);
			vertical_pagenum_list = [];
			horizontal_pagenum_list = [];
		except:
			print 'Error : Page Extraction Error with file ', item;
			print 'We skip this file';
			print '--------------- system error message -----------------';
			traceback.print_exc();			
			print '------------------------------------------------------';		
	return page_extraction_result_with_criteria;






def pdf_page_extraction_main_debug_cl():
	page_extraction_result_with_criteria = [];
	for item in pdf_file_name_list:
		print '';
		print '';
		print '------------------------------------------------------------------------------';
		print item;
		try:
			sorted_block_level_component_list = [];
			sorted_charanno_level_component_list = [];
			doc_component_instance_list = [];
			csv_file_name = CSV_Generator.get_csv_path(item);
			pdf_name = CSV_Generator.get_pdf_name(item);
			agency_type, deal_month = check_file_name(pdf_name);
			extraction_criteria_list = DB_Controller.get_extraction_criteria_list(agency_type);

			endding_criteria_list = extraction_criteria_list.loc[extraction_criteria_list['Extraction_Description'] == 'doc_end_str'];    # get the ending string of a document

			"""
				the following statement is to get all the criteria that require to do a character analysis of the page 
				these criteria need a characters analysis about certain pdf pages
				for now, it's 'key_value_str' and 'table_begin_str'
			"""
			criteria_requrie_character_analysis = extraction_criteria_list.loc[(extraction_criteria_list['Extraction_Description'] == 'key_value_str') | (extraction_criteria_list['Extraction_Description'] == 'table_begin_str')] ;
			print "Number of criteria that require characters analysis of pages:",len(criteria_requrie_character_analysis);
		

			global vertical_pagenum_list;
			global horizontal_pagenum_list;
			doc_id = 0;
			if CSV_Generator.get_existing_csv(item):
				print 'File ', pdf_name, ' has been extracted. ';
				sorted_block_level_component_list = CSV_Generator.get_existing_csv(item);
				for sub_item in sorted_block_level_component_list:
					sub_item[0] = int(sub_item[0]);
					sub_item[1] = int(sub_item[1]);
					sub_item[3] = float(sub_item[3]);
					sub_item[4] = float(sub_item[4]);
					sub_item[5] = float(sub_item[5]);
					sub_item[6] = float(sub_item[6]);
					sub_item[14] = float(sub_item[14]);
					sub_item[-1] = float(sub_item[-1]);
				
				sorted_charanno_level_component_list = CSV_Generator.get_existing_detailed_csv(item);
				for sub_item in sorted_charanno_level_component_list:
					sub_item[0] = int(sub_item[0]);
					sub_item[1] = int(sub_item[1]);
					sub_item[4] = float(sub_item[4]);
					sub_item[5] = float(sub_item[5]);
					sub_item[6] = float(sub_item[6]);
					sub_item[7] = float(sub_item[7]);
					sub_item[-2] = float(sub_item[-2]);
					sub_item[-1] = float(sub_item[-1]);
				doc_id = DB_Controller.insert_or_update_doc_info(pdf_name, agency_type);


			else:
				print 'Extracting file ' ,pdf_name;
				pdf_document = process_pdf_file(item);
				print 'Success!', item;
				end_string = None;
				if not endding_criteria_list.empty:
					end_string = endding_criteria_list.iloc[-1]['Anchor_Search_String'];

				global pool;
				doc_component_instance_list = get_doc_component_list(pdf_document,end_string);
				
				sorted_block_level_component_list = decode_page_instance_of_doc(doc_component_instance_list,'horizontal');
				############################################################
				doc_component_instance_list_rotated = rotate_vertical_pages_and_merge(item,vertical_pagenum_list);
				############################################################
				sorted_block_level_component_list = sorted_block_level_component_list + decode_page_instance_of_doc(doc_component_instance_list_rotated, 'vertical');
				sorted_block_level_component_list = sort_component_by_pos(sorted_block_level_component_list, 1);

				page_number_list = [];
				for i in range(0, len(criteria_requrie_character_analysis)):
					page_number = specify_page_number(sorted_block_level_component_list, criteria_requrie_character_analysis.iloc[i]);
					print 'Page number list found for anchor string ',criteria_requrie_character_analysis.iloc[i]['Anchor_Search_String'],'                 page list:',page_number;
					page_number_list = page_number_list + page_number;

				page_number_list = list(set(page_number_list));

				for page_num in page_number_list:
					if page_num in vertical_pagenum_list:
						temp_sorted_charanno_level_component_list = split_string_detail_process(doc_component_instance_list_rotated,page_num, 'vertical');
						temp_sorted_charanno_level_component_list = sort_component_by_pos(temp_sorted_charanno_level_component_list,2);
						sorted_charanno_level_component_list = sorted_charanno_level_component_list + temp_sorted_charanno_level_component_list;
					if page_num in horizontal_pagenum_list:
						temp_sorted_charanno_level_component_list = split_string_detail_process(doc_component_instance_list,page_num, 'horizontal');
						temp_sorted_charanno_level_component_list = sort_component_by_pos(temp_sorted_charanno_level_component_list,2);
						sorted_charanno_level_component_list = sorted_charanno_level_component_list + temp_sorted_charanno_level_component_list;
				sorted_charanno_level_component_list = sort_component_by_pos(sorted_charanno_level_component_list,2);




				print 'Number of pages we processed: ',len(doc_component_instance_list), type(doc_component_instance_list);
				title_list = ['Page_Num','Component_Index','Component_Type','Coor_Min_X','Coor_Min_Y','Coor_Max_X',\
				'Coor_Max_Y','Text','Matrix', 'Font', 'Adv(wid*fsize*scal)','FontSize(pt)','Upright(Bool)','Text_Direction','Box_Width','Box_Height']
				CSV_Generator.generate_mid_csv(item,sorted_block_level_component_list,title_list);

				title_list = ['Page_Num','Component_Index','Parent_Component_Type','Component_Type','Coor_Min_X','Coor_Min_Y','Coor_Max_X',\
				'Coor_Max_Y','Matrix', 'Font', 'Adv(wid*fsize*scal)','Text','FontSize(pt)','Upright(Bool)','Text_Direction','Box_Width','Box_Height']

				CSV_Generator.generate_mid_csv(item,sorted_charanno_level_component_list,title_list, pdf_name[:-4]+'_LTTextBoxes_Details');
				doc_id = DB_Controller.insert_or_update_doc_info(pdf_name, agency_type);


			print 'Length of pl component list: ',len(sorted_block_level_component_list);
			print 'Vertical Page Number List: ',vertical_pagenum_list;
			print 'Horizontal Page Number List: ', horizontal_pagenum_list;
			print '------------------------------------------------------------------------------';
			print '';
			print '';
			page_extraction_result_with_criteria.append([agency_type, doc_id, sorted_block_level_component_list, sorted_charanno_level_component_list, vertical_pagenum_list, horizontal_pagenum_list, item, extraction_criteria_list]);
			vertical_pagenum_list = [];
			horizontal_pagenum_list = [];
			gc.collect();
		except:
			print 'Error : Page Extraction Error with file ', item;
			print 'We skip this file';
			print '--------------- system error message -----------------';
			traceback.print_exc();			
			print '------------------------------------------------------';	

	return page_extraction_result_with_criteria;



###########################################################################################


